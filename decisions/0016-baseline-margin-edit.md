# 0016 — 기준마진율(baseline_margin) 대시보드 편집: 현재 마진율 → 기준

날짜: 2026-06-12 · 상태: 채택

## 맥락
baseline_margin.csv(관리코드×10채널 확정마진율)는 전 채널 모니터의 기준마진율·탐지·권장가 단일 진실원. 1,228행 CSV 직접 편집이 불편 → 모니터에서 "현재 마진율을 기준으로 받아들이기"(특히 미달 상품을 목표로 인정해 미달 해제)를 편하게.

## 결정
1. **편집 위치 = 모니터 페이지 하단, 표 선택 재사용.** 현재/기준/탐지가 한 화면에 있으므로 그 자리에서 선택→한 방. 별도 화면 없음.
2. **선택 행 기준 + 충돌 시 사용자 선택.** baseline 키=관리코드, 표 행=상품번호. 같은 관리코드에 상품번호가 여럿(합포·중복리스팅)이고 현재마진이 다르면 충돌 → 경고 + 관리코드별 후보값 라디오. 비충돌은 자동.
3. **즉시 반영 = baseline GitHub 라이브 read.** 기존엔 load_references가 배포본 로컬에서 읽어 커밋 후 재배포(1~2분) 전 미반영. → 페이지가 GitHub raw(@st.cache_data)로 읽어 compute_listing(baseline_override=)에 주입. 저장 시 cache clear+rerun으로 재배포 없이 반영. (listing과 동일 메커니즘)
4. **0.1%p 반올림 저장.** round(현재마진−offset, 3). 0.0917→0.092. offset 프리셋: 현재 그대로 / 현재−1%p(여유).
5. **채널 컬럼만 수정.** update_baseline_csv가 그 채널(baseline_col) 컬럼만 갱신, 다른 채널·다른 관리코드·헤더/열순서/BOM/CRLF 보존. 없는 관리코드는 행 추가(그 채널만).

## 근거 / 검증
- 미달 10개(관리코드 유니크)→baseline=현재→전부 미달 해제, 전체 미달 49→29. 구조 보존·타 채널 불변·override 즉시반영 확인.

## 영향
core(compute_listing override + propose_baseline/update_baseline_csv/parse_baseline_dict) + page(라이브 baseline + 편집 섹션). Reboot app 1회. 2차(인라인·일괄)는 추후.
