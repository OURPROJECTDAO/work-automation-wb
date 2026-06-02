# 알려진 함정 / 주의 (작업 전 필독 — 전역/공통)

> 워크플로우 **전용** 함정은 여기 없다. 해당 워크플로우의 `workflows/<name>.md`를 읽을 것.
> (openmarket-merge · onnuri-order · logistics-order)

## GitHub contents API (KB 저장소)
- 기존 파일 덮어쓰기: 먼저 GET으로 현재 sha 받아 PUT에 포함. 안 하면 409/422. 신규 파일은 sha 불필요.
- 읽기는 Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8). 기본 JSON 응답의 content는 base64+줄바꿈이라 디코딩 필요.
- PUT의 content는 base64 인코딩(줄바꿈 없이).
- 한글 파일명 API 경로: urllib.request는 한글 URL을 ASCII로 못 보냄. urllib.parse.quote(segment)로 퍼센트 인코딩 필수 (app/pages/1_파일처리.py 등).
- 대용량 파일 업로드(예: 10551행 csv): curl 명령줄이 "Argument list too long" → Python urllib으로 업로드.
- PAT은 비밀: repo·KB·로그에 절대 안 적음. 프로젝트 지식 파일에만. 만료 시 그 파일만 갱신. fine-grained(work-automation-wb + work-automation-app, contents 읽기·쓰기).

## 인코딩
- 한글은 UTF-8. base64 디코딩 시 Latin-1 금지(모지바케). raw 헤더로 받으면 디코딩 자체가 불필요.
- 향후 커스텀 Worker 만들 때 atob() UTF-8 미디코딩 버그 주의.

## Google Drive (엑셀 작업물 전용 — KB 아님)
- 커넥터 update/delete 없음, 생성+읽기만. 엑셀은 템플릿=읽기전용·결과=날짜별 새 파일이라 무방. 삭제는 사용자 수동.
- 읽기는 download_file_content(base64→UTF-8). read_file_content는 마크다운 변형(미리보기용).
- 파일 생성 시 contentMimeType + disableConversionToGoogleType=true.

## 보안 (업무 도메인)
- KB에 PII·비밀 금지(고객정보·자격증명·계좌·주문자정보). 식별자(주문번호/참조ID)만.
- 부수효과·되돌릴 수 없는 동작(발송·삭제·결제·권한·외부쓰기)은 정확한 payload(무엇을 누구에게) 보여주고 승인.

## 작업 규율 (투자시스템에서 배움)
- 검증 단계화: 변경 전 실물(템플릿/VBA/데이터) 재확인 → 변경 후 대조. KB는 길잡이지 진실의 원천 아님. 최고 ROI.
- 1작업단위 1로그. 막힌 것·미완·실패도 로그 "다음/상태"에 정직하게(작업>로그 지연이 제일 위험).

## 한국어 처리 (엑셀/앱 — 전 워크플로우 공통)
- 주소·상품명 매칭 전 NFC 정규화 필수(unicodedata.normalize("NFC", s)). 출처 다른 데이터가 NFD(자모 분리)면 같은 글자라도 부분일치 매칭 실패 → 도서산간/미배송 매칭 치명적.
- reference csv는 UTF-8-sig(BOM)로 저장. Excel에서 직접 열어도 안 깨짐.
- 대시보드 차트: matplotlib는 한글 폰트 미설치 시 □□□. Plotly/Altair(브라우저 폰트) 권장.
- 정렬: VBA xlPinYin vs Python 코드포인트 정렬 차이 가능 → 골든 파일 대조로 확인.

## 마켓플레이스 입력 파일 (.xls — 데이터 포맷, 여러 워크플로우 공통)
- 스마트스토어/쿠팡/G마켓 등이 내보내는 .xls 파일은 실제로 HTML 테이블. xlrd나 openpyxl로 열리지 않음.
- 읽기: raw.decode('utf-8').replace('\ufeff','').replace('<feff>','') 후 pd.read_html(io.StringIO(html), header=0)[0].
- 송장번호는 숫자로 파싱될 수 있음 → astype(str).str.replace('.0$','') 처리 필요.

## Streamlit 멀티페이지 / 네비게이션 (전역 인프라)
- pages/ 하위 디렉토리는 자동으로 섹션 인식 안 됨. st.navigation() 명시 필수.
- **이름 있는 섹션 페이지는 반드시 subdirectory에**: st.navigation()의 named section(비어있지 않은 key)에 등록할 페이지는 pages/하위디렉토리/ 안에 두어야 표시됨. pages/ root에 직접 두면 안 보임. (headerless 섹션 ""·" "은 root 파일 OK)
  - 새 섹션 추가 시: ① pages/<섹션명>/ 디렉토리 생성, ② 파일 생성, ③ streamlit_app.py에 _X = _P/"<섹션명>" 변수 추가 후 st.Page() 등록.
  - sys.path: subdirectory 파일은 parent 4번 (root pages 파일은 3번).
- 섹션 헤더 없는 페이지: dict 키를 "" 또는 " "(공백)으로 설정. Python dict 중복 키 불가라 두 번째 무헤더 섹션은 " "(공백 1개) 사용.
- **import된 하위 모듈 변경은 리부트 필요**: core/workflows/*.py 같은 import된 모듈을 수정·커밋하면, Streamlit이 페이지 스크립트는 새로 읽지만 sys.modules에 캐시된 모듈은 옛 버전 유지. 증상: 함수 시그니처 불일치(예: "not enough values to unpack expected 4 got 3"). 해결: Manage app → ⋮ → Reboot app으로 프로세스 재시작. 페이지 파일(.py in pages/) 수정은 자동 반영되지만 import 모듈은 아님.

_갱신: 2026-06-02 (전역/공통만 남기고 워크플로우 전용 함정은 workflows/로 분리 — decisions/0004)_
