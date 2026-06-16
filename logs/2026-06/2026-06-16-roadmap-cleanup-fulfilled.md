# 2026-06-16 — 로드맵 충족 항목 정리 (planned 표류 제거)

## 무엇
캐치업 후, systemmap.json(로드맵 정본·ADR 0019)의 planned/later/backlog 항목 중 **이미 기능상 충족되어 만들 필요가 없는 것**을 제거. 실사용 코드/워크플로우 문서로 충족 여부 재확인 후 정본+미러 동기화.

## 왜
완료된 작업이 planned에 남아 "할 일"처럼 표류 → 다음 한 수 선택 시 노이즈. 사용자 요청("이미 충족되어 만들 필요 없는 것 지워줘").

## 변경
**삭제(planned 2건, 둘 다 노드 line/produces에 이미 완료 박제됨 → '같은 사실 양쪽 기재' 위반 해소):**
1. dashboard / "온라인 상품마진 실측화"(추정송장·k → 송장 실배분 교체) — ✅ P2 실측 교체 완료(2026-06-15, ship_alloc.py·`use_actual` 기본 ON). dashboard.md 확인.
2. intelligence-layer / P1·1f "채널 내 고객키 + 합포박스키 적재"(ADR 0021) — ✅ 적재(39개월 430,592행)+ship_alloc 합포박스키 연동 완료(2026-06-16). detail 자체가 ✅완료로 기재돼 있었음.

- systemmap.json: 위 2개 roadmap 엔트리 제거 + meta.updated=2026-06-16k. (커밋 ae63c87)
- roadmap.md: 완료 이정표 현행화(고객키/합포박스키 적재·두뇌③ A/B v1+탄력성·상품360 카드 v1 추가). 표류한 "다음(초점)" 두뇌 신호결합 1~4단계(전부 완료) → "다음 한 수=사용자 선택 후보" 4묶음으로 재작성. 나중 묶음에서 systemmap 비추적 항목(2023 여름 갭 백필=고객키 적재 시 동시 완료) 제거·systemmap later 5종으로 정합. (커밋 3a1c1ef)

**유지(진짜 미구현 — 충족 아님):** 알리 가격변경 · baseline↔master 조인 갭 · dashboard 물류량/콤보 차트 · upload-monitor 제외목록 편집 UI/L4/L5/재고금액×예상마진 · intel 1c 리드타임/listing 스냅샷/행사로깅/데이터현황 2단계/시장지능/퍼널/세트보정/상품택배비 실측 · Phase3 템플릿 · 인프라(Railway). (테스트 fixture류 onnuri 빈G셀·logistics 합포 회귀 포함)

## 검증
- systemmap.json 편집 = Python 파싱 후 수술 + PUT 전 검증 3종(json round-trip / 필수키·enum(status·tier) / 참조해소(edges·asset consumers→node id)) 전부 OK.
- 충족 판정 근거 = 실워크플로우 문서: dashboard.md("✅ P2 실측 교체") · state.md/intelligence-layer 노드 produces(고객키·ship_alloc 합포 교정 박제). 경계선 항목(upload-monitor 제외목록 편집 UI)은 upload-monitor.md "다음=L4 + 제외목록 편집 UI"로 미구현 확인 → 유지.
- 잔여 roadmap 엔트리: planned/later=22, done=2, backlog=2.

## 다음 · 상태
- 상태: 정리 완료. 코드 repo 무변경(KB만) → Reboot 불요.
- 다음 한 수 = 사용자 선택(roadmap '다음' 4후보): ① intel 1c 진짜 리드타임 ② 알리 가격변경 ③ dashboard 물류량 차트 ④ upload-monitor 두뇌② 품절예측 결합.
