# 알려진 함정 / 주의 (작업 전 필독)

## GitHub contents API (KB 저장소)
- 기존 파일 덮어쓰기: 먼저 GET으로 현재 sha 받아 PUT에 포함. 안 하면 409/422. 신규 파일은 sha 불필요.
- 읽기는 Accept: application/vnd.github.raw 헤더 → base64 아닌 raw 텍스트 직행(UTF-8). 기본 JSON 응답의 content는 base64+줄바꿈이라 디코딩 필요.
- PUT의 content는 base64 인코딩(줄바꿈 없이).
- 한글 파일명 API 경로: urllib.request는 한글 URL을 ASCII로 못 보냄. urllib.parse.quote(segment)로 퍼센트 인코딩 필수 (app/pages/1_파일처리.py 등).

- PAT은 비밀: repo·KB·로그에 절대 안 적음. 프로젝트 지식 파일에만. 만료 시 그 파일만 갱신. fine-grained(work-automation-wb + work-automation-app, contents 읽기·쓰기).

## 인코딩
- 한글은 UTF-8. base64 디코딩 시 Latin-1 금지(모지바케). raw 헤더로 받으면 디코딩 자체가 불필요.

## Google Drive (엑셀 작업물 전용 — KB 아님)
- 커넥터 update/delete 없음, 생성+읽기만. 엑셀은 템플릿=읽기전용·결과=날짜별 새 파일이라 무방. 삭제는 사용자 수동.
- 읽기는 download_file_content(base64→UTF-8). read_file_content는 마크다운 변형(미리보기용).
- 파일 생성 시 contentMimeType + disableConversionToGoogleType=true.

## 보안 (업무 도메인)
- KB에 PII·비밀 금지. 부수효과 동작은 정확한 payload 보여주고 승인.

## 작업 규율 (투자시스템에서 배움)
- 검증 단계화: 변경 전 실물 재확인 → 변경 후 대조. 최고 ROI.
- 1작업단위 1로그. 막힌 것·미완·실패도 로그 "다음/상태"에 정직하게(작업>로그 지연이 제일 위험).
- 향후 커스텀 Worker 만들 때 atob() UTF-8 미디코딩 버그 주의.

## 한국어 처리 (엑셀/앱)
- 주소·상품명 매칭 전 NFC 정규화 필수(unicodedata.normalize("NFC", s)). 출처 다른 데이터가 NFD(자모 분리)면 같은 글자라도 부분일치 매칭 실패 → 도서산간/미배송 매칭 치명적.
- reference csv는 UTF-8-sig(BOM)로 저장. Excel에서 직접 열어도 안 깨짐.
- 대시보드 차트: matplotlib는 한글 폰트 미설치 시 □□□. Plotly/Altair(브라우저 폰트) 권장.
- 정렬: VBA xlPinYin vs Python 코드포인트 정렬 차이 가능 → 골든 파일 대조로 확인.

## 마켓플레이스 입력 파일 (.xls)
- 스마트스토어/쿠팡/G마켓 등이 내보내는 .xls 파일은 실제로 HTML 테이블. xlrd나 openpyxl로 열리지 않음.
- 읽기: raw.decode('utf-8').replace('\ufeff','').replace('<feff>','') 후 pd.read_html(io.StringIO(html), header=0)[0].
- 송장번호는 숫자로 파싱될 수 있음 → astype(str).str.replace('.0$','') 처리 필요.
- dosan_list.csv가 크면(10551행) curl 명령줄이 "Argument list too long" 오류 → Python urllib으로 업로드.

## VBA FasterCopyRows 버그 (재현 필수)
- ListSheet.Range("B1:B" & LastRowList) — B1(헤더='주소')부터 읽음.
- '주소' 자체가 키워드로 포함 → '(상세주소 없음)', '김승주소아과' 등 매칭됨.
- 도서산간아님 예외 로직 없음 (VBA에 미구현, 해당 시트는 데이터만 있고 미사용).
- Python 재현: ds_kw = ['주소'] + [normalize_kr(k) for k in ds['주소'].tolist() if k.strip()]

## 상품명 줄바꿈 인코딩
- 골든 xlsm: ,_x000D_\n (OOXML CRLF 인코딩) — pd.read_excel로 읽으면 리터럴 문자열.
- HTML-xls 원본: ', ' (컴마+공백) — 같은 데이터, 표현 형식만 다름.
- 테스트 비교 시 골든 정규화 필요: df['상품명'].str.replace(',_x000D_\n', ', ', regex=False)

## 합포확인 정렬
- VBA SortColumnBDescending: xlPinYin 정렬 (C열=주소 내림차순).
- Python sort_values('주소', ascending=False)와 그룹 내 행 순서 차이 발생.
- 테스트 시 check_like=True 단독으로는 부족 (index 기준 비교됨).
  → 송장번호 기준 정렬 후 assert_frame_equal 사용.

## 온누리양식_발주서 (onnuri_order)
- openpyxl read_only로 읽은 셀 값은 숫자도 str로 읽힐 수 있음 → int() 명시 변환 필수.
- SKU 테이블에 동일 관리코드 중복 존재 → drop_duplicates('관리코드', keep='first') 필수.
- 수식: 합계 = 공급가 × 수량 + ceil(수량/최대합포수량) × 배송비
  - 최대합포수량 = SKU!F열(배송비 부과 규칙). 코카콜라500=1, 일반음료=2~3.
  - 배송비는 합포수량 초과 시 1배송당 1회 추가 (ceil로 반올림).
- 출력: 원본 xlsx를 shutil.copy2 후 합계 컬럼만 openpyxl로 덮어쓰기 → 우편번호 등 원본 서식 보존.
- VBA 로직: 천년경영업로드 시트 F열(총액)을 발주서 G열에 복사 후 SaveCopyAs (확인).
  Python은 이 계산을 직접 수행하므로 천년경영업로드 시트 재현 불필요.


## Streamlit 멀티페이지 / 네비게이션
- pages/ 하위 디렉토리는 자동으로 섹션 인식 안 됨. st.navigation() 명시 필수.
- 새 워크플로우 기준데이터 서브페이지 추가 시: ① pages/2_기준데이터관리/ 에 파일 생성, ② app/streamlit_app.py 의 기준데이터관리 섹션에 st.Page() 한 줄 추가. 두 번째를 빠뜨리면 사이드바에 안 보임.
- **이름 있는 섹션 페이지는 반드시 subdirectory에**: st.navigation()의 named section(비어있지 않은 key)에 등록할 페이지는 pages/하위디렉토리/ 안에 두어야 표시됨. pages/ root에 직접 두면 안 보임. (headerless 섹션 ""·" "은 root 파일 OK)
  - 새 섹션 추가 시: ① pages/<섹션명>/ 디렉토리 생성, ② 파일 생성, ③ streamlit_app.py에 _X = _P/"<섹션명>" 변수 추가 후 st.Page() 등록.
  - sys.path: subdirectory 파일은 parent 4번 (root pages 파일은 3번).
- 섹션 헤더 없는 페이지: dict 키를 "" 또는 " "(공백)으로 설정. Python dict 중복 키 불가라 두 번째 무헤더 섹션은 " "(공백 1개) 사용.

_갱신: 2026-06-01 (Streamlit 네비게이션 함정 추가)_
