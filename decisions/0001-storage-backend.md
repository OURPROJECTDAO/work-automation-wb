# ADR 0001 · 기억 저장소 = GitHub(KB) + Google Drive(엑셀)

## 결정
KB(기억) = GitHub private repo OURPROJECTDAO/work-automation-wb (main, 고정 파일명, bash+PAT contents API).
엑셀 작업물 = Google Drive (templates/inputs/outputs).

## 맥락 / 경위
- 처음엔 Drive 단일 백엔드 시도(이미 연결 + 엑셀 colocate). 그러나 Drive 커넥터가 생성+읽기만 → "타임스탬프 스냅샷 + read-newest" 우회 설계 필요.
- 실사용에서 캐치업이 느림: 폴더마다 나열→최신탐색→다운로드라 세션 시작에 호출 7~10번 순차 = 수십 초.
- GitHub는 제자리 수정 가능 → 고정 파일명 → 탐색 단계 소멸 + bash 한 번에 묶어 읽기 → 캐치업 1턴. 투자시스템에서 검증된 단순 모델 재사용.

## 트레이드오프
- 층 분리: 읽기 많고 매 세션인 KB(작은 텍스트)는 GitHub가 빠름·단순. 바이너리 엑셀은 Drive가 적합.
- 비용: PAT 관리(만료·보안). fine-grained로 blast radius 최소.
- 이식성: 전부 평문 .md라 이전 비용 낮음(Drive→GitHub 즉시 이전).

_2026-05-31_
