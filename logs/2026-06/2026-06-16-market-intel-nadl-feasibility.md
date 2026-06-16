# 2026-06-16 시장 지능(경쟁가) — nadl 수집 타당성 조사

## 무엇
intelligence-layer 시장지능(경쟁가) 1순위 소스 nadl.kr 크롤 타당성 실측 + 아키텍처 확정(ADR 0025).

## 왜
두뇌① 권장가를 시장 대비로 격상(roadmap P3). nadl = 사람검수 B2B몰·행사 근사최저가·중복없음(매칭 쉬움, 사용자 지목).

## 변경
- 코드 변경 없음(설계/조사 단계). ADR 0025 신설 · systemmap 시장지능 항목 갱신(tier later→planned) · state 다음한수.

## 검증 (실측 2026-06-16)
- nadl: 클라우드 도달 불가 — Envoy 503 upstream timeout(15s)·robots disallow(web_fetch ROBOTS_DISALLOWED). DNS OK(110.10.129.96 SK브로드밴드 서울). raw TCP는 intercept라 0s지만 실 upstream 타임아웃 → 해외 IP 지오펜스.
- 대조군: danawa 200(462KB·서버렌더·파싱가능 but 소매노이즈)·foodspring 200(식봄=B2B 로그인벽 가능·검색 404)·naver 403.
- 결론: 클라우드(Streamlit/Actions 포함 해외 IP) 전부 nadl 못 닿음 → KR 로컬 수집기 필수.

## 다음 · 상태
- **막힘: nadl 행사목록 페이지 실물 1장 대기**(지오펜스로 내가 못 봄). 받으면 파서 + 주1회 수집기 스크립트(Windows 스케줄러) + data repo push 작성.
- 전송=PAT로 work-automation-data push(자동)·소비=두뇌① 시장대비 권장가. 네이버 API=클라우드 보완 후순위.
