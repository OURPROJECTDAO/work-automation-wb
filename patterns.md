# patterns.md — 상황별 패턴 (작업 종류별로 읽음)

> 항상읽기 아님. **Streamlit/앱 개발 시 → 'Streamlit / 앱' 절**, **Excel 파싱 시 → 'Excel 파일 포맷' 절**을 읽는다.
> 프로토콜·환경·공통 데이터위생은 pitfalls.md, 자산 연결은 manifest.md.

## Streamlit / 앱 개발
### Streamlit Community Cloud 서버 시각 = UTC (날짜 하루 차이 버그)
- **Streamlit Community Cloud는 UTC 타임존** 서버로 동작. `datetime.now()` / `datetime.date.today()` 는 UTC 반환.
- 한국(KST) = UTC+9. 한국 자정~오전 9시 사이에 실행하면 UTC는 전날 → 파일명/셀 날짜가 하루 뒤쳐짐.
- **모든 날짜 호출은 반드시 KST 기준**:
  ```python
  from datetime import datetime, timezone, timedelta
  _KST = timezone(timedelta(hours=9))  # 모듈 상단에 선언
  datetime.now(_KST)                   # datetime.now() 대체
  datetime.now(_KST).date()            # datetime.date.today() 대체
  ```
- 적용 범위: 다운로드 파일명(mmdd·yymmdd·yyyymmdd), 엑셀 헤더 날짜, run_date 기본값, 처리 시간 표시 등.
- 신규 워크플로우 추가 시 템플릿에 _KST 선언 포함할 것. (2026-06-05 전수 적용 완료)

### Streamlit 멀티페이지 / 네비게이션 (전역 인프라)
- pages/ 하위 디렉토리는 자동으로 섹션 인식 안 됨. st.navigation() 명시 필수.
- **이름 있는 섹션 페이지는 반드시 subdirectory에**: st.navigation()의 named section(비어있지 않은 key)에 등록할 페이지는 pages/하위디렉토리/ 안에 두어야 표시됨. pages/ root에 직접 두면 안 보임. (headerless 섹션 ""·" "은 root 파일 OK)
  - 새 섹션 추가 시: ① pages/<섹션명>/ 디렉토리 생성, ② 파일 생성, ③ streamlit_app.py에 _X = _P/"<섹션명>" 변수 추가 후 st.Page() 등록.
  - sys.path: subdirectory 파일은 parent 4번 (root pages 파일은 3번).
- 섹션 헤더 없는 페이지: dict 키를 "" 또는 " "(공백)으로 설정. Python dict 중복 키 불가라 두 번째 무헤더 섹션은 " "(공백 1개) 사용.
- **import된 하위 모듈 변경은 리부트 필요**: core/workflows/*.py 같은 import된 모듈을 수정·커밋하면, Streamlit이 페이지 스크립트는 새로 읽지만 sys.modules에 캐시된 모듈은 옛 버전 유지. 증상: 함수 시그니처 불일치(예: "not enough values to unpack expected 4 got 3"). 해결: Manage app → ⋮ → Reboot app으로 프로세스 재시작. 페이지 파일(.py in pages/) 수정은 자동 반영되지만 import 모듈은 아님.

- **st.stop()은 탭 하나가 아니라 스크립트 전체를 중단 → 코드상 뒤에 오는 `with tabX:` 블록 미렌더**: st.tabs는 한 번의 스크립트 실행에서 모든 탭 컨테이너에 순차로 그린다. 어떤 탭 블록이 전제조건 미충족으로 st.stop()을 호출하면, 그 호출 시점 이후의 모든 코드(다른 탭 블록 포함)가 안 그려진다. 증상: 탭 제목은 보이는데 본문이 텅 빔. 해결: **st.stop()을 호출할 수 있는 탭 블록을 코드상 맨 뒤에 배치**(앞 탭들이 먼저 렌더되도록). 또는 전제조건 검사를 해당 탭 안에서 return-가능한 함수로 감싸기. (천년경영 탭이 발주서 탭의 상품관리-미확인 st.stop() 뒤에 있어 빈 화면 — logs/2026-06-04-cheonnyeon-tab-stop-order)
- **download_button 클릭 = rerun → 실행 블록 안 위젯 소멸**: `if st.button("실행"):` 블록 안에서 결과·다운로드 버튼을 그리면, 다운로드 버튼 하나를 누르는 순간 rerun되어 실행버튼이 False → 블록 전체가 사라짐(여러 산출물 중 하나만 받고 끝남). 해결: 처리 결과를 st.session_state에 저장하고 download_button은 실행 블록 **밖**에서 session_state 기반으로 렌더(버튼마다 고유 key). (openmarket 결과/송장 2버튼 사례 — logs/2026-06-02-openmarket-download-persist)

- **st.dataframe 헤더 정렬은 컬럼 dtype 기준**: 숫자를 보기 좋게 `f"{v:,.0f}"` 문자열로 변환해 넣으면 컬럼이 object가 되어 헤더 클릭 정렬이 **사전식(문자열)**으로 동작 → 962·916·5,625·27,999처럼 첫 글자순 정렬. 숫자는 numeric(int/float)으로 유지하고 `st.column_config.NumberColumn(format="localized")`(천단위 콤마)·`"%.2f"` 등 **표시 포맷만** 입힐 것. (대시보드 거래처 이익 표 송장 정렬 — logs/2026-06-08-dashboard-table-sort-fix)

### 기준데이터 편집표 (st.data_editor — 전 ref 페이지 공통)
- **st.data_editor는 height 윈도우만 렌더+스크롤. 게다가 셀 편집 시 스크롤이 top으로 리셋됨(streamlit #10181)** → 수백 행 표에서 아래쪽 행 편집이 사실상 불가. `head(N)` 미리보기+업로드교체-only인 표는 N행 이후 아예 손도 못 댐(천년경영 소분목록 356행이 head(50)이던 사례).
- **해결 패턴**: 검색창으로 필터 → 필터된 행만 data_editor에 표시 → 저장 시 `pd.concat([df[~mask], edited])`로 **merge-back**(필터 밖 행 보존). ⚠️ 필터 부분집합으로 전체 CSV를 덮어쓰면 나머지 행이 통째로 소실 — 반드시 merge.
- 높이는 `min(38*(행+1)+3, cap)` 동적. 검색 contains는 `regex=False`(사용자 입력 특수문자 크래시 방지) + `fillna("").astype(str)`. 검색어 없으면 mask 전체 True → 기존 전체 편집과 동일.
- 부작용: 검색 후 저장 시 행 순서가 (필터밖+편집본)으로 재배열 — 룩업/키워드 매칭표는 순서 무관이라 무해. 순서 의존 표엔 부적합.
- 대용량(규격 4366 등)은 **검색했을 때만** 편집표 노출(게이트) — 검색 전엔 읽기전용 미리보기, 전체 편집표는 비활성. 더 큰 표(도서산간 1만+)는 읽기전용 검색+파일교체 유지.
- 적용: app/pages/2_기준데이터관리/*.py 전 4파일. (2026-06-09, logs/2026-06/2026-06-09-refdata-editor-search-mergeback)

## Excel 파일 포맷 (파싱)
### 마켓플레이스 입력 파일 (.xls — 데이터 포맷, 여러 워크플로우 공통)
- 스마트스토어/쿠팡/G마켓 등이 내보내는 .xls 파일은 실제로 HTML 테이블. xlrd나 openpyxl로 열리지 않음.
- 읽기: raw.decode('utf-8').replace('\ufeff','').replace('<feff>','') 후 pd.read_html(io.StringIO(html), header=0)[0].
- 송장번호는 숫자로 파싱될 수 있음 → astype(str).str.replace('.0$','') 처리 필요.

### 진짜 OLE2 .xls 읽기 — xlrd CompDocError (여러 워크플로우 공통)
- 채널 업로드 템플릿 .xls(스마트스토어 발 식봄 등)는 진짜 OLE2 BIFF(HTML-테이블 아님, xlrd로 읽음).
- 일부 export는 CompDoc(OLE2) 디렉터리가 비표준 → `xlrd.open_workbook(...)`이 `CompDocError: Workbook corruption: seen[i]==n`로 죽음. 증상: 파일은 Excel에서 멀쩡히 열리는데 앱에선 "아예 안 들어감"(파싱 전체 실패).
- 해결: **`xlrd.open_workbook(file_contents=..., ignore_workbook_corruption=True)`**. 정상 파일엔 무영향, 비표준 디렉터리만 관대 처리. (invoice-fill 식봄 2026-06-08)
- xlwt로 다시 쓴 출력은 표준 OLE2라 기본 파서로 재독됨(출력엔 옵션 불필요).

### 암호 걸린 xlsx 입력 (스마트스토어 등)
- 일부 마켓 내보내기 xlsx는 열기 암호가 걸림(예: 스마트스토어 스스주문, 암호 1323). openpyxl이 못 엶.
- 복호화: msoffcrypto-tool. `off=msoffcrypto.OfficeFile(io.BytesIO(b)); off.load_key(password=pw); off.decrypt(buf)` → openpyxl.load_workbook(buf).
- robust 패턴: `off.is_encrypted()`로 분기 — 평문 업로드면 그대로 열어 사용자가 미리 푼 파일도 허용.
- requirements에 `msoffcrypto-tool` 추가 필수(Streamlit Cloud). (cheonnyeon-upload 사례)
- 헤더가 1행이 아닐 수 있음: 안내문 행(r1) 다음 r2가 헤더, r3+ 데이터 (스스주문). read_only 차원 오인 가능 → 비 read_only로 calculate_dimension 확인.

_갱신: 2026-06-09 (pitfalls에서 분리 신설)_
