# 2026-06-19 기준마진율 최적화(두뇌④) v0 구현 — 코어·페이지·결정 원장

## 무엇
설계(ADR 0026)를 v0로 빌드·커밋. 권장 기준마진율 자동 산출 + 작업목록 페이지 + Gate3 결정 원장.

## 변경 (work-automation-app)
- NEW `core/intelligence/margin_optimizer.py` — 순수함수. cell_stats(prod)·base_margin·recommend_code·worklist. 마진=순이익/정산액(택배 실배분). 상수 PROVEN_CUM=0.85·IGNORE_SHARE=0.01·HALF_STEP=0.5·BIG_MOVE=0.03·MIN_DELTA=0.003·MIN_MONTHS=6·FLAT_STD=0.015.
- NEW `core/intelligence/decision_log.py` — forward-only 원장. read_all·append·init_empty → work-automation-data:`history/decisions.parquet`(18컬럼). Gate3.
- NEW `app/pages/13_기준마진율최적화.py` — 두뇌③ 로더 재사용(compute_online_margin·ship_alloc 실측). 필터(채널·플래그·검색)·KPI(손볼것·🟢🟡🔴)·작업목록 표(임팩트순)·행 선택→원장 기록·CSV.
- UPD `app/streamlit_app.py` — 네비 " " 그룹에 등록(🎯).
- (data) NEW `history/decisions.parquet` — 빈 원장 seed.

## 핵심 구현 결정 / 버그수정
- **proven = 월순이익(run-rate) 누적 85%, 경계 넘는 채널까지 포함**(prev_cum<0.85). ★초기 버그: 총 순이익 기준이라 개월 적은 채널(스마트 7개월)이 밀려 hold-low 오분류 → run-rate+크로서 포함으로 수정. 15-04에서 식봄·스마트·캐시 3개 proven(사용자 수작업과 일치).
- 비proven이지만 주력급(비중≥10%) 베이스 미만 → hold-low 아니라 ↑상향(가격둔감 여지) guard.
- MIN_DELTA 가드: |Δ|<0.3%p → 유지(작업목록 노이즈 컷).

## 검증 (실데이터 18개월·prod18 = ship_alloc 실측)
- 15-04 스팸클래식340: 식봄 유지·스마트 유지·캐시노트↑절반스텝·알리↓·배민↓·ESM hold-low🔴·올웨이즈 실험큐 — 사용자 수작업 결론과 일치.
- 31-04-02 코카콜라500[업소]: ESM(최대볼륨) proven·base 5.2%·식봄/배민↓·올웨이즈 hold-low·쿠팡(0.1%) 실험큐.
- 전체 624코드/2596셀 worklist 작동. 손볼것 1328(🟢227·🟡417·🔴684)·실험큐 155.

## 알려진 v0 한계 (후속)
- 손볼것 53% — 절반스텝 미세조정 多. 실무=임팩트순 top-down·작아지면 멈춤(min-Δ 컷 적용했으나 여전히 많음).
- ⑧ 시즌(명절세트) 미보정 → 개월 적은 세트류가 월순이익 상위 부풀려짐. ⑧ 라벨로 제외/특수처리 후속.
- 나들=하한 참조 채널이나 v0엔 명시적 floor 클램프 없음(베이스가 de-facto floor). 명시 클램프 후속.
- ② 회전 markdown·cmm 편집창 직접 prefill·측정 루프(원장 측정후 채움) 미구현 — 다음.

## 다음 · 상태
- **상태 = partial(v0 라이브).** ★**Reboot app 필요**(신규 core import → sys.modules 캐시).
- 다음: ① 측정 루프(다음 사이클 매출/스냅샷으로 원장 측정후·결과 채움 → 유지/되돌림 자동 판정) ② ⑧ 시즌 라벨 제외 ③ cmm 편집창 직접 prefill ④ ② 회전 markdown 결합.

## 관련
ADR 0026 · workflows/margin-optimizer.md · 2026-06-19-margin-optimizer-design.md(설계)
