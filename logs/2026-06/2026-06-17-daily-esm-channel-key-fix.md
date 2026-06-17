# 데일리 대시보드 — ESM 채널키 불일치 버그 fix (2026-06-17)

## 무엇
데일리 대시보드 당일 점검 표에서 **ESM 행만 현재가·권장가·판정·가격변경이 전부 누락**(판정='listing 없음')되던 버그 수정. 0b page-only.

## 원인 (채널키 대소문자 불일치)
- `cmm.CHANNEL_CONFIG`의 ESM 채널 **딕셔너리 키 = `'esm'`(소문자)** — 타 채널은 모두 한글 표시명(스마트스토어/식봄/…). ESM만 영문 소문자라는 예외.
- 데일리 `daily_margin.SHEET_TO_CMM`은 ESM 시트를 **`'ESM'`(대문자)** 채널명으로 산출.
- → 0b의 `_cmm_listing("ESM")`·`_reco_from_master("ESM")`·`_do_price_change("ESM")`이 `CHANNEL_CONFIG.get("ESM")` → **None** → listing 미로드 → 현재가/권장가 빈칸 + 판정 'listing 없음' + 가격변경 "양식 없음" 오판.
- 채널마진모니터 페이지는 셀렉트박스가 `CHANNEL_CONFIG.keys()`(='esm')를 그대로 써서 정상 — 그래서 그쪽엔 ESM listing이 멀쩡(사용자 지적). **데일리↔cmm 교차 참조에서만** 터짐. 확장판②(2026-06-17)부터 잠복.

## 변경
- 0b에 `_cmm_key(channel)` 보정 헬퍼 — `CHANNEL_CONFIG`에 그대로 있으면 통과, 없으면 **대소문자 무시 매칭**으로 키 해소(전 채널 방어). ESM 'ESM'→'esm'.
- `_cmm_listing`(cfg 조회 + compute_listing 호출), `_reco_from_master`(cfg), `_do_price_change`(cfg) 3곳을 `_cmm_key(channel)`로 해소. listing_esm.csv(1,219건, 관리코드 표준형) 정상 매칭 확인.
- 커밋 29990bc. ast 통과. **page-only → 재배포 자동반영, Reboot 불요.**

## 다음 · 상태
- 재배포 후 ESM 행 현재가/권장가/판정 + ESM 가격변경 시트 정상화. 사용자 확인 대기.
- ★ 근본 잔여: `CHANNEL_CONFIG` ESM 키 `'esm'`(소문자)는 **타 채널 명명 규칙과 어긋난 잠복 지뢰** — daily 외 다른 cross-module 채널명 교차(예 두뇌①/EA 채널명 'ESM')에서도 같은 미스 가능. 현 fix는 데일리 한정 방어. **근본 해결안 = core CHANNEL_CONFIG 키 'esm'→'ESM' 통일**(단 Reboot + 셀렉트박스/저장 채널값 영향 검증 필요) — 사용자 확정 후 별건 진행 권장.
