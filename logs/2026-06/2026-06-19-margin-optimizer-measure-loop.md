# 2026-06-19 두뇌④ 측정 루프 (Gate 3 닫기) 구현

## 무엇
두뇌④ 결정 원장의 pending 결정을 **결정일 이후 실적**으로 측정 → 효과 판정(개선/악화/무변화) → 유지/되돌림. Gate 3("잘못된 결정 리뷰") 가동. v0가 "결정 기록"까지였다면, 이번에 "측정→조치" 루프를 닫음.

## 사용자 확정 (인터뷰)
- 측정창 = **30일**(빠른 피드백).
- 되돌림 = **버튼이 baseline Δ 역가산 자동 원복**(승인 후, cmm 반영).

## 변경 (work-automation-app)
- UPD `core/intelligence/margin_optimizer.py` — 측정 루프 순수함수 추가:
  - `MEASURE_MIN_DAYS=30`·`RESP_BAND=0.10`(±10% 월순이익 밴드).
  - `_verdict(action, before, after, ready)` → (결과, 제안). before>0면 ±밴드, before≤0면 절대델타(thr=max(|before|×0.1, 1000)). 개선→유지(↓면 추가인하 후보)/악화→되돌림/무변화→유지(관찰).
  - `measure(prod, pending, today, min_days)` — 각 pending의 (관리코드·채널) ts 이후 거래만으로 월 run-rate 재계산(월수=YYYY-MM nunique·동일 마진정의 순/매출). ready=경과일≥30 ∧ post_개월>0. 측정후 월순이익/월볼륨/마진·결과·제안 부착.
- UPD `core/intelligence/decision_log.py` — `update(records, pat, repo)`: decision_id로 기존 행 in-place 갱신(측정/조치 공용). COLS 내 키만 덮어씀. 스키마 무변경(18컬럼 그대로 — 측정후마진은 화면계산만, 미저장).
- UPD `app/pages/13_기준마진율최적화.py` — **탭 구조 도입**(작업목록 / 측정 결과). 
  - `build_prod()` 분리(작업목록·측정 공용 캐시) · `build_worklist`가 이를 사용 · `_apply_baseline` 모듈레벨 승격.
  - 측정 결과 탭: KPI(측정가능·개선·악화·대기) → ① pending·ready 라이브 산출 표 + [측정 확정](원장 측정후·결과·status=measured) → ② measured 표 + [유지로 닫기](status=closed) / [되돌림](baseline −Δ 역가산 원복 + status=reverted, 원복 payload 미리보기 후 버튼). 측정대기는 expander.
  - 45일 억제 필터에 `status=="pending"` 조건 추가(measured/closed/reverted는 새 결정 위해 재노출 허용).

## 핵심 결정
- **되돌림 = 상대 역가산**(현 타깃 + (마진_before − 마진_적용)) — 절대복원 아님(ADR 0027 상대 철학 유지). 사이 다른 baseline 변경에 안전. 기록만 결정(마진_적용==마진_before)은 원복 대상 아님 → 종료만.
- 측정후=ts 이후만(결정 전 실적 섞임 방지). post 데이터 없으면 측정대기.
- 판정은 **제안**(행사·시즌·품절 교란 미보정·관찰 한계 명시) — 사람 최종.
- status 어휘 확장: pending→measured→closed/reverted (forward·비-PII).

## 검증
- 합성 prod+pending 4건 스모크: aaa(↓·전 11만→후 26만)=개선·"유지·추가인하 후보" / bbb(↑·전 1만→후 0.3만)=악화·되돌림 / ccc(경과 7일<30)=측정대기 / ddd(post 매출 0)=측정대기. 전건 일치.
- ast.parse 3파일 OK. 결정 원장 현재 0행(forward seed) → 실데이터 측정 대상은 결정 누적+30일 경과 후 자연 발생.

## 다음 · 상태
- 상태 = partial(v0 + 측정 루프 라이브). ★**재배포(1~2분) + Reboot 1회 필요** — 기존 import 모듈(margin_optimizer·decision_log)에 함수 추가 → sys.modules 캐시. 페이지는 자동반영이나 새 core 함수 참조라 Reboot 없으면 AttributeError.
- 검증 대기(사용자): 결정 기록 → 30일 후 측정 결과 탭에 등장 → 측정 확정 → 유지/되돌림(되돌림 시 baseline 원복 cmm 반영).
- 다음 한 수: ⑧ 시즌(명절세트) 라벨 제외(월순이익 부풀림) → ⑦ 매출목표 라벨(sales_target.csv 포맷 선결) → ② 회전 markdown·나들 floor 클램프.

## 관련
ADR 0026·0027 · workflows/margin-optimizer.md §15 · 2026-06-19-margin-optimizer-{build,ops}.md
