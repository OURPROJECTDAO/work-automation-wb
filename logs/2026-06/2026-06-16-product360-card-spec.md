# 2026-06-16 상품 360도 카드 — 로드맵 detail 보강 (실무 조회 트리거)

## 무엇
systemmap.json `nodes[intelligence-layer].roadmap[3]` (상품 360도 카드, tier=planned·star) 의 detail 확장. 구현 아님 — 스펙 보강.

## 왜
사용자가 식봄 31-22-02 단발 마진 조회(현재 판매가·마진·N·권장가)를 요청 → 답하려고 product_master(매입가)+listing_sikbom(현재가)+hapo_multiplier(N)+baseline_margin(기준마진) 4파일을 수동 조인. 사용자: "이런 실무적인 업무도 있을 것" → 360카드에 빠진 내용 추가 지시. 기존 detail은 추상적 통합뷰 가치만 있고 (a) 일상 ad-hoc 조회 트리거 (b) 같은 관리코드의 채널 내 다중 리스팅(합포 N 상이) 케이스가 없었음.

## 변경
detail에 2가지 추가:
1. **실무 트리거(★일상 ad-hoc)**: "이 상품 채널 X에서 지금 얼마·마진·기준여유·권장가?" 단발 조회 = product_master+listing_<채널>+hapo_multiplier+baseline_margin 4파일 수동 조인을 카드 1회로.
2. **채널 내 다중 리스팅(N 상이)**: 같은 관리코드가 한 채널에 여러 리스팅(합포 N 다름)으로 존재 가능 → 리스팅별 행으로 펼쳐 각각 매입가(base×N)·마진·권장가. 실증 사례 식봄 31-22-02 = 24개입(상품번호 466071·N1·18,600원·마진 14.9%)·48개입(657403·N2·35,300원·마진 11.3%).
   + 채널별 현재마진 옆 기준마진 여유/미달 + 권장가(채널마진모니터 재사용) 명시.
meta.updated 2026-06-16c→d.

## 검증
- 치환 유일성: old_detail 1건·meta "2026-06-16c" 1건 (텍스트 치환 안전, 포맷 보존).
- ADR 0019 검증 3종: JSON 파싱 OK / 필수키·tier enum(planned) OK·detail·meta 일치 / 구조(edges·assets·nodes) 불변=참조 무결. 바이트 14747→15048.
- PUT commit c62f6e6 (sha c10808c).

## 다음·상태
- 상품 360도 카드 = 여전히 **planned**(구현 순서: 두뇌③ 채널 가격 A/B [next] → 360카드). 이번은 스펙만, 코드 없음. Reboot 불필요(KB만).
- 정본=systemmap.json. state.md/roadmap.md 미수정(ADR 0019 같은 사실 양쪽 기재 금지 — 다음 한 수에 이미 360카드 언급, 상세는 systemmap 포인터).
- 구현 착수 시 재사용 가능: 마진 정산식·4-tier·권장가=channel_margin_monitor core, 매입가 추이=intelligence price_history, 재고/소진=stockout, 침식=margin_erosion. 전부 관리코드 조인.
