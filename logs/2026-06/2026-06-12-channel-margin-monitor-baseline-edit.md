# 2026-06-12 channel-margin-monitor: 기준마진율 편집 (현재 마진율 → 기준)

## 무엇
모니터 표에서 상품 선택 → **현재 마진율을 그 채널의 기준마진율(baseline_margin)로 저장**하는 편집 기능. 전 채널 공통(어느 채널에서든 그 채널 컬럼 편집). 미달 상품의 마진을 목표로 인정 → 미달 해제 용도.

## 왜
baseline_margin은 전 채널 모니터·권장가의 단일 진실원인데 1,228행 CSV 직접 편집이 불편. 모니터는 이미 현재/기준/탐지를 나란히 보여주므로 그 자리에서 한 방에 목표 갱신.

## 설계 결정 (사용자 확정, ADR 0016)
1. **선택 행 기준 + 충돌 시 사용자 선택**: baseline는 관리코드 키인데 표 행은 상품번호. 같은 관리코드에 여러 상품번호(합포·중복리스팅)가 서로 다른 현재마진이면 충돌 → 경고 + 관리코드별 라디오로 값 선택.
2. **즉시 반영**: baseline를 배포본 로컬(load_references)이 아니라 **GitHub 라이브(@st.cache_data ttl600)로 read** → 커밋 후 cache clear+rerun으로 재배포 없이 반영. compute_listing(baseline_override=) 주입.
3. **0.1%p 반올림**: round(현재마진−offset, 3). 0.0917→0.092. 저장 표기 `_fmt_margin`(끝 0 제거).
4. **위치**: 모니터 페이지 하단, 기존 표 체크박스 선택(sel_pids) 재사용. 별도 화면 없음.

## 변경 (core + page)
- core:
  - `compute_listing(..., baseline_override=None)` — 주어지면 refs["baseline"] 대체(라이브 기준마진).
  - `parse_baseline_dict(text)` — CSV → {관리코드:{채널:값}} (override·미리보기용, BOM 처리).
  - `propose_baseline(rows, pids, offset, round_to=3)` — 선택→관리코드별 (proposals, conflicts). 마진율 None 제외.
  - `update_baseline_csv(text, channel_col, updates)` — 그 채널 컬럼만 갱신(타 채널·타 관리코드 보존), 없는 관리코드 행 추가. 헤더/열순서/BOM/CRLF 보존. → (새텍스트, 수정수, 신규수).
  - `_fmt_margin(v)` — 0.092/0.05 표기.
- page(6_채널마진모니터.py):
  - `_load_baseline_text`(GitHub 라이브 캐시) + `_commit_baseline`. compute_listing에 override 주입.
  - 하단 "🎯 기준마진율 설정" 섹션: offset 라디오(현재 그대로/−1%p) → "기준마진율=현재(선택N)" → propose → 충돌 라디오 + 미리보기(기존→새·방향) → "저장(커밋)"/"취소". 저장 시 update→commit→cache clear→rerun(즉시 반영).

## 검증
- propose: 40선택 → 18 관리코드 제안 + 6 충돌 분리. 반올림 0.1016→0.102.
- **미달 10개(관리코드 유니크) → baseline=현재 적용 → 전부 미달 해제(0), 전체 미달 49→29.** offset −1%p: 0.0588→0.049.
- update_baseline_csv: ESM 14수정+4신규, 헤더·행수·CRLF·BOM 보존, 식봄 등 타 채널 불변.
- override 즉시반영: parse_baseline_dict→compute_listing → 탐지 재계산 확인. ast.parse OK.

## 다음·상태
- **⚠️ core+page 수정 → Reboot app 1회 필요.**
- 전 채널 공통(스마트스토어~ESM 어디서든 그 채널 컬럼). baseline 라이브 read라 가격변경 권장가도 편집 즉시 반영.
- 미검증: 실제 앱에서 충돌 라디오·저장·즉시반영 사용자 확인.
- 향후(2차): ② 인라인 편집(data_editor) ③ 일괄 규칙(필터 전체=고정값) — 1차(선택→현재)만 구현.
