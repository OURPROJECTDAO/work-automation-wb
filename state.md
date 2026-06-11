# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
> 상태는 통제어휘(운영중/진행중/이슈/개념doc). **상세·검증·미해결·자산은 각 workflows/<name>.md**. 연결=manifest.md.

| 워크플로우 (내부명) | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영중 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서/제이티발주) | 3 | 운영중 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영중 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영중 | workflows/cheonnyeon-upload.md |
| invoice-fill (송장처리) | 3 | 운영중 (4채널) | workflows/invoice-fill.md |
| dashboard (영업이익현황) | 4 | 운영중 (이익률·물류량 점진) | workflows/dashboard.md |
| product-registration-common (등록 공통) | — | 개념doc | workflows/product-registration-common.md |
| smartstore-register (스마트스토어) | — | 운영중 (챗) | workflows/smartstore-register.md |
| easyadmin-register (이지어드민·정산채널) | — | 운영중 (챗) | workflows/easyadmin-register.md |
| esm-register (ESM=G마켓) | — | 운영중 (챗) | workflows/esm-register.md |
| channel-margin-monitor (채널 가격·마진 모니터) | — | 운영중 (5채널 모니터+가격변경) | workflows/channel-margin-monitor.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (운영 최소): 대시보드 — 데이터계층+저장어댑터+3개년 적재(313K행)+최소 페이지(매출 집계)+증분 업로더([데이터 추가] 탭) 배포. 차트/물류량/이익률/거래처그룹 점진추가. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- 없음. (B2 인프라 완료 — repo·PAT R/W·st.secrets 검증됨 2026-06-08.)

## 다음 한 수
- **Phase 4 대시보드 점진 확장**: 매출집계·증분업로더·거래처그룹·구분분류·기간 날짜범위·일/월/연 추이·**이익 모드(택배비=ERP 00-12 라인, 3000/2500 보정 토글, 이익률=이익/매입가, 전체 거래처)** 배포 완료(decisions/0008). 다음 후보 — ① 물류량(수량÷박스내품) ② 이익/물류량 콤보(이중축). 상세 workflows/dashboard.md.
- core/ 신규 모듈을 페이지가 import → 첫 배포 후 Reboot app 필요(pitfalls 모듈캐시).
- **상품등록 운영 중**(챗 네이티브, ADR 0009): smartstore·esm·easyadmin. **멀티채널 배치 입력폼 v2**(`reference/product_input_form_v2.xlsx`, 대상 채널=스마트스토어/G마켓/둘 다) 배포 완료(2026-06-10) — smartstore·esm 공용, 구 v1 deprecated. 이미지확장자=URL 실검사 자동판별 확정. 미해결 — 결정적 엔진/캐시 미구현. 상세 workflows/product-registration-common.md·*-register.md.
- **대시보드 product_attributes**: ✅ 슬림화(ADR 0011, 2026-06-10) — 4컬럼(식품음료·합포수량·최종분류). 차원=세분류만 + 식품음료 구분 3차 fallback(브랜드·b2b 폐기). **Reboot app 필요.** 451 합포수량 채우면 병합. 상세 workflows/dashboard.md.
- **상품마진(온라인) 탭**: ✅ 신설(ADR 0012, 2026-06-10) — 합포×내품 택배배분 추정 + 채널 보정계수(실제송장÷추정송장). 온라인 거래처 자동스코프. page-only. 상세 workflows/dashboard.md.
- **channel-margin-monitor**(채널 가격·마진 모니터, 운영중): 스마트스토어·식봄·**캐시노트** 모니터. 스마트스토어·식봄은 가격변경도. 표준 정산식=스마트스토어형(2700·ceil), 수수료만 채널별(스마트스토어/캐시노트 6%·식봄 7%). **캐시노트 추가 완료(2026-06-11, ADR 0014)** — 골든 513/513 입력 일치(N·배송비 전건). 신규 축: `ship_fee_policy`(배송정책코드 조건부 배송비)·`_pid`(상품번호 숫자셀 정수정규화). 행사 차등수수료는 무시(소스 없음). **캐시노트 가격변경 완료(2026-06-11)** — '(캐시노트)양식' append(A=OFR·D=SKU 다운로드 Q/R `extra_cols` 보존, F=수정·L=Y·N=9999 고정, G=권장가·H=정가). 식봄 append 로직 `build_append_items` 헬퍼로 공용화. **⚠️ core 수정분 Reboot app 필요**. 미해결 — baseline↔product_master 조인 갭. **배민상회 추가 완료(2026-06-11, 모니터)** — 골든 394/394 입력 일치(수수료·정산가 전건). 신규 축: **상품별 수수료**(`commission_source="download"` — 다운로드 BU/100+0.03, 채널 단일값 아님)·listing CSV 스키마 유연화(extra_cols 자동 보존). **배민상회 가격변경도 완료(2026-06-11)** — '(배민)양식' append, J=변경판매가(권장가)·H=변경소비자가=무늬용 가짜(표준 FAKE_JEONG). 옵션번호/옵션명 extra_cols 보존. **무늬용 가짜정가=전 채널 표준 단일화**(권장가+20~30% 랜덤·100원, jeong_field 있으면 기본) — 식봄·배민도 적용(2026-06-11). **쿠팡 추가 완료(2026-06-11, 모니터+가격변경)** — 골든 1989/1989(정산가·N·판매가). 수수료 12% 단일·배송비 0·키=옵션ID. 가격변경은 **filter형 신설**(다운로드 자체가 조회+변경요청 컬럼형 → 원본 P/Q 기입, build_filter_price_xlsx). 5채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡) 전부 모니터+가격변경. **다음: 알리.** 상세 workflows/channel-margin-monitor.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-11 (channel-margin-monitor 쿠팡 추가 — filter형 가격변경·옵션ID키·단일12%)_
