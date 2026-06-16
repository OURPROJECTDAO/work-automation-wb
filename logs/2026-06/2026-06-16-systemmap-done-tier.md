# 2026-06-16 systemmap 렌더러 — done(완료) tier 버킷 추가 (크래시 핫픽스)

## 무엇 / 증상
상품 360 카드 작업 때 systemmap.json intelligence-layer 로드맵 항목 tier를 신규 `"done"`으로 바꿨더니
지도·로드맵 페이지(`0_지도로드맵.py`)가 안 뜸(빈 화면). 사용자 보고.

## 원인
렌더러 JS가 `const tiers={next:[],planned:[],later:[]}` 3버킷만 → `tiers["done"].push(...)` =
**undefined.push → TypeError**로 로드맵 렌더 스크립트 전체 중단. JSON 자체는 유효(파싱 OK).
= ADR 0019 위반: **enum(tier) 추가 시 렌더러 동반 수정** 누락.

## 변경 (렌더러 page-only)
`app/pages/0_지도로드맵.py`:
- JS `tiers`에 `done:[]` 추가 + **미지 tier 안전가드** `(tiers[r.tier]||tiers.later)` — 앞으로 어떤 새 tier든 크래시 대신 later로 흡수.
- HTML: 로드맵 3컬럼 위에 **"✓ 최근 완료"** 섹션(`#sec-done`·full-width·2열)·비면 자동 숨김.
- CSS: `.rmdone`(완료 카드 opacity .72·✓ 접두·live색 bar)·`.d-rm .rm-i.t-done` 테두리.
- JS: `#rm-done` 렌더·`#c-done` 카운트·done 0건이면 섹션 display:none.

## 검증
- ast.parse OK. done 버킷 존재 확인. tier 분포 {later14·planned10·next1·done1} → done 1건(상품360) 정상 분류.
- 미검증(앱): 실제 페이지 렌더(redeploy 후 사용자 확인).

## 다음 · 상태
- ✅ 커밋(app repo 838c403). page → 자동 재배포(1~2분), Reboot 불요.
- **사용자 재배포 후 지도/로드맵 정상 표시 확인 대기.** 상품360은 '완료' 섹션, '지금 만들 것'=두뇌③ 탄력성.
- 교훈: systemmap tier/status/cluster enum 추가 = **반드시 렌더러(0_지도로드맵.py) 동반 수정**(ADR 0019). 이제 안전가드 있어 크래시는 막힘(다만 미지 tier는 later로 잘못 분류되니 여전히 동반 수정 필요).
