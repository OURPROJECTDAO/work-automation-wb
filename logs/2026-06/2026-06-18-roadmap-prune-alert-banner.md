# 2026-06-18 로드맵 프루닝 — 알림 배너 항목 삭제

## 무엇
로드맵(systemmap.json) 예정/나중 전건 감사 → **이미 비슷하게 구현돼 불필요한 1건 삭제**:
intelligence-layer 나중(UI) "데이터현황 2단계(업로드) + **알림 배너**" 에서 알림 배너 부분 제거.

## 왜
원래 알림 배너 설계(§5.6 B "앱 상단 배너": 지난 스냅샷 대비 입고 N·신규 품절 M·마진 침식 K 요약 배너)의 의도가 **데일리 대시보드 섹션들로 이미 충족**:
- 입고 → 신규 업로드 대상(확장판③·detect_new_stock)
- 품절 → 품절 알림판(stockout_board)
- 침식/가격 → 가격 변동 알림(확장판①·detect_price_changes) + 두뇌① 마진침식
→ 별도 상단 배너 신설 불요. 인앱 스냅샷 diff 알림이라는 핵심 가치는 데일리 대시보드가 이미 제공.

## 변경
- systemmap.json: intel node roadmap[] UI 항목 title "데이터현황 2단계(업로드)"로 축소·detail에서 알림 배너 제거+포인터. meta.updated 2026-06-18f. (검증 3종 통과: json·필수키/enum·edge 참조)
- workflows/intelligence-layer.md §5.6 B: 앱 상단 배너 ~~취소선~~+실현 포인터, 푸시는 net-new 유지.
- roadmap.md: later 묶음 라인에서 '+알림 배너' 및 stale '시장지능 크롤링'(=nadl 완료) 정리.
- state.md: 갱신 라인.

## 검증
- 로드맵 전건 점검(예정 7·나중 11·백로그 2). 실물 대조(app/pages 14개·daily-dashboard.md·intelligence-layer.md).
- 데일리 대시보드 확장판①②③(채널요약·가격변동·이상치권장가·이중검수·신규업로드) 모두 빌드 확인 → 알림 배너 가치 충족 확정.
- 경계선 유지 판정: daily '확장판 추가 인사이트'(열린 워크스트림·④⑤ 여지) / upload-monitor '재고금액×예상마진'(두뇌② 매트릭스 결합 미구현) / intel '1d listing 스냅샷'(현재 덮어쓰기만·날짜본 이력 없음) → 전부 유지.

## 다음·상태
- 완료. 로드맵 정본 슬림화됨.
- 다음 한 수=두뇌① 시장대비 권장가(매핑 누적 후). 즉시 착수 후보=1d listing 날짜본 스냅샷(forward-only·시급).
