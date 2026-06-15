# 2026-06-15 intelligence-layer — 로드맵 재배열 (backbone 완성 점검)

## 무엇 / 왜
사용자: 줄 수 있는 데이터 backbone 다 줬다 → 로드맵 점검·업그레이드 요청. 이력 엔진 완성(매출·주문·가격이력·재고·매입현황 전부 적재, 관리코드/일자 조인 가능)으로 두뇌가 단일신호→신호결합 단계 진입. 재우선순위 합의(ADR 0020).

## 변경 (계획 — 코드 변경 없음)
- decisions/0020-roadmap-resequence.md 신규.
- systemmap.json intelligence-layer.roadmap 전면 재배열: 두뇌① 강화(2C+velocity) next1·두뇌② 승격 next2·두뇌③ planned 강등(실현마진×velocity 강화)·상품360카드 신규 planned. velocity 가중(later)→두뇌① 흡수. upload-monitor 두뇌② 연계 명시. meta.updated.
- state.md·roadmap.md 미러.

## 핵심 업그레이드 아이디어 (데이터 결합으로 세진 것)
- 두뇌① **2C 예방경보**: 실입고단가↑∩master 미수정 = 침식 전 경고(반응형→예방형). + velocity 가중=월 손실액 정렬.
- 두뇌② planned→가능: 현재고+velocity+리드타임 충족. upload-monitor 예방형 확장.
- 두뇌③: 가격 vs velocity → **채널별 실현마진×velocity 단위경제**.
- 신규 상품 360도 카드: 관리코드 단일 통합 뷰(두뇌 3종 후).

## 검증
- systemmap 검증3종 OK(json·필수키/enum·참조해소). 두뇌 roadmap tiers=[next,next,planned×5,later×6].

## 다음 / 상태
- **착수 = 두뇌① 강화(2C 조기경보 + velocity 가중).** 8_마진침식.py + margin_erosion.py 확장. ⚠️ core → Reboot.
- 입력: buyin_purchases(실입고단가) + price_changes(master 수정 여부) + easyadmin_orders(velocity). 조인=관리코드·일자.
