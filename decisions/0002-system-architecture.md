# 0002 — 자동화 시스템 아키텍처

_2026-06-01_

## 맥락
업무 자동화(오픈마켓 발주 정제 등)를 VBA 매크로 엑셀에서 시스템으로 발전.
- 요구: 원격·기기 무관 동작. 입력/출력은 Excel. VBA 로직을 점진적으로 Python 이관.
- 실행 환경 = 클라우드 희망 → 서버에 Excel 없음(따라서 xlwings 제외).
- 프론트: 일상 실행은 Web UI(토큰0), 수정·개발은 채팅(Claude).

## 결정
- 처리 코어: Python (pandas + openpyxl). VBA 워크플로우를 함수로 재구현.
  - 로직/데이터 분리: 참조 데이터(도서산간/필터링/미배송)는 xlsm에서 csv로 추출.
  - 워크플로우 = 플러그인: 공통 base(load→steps→save) + 템플릿별 모듈. 새 템플릿 = 모듈 1개 추가.
- 검증: 기존 VBA 출력 결과물 = 골든 파일로 회귀 테스트(Python 출력 == 골든).
- Web UI: Streamlit. 파일 처리 + 대시보드를 한 앱에. 다중 페이지로 분리.
  - 역할분담: Web UI=런타임(반복실행·토큰0), 채팅=수정/개발.
- 코드 저장소: KB와 분리한 새 repo(work-automation-app). 자동배포는 코드 repo만 감시.
  - → PAT 권한을 두 repo로 확장 필요(미완).
- 호스팅: Streamlit Community Cloud(무료, 비공개앱 1개·뷰어 허용명단)로 시작 → 필요시 Railway(~$5/mo).

## 제외 / 대안
- xlwings: 서버에 Excel 없으므로 제외. (로컬 Excel UI 유지가 필요했다면 후보였음)
- FastAPI: 솔로+대시보드엔 Streamlit 우위. 추후 외부연동/규모 확대 시 같은 코어 공유하며 병행 가능.

## 결과 / 주의
- 이전 무통증 규율: 처리 로직을 Streamlit 파일에 넣지 말 것(화면=코어 호출만). 지키면 Railway/FastAPI 이전 시 코어 그대로 재사용.
- 주문 데이터가 무료 외부 서버(Community Cloud) 경유 — 비공개 허용명단이지만 통제권 밖임을 인지. 께름칙하면 Railway부터 시작.
