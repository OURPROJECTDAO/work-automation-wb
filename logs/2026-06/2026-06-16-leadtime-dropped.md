# 2026-06-16 — 1c 진짜 리드타임 폐기 (입고주기 cadence 확정)

## 무엇
로드맵 1c(발주자료⨯매입현황 조인 → 진짜 발주→입고 리드타임 → 두뇌② 재발주 정밀화)를 **폐기**. 두뇌② 리드타임=입고주기 cadence로 확정.

## 왜
조사 결과 발주 타임스탬프가 미적재(발주자료=Drive 일별만·orders 발주일=고객 연속수요 부적합·buyin 거래처코드 2024+ 결측) + 사용자: "재발주 시기 정밀화 불필요, cadence로 충분." ROI 낮음·발주신호 자체 불완전(수요≠PO). 갈림길 → ADR 0022.

## 변경 (KB만, 코드 무변경)
- systemmap.json: intelligence-layer P1·1c roadmap 엔트리 삭제 + meta 2026-06-16m. 검증 3종 OK.
- roadmap.md: '다음' 후보에서 1c 착수 라인 제거·재번호 + 두뇌② cadence 확정 명시.
- state.md: '다음 한 수=사용자 선택' 후보 list에서 1c·물류량 차트·알리 가격변경 제거(폐기 표기).
- workflows/intelligence-layer.md: §5 1c bullet 폐기 표기·§6② 한계 cadence 확정·§4 derived/lead_time.csv 폐기·§3.3 용도 갱신.
- decisions/0022-leadtime-cadence-final.md 신설.

## 검증
- 조사 실데이터(probe): buyin 53파티션 거래처코드 2022=100%/2024~26=0%·관리코드 조인 OK·기준일=입고일. orders cols에 발주일 있으나 고객 연속수요. data repo에 발주자료 폴더 없음(groups/history/master/orders/purchases/snapshots).
- stockout.py 현행 = lead: cadence(입고주기)>기본14 — 폐기로 인한 코드 변경 불필요(이미 cadence 확정 동작).

## 다음 · 상태
- 상태: 1c 폐기 정리 완료. Reboot 불요(코드 무변경).
- 다음 한 수 = 사용자 선택(roadmap 후보): intel listing 스냅샷/행사로깅 · dashboard 이익/물류량 콤보 · upload-monitor 두뇌② 품절예측 결합 · Phase3 템플릿.
