# 로드맵 / 백로그

> **상세 우선순위·노드별 로드맵 정본 = `systemmap.json`** (ADR 0019). 이 파일은 큰 그림(완료 이정표·다음 초점·나중)만 둔다.

## 완료
- KB 기억 시스템 구축 / 아키텍처 확정(Streamlit+Python+Community Cloud). 2026-05-31~06-01. (0001·0002)
- **Phase 1**: 오픈마켓합포도서산간확인V7 Python 재구현 + pytest PASSED. 2026-06-01.
- **Phase 2**: Streamlit 앱 배포 + 기준 데이터 관리 UI. 2026-06-01.
- **Phase 3 4종**: onnuri-order · logistics-order(0003·2-phase 게이트·프린트·골든) · cheonnyeon-upload(0005·분류표 공유·골든 27시트 0불일치) · invoice-fill(식봄·올웨이즈·배민상회·캐시노트 4채널). ~2026-06-05.
- **KB 구조 재편**: 전용 함정·상태를 workflows/<name>.md로 분리. 2026-06-02. (0004)
- **smartstore-register**: 챗 네이티브 상품등록(2모드·판매가공식·합포배송비·AI 상품명/카테고리·셀서식 일치). 2026-06-09. (0009)
- **Phase 4 대시보드 운영**: 3년 매출 parquet → KPI·피벗·추이·거래처그룹·상품분류. 온라인 상품마진(P2 송장 실배분·EA 송장그룹÷매출낱개·00-12 정합). 2026-06.
- **channel-margin-monitor 운영**: 8채널 리스팅 마진·기준 이탈·권장가 + 7채널 가격 일괄변경.
- **upload-monitor 운영**: 박스재고 있는데 채널 미업로드 탐지(8채널 갭 매트릭스·이미지 XLSX·skip 관리). 설계 0017. L4 등록 핸드오프=후순위.
- **intelligence-layer 이력엔진 완성**: 가격이력(수정로그·1년 롤링·역재생)·재고 스냅샷(forward)·**주문 398K(2023-03~2026-05)**·**매입현황 66K(2022-01~2026-05)**·판매가 3중 검증·P2 송장 실배분. 설계 0018. 모두 관리코드/일자 조인. (1a·1b·P2·주문/매입 적재 완료)
- **두뇌① 마진 침식 강화**: 3렌즈(이미침식·곧침식2C·실판매이상) + velocity 월손실액. margin_erosion.py +5함수·8_마진침식.py 3탭. 2026-06-15. (0020)
- **두뇌① 탭D 당일 점검**: 당일 3파일(천년경영 output·송장출력·master)→당일 실현마진 이상치. 매출=실제기입단가(net)·택배=채널flat×실박스(송장)×물류량. daily_margin.py·8_마진침식 4탭. 2026-06-15.

## 다음 (초점) — 상세·순서 정본 = systemmap.json
- **intelligence-layer 두뇌 신호결합 단계** (데이터 backbone 완성, 0020 재배열):
  1. ✅ 두뇌① 강화(3렌즈+velocity) — 2026-06-15
  2. **두뇌② 입고·품절 예측** [next] — 현재고(product_master)+소진율(velocity)+리드타임(1c 발주⨯매입현황 입고일). upload-monitor 반응형→예방형 확장 또는 신규 '재고 지능' 페이지.
  3. 두뇌③ 채널 가격 A/B(실현마진×velocity 단위경제) → 상품 360도 카드(통합 뷰). [planned]
- **Phase 3 나머지 템플릿**: 1종씩 Python 이관 — 업무의 1/10 미만 이관됨(다수 남음), 사용자 실물 파일 제공 대기.

## 나중
- 입력 자동 수집(API/크롤링) — ERP API 연동 현재 불가 확인(0006).
- 대시보드 미분류 코드 분류 UI(사용자가 구분 값 배정).
- 동료 접근 확대 / 필요 시 Railway 이전(Streamlit Cloud RAM 1GB·스케줄러 없음 대비).
- 상품등록: 결정적 엔진 추출 + 관리코드→{상품명,카테고리} 캐시 성숙 후 재업로드 Streamlit/API 분리 검토. 채널 7~8개 확대.
- intelligence-layer later 묶음(systemmap 참조): listing 스냅샷·행사 로깅·시장지능(경쟁가)·퍼널·세트 보정·상품택배비 실측·2023 여름 갭 백필·데이터현황 2단계 업로드.

_갱신: 2026-06-15 (roadmap.md 표류 정리 — 본문이 dashboard·upload-monitor·intelligence-layer를 '미구현'으로 적은 구식 상태였음. systemmap.json 정본 체제(ADR 0019)에 맞춰 완료 이정표 현행화 + 상세는 systemmap 포인터로 슬림화. 두뇌① 강화 완료 반영)_
