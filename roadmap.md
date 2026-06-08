# 로드맵 / 백로그

## 완료
- KB 기억 시스템 구축. 2026-05-31. (decisions/0001)
- 아키텍처 확정: Streamlit + Python + Community Cloud. 2026-06-01. (decisions/0002)
- **Phase 1 완료**: 오픈마켓합포도서산간확인V7 Python 재구현 + pytest PASSED. 2026-06-01.
- **Phase 2 완료**: Streamlit 앱 배포 + 기준 데이터 관리 UI. 2026-06-01.
- **Phase 3 4종 완료**:
  - 온누리양식_발주서 (onnuri-order). 2026-06-01.
  - 발주서출력업무 (logistics-order) — 2-phase+게이트, 프린트 디자인, 골든 테스트. 2026-06-02. (decisions/0003)
  - 천년경영업로드 (cheonnyeon-upload) — logistics 체인·분류표 공유, 배송비 조인, 낱개 분해, 골든 27시트 0 불일치. 2026-06-04. (decisions/0005)
  - 송장처리 (invoice-fill) — 식봄·올웨이즈·배민상회·캐시노트 4채널, 송장형식 채널별, 배송상태 변환. 2026-06-05.
- **KB 구조 재편**: 워크플로우 전용 함정·상태를 workflows/<name>.md로 분리. 2026-06-02. (decisions/0004)
- **Phase 4 설계 확정**: 대시보드 데이터 계층·수집 아키텍처(calamine→월 parquet 파티션·날짜구간 교체·@st.cache_data·거래처 그룹 기준표·물류량=수량÷박스내품). 2026-06-08. (decisions/0006)

## 다음 (우선순위)
1. ~~Phase 1~~ ✅
2. ~~Phase 2~~ ✅
3. **Phase 3 계속**: 나머지 템플릿 1종씩 Python 이관.
   - 온누리양식_발주서 ✅ / 발주서출력업무 ✅ / 천년경영업로드 ✅ / 송장처리 ✅
   - 다음 템플릿: 사용자 실물 파일 제공 대기. (업무의 1/10 미만 이관됨 — 다수 남음)
4. **Phase 4 대시보드 구현**: 설계 확정됨(decisions/0006). 미결정 master 저장위치(Drive/세션) 확정 후 착수.
   - ① reference 조인 검증 ② 부트스트랩 업로더 ③ 파티션 누적 ④ 대시보드 페이지 + 거래처 그룹 관리 탭.

## 나중
- 입력 자동 수집 (API/크롤링) — ERP API 연동은 현재 불가 확인(0006).
- 동료 접근 확대 / 필요 시 Railway 이전 (RAM 1GB 한계 대비).

_갱신: 2026-06-08 (invoice-fill 완료 + Phase 4 설계 확정 반영)_
