# 0019 — systemmap.json (지도+로드맵 단일 진실원천 + 갱신 규칙)

_2026-06-15 · 관련: manifest.md, state.md, roadmap.md, workflows/*, outputs/system-map.html_

## 결정
지도(업무·데이터 연결)와 로드맵을 **하나의 구조화 파일 `systemmap.json`**(KB 루트, private)에서 렌더한다.
HTML 프로토타입과 (예정) 웹앱 인앱 페이지가 **같은 파일**을 읽어 사용자·Claude 둘 다 같은 최신본을 본다.
손으로 갱신하므로(코드 자동추출 아님) drift 방지 규칙을 함께 못박는다.

## 스키마 계약 (고정)
- 키: `meta / assets[] / clusters[] / nodes[] / backlog[] / edges[]`.
- `meta`: {updated(KST YYYY-MM-DD), source, schema, renderer}.
- `assets[]`: {id, label, consumers[node.id], note}. **다중소비(≥2)·교차클러스터 공유자산만** 등재(단일소비 ref는 workflows/.md). id = reference 파일 stem.
- `clusters[]`: {id, num, label, flow}. 고정 셋 {fulfillment, registration, intelligence}.
- `nodes[]`: {id, cluster, status, label, line, consumes[asset.id|node.id], produces[str], feeds[node.id], page, star?, brain?, roadmap[]}.
  - **id = workflows/<id>.md stem = (가능하면) 앱 페이지. KB↔JSON↔앱 조인 단일키.**
  - status ∈ {live, partial, design, concept} (통제 어휘).
  - line ≤ 한 줄.
  - roadmap[]: {tier, title, detail, phase?, star?, cross?}. tier ∈ {next, planned, later}. detail ≤ 한두 줄.
- `backlog[]`: {node(node.id|null), title, detail}. **가로지르는(특정 노드 없는) 항목만**. 노드 특정 항목은 그 node.roadmap에.
- `edges[]`: {from(node.id), to(node.id)}. 체인/상속/공급.
- **통제 어휘(status/tier/cluster) 임의 추가 금지** — 렌더러가 이 값으로 CSS 분기. 바꾸려면 렌더러 동반 수정.
- PII/비밀 금지(식별자만).

## 권한 경계 (중복 방지 — 핵심)
| 사실 | 정본 |
|---|---|
| 노드 status · 한 줄 요약 · 로드맵 항목 · edges · asset→소비처 | **systemmap.json** |
| 공식 · 함정 · 컬럼맵 · 검증 등 깊은 디테일 | workflows/<id>.md |
| 날짜별 변경 서사 | state.md |
| 혈류(blast radius) 경고 · 편집 경로 산문 | manifest.md |

- 규칙: **상태·로드맵·연결 변화 → JSON만. 근거·서사 변화 → .md만.** 같은 사실 양쪽 기재 금지. 충돌 시 구조=JSON, 산문=.md.
- state.md 워크플로우 인덱스 표·다음 한 수는 **사람용 서사 미러**(구조 정본은 JSON).

## 갱신 트리거 (작업 종료 루틴 결합)
다음 중 하나면 그 작업단위에 systemmap.json 갱신 + `meta.updated`(KST):
- 워크플로우 status 변화
- 로드맵 항목 완료·추가·재우선순위
- 공유자산·소비처 추가
- 새 워크플로우간 체인/상속(edges)
- 새 워크플로우(노드 추가; workflows/.md 생성과 동시)

한 줄: **"지도나 로드맵에 보이는 게 바뀌면 systemmap.json도 같이."** workflows/.md·state.md 갱신과 같은 커밋에.

## 저장 · 검증
- 위치: `work-automation-wb` 루트 `systemmap.json`(고정명·private). 읽기 raw / 쓰기 PUT + fresh sha.
- **캐치업 상시읽기 세트에 포함**: INDEX/state/pitfalls/roadmap + **systemmap.json**.
- **PUT 전 필수 검증 3종** (실패 시 PUT 금지 — 깨진 JSON = 인앱 페이지 사망):
  1. `json.loads` 파싱 OK.
  2. 필수키 존재 + enum 값(status/tier/cluster) 통제어휘 내.
  3. 참조 해소 — 모든 consumes/feeds/edges/asset.consumers/backlog.node/roadmap.cross 가 실제 node/asset id로 풀림.
- 렌더러 관대: 모르는 선택 필드 무시·없는 선택 필드 graceful → **내용 추가 = JSON만(코드 무수정)**, enum 변경 때만 렌더러 동반.

## 렌더러
- 프로토타입: `outputs/system-map.html` — 지도/로드맵 토글 · 노드↔로드맵 칩 링크 · 자산 blast-radius 하이라이트. 임베드 데이터 = 이 스키마(verbatim).
- 예정(인앱): private repo `systemmap.json` 런타임 read(st.secrets PAT, 대시보드 패턴) → 지도는 components.html 임베드 + `st.page_link` 칩으로 실제 페이지 점프. (코드 public·내용 private 분리.)

## 비고
- 신설 시 검증이 onnuri-order 노드 누락을 잡음(INDEX 13 ↔ 지도 12) → 노드 추가로 13개 일치. 검증 3종의 효용 입증.
