# 2026-06-15 velocity 갈림길 해소 — 우선순위 확정

## 무엇
지난 세션 재개점이던 "velocity 활용 갈림길"(EasyAdmin 주문 51,641행 적재+판매가 신뢰도
검증 완료 후 멈춰 둔 4갈래)을 사용자가 확정. 4개 후보를 순서 매김.

## 왜
주문 velocity·송장그룹 데이터를 다 준비해놓고 "어디에 먼저 연결할지"만 미정이었음.
사용자 결정으로 분기 해소 → 다음 작업이 P2로 확정.

## 변경 (확정 순서)
1. **P2 송장 실배분 → 진짜 마진** — 최우선. EasyAdmin 송장번호 그룹으로 박스당 실택배비를
   구성 상품에 배분 → 상품별·채널별 실현마진. 대시보드 온라인마진 탭의 추정송장·k계수를
   실측으로 교체. core `intelligence/ship_alloc.py` 신설 예정. 데이터 준비됨.
2. **2025 주문 백필** — P2 다음. = EasyAdmin **확장주문검색 .xls** 를 2025 기간으로 추가적재
   (`orders/easyadmin_2025-*.parquet`). velocity 이력을 과거로 확장. 컨테이너 처리(Streamlit 1GB 회피).
   (사용자 확인: "주문백필 = 이지어드민 확장주문검색 추가적재" 맞음.)
3. **두뇌③ 채널 가격 A/B** — 2025 백필 다음. 채널별 가격·velocity 준실험 + 가격변경 전후.
   신규 '가격 A/B' 페이지.
4. **두뇌① velocity 가중 정렬** — **후순위(지금 불요)**. 마진침식 정렬에 velocity 결합
   (침식×판매량=월 손실액). tier next→later 강등.

## 검증
- systemmap.json intelligence-layer.roadmap 재정렬 + 2025 백필 항목 신규 추가(기존엔 갈림길에만 존재).
  검증 3종(json 파싱·필수키/enum·edge 참조) 통과. PUT 200.
- state.md '다음 한 수' 슬림화(4-택1 → 확정 순서), 재개점 헤더 갱신.
- roadmap.md 서사 미러 note.

## 다음 · 상태
- **다음 작업 = P2 송장 실배분 착수.** 입력=EasyAdmin 주문 parquet(orders/easyadmin_2026-*, 송장그룹 해시 보유).
  대상=대시보드 온라인 상품마진 탭(현 추정송장·k). 신규 core `ship_alloc.py`.
  P2 시작 전 워크플로우 = intelligence-layer.md §5 Phase 2 + dashboard.md(온라인 상품마진 탭) 재확인.
- ADR 신설 안 함(아키텍처 변경 아닌 기확정 항목 순서조정) — 본 로그가 결정 기록.
