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

## 한국어 처리 (엑셀/앱 — 전 워크플로우 공통)
- 주소·상품명 매칭 전 NFC 정규화 필수(unicodedata.normalize("NFC", s)). 출처 다른 데이터가 NFD(자모 분리)면 같은 글자라도 부분일치 매칭 실패 → 도서산간/미배송 매칭 치명적.
- **숫자 ID 키 정규화 (전 워크플로우 공통)**: openpyxl은 정수 ID 셀(예 상품번호 46903)을 **float(46903.0)**로 읽음. str()/NFC만 하면 '46903.0' → CSV/reference의 '46903' 키와 매칭 실패(조용히 미매칭=기본값). 정수값 float은 int화 후 키로 쓸 것(`int(v) if isinstance(v,float) and v.is_integer() else v`). (channel-margin-monitor 캐시노트 N 전건 1 오류 사례, logs/2026-06-11-cashnote)
- reference csv는 UTF-8-sig(BOM)로 저장. Excel에서 직접 열어도 안 깨짐.
- 대시보드 차트: matplotlib는 한글 폰트 미설치 시 □□□. Plotly/Altair(브라우저 폰트) 권장.
- 정렬: VBA xlPinYin vs Python 코드포인트 정렬 차이 가능 → 골든 파일 대조로 확인.

_갱신: 2026-06-11 (openpyxl 저장 네이티브 포맷 파괴 함정 추가 — 쿠팡 업로드 사례)_
