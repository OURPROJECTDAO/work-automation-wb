# 2026-06-15 systemmap.json — 지도+로드맵 단일 진실원천 신설

## 무엇 / 왜
지도(업무·데이터 연결)는 manifest.md, 로드맵은 state.md/roadmap.md에 산문으로만 있어 사용자·Claude 둘 다 시각적으로 캐치하기 어려웠음. 단일 구조화 파일 `systemmap.json`으로 통합 → HTML 프로토타입(+예정 인앱 페이지)이 같은 소스 렌더. 손갱신이라 drift 방지 규칙(스키마 계약·권한 경계·트리거·검증) 동반.

## 변경
- 신규 `systemmap.json`(KB 루트): meta / assets(8 공유자산) / clusters(3) / nodes(13 워크플로우 — status·line·consumes·produces·feeds·page·roadmap) / backlog(2 가로지르는) / edges(11). 노드별 roadmap 항목 = tier(next/planned/later)·phase·detail.
- 신규 `decisions/0019-systemmap.md`: 스키마 계약·권한 경계(JSON=상태/로드맵/연결 정본, workflows/.md=디테일, state/manifest=서사)·갱신 트리거·저장/검증/렌더러.
- `INDEX.md`: 캐치업 상시읽기에 systemmap.json 추가(4→5) + 쓰기 규칙에 systemmap.json 갱신·검증 3종 한 단락.
- `state.md`: 워크플로우 인덱스에 "구조 정본=systemmap.json" 포인터 + 변경 로그.
- 렌더러 프로토타입 `outputs/system-map.html`(미커밋, outputs): 지도/로드맵 토글·노드↔로드맵 칩 링크·자산 blast-radius 하이라이트. 임베드 데이터 = systemmap.json verbatim.

## 검증
- systemmap.json 검증 3종 통과: ① json.loads ② 필수키·enum(status/tier/cluster) 전수 ③ 모든 consumes/feeds/edges/consumers/backlog.node/roadmap.cross 참조가 node/asset id로 해소(미해소 0).
- 검증이 onnuri-order(제이티발주) 노드 누락을 적발(INDEX 13 ↔ 초안 12) → 노드 추가·backlog의 onnuri 항목을 노드 roadmap으로 이동. 13개 일치.
- 내용 = 2026-06-12 워크플로우 상태 스냅샷(이후 변동 없음). channel-margin-monitor 8채널 모니터/7채널 가격변경, upload-monitor partial(L4 대기), intelligence-layer design.

## 다음 / 상태
- 다음: 웹앱에 인앱 지도+로드맵 페이지 삽입 — private repo systemmap.json 런타임 read(st.secrets) + st.page_link 점프 + components.html 임베드. (사용자 OK 후 착수)
- 이후 모든 작업 종료 시: 상태/로드맵/연결 변화 → systemmap.json 동시 갱신(ADR 0019 트리거 준수).
- 미해결: 인앱 렌더 방식(components.html iframe vs 네이티브 그래프 위젯) 최종 결정은 삽입 시. onnuri-order page는 1_파일처리.py로 추정 기입(미확인 — 삽입 시 실페이지 확인).
