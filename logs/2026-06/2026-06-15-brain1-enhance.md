# 2026-06-15 두뇌① 강화 — velocity 가중 + 2C 예방경보 + 실판매 마진 이상 (ADR 0020)

## 무엇 / 왜
데이터 backbone 완성 후 두뇌① 첫 강화(ADR 0020 1순위). 기존 v1(가격이력 매입↑ ∩ 채널 listing 마진 미달, 반응형 단일신호)을 **3렌즈 + velocity**로 확장. 사용자 아이디어(실판매 마진 이상) 흡수.

## 변경
- core `margin_erosion.py` 확장(+160줄): 채널 매핑(`EA_TO_CMM`+`_sangho_to_cmm`=ship_alloc.SANGHO_TO_EA∘EA_TO_CMM) · `channel_velocity`(orders 상품수량×박스내품=월낱개) · `latest_buyin_price`(박스오입력 정규화) · `pending_buyin_raises`(2C·alerts/suspect) · `sales_margin_anomalies`(실판매 실현마진 이상).
- page `8_마진침식.py` 전면 개편 → **3탭**: A 이미침식(v1+월손실액)·B 곧침식(2C)·C 실판매이상. 로더 추가(orders·buyin·sales·product_master·baseline). ⚠️ core 수정 → **Reboot app 1회**.

## 3렌즈 (사용자 확정 설계)
- **A 이미 침식**: listing 매입↑(price_changes) ∩ 채널마진 미달. 기존 v1 + **velocity 월손실액=(현재매입−과거매입)×월낱개판매** 정렬.
- **B 곧 침식 (2C)**: 최근 실입고가 > master 매입가(min_pct↑) ∩ master 미수정(∉raises). master 반영 시 줄어들 마진 예고. velocity 월손실액=(실입고−master)×월낱개.
- **C 실판매 이상**: 매출자료 실현마진(판매이익/판매금액) = **역마진 OR 채널 baseline−2%p 미달**. 오프라인(상호명 미매핑)=역마진만. **합포·소분 포함**(ERP 낱개분해 이익 정확, Q3).

## ★ 핵심 사실 (사용자 실무 답)
- 마진 기준 = master 매입가(ERP가 상품관리에서 직접 고친 값). 매출자료 판매이익도 같은 기준 → 탭B(2C)가 탭C 마진 과대를 예고(셋 맞물림).
- 이상 판정 = 역마진 + 안전마진(baseline) −2%p. (a) baseline 대비 기본.

## 검증 (실데이터, NOW=2026-05-31)
- **velocity**: 채널별 월낱개 합 합리(스마트94K·ESM93K·식봄46K·캐시44K·쿠팡42K·알리25K·배민21K·올웨7K). 1044(채널,코드)·404코드.
- **2C**: 정규화·상한 후 **경보 385건·suspect 6건**. Δ% 중앙 20%·p90 40%·최대 59%(현실적). 274-245(단가==박스단가 박스오입력)→정규화로 제외(master 일치).
- **실판매**: **34건**(역마진 23·baseline 미달 11·오프라인 18). 칠성사이다 −33%·펩시 −21%·가야알로에 −1% 등 진짜 손해 거래 포착.

## ★ 전용 함정 (구현 중 발견)
- **매입현황 단가 박스단위 오입력 3.2%**: '단가==박스단가 & 박스내품>1' = 박스단가가 단가칸에 들어감 → 낱개단가 = 박스단가/박스내품 으로 정규화(`latest_buyin_price`). 안 하면 +900% 거짓 2C 경보. (전체 99.5%는 단가×박스내품=박스단가 정상)
- **2C Δ% 상한(max_pct=0.6)**: 초과(+60%↑)는 관리코드 충돌/단위잔류/극과거 master 미갱신 의심 → suspect 분리(자동경보 제외, 검토용).
- price_changes 관리코드 트레일링 하이픈은 raises에서 NFC strip(기존). buyin/orders/master는 풀코드 동일(트레일링 없음).
- 단위: orders 상품수량=판매단위 ×박스내품=낱개. 매출=낱개. 매입Δ=원/낱개. 손실액=낱개 일치(P2 단위 함정 회피).

## 다음 / 상태
- ✅ 두뇌① 강화 완료(3렌즈+velocity). ⚠️ **Reboot app** 후 동작.
- 향후 정밀화: ② 실현마진(P2 송장)으로 탭C 택배 반영 · velocity를 매출 낱개(정산)로 교차 · 합성코드 listing 조인(탭A 한계).
- **다음 = 두뇌② 입고·품절 예측**(현재고+velocity+리드타임 1c). velocity 함수 재사용.
