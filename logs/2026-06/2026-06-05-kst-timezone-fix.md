# 2026-06-05 날짜 KST 픽스 (datetime.now() UTC→KST 전체)

## 증상
모든 다운로드 파일명 날짜 및 엑셀 내 날짜 표시가 한국 현재 날짜보다 하루 뒤쳐짐.
예) 한국 2026-06-05인데 파일명에 0604 / 발주서 엑셀 헤더에 "2026년 6월 4일" 표시.

## 원인
Streamlit Community Cloud 서버가 **UTC** 기준으로 동작.
코드 전체에서 `datetime.now()` / `datetime.date.today()` 를 timezone 없이 호출 → UTC 시각 반환.
한국(KST) = UTC+9이므로 한국 자정~오전 9시 사이에는 UTC 날짜가 전날 → 하루 차이 발생.

## 변경 (work-automation-app, 4파일)

| 파일 | 변경 내용 |
|---|---|
| `core/workflows/logistics_order.py` | `from datetime import datetime, timezone, timedelta` + `_KST = timezone(timedelta(hours=9))` → `datetime.now(_KST)` |
| `core/workflows/cheonnyeon_upload.py` | `_KST = datetime.timezone(datetime.timedelta(hours=9))` → `datetime.datetime.now(_KST).date()` |
| `app/pages/5_송장처리.py` | `_KST` 상수 추가 → `datetime.now(_KST)` |
| `app/pages/1_파일처리.py` | `_KST` 상수 추가 → `datetime.now(_KST)` (4곳: 송장mmdd, 천년경영ymmdd, 발주자료아카이브mmdd, 물류팀mmdd) |

패턴: 각 파일 import 바로 아래에 `_KST = timezone(timedelta(hours=9))` 상수 선언.
모든 `datetime.now()` → `datetime.now(_KST)`, `datetime.date.today()` → `datetime.datetime.now(_KST).date()`.

## 영향 범위 (날짜 사용처 전수)
- **★★송장{mmdd}.xlsx** 파일명 (1_파일처리.py L68)
- **천년경영 {yymmdd}.xlsx** 파일명 (1_파일처리.py L125)
- **발주자료 아카이브 다운로드** 파일명 표시 (1_파일처리.py L290)
- **물류팀_{mmdd}.xlsx** 파일명 (1_파일처리.py L362)
- **발주서 엑셀 헤더 날짜** "○년 ○월 ○일 ○요일" (logistics_order.py L462)
- **천년경영 run_date** 기본값 (cheonnyeon_upload.py L304)
- **{channel}배송{yyyymmdd}_처리후_.xls** 파일명 (5_송장처리.py L139)
- **송장처리 시간** HH:MM 표시 (5_송장처리.py L52)

## 배포 방식
- `1_파일처리.py`, `5_송장처리.py`: pages 파일 → Streamlit 자동 반영 (rerun).
- `logistics_order.py`, `cheonnyeon_upload.py`: **import 모듈** → **Reboot app 필요**.
  Manage app → ⋮ → Reboot app.

## 상태 / 다음
- 완료. Reboot 후 한국 날짜 정상 반영 예상.
- 전역 pitfalls.md에 "Streamlit Cloud = UTC, 한국날짜는 _KST 상수 필수" 추가.
