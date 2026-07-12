# 2026-07-13 Streamlit Community Cloud 세그폴트 — 네이티브 스택 핀 고정

## 무엇
웹앱이 "Error running app. ... contact support" 전체 페이지 오류. Cloud 로그:
`run-streamlit.sh: line 9: 194 Segmentation fault ... streamlit`. 리부트하면 잠깐 되다 재발.

## 왜 (근본원인)
requirements.txt가 `pandas>=2.0`·`pyarrow>=14`·numpy 미핀 → Community Cloud가 재배포마다
최신을 끌어와 **pandas 3.0.2 + pyarrow 25.0.0 + numpy 2.4.4** 조합이 됨. 이 조합이
`pd.read_csv`의 arrow 백엔드 문자열 변환(`pandas/core/arrays/string_arrow.py:_from_sequence`)
에서 **네이티브 SIGSEGV**. pandas 3.0은 문자열 컬럼(=`dtype=str` 포함)을 기본으로 ArrowStringArray
로 읽는데, 그 ABI 조합이 불안정. 한글 문자열 많은 product_master.csv 등을 읽는
상품360(load_pm)·두뇌④·가격AB·대시보드에서 프로세스 통째로 죽음.
- 힙-상태 의존 heisenbug: pyarrow가 parquet 로드로 먼저 쓰인 뒤에만 터짐 → 리부트 직후엔
  되다가 그 페이지 다시 열면 재발.

## 진단 (faulthandler)
- 현 HEAD 코드는 건강(문법0·엔트리/config/랜딩/20페이지 구조정상·width전환 정상). 코드 회귀 아님.
- combined 루프(한 프로세스에 20페이지 연속 = Cloud 재실행 모사)로 세그폴트 재현 → faulthandler가
  `string_arrow.py _from_sequence` ← `read_csv` ← `11_상품360.py:130 load_pm` 지목.
- 단일 페이지 독립 실행은 세그폴트 안 남(그래서 처음엔 하네스 부작용으로 오판) — Cloud=단일 장수명
  프로세스라 combined가 진짜 재현.

## 변경
- app repo requirements.txt 네이티브 3종 핀 고정 (커밋 51313801):
  `pandas>=2.2.3,<2.3` · `numpy>=1.26,<2.0`(신규) · `pyarrow>=16,<18`(기존 >=14.0).
  나머지 동일. 코드 변경 0(`.map` 등 이미 2.2 호환·pandas3.0 전용 API 없음 확인).

## 검증
- 불안정 조합: combined 루프 2/2회 세그폴트.
- 안정 조합(numpy1.26.4/pandas2.2.3/pyarrow17.0.0): 동일 루프 3/3회 완주(세그폴트 소멸).

## 다음·상태
- Cloud 재배포(requirements 변경=환경 재빌드). **확실히 하려면 재배포 후 Reboot app 1회**
  (새 핀으로 venv 깨끗이 재설치). 사용자 실앱 정상화 확인 대기.
- 재발 시 Manage app 로그로 SIGSEGV/트레이스백 재확인.
- 교훈: Community Cloud는 `>=` 열린 핀이면 재배포마다 bleeding-edge를 끌어옴 → 데이터 커밋 하나가
  네이티브 스택을 최신으로 밀어 터뜨릴 수 있음. 네이티브 3종(numpy/pandas/pyarrow)은 상한 캡 유지.

---
## 정정 (같은 날, 2차) — 핀 접근 폐기, 런타임 가드로 교체
- **문제**: requirements 핀(`pandas==2.2.x`·`numpy<2.0`·`pyarrow<18`)은 로컬 py3.12에선 검증됐지만,
  **Cloud는 Python 3.13/3.14** → 그 버전엔 해당 핀들의 **binary wheel이 없어** pip이 소스에서 컴파일
  → "Preparing metadata (pyproject.toml)"에서 무한 대기(numpy/pyarrow 소스빌드는 Cloud서 사실상 실패).
  사용자 실앱 배포가 hang.
- **교체 픽스**:
  1) requirements.txt **원복**(open 핀 → py3.14 wheel 최신 설치, 빠름). 커밋 3bb27e2.
  2) app/streamlit_app.py(엔트리·매 로드 최선두 실행)에 런타임 가드:
     `pd.set_option("mode.string_storage","python")` → pandas 3.0 문자열 dtype이 ArrowStringArray
     (`string_arrow._from_sequence`) 대신 python 백엔드 사용 → 세그폴트 경로 원천 회피. 커밋 0fec9cf.
- **검증(크래시 조합 pandas3.0.3/pyarrow25/numpy2.5에서)**: 가드없음 2/2 세그폴트 → 가드있음 3/3 완주.
- **교훈(중요)**: Cloud Python이 최신(3.14)이라 **다운핀은 wheel 부재로 hang**. 네이티브 크래시는
  버전 다운핀이 아니라 **런타임 가드**로 회피하는 게 맞음(pandas 최신 유지=wheel 확보). 진짜로 버전을
  낮추려면 Cloud 앱 설정에서 **Python 버전을 3.12로 내려야** 함(사용자 대시보드 조작 필요·이번엔 안 함).
- **다음·상태**: Cloud가 새 커밋(3bb27e2 requirements)으로 빠르게 재빌드. 이전 hang 빌드(5131380)는
  최신 커밋으로 대체됨 — 안 풀리면 **Reboot app 1회**로 최신 커밋 재빌드 강제. 사용자 정상화 확인 대기.
