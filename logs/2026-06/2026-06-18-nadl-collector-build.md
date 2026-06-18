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


## 결과 — 라이브 검증 (2026-06-18) ✅
- 워크플로 yaml: PAT에 Workflows:R/W 추가 후 재푸시 성공(.github/workflows/nadl.yml, sha 0dd10cf).
- 로컬 fetcher 1회 실행: ps_page 1~20=각 30, p21=6, p22=0→자동종료. **21페이지/606상품 push + 마커 발행.** (콘솔 한글 깨짐=PowerShell 코드페이지 표시문제, push 데이터는 UTF-8 정상.)
- 마커→Actions(nadl-parse) 자동 파싱→`market/nadl/prices_2026-06-18.parquet` 커밋(내가 안 올림=Action 생성 확정).
- parquet 실측: **606행/21페이지/고유 ps_goid 606(중복0)**, 박스가 606/606·개당가 599/606(7건은 listing에 개당가 없음). 개당가 분포 min160·중앙1480·max43000원.
- ⚠️ 이 PAT엔 Actions *읽기* 권한 없어 runs 목록 API는 빈값(실행 자체는 parquet이 증명). 모니터링 필요시 Actions:read 추가.
- 박스 PAT: 테스트는 기존 PAT로 진행. **주1회 상시화 전 work-automation-data Contents 전용 fine-grained PAT로 교체 권장**(최소권한) + Windows 작업스케줄러.
- 상태=**운영중**. systemmap nadl tier planned→done. 다음=개당가↔관리코드 매칭→두뇌① 시장대비 권장가.

## 운영 메모 (세션 클로즈)
- **로컬 운영 경로: `C:\claudeworkautolocal\nadl`** — nadl_fetch.ps1 + run_nadl.bat 동거.
- 운영 방식=**수동 더블클릭(run_nadl.bat)**. bat은 `%~dp0`로 같은 폴더 ps1 실행. **ASCII+CRLF 필수**(한글/LF면 cmd가 한글조각을 명령으로 오해해 깨짐 — 첫 bat 실패 원인).
- 토큰=`setx NADL_PAT`로 영구 저장(테스트는 기존 PAT, 상시화 전 data 전용 PAT 권장).
- 자동 스케줄 보류(사용자: 신뢰 후). 준비된 명령: `schtasks /Create /TN nadl-weekly /TR "powershell.exe -NoProfile -ExecutionPolicy Bypass -File <경로>\nadl_fetch.ps1" /SC WEEKLY /D MON /ST 09:00 /F`.
- 다음 세션 재개점=**nadl 개당가↔관리코드 매칭→두뇌① 시장대비 권장가**.
