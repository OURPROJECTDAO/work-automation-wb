# 2026-06-19 · UI 디자인 Phase C 시작 (랜딩 리스킨)

## 무엇
랜딩(지도·로드맵, app/pages/0_지도로드맵.py) 팔레트를 케이스 스터디/앱 톤으로 통일.

## 왜
실물 확인 결과 랜딩은 이미 정교한 인터랙티브 컴포넌트(systemmap.json 런타임 렌더·지도/로드맵 토글)였으나, 팔레트가 크림(#E9E7DF)+petrol(#0E4A43)+테라코타(#C5402A) = AI 기본값 룩이라 Phase A 인디고 톤과 분리감. 사용자: 케이스 스터디 느낌 앱에 이식.

## 변경 (app repo · dae597f)
- 컴포넌트 TEMPLATE `:root` 색 토큰만 교체 — bg #FCFCFD·card #FFFFFF·ink #14161B·line #E7E9EE·**petrol→인디고 #3B5BDB**·live #2F9E44·partial #F08C00·design(미구현/★) #E03131·concept #868E96·hub 인디고. 상태색을 앱 핀필(core/ui.py)과 통일.
- **두뇌 노드 분리**: 기존 테라코타 공유 → 두뇌=인디고 계열(border #C7D0F7·badge #3B5BDB), 미구현 status=레드로 분리(이전엔 둘 다 테라코타).
- ★ 다음 한 수 카드 글로우·hub 자산칩 인디고화.
- 중복 제거: 컴포넌트 자체 hero(h1 "지도와 로드맵, 한 소스에서")가 제목 → Streamlit `st.title`+`st.caption` 제거.
- **기능/구조/JS 무변경**(토큰·중복헤더만). ast.parse PASS·13개 치환 전건 유니크 매칭.

## 검증
- 13 치환 각 count==1 확인 후 적용(불일치 시 PUT 보류 가드). ast.parse PASS.
- near-white 컴포넌트 ↔ 앱 bg(#FBFBFD) 이음새 최소(이전 크림 대비 통합도↑).

## 다음 · 상태
- page-only(컴포넌트 HTML) → **재배포 자동반영**(Reboot 불요). 사용자 체감 확인 대기.
- Phase C 잔여 = 상단 "오늘 할 일" 요약(검토대기·품절·신규업로드 → 점프) 미착수.
- Phase B(데일리부터 헬퍼 적용) 미착수. 다음 = 사용자 선택(Phase B vs Phase C 잔여).
