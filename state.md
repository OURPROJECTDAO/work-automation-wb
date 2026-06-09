# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
| 워크플로우 | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영 중 · 골든 5시트 PASS · 송장 단독파일(★★송장) 복원 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서) | 3 | 운영 중 · 골든 15/15 · 빈 G셀 픽스 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영 중 · 골든 4 passed · 프린트 디자인 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영 중 · 골든 27시트 0 불일치 · pytest 29 · logistics 체인 | workflows/cheonnyeon-upload.md |
| invoice-fill (송장처리/송장번호 일괄입력) | 3 | 운영 중(확인) · 식봄·올웨이즈·배민상회·캐시노트 4채널 · 송장형식 채널별 · 배송상태 변환 | workflows/invoice-fill.md |
| dashboard (영업이익현황 대시보드) | 4 | 운영 · 📊 지표 토글 매출/이익(택배비=ERP 00-12 라인·3000/2500 보정) · 집계기준 행×열 교차표(피벗) · 기간/구분/그룹·거래처 체크박스·일/월/연 추이 · 마스터 41파티션·42.2만행·거래처1041 · 물류량 점진 | workflows/dashboard.md |
| product-registration (공통 개념) | — | 전 채널 공유: 낱개/박스·합포장→배송비N·마진산정공식·상품명정제·카테고리매핑·캐시·서식일치. 플랫폼별 슬롯(양식·카테고리표·배송비코드·수수료) 정의 | workflows/product-registration-common.md |
| smartstore-register (스마트스토어) | — | 운영(챗 네이티브) · 공통=product-registration-common · SS 전용값(양식13컬럼·수수료6%·카테고리csv·N→코드표·고정값·이미지) · 글로벌하베스트 배치 생성 | workflows/smartstore-register.md |

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
- **smartstore-register 운영 시작**(챗 네이티브, ADR 0009): 규칙·reference·캐시 KB화. 미해결 — reference 커밋 승인대기·이미지확장자 자동검증·결정적 엔진/캐시 미구현. 상세 workflows/smartstore-register.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-09 (상품등록 공통/플랫폼별 분리 — product-registration-common 신설 + smartstore 전용값 슬림화)_
