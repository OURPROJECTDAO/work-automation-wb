# 2026-06-12 channel-margin-monitor — 올웨이즈 가격변경(append) 추가

## 무엇
올웨이즈(올팜) **가격 일괄변경** 추가 — '(올웨이즈)양식' 템플릿에 선택 행 append(식봄/캐시노트/배민형). 모니터에 이어 같은 세션. 이제 6채널 전부 모니터+가격변경.

## 왜
사용자가 가격바꾸기까지 이어서 요청. 가격변경 양식 파일(`올웨이즈_가격바꾸기.xlsx`) 제공.

## 변경 (커밋: 템플릿 f0204d84 · 코어 acafaab6)
- `reference/allways_price_template.xlsx` 신규 — 제공받은 '(올웨이즈)양식'(헤더 r1·가이드 r2·예시 r3·샘플 r4~5). 외부링크 0.
- `core/workflows/channel_margin_monitor.py` 올웨이즈 config 확장:
  - **extra_cols**: 카테고리코드(C3)·판매상태(D4)·옵션명1(F6)·옵션값1(G7)·재고수량(L12). (2옵션명/값 H/I·옵션ID M은 **선택+항상공백** → 미캡처: 양식 H/I/M 공백 유효 + stale 가드 거짓경고 방지)
  - **price_form**(mode append): template allways_price_template.xlsx · sheet '(올웨이즈)양식' · data_start 4 · price_field=**팀구매가(K)**=권장가 · jeong_field=**개인구매가(J)**=표준 FAKE_JEONG(골든 O 가짜가격 대응) · source(상품ID·상품명·카테고리코드·판매상태·관리코드·옵션명1·옵션값1·재고수량) · **int_fields=[카테고리코드,재고수량]**.
- **신규 코어 기능 `int_fields`**(opt-in): build_price_form_append가 지정 양식필드의 all-digit 문자열을 int로 기입(카테고리코드 '103407'·재고 '9999' 텍스트화 방지). 타 채널 미설정 → 무영향.

## 검증 (실데이터 엔드투엔드)
- parse(621) → recs에 extra_cols 보존 → **CSV 라운드트립**(recs_to_csv/csv_text_to_recs) 카테고리코드 등 보존 확인 → compute → build_append_items → build_price_form_append.
- 생성 양식: 헤더 r1·가이드 r2·예시 r3 보존, 템플릿 샘플행(r4~5) 제거, 데이터 r4+.
  - C(카테고리)·L(재고) **int 셀**, D(판매상태)='판매중', E(관리코드), F/G(옵션명/값)=상품명, **J(개인구매가)=FAKE_JEONG > K(팀구매가=권장가)**, H/I/M 공백(None), 외부링크 0.
  - K(팀구매가) = 모니터 권장가와 일치(예 환타 27800). 골든 O(가짜가격)↔J(개인구매가) 가짜 대응.
- **stale 가드 거짓경고 0**: source∩extra_cols 5필드 전부 채워짐(옵션ID 류 제외해서 항상-공백 거짓양성 제거).
- **페이지 무수정**: 6_채널마진모니터.py가 `pf['mode']=="append"` 자동 분기(342행) → 올웨이즈 자동 처리.

## 핵심 결정
- 올웨이즈 가격변경 양식 = **전 컬럼 재업로드형**(필수 多: 상품명·카테고리·판매상태·옵션명/값·재고). 단순 가격칸만 아님 → 필수 컬럼 listing 보존(extra_cols) 후 양식 재기입.
- **J(개인구매가) = 무늬용 가짜(FAKE_JEONG)** — 골든 O 가짜가격과 동일 패턴. 마진엔 미반영(표시용). 개인구매가 ≥ 팀구매가 제약 자동충족(FAKE_JEONG > 권장가).
- 양식 sheet '(올웨이즈)양식'은 다운로드 시트('…수정용')와 컬럼 동일하나 별도 템플릿 → append 채택(스마트스토어형 raw 편집 아님).

## 다음·상태
- **모니터+가격변경 운영 가능. ⚠️ core 수정 → Reboot app 1회 필요**(사용자 이번 세션 후 reboot 예정). listing은 첫 '상품관리 갱신(전체 교체)' 시 extra_cols 포함 자동 생성.
- **미검증(실업로드)**: 올웨이즈 업로더의 inlineStr 허용 여부. build_price_form_append는 openpyxl 저장(inlineStr)이라 식봄/캐시노트/배민과 동일 — 그 3채널은 정상 업로드되나 올웨이즈 실업로드는 미확인. 거부 시 쿠팡식 네이티브 수술 필요(현재 불요 추정).
- 다음 채널: 알리.
