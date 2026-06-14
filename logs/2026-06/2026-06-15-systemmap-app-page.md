# 2026-06-15 systemmap 인앱 페이지 — work-automation-app 0_지도로드맵.py

## 무엇 / 왜
systemmap.json(KB) 단일 소스를 웹앱에서도 보게 — 사용자가 앱 안에서 지도+로드맵을 캐치하고 실제 페이지로 바로 이동. (ADR 0019 ②)

## 변경 (work-automation-app)
- 신규 `app/pages/0_지도로드맵.py`: private KB repo의 systemmap.json을 **런타임 read**(시크릿 PAT — `[data] pat` 또는 `GITHUB_PAT` 순차 시도) → 표준 렌더러 HTML(임베드 데이터를 `__SYSTEMMAP_JSON__` 플레이스홀더로 주입)을 `components.html`로 표시 + 실제 페이지 `st.page_link` 바로가기(try/except 폴백). `@st.cache_data(ttl 300)`. PAT 권한 없으면 명확한 안내 후 st.stop().
- `app/streamlit_app.py`: 첫 헤더리스 섹션 맨 위에 `st.Page(0_지도로드맵.py, "지도·로드맵", 🗺️)` 등록.
- **코드=공개 app repo, 데이터=private KB repo 분리** 유지(공개 코드에 업무내용 0).
- core 미사용 → Reboot 불필요, 커밋 자동 재배포만(1~2분).
- 렌더러 = outputs/system-map.html(휴대용 프로토타입)과 동일 템플릿(MAP만 런타임 주입). systemmap.json 1개 갱신으로 인앱·휴대용 둘 다 반영.

## 검증
- 페이지·streamlit_app 둘 다 commit 전 `compile()` 통과(깨진 페이지 미배포).
- PUT 201(page)/200(nav). 런타임 렌더는 재배포 후 사용자 확인 필요.
- 미확인 2: ① 배포 PAT가 work-automation-wb 읽기 권한 보유 여부(둘 다 시도 + 에러 안내로 방어) ② st.page_link 경로 형식("pages/..") 실작동(try/except 텍스트 폴백).

## 다음 / 상태
- 사용자: 재배포(1~2분) 후 '지도·로드맵' 페이지 확인. PAT 권한 에러 뜨면 시크릿에 KB repo 읽기 PAT 추가(안내 표시됨).
- 이후 systemmap.json만 갱신하면 인앱·휴대용 둘 다 자동 반영(렌더러 무수정).
- 향후(선택): 인앱 경량 편집 UI(현재는 채팅으로 갱신). st.page_link 경로 미작동 시 st.Page 객체 참조 방식으로 교체.
