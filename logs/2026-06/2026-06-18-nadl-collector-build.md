# 2026-06-18 시장지능 nadl 로컬 수집기 — 구조 B 구현(파서/워크플로/fetcher)

## 무엇
ADR 0025 nadl 수집기 착수. **구조 B 확정**(로컬=fetch만, 파싱/정제/저장=클라우드). 막힘(행사 샘플)이 사용자 제공으로 해소.

## 왜
parser는 fragile→자주 수정. 클라우드 코드는 내가 직접 수정+자동배포 가능하나 로컬 박스는 불가 → 파서를 클라우드(GitHub Actions)에 둠(B). 로컬은 지오펜스 때문에 fetch만.

## 스코프 (사용자 확정)
- **행사상품만**: ps_ctid=01320000. 페이지 파라미터=**ps_page**(1~21 현재, 매번 변동→동적 감지: 상품 0이면 종료). 나머지 카테고리는 동일 패턴이나 지금 제외.
- 소스 URL: http://www.nadl.kr/home/m_mall_list.php?ps_ctid=01320000&m=1&...&ps_page=N (http·국내IP만 도달, STATUS 200 실측).

## 변경 (work-automation-data)
- scripts/nadl_parse.py — 파서+main. raw(.gz)→DataFrame→market/nadl/prices_{date}.parquet. 마커 market/nadl/runs/latest.json에서 collected_date·raw_dir 읽음(실행별 격리 dir로 stale 혼입 방지). 스키마: collected_date·source·ps_ctid·ps_page·ps_goid·name·spec·box_price·unit_price·exp·img. ✅커밋.
- scripts/nadl_fetch.ps1 — 로컬 fetcher(PowerShell·curl·Python/git 불요). ps_page 동적 루프(상품0=종료·MAXP60)·gzip·contents API push(sha 재시도)·요청간 3~7s 랜덤 지연·완료 시 마커 발행. raw=market/nadl/raw/{date}/{ctid}_p{N}.html.gz. ✅커밋.
- .github/workflows/nadl.yml — 마커 push 트리거만(parquet는 trigger 밖+[skip ci]=재발동 방지)·py3.12·pandas/pyarrow·parser 실행·parquet 커밋. **❌ PAT 403(Workflows 권한 없음)→미커밋.**

## 검증
- 파서 골든: 실 행사상품 샘플(417KB·1페이지)→**30/30** 전건(이름·판매가·개당가·규격)·parquet 왕복 OK. 마커 raw_dir 격리 동작 확인.
- 페이지 파라미터 ps_page 확정(순수 page= 0건).
- fetcher/Action 라이브 미검증(첫 실행=사용자와 동시 확인).

## 다음 · 상태
- **워크플로 yaml 미반영(블로커):** PAT에 Workflows 쓰기 권한 없음. → ① PAT에 "Workflows: R/W" 추가 후 재푸시, 또는 ② 웹UI로 .github/workflows/nadl.yml 수동 추가(내용 제공).
- **첫 라이브 테스트:** 박스용 fine-grained PAT(work-automation-data·Contents R/W만) 생성→$env:NADL_PAT→nadl_fetch.ps1 실행→마커→Action→parquet 확인. repo Settings의 Actions 활성 확인.
- 라이브 그린 확인되면 systemmap/state status 갱신(planned→운영중)+ADR 0025 보강(파서=클라우드/구조 B). 그 전까지 진행중.
- 후속: nadl 가격↔관리코드 매칭→두뇌① 시장대비 권장가.
