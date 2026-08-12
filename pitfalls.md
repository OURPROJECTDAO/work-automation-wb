# 알려진 함정 / 주의 (작업 전 필독 — 프로토콜·환경·공통 데이터위생)

> **항상 읽는 슬림 세트.** 여기엔 매 세션 환경 운영에 필요한 것만 둔다.
> 상황별 패턴은 분리 → **Streamlit 앱 작업 / Excel 파싱 시 `patterns.md`** 를 읽을 것.
> 공유 자산 바꾸기 전 영향범위 → `manifest.md`. 워크플로우 전용 함정 → `workflows/<name>.md`.

## ## GitHub contents API (KB 저장소)
- 기존 파일 덮어쓰기: 먼저 GET으로 현재 sha 받아 PUT에 포함. 안 하면 409/422. 신규 파일은 sha 불필요.
- 읽기는 Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8). 기본 JSON 응답의 content는 base64+줄바꿈이라 디코딩 필요.
- PUT의 content는 base64 인코딩(줄바꿈 없이).
- 한글 파일명 API 경로: urllib.request는 한글 URL을 ASCII로 못 보냄. urllib.parse.quote(segment)로 퍼센트 인코딩 필수 (app/pages/1_파일처리.py 등).
- 대용량 파일 업로드(예: 10551행 csv): curl 명령줄이 "Argument list too long" → Python urllib으로 업로드.
- PAT은 비밀: repo·KB·로그에 절대 안 적음. 프로젝트 지식 파일에만. 만료 시 그 파일만 갱신. fine-grained(work-automation-wb + work-automation-app, contents 읽기·쓰기).

## GitHub raw read-after-write 지연 → 앱 자동훅 중복쓰기 (data repo 영속 훅 공통)
- **contents API `raw`(및 `?ref=main` GET)는 CDN 캐싱이라 방금 PUT 한 걸 몇 초~수십초 stale 하게 읽는다**(eventual consistency). Streamlit 앱은 위젯 상호작용마다 스크립트 전체 rerun 하므로, **"읽고→판정→쓰고" 훅이 페이지 로드마다 자동으로 도는 구조면** 방금 쓴 결과를 stale 하게 다시 읽어 **같은 건을 반복 판정 → 중복 기록 + 같은 파일 반복 PUT**이 된다. 반복 PUT 은 GitHub 가 **409(Conflict, 직전 커밋 처리 중) 또는 403(secondary rate limit, 짧은시간 쓰기 다발)**로 거부 → 앱에 `urllib.error.HTTPError`.
- **관측(2026-07-20)**: 데일리 대시보드 품절 알림판 재입고 자동처리 — `restock_log.csv` 에 동일 2건이 각 2번 중복 기록(커밋 11초 간격 2회), "상품관리 다시 읽기"가 HTTPError. board 삭제는 정상 1회였는데 로그만 중복(read_board stale 로 지운 board 가 다시 읽힘).
- **처방(이 계열 모든 data repo 영속 훅에 적용)**: ① **append 는 멱등**하게 — 커밋 직전 최신본 재확인해 자연키(예 `관리코드+입고일`) 중복분 skip·실제 추가분만 return. ② **PUT 은 재시도** — 409/422/403/429 시 **sha 재취득 + backoff** 최대 3~4회(`stockout_board._put_retry` 패턴). ③ 가능하면 **자동 rerun 훅을 버튼/1회성 트리거로 게이팅**해 race window 축소. 삭제/치환류 write 는 stale 여도 멱등이면(이미 지운 걸 또 지움) 무해.
- 같은 계열 훅: `stock_history`(1b 재고 스냅샷)·`listing_history`(1d listing 스냅샷)·`decision_log`(두뇌④ 원장)·`stockout_board` — dedup 키가 이미 있으면 대체로 안전하나, **자동 rerun 경로에서 write 하는 곳**은 위 3종 처방 점검할 것.

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
- VBA→Python 이관 시 **메인 단계 외 별도 모듈에 숨은 저장 Sub(SaveAs/Workbooks.Add/SaveCopyAs)** 누락 주의. 메인 흐름만 분석하면 빠짐. olevba 전체 추출 후 SaveAs|Workbooks.Add 류 전역 grep으로 채집. (openmarket 송장 단독 저장 SaveSheetToNewFile이 최초 이관 때 통째 누락된 사례 — logs/2026-06-02-openmarket-invoice-save-restore)

## openpyxl 행 삭제 (전 워크플로우 공통)
- **`delete_rows`는 셀만 지우고 `ws.row_dimensions`(행 높이/서식)는 남긴다** → 빈 `<row>` 요소가 sheet XML에 잔존. openpyxl max_row로는 안 보여도 외부 파서(플랫폼 업로드 등)는 빈 상품행으로 인식. 행 삭제 후 마지막 유효행 초과 `row_dimensions` 키를 직접 삭제할 것. (channel-margin-monitor 가격변경 양식, logs/2026-06-11)

## xlsx 외부링크(externalLinks) 잔존 (템플릿 기반 출력 전 워크플로우 공통)
- **원본 마스터 통합문서를 가리키던 양식 템플릿이 고아 외부참조(`xl/externalLinks/`+workbook `<externalReferences>`)를 품으면**, openpyxl `load→save`가 이를 **그대로 전파** → 출력 파일을 엑셀에서 열 때 '외부 연결을 업데이트할 수 없습니다' 경고. **데이터 셀이 전부 리터럴(inlineStr/숫자)이라 수식 의존이 없어도** 경고는 뜸(숫자는 다 맞음). 
- 진단: `unzip -l out.xlsx | grep externalLink` / `unzip -p out.xlsx xl/workbook.xml | grep externalReference`.
- 해결: ① 템플릿 자체를 정리(외부링크 4종 제거: 파트·workbook `<externalReferences>`·workbook.xml.rels 관계·`[Content_Types].xml` override) ② 코드에서 저장 직후 zip레벨 strip(외부링크 없으면 no-op). channel-margin-monitor `_strip_external_links` 참고(배민 양식, logs/2026-06-11).

## openpyxl 저장이 네이티브 포맷 파괴 (엄격 업로더 거부 — 전 워크플로우 공통)
- **openpyxl(≥3.1) `load_workbook→wb.save()` 라운드트립은 로드된 문자열 셀을 전부 `t="inlineStr"`로 재직렬화**(sharedStrings.xml 제거·XML 선언 누락·네이티브 네임스페이스 상실). Excel은 열리지만 **엄격한 플랫폼 업로더(쿠팡 등 Apache POI류)는 inlineStr를 거부**. 증상: 숫자·내용 다 맞는데 업로드만 실패.
- 진단: `unzip -l out.xlsx | grep sharedStrings`(없으면 의심), 시트 xml에 `t="inlineStr"` 존재.
- 해결: 플랫폼 양식을 **선택행 남기기·몇 칸 기입** 정도만 수정할 땐 openpyxl 대신 **원본 .xlsx를 zip레벨로 수술**(원본 sheet xml 텍스트 편집 + sharedStrings/styles 등 그대로 repack) → 네이티브 포맷 100% 보존. 단 원본 raw 자체가 네이티브여야 함(업로드 바이트 그대로 저장). channel-margin-monitor 쿠팡 `build_filter_price_xlsx` 참고(logs/2026-06-11).
- **append류(`append_rows_to_raw`)도 openpyxl 저장 → 네이티브 파괴**. 네이티브 보존이 필요한 채널(쿠팡)은 '신규만 추가'(=append) 대신 '전체 교체'(업로드 바이트 저장)를 쓸 것.

## Streamlit Community Cloud 네이티브 스택 자동 업그레이드 세그폴트 (배포 인프라 — 전 워크플로우 공통)
- **Community Cloud는 requirements.txt의 `>=` 열린 핀을 재배포마다 최신으로 재해석**(각 커밋=데이터
  커밋 포함=재빌드 트리거) → 어느 날 갑자기 bleeding-edge 조합이 설치됨. 코드 무변경인데 앱이
  "Error running app"(전체 페이지)로 죽고, Cloud 로그에 `Segmentation fault ... streamlit`(SIGSEGV,
  OOM의 `Killed`/SIGKILL 아님). 리부트하면 잠깐 되다 특정 페이지 열면 재발(힙-상태 의존 heisenbug).
- **관측 사례(2026-07-13)**: `pandas 3.0.2 + pyarrow 25 + numpy 2.4`에서 `pd.read_csv`의 arrow 백엔드
  문자열(`string_arrow.py _from_sequence`, pandas3.0 기본 문자열 dtype=ArrowStringArray)이 한글
  CSV(product_master 등) 읽을 때 네이티브 크래시. 상품360/두뇌④/가격AB/대시보드에서 발생.
- **진단**: 한 프로세스에 여러 페이지 연속 로드(=Cloud 장수명 프로세스 모사) + `faulthandler.enable()`로
  C레벨 크래시 지점 캡처. 단일 페이지 독립 실행은 안 터질 수 있음(누적 네이티브 상태 필요).
- **해결(권장) = 런타임 가드**: 버전 다운핀은 **Cloud Python이 최신(3.13/3.14)이라 wheel 부재→소스빌드
  hang**("Preparing metadata (pyproject.toml)" 무한대기)이 되므로 피한다. 대신 pandas는 최신 유지(wheel 확보)
  하고, 엔트리(streamlit_app.py, 매 로드 최선두)에서 `pd.set_option("mode.string_storage","python")`로
  문자열 dtype을 python 백엔드로 고정 → ArrowStringArray(`string_arrow._from_sequence`) 크래시 경로 회피.
  검증: 크래시 조합에서 가드없음 세그폴트→가드있음 정상(2026-07-13). 커밋 app 0fec9cf.
- **버전으로 낮추고 싶으면**: requirements 캡만 걸지 말고 **Cloud 앱 설정에서 Python 버전을 3.12로** 내려
  안정 wheel(pandas2.2/numpy1.26/pyarrow17)을 확보해야 함(둘 중 하나만 하면 hang 또는 세그폴트 재발).
- 코드가 pandas 3.0 전용 API 안 쓰는지만 확인(`applymap`은 이미 `.map`으로 이관됨).

## Streamlit 위젯 경합/버전 함정 (앱 전체 — 전 워크플로우 공통)
- **`st.data_editor` + 폼 밖의 별도 `st.button` = 마지막 셀 미확정 상태로 저장되는 경합**: 표에서 셀을
  편집(특히 새 행 추가 후 마지막 셀)한 직후 곧바로 폼 밖 버튼을 누르면, 그 편집이 위젯 상태에 커밋되기
  전에 버튼 클릭이 먼저 처리돼 **직전 상태로 저장**됨 → 사용자 입장에선 "한 번에 저장이 안 되고
  두 번째 클릭에야 반영"되는 것처럼 보임. 해결: `st.data_editor`와 저장 버튼을 **`st.form`으로 묶고
  `st.form_submit_button` 사용** — 폼 제출은 모든 위젯 값을 한 번에 확정한 뒤 처리되므로 경합이 없음.
  (기준데이터관리 천년경영업로드 소분목록 저장, 2026-07-07, logs/2026-07/2026-07-07-cheonnyeon-sublist-save-fix)
- **`use_container_width` deprecated → `width` 파라미터**: 최신 Streamlit은 `use_container_width=True/False`
  대신 `width="stretch"`/`width="content"`(또는 픽셀 정수)를 요구, 구 파라미터 사용 시 배포 로그에 매
  상호작용마다 경고가 반복 출력됨(st.dataframe/data_editor/button/image/plotly_chart 등 전 위젯 공통).
  전환 시 `True`→`width="stretch"`, `False`→`width="content"` 단순 매핑. (2026-07-07 전 페이지 83건 일괄
  전환, logs/2026-07/2026-07-07-cheonnyeon-sublist-save-fix-and-width-deprecation)

## pandas Styler (st.dataframe 색상 — 전 워크플로우 공통)
- **`Styler.applymap`은 pandas 3.x(Streamlit Cloud 현행·py3.14)에서 제거됨** → `AttributeError: 'Styler' object has no attribute 'applymap'`. 원소별 스타일은 **`Styler.map(func, subset=...)`** 사용(2.1.0부터 rename). `DataFrame.applymap`도 동일하게 `DataFrame.map`. (daily-dashboard 가격 변동 알림 색상, logs/2026-06-17-price-alert-boxstock-color)

## 상품명 검증(웹서치 vs 실물 이미지) 함정
- **일반 웹서치/식봄크롤링 결과는 "그 브랜드/제품군"을 확인해줄 뿐, 우리 관리코드의 정확한 그 SKU를 보증하지 않음.**
  같은 이름의 제품이 여러 변종(백미식혜 vs 이천쌀식혜, 큐원 vs 올바른농부 등 다른 제조사의 동일 카테고리 제품)으로
  존재할 수 있어, 검색 결과의 "흔한 이름"으로 우리 코드의 원래 이름을 덮어쓰면 오히려 틀릴 수 있음(2026-07-02 사례:
  3건 중 3건 다 웹서치 기반 "정정"이 실물 라벨과 어긋남 — 원래 이름이 맞았는데 잘못 고침).
  **상품명을 실제로 바꾸기 전, 그 관리코드의 gi.esmplus 이미지로 최종 확인이 먼저**(웹서치는 후보 좁히기 용도로만).
- 이 규칙은 sikbom-register §8b의 "소스 폴더≠관리코드 1:1 주의"와 같은 계열 함정 — 순서만 다름(그건 이미지 자체가
  다른 상품, 이건 텍스트 검색이 다른 SKU).

## 외부 플랫폼(쿠팡 등) export 공통 함정

- **집계표 하단 TOTAL/합계 행**: 쿠팡 WING 판매통계 등 플랫폼 export는 마지막에 헤더 없는 합계행이 딸려오는 경우가 흔함(옵션ID 등 키 컬럼은 빈칸, 금액 컬럼만 채워짐). 데이터 순회 시 `v[0]=='TOTAL'`류 필터 없이 합산하면 **정확히 2배로 잡히는 특징적인 오류** — 총합이 항목별 합의 정확히 2배면 이 패턴을 의심할 것. **외부 플랫폼뿐 아니라 자사 ERP(천년경영) export에서도 발생** — 입금전표관리 export 마지막 행이 거래처명 등 키 컬럼 전부 빈칸 + 결제금액만 채운 합계행이었음(입금 대사 시 ERP 총액이 은행의 정확히 2배로 잡혀 완전히 어긋나 보임). export류는 소스 불문 마지막 행 TOTAL 여부를 항상 확인할 것. (쿠팡 로켓그로스 정산 logs/2026-07-02 · 입금 대사 logs/2026-07-14)
- **딕셔너리 멤버십 체크와 빈 문자열 값**: `if key in dict`는 값이 빈 문자열('')이어도 True — 매핑 소스 export가 키는 있는데 값 칸이 비어있는 행(예: 관리코드 미기입)을 놓치기 쉬움. 값을 실제로 쓸 거면 `dict.get(key)`의 **truthy 체크**로 폴백 처리할 것. (쿠팡 로켓그로스 정산, logs/2026-07-02)

## 한국어 처리 (엑셀/앱 — 전 워크플로우 공통)
- 주소·상품명 매칭 전 NFC 정규화 필수(unicodedata.normalize("NFC", s)). 출처 다른 데이터가 NFD(자모 분리)면 같은 글자라도 부분일치 매칭 실패 → 도서산간/미배송 매칭 치명적.
- **숫자 ID 키 정규화 (전 워크플로우 공통)**: openpyxl은 정수 ID 셀(예 상품번호 46903)을 **float(46903.0)**로 읽음. str()/NFC만 하면 '46903.0' → CSV/reference의 '46903' 키와 매칭 실패(조용히 미매칭=기본값). 정수값 float은 int화 후 키로 쓸 것(`int(v) if isinstance(v,float) and v.is_integer() else v`). (channel-margin-monitor 캐시노트 N 전건 1 오류 사례, logs/2026-06-11-cashnote)
- reference csv는 UTF-8-sig(BOM)로 저장. Excel에서 직접 열어도 안 깨짐.
- 대시보드 차트: matplotlib는 한글 폰트 미설치 시 □□□. Plotly/Altair(브라우저 폰트) 권장.
- 정렬: VBA xlPinYin vs Python 코드포인트 정렬 차이 가능 → 골든 파일 대조로 확인.
- cmm 기준마진율 = 노출가(표시가) 기반 forward target ≠ 매출자료 realized(할인·쿠폰·믹스로 realized<target가 정상). 두 값 동일시 금지 — 교차 반영은 Δ(변화량) 가산으로(두뇌④, ADR 0027).

_갱신: 2026-06-11 (openpyxl 저장 네이티브 포맷 파괴 함정 추가 — 쿠팡 업로드 사례)_

_갱신: 2026-06-17 (pandas Styler.applymap 제거(3.x) → .map 함정 추가 — Streamlit Cloud)_

_갱신: 2026-06-19 (cmm target↔매출자료 realized 마진 정의 정합 함정 — 두뇌④/ADR 0027)_

_갱신: 2026-07-07 (Streamlit 위젯 경합/버전 함정 섹션 신설 — data_editor+폼밖버튼 경합(st.form 해결)·use_container_width→width 전환)_

_갱신: 2026-07-13 (Community Cloud 네이티브 스택 자동 업그레이드 세그폴트 함정 신설 — pandas3.0+pyarrow25 arrow-string read_csv. 네이티브 3종 상한 캡 핀)_

_갱신: 2026-07-13 (위 함정 정정 — 다운핀은 py3.14 wheel 부재로 hang. 해결책을 런타임 가드 pd.set_option mode.string_storage=python 으로 교체)_

_갱신: 2026-07-20 (GitHub raw read-after-write 지연 → 앱 자동훅 중복쓰기 함정 신설 — 데일리 재입고 자동처리 HTTPError. 처방=append 멱등+PUT 재시도(sha재취득·backoff)+훅 게이팅. stockout_board._put_retry 패턴)_

## pandas 3.x — 숫자열 `astype(str)` 은 결측을 'nan' 문자열로 만들지 않는다
`pd.to_numeric()` 으로 만든 float 열에 `.astype(str)` 을 걸면, pandas 3 에서는 결측이
**'nan' 문자열이 아니라 NaN(float) 그대로 남는다**. 그래서 `.replace("nan","")` 이 안 먹고,
이후 `len(v) for v in series` 같은 순회에서 `TypeError: object of type 'float' has no len()`.
→ 문자열 순회가 필요하면 `.fillna("")` 을 먼저 걸거나, 원본 문자열 프레임 기준으로 계산할 것.
(2026-07-29 SKU단가표 엑셀 다운로드 구현 중 적발)

## UTF-8 BOM 이 CSV **첫 컬럼 키만** 오염시킨다 → 조용한 빈값 (2026-08-04)
`csv.DictReader` 는 BOM 을 안 벗긴다. 저장본에 BOM 이 있으면 **첫 헤더만** `'\ufeff상품번호'` 가 되어
`row["상품번호"]` 가 `None`. **나머지 열은 전부 정상**이라 발견이 아주 늦다.
- 실사고: `listing_cafe24.csv` 를 `encoding="utf-8-sig"` 로 저장 → 상품번호 전건 빈값 →
  `n_source:"ref"` 의 hapo 조회 실패 → **N=1 폴백** → 선물세트 매입가가 박스 통째로 잡혀
  마진율 **−200~300%** 로 표시. 관리코드·상품명은 멀쩡해서 원인 파악이 늦어짐.
- **진단법**: 표에서 **첫 컬럼만** 비고 나머지는 정상 → BOM 의심. `open(f,"rb").read()[:3] == b"\xef\xbb\xbf"` 확인.
- 처방: ① 읽기측 `text.lstrip("\ufeff")`(`csv_text_to_recs` 반영) ② **쓰기측은 BOM 없이**.
  앱 `_commit_listing`/`recs_to_csv` 는 원래 BOM 없이 쓴다 — **수기로 파일을 만들어 커밋할 때
  `utf-8-sig` 를 쓰면 안 된다**(reference CSV 는 `utf-8-sig` 로 읽지만 listing 은 아님).
- 파생 규칙: **N=1 이 비정상적으로 많으면 키 컬럼부터 의심**한다. hapo 미등록과 증상이 같다.

## 참조 CSV 셀에 붙여넣기 개행이 딸려 들어감 → lookup 전멸 + 유령 행 증식 (2026-08-04)
엑셀에서 셀 범위를 복사해 `st.data_editor` 에 붙여넣으면 **셀 끝 개행(`\n`)이 값에 그대로
들어온다.** CSV 는 그 값을 따옴표로 감싸 보존하므로 **파일도 앱 화면도 정상으로 보이는데**,
이후 그 코드로 하는 모든 조회가 조용히 실패한다 — `'PC005982\n' != 'PC005982'`.
- 증상이 엉뚱한 데서 터진다: 온누리 발주서에서 `int(nan)` ValueError 로 표면화됐다
  (미매칭 → None → 다른 행 정수와 섞여 float64 추론 → NaN).
- **자가 증식**: 마지막 열에 개행이 남으면 재읽기 때 유령 빈 행이 생기고, 그게 다시
  저장되며 행수가 매 저장마다 1씩 는다(122→123→…). `key_col` 빈값 필터가 못 잡는 이유 =
  **pandas 3 의 `astype(str)` 이 결측을 'nan' 문자열로 안 만들고 NaN 으로 남기기 때문**
  (아래 pandas 3.x 항목과 같은 계열). `NaN.strip()` → NaN, `NaN != ""` → True → 생존.
- **처방 = `core/base.sanitize_ref_df(df, key_col=None)`** 를 참조 CSV `to_csv` **직전**에 건다.
  개행/탭→공백·strip·NFC + 전열 빈 행 제거 + key_col 빈 행 제거. 멱등.
  기준데이터관리 4개 페이지가 **각자 저장 함수를 복제**해 갖고 있으므로
  (`_gh_put_csv`×2 · `_save_csv` · `_commit_csv`) 새 저장 경로를 만들면 여기도 걸 것.
- ★ 구현 함정: pandas 3 는 `dtype=str` 로 읽은 열이 `object` 가 아니라 **str dtype** 이라
  `if df[c].dtype == object` 로 거르면 위생 처리가 통째로 no-op 된다. 전 컬럼에 map 할 것.

## 참조 CSV → 엑셀 변환 시 '코드' 열은 반드시 문자열 유지
관리코드·원코드는 `45-21`·`23-18`·`01-17` 형태라 엑셀이 **날짜로 자동 변환**한다.
숫자형 복원은 '코드'가 이름에 없는 열에만 적용할 것. (core 공통 규칙)

## 분석 중 출력 잘림 — 결론 내기 전 전량 확인 (2026-08-03)
`tail -N`·`head -N`으로 자른 출력의 **보이는 부분만 보고 전체를 단정하지 말 것.**
실제 사고: ERP 음수 전표를 조회하면서 `tail -30`에 잘린 뒷부분만 보고 "음수는 전부 6/28에 몰려 있다"고
결론냈는데, 실제로는 5/31·6/19·6/23에도 있었음. 이 오독 위에 "5월 판매분 차감이 안 돼 있다"는
2차 잘못된 진단까지 쌓임.
- 건수를 먼저 출력하고(`print(len(...))`), 그 건수와 실제 표시된 행 수가 맞는지 확인한 뒤 결론낼 것.
- 집계·분류 결론은 잘린 출력이 아니라 **집계값**으로 낼 것.

## 미확인 추론을 원인으로 제시하지 말 것 (2026-08-03)
데이터로 확인되지 않은 가설을 원인처럼 단정해 사용자에게 추가 작업을 요구한 사고 2건:
- "반출목록이 화면 캡처라 스크롤이 잘렸을 것" → 실제로는 처음부터 완전(4장 합산이 정확히 일치).
- "입고 전표가 중복 입력됐다"(같은 날 같은 코드 반복) → 실제로는 파렛트 단위 정상 분할 기입.
가설은 가설로 제시하고, **먼저 검증 가능한 대조부터 요청**할 것.

## ★ 거래처그룹 집계 시 `쿠팡(로켓창고)` 제외 필수 (2026-08-05)
`groups/store_groups.csv`는 **`쿠팡(로켓창고)`를 「오프라인」으로 분류**하고 있다.
그런데 이 계정은 매출처가 아니라 **위탁재고 계정**이다
(로켓그로스 창고 입고 = 전량 매출(+) → 실판매 시 쿠팡 채널 매출 별도 입력 +
이중계상분을 판매수량만큼 음수(−) 상계. 정본 = workflows/coupang-rocketgrowth-settlement.md §0).
- **증상**: 오프라인 매출이 입고월엔 부풀고 상계월엔 깎여 **추이·마진율이 통째로 왜곡**된다.
  실측(식자재 137품, 2026): 5월 오프라인 **+26,108,065 과대** / 7월 **−25,560,202 과소**,
  월마진율이 3.6~7.8%로 널뜀 → 제외 후 4.5~5.9%로 수렴.
- **처방**: 거래처그룹 기준 매출·마진 집계는 `상호명 == '쿠팡(로켓창고)'` 행을 **오프/온 어디에도
  넣지 말고 제외**할 것. 로켓그로스의 진짜 판매는 `오픈마켓 쿠팡 (윙배송)`에 별도 기록돼 있으므로
  제외해도 매출 누락이 아니다. 계정 자체는 존속(재고 대사용)이라 store_groups 값 수정은 보류.
- **적용 대상**: Phase 4 대시보드 거래처그룹 집계 · 챗 네이티브 매출 분석 전반.
  2026-05 이전 데이터엔 이 계정이 없어 영향 없음(로켓그로스 개시가 2026-05).

## 쿠팡 로켓그로스 매출은 월 1회 발주일에 몰려 기록됨 (2026-08-05)
정산분 일괄 입력이라 거래일자가 **2026-05-31 / 06-28 / 07-26** 한 날에 집중된다.
**일 단위 추이·이상치 탐지에서 스파이크로 오탐**하기 쉬움. 월 단위 집계는 정상.

_갱신: 2026-08-04 (참조 CSV 붙여넣기 개행 오염 함정 신설 — lookup 전멸·유령행 증식. 처방=core/base.sanitize_ref_df)_
_갱신: 2026-08-04 (BOM 첫컬럼 오염 함정 신설 — 상품번호 빈값→N=1 폴백→선물세트 역마진 오탐)_
## 스마트스토어 listing 가격 비교 시 **즉시할인 차감 필수** (2026-08-05)
`listing_smartstore.csv`의 `판매가`는 **즉시할인 적용 전** 값이다. 742행 중 **272행에 즉시할인**(평균 2,701원)이 걸려 있어,
판매가 원값으로 경쟁가·오프라인가와 비교하면 프리미엄이 통째로 과대계산된다.
- 실측: 곰표 튀김가루 판매가 2,100 → 즉시할인 300 = 실판매 1,800. 원값 비교 시 오프라인 대비 +27.5%로 보이지만 실제 +9.3%.
  목우촌 뚝심 +30.1% → 실제 +17.9%.
- **처방**: 소비자 체감가·비교 기준은 항상 `판매가 − 즉시할인 − 포인트`(cmm `판매가net`). 합포 리스팅은 추가로 `÷N`.
- 식봄 listing은 즉시할인 0건(마켓보로 플랫폼 즉시할인은 정산 무관·미포착)이라 해당 없음 — **채널마다 다르므로 일괄 가정 금지.**

_갱신: 2026-08-05 (거래처그룹 집계 시 쿠팡(로켓창고)=위탁재고 제외 필수 함정 신설 + 로켓그로스 발주일 집중 기록)_
_갱신: 2026-08-05b (스마트스토어 listing 판매가=즉시할인 전 → 가격비교 시 net 차감 필수 함정 신설)_

## ★ 집계 데이터는 파생 분류 만들기 전에 **행 단위(granularity)**부터 확인 (2026-08-12)
`master/sales_*.parquet` 의 한 행은 주문·전표가 아니라 **(거래일자 × 관리코드 × 상호명) 일별 집계**다.
- **실사고**: 행 수량 ≥50 을 "B2B 대량주문"으로 규정해 "추석25 온라인 매출의 82%가 대량 수주"라고
  결론냈고, 그 위에 "그러니 특수 케이스 → 오픈마켓 목표 5억" 까지 쌓았다. 전부 오판이었다.
  실제로는 ESM 의 한 상품이 시즌 내내 25행 = **25일치**였고, 수량 418 은 9/16 **하루 판매량**이다.
- **놓친 단서**: 스마트스토어(순수 리테일)도 행 수량 중앙값 48·최대 1,224 였다. 리테일 채널에서
  그런 행이 나온다는 것 자체가 일별집계 증거인데, 가설에 맞는 채널(ESM)만 들여다보느라 못 봤다.
- **처방**: 행 기반 파생 분류(대량/소량, 건당 규모, 주문 크기 분포 등)를 만들기 **전에**
  `df.groupby(키후보).size()` 로 중복도를 확인한다. 30초면 끝난다.
  `(거래일자, 관리코드, 상호명)` 조합이 거의 1:1 이면 그 데이터로는 **주문 단위 논의를 할 수 없다**.
- 파생 규칙: 어떤 지표가 "놀라운 발견"처럼 보이면, 결론을 쌓기 전에 **그 지표를 만든 키의 의미**부터 되짚는다.

## 명절 시즌 실적 — 설↔추석 교차 외삽 금지 (2026-08-12)
같은 명절끼리의 YoY 만 비교하고, 직전 명절 실적으로 다음 명절을 예측하지 않는다.
- 추석/설 배율이 **1.28배(추석24/설25) → 2.64배(추석25/설26)** 로 벌어지는 중이라 배율 자체가 불안정.
- 설26 오픈마켓이 4.66억으로 추석25 12.29억의 38% 밖에 안 되는 건 라인업이 죽어서가 아니라
  **설이 구조적으로 작은 명절**이기 때문(판매코드 34개 동일, 조합당 매출만 910만→409만).
- 명절 실적은 **거의 단월에 몰린다**(추석25 오픈마켓 12.29억 중 12.06억이 2025-09). 월 단위 추이에서 스파이크로 오탐 주의.
- 정본 = workflows/giftset-season-ops.md

_갱신: 2026-08-12 (집계 데이터 행 단위 확인 함정 신설 — 일별집계를 주문단위로 오독한 실사고 + 명절 교차 외삽 금지)_
