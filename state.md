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
| dashboard (영업이익현황 대시보드) | 4 | 데이터계층 코어 완료(테스트 8) · 저장어댑터·페이지 대기(B2) | workflows/dashboard.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (진행 중): 대시보드 — 데이터 계층 코어(sales_data) 구현·테스트·커밋 + 조인검증 완료. 분류방식(A)·저장소(B2) 확정. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- **B2 인프라(사용자 수동)**: fine-grained PAT는 repo 생성 권한 없음(403). 사용자가 ① private repo `OURPROJECTDAO/work-automation-data` 생성 ② PAT에 그 repo Contents R/W 권한 추가 ③ 앱 st.secrets에 PAT+repo 등록. 완료 후 저장어댑터·대시보드 진행.

## 다음 한 수
- **Phase 4 ④ 대시보드 마무리**(B2 인프라 후): 저장어댑터(work-automation-data parquet R/W) → 부트스트랩 업로더 UI → 대시보드 페이지(`3_대시보드.py` 현 플레이스홀더) + 거래처 그룹 관리 탭. 데이터계층 코어·조인검증은 완료. 상세 workflows/dashboard.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-08 (Phase 4 데이터계층 코어 구현·조인검증 + 분류(A)·저장소(B2) 확정 — decisions/0006)_
