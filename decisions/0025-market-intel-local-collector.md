# 0025 — 시장 지능(경쟁가): 로컬 수집기 아키텍처

## 맥락
intelligence-layer 두뇌① 권장가를 "내 baseline 기준" → "시장 대비"로 격상하려면 외부 경쟁가 신호 필요(roadmap 시장지능 P3). 1순위 소스 = **nadl.kr(m.nadl.kr)** — 사람이 검수하는 B2B 식자재몰, **행사상품이 근사 최저가·중복 없음 → 매칭 쉬움**(사용자 지목).

## 실측 (2026-06-16)
- nadl: DNS 정상(110.10.129.96·SK브로드밴드 서울). 그러나 **클라우드(샌드박스/Streamlit/GitHub Actions = 해외 IP)에서 도달 불가** — Envoy 503 upstream connection timeout(15s, 해외/데이터센터 IP 드롭=지오펜스 패턴) + robots.txt 자동접근 불허(web_fetch ROBOTS_DISALLOWED). raw TCP는 intercept라 0s 성공이나 실 upstream 타임아웃. 대조군 danawa·foodspring(국내몰)은 클라우드 200.
- 사용자 판단: 약관에 크롤 금지 조항 없음(물리적 수동열람 방지 수준)·주1회 저속이면 사람 행동과 구분 안 됨.
- 대체 후보: 다나와/에누리(클라우드 OK·소매·중복/노이즈 큼)·네이버 쇼핑 API(클라우드 OK·공식·무료·소매). **단 nadl의 B2B 바닥값+쉬운 매칭은 대체 불가 = 다른 신호.**

## 결정
1. **nadl = KR 로컬 수집기.** 클라우드에서 못 닿으므로 사용자 KR 머신(회사 PC·이미 사이트 접속됨)에서 수집기 실행. **Windows 작업 스케줄러로 주1회·저속**(요청 간 지연·행사 카테고리만·사람 모방).
2. **전송 = 자동 push.** 수집기 → 행사 가격 parquet/csv → GitHub API로 work-automation-data(private)에 push(기존 데이터계층 패턴, 앱이 parquet read). **완전 자동**(수동 업로드 단계 없음). PAT는 PC에 env/파일로 보관(스크립트 하드코딩·동기화 금지), fine-grained = data repo contents:write 한정. (대안 B: CSV→Drive→앱; 대안 C: CSV→기존 업로더 수동=자동 아님, fallback)
3. **소비 = 두뇌① 시장 대비 권장가.** 앱이 nadl 가격 read → 관리코드 매칭 → 채널 판매가 vs 시장 최저가 비교(intelligence-layer).
4. **네이버 쇼핑 API = 클라우드 보완(후순위)·다나와 = 소매 노이즈로 후순위.**

## 미해결 / 다음
- **구현 막힘 = nadl 행사목록 페이지 실물 대기.** 샌드박스가 지오펜스로 못 봐서 파서(상품명·규격·가격·행사여부·페이지네이션) 작성 불가. 사용자 저장본 1장 받으면 파서 + 수집기 스크립트(Windows 스케줄러) + data repo push 작성.
- 위험: IP 차단 가능성(저속·주1회로 완화)·페이지 구조 변경 시 파서 갱신.
