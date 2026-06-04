# 로그: 발주서출력업무 — 다른 상품 합포 버그픽스 (split_multiproduct_cells)

## 무엇
합포 주문에서 서로 다른 상품 2개가 묶인 케이스가 1행으로 뭉쳐 나오는 버그 수정.

## 왜
사용자가 0604 실데이터 처리 결과와 기대 출력을 비교 제출. 발주자료 아카이브 2행 이상.

## 버그 패턴 (신규 발견)
- **합포 + 같은 상품** (기존): HTML rowspan → 두 번째 행 수량 NaN → `split_merged_cells` 감지·처리.
- **합포 + 다른 상품** (신규): `pd.read_html`이 어드민옵션·옵션추가항목1을 한 셀에 이어붙임.
  - 예) `옵션추가항목1='31-03-0531-22-02'`, 어드민옵션에 두 상품명 연속.
  - 두 번째 행이 생기지 않고 1행으로 통합됨 → 수량 NaN 방식으로 감지 불가.
  - 발생 케이스 2건: 식봄(코카콜라355+코카콜라제로), 캐시노트(코카콜라제로+환타파인).

## 변경 (work-automation-app)
- `core/workflows/logistics_order.py`:
  - `import re` 추가, `_ERP_CODE_RE = re.compile(r'\d{2}-\d{2}-\d{2}')` 상수 추가.
  - `split_multiproduct_cells(df)` 함수 신규: `옵션추가항목1`에서 erp코드 2개 이상 감지 시
    수량·정산금액 ÷ 2, 어드민옵션을 첫 번째 `[erp코드]` 기준으로 두 행 분리, 선결제비·판매처·평균단가 복사.
  - `run_phase1`에서 `parse_sales_report` 다음, `fill_management_code` 전에 `split_multiproduct_cells` 호출.
  - 주석: `fill_management_code` → Step 0b로 변경 (split_multiproduct = Step 0a).

## 검증
- 출력파일(실제) + 새 로직 시뮬레이션: 213행 → 215행 (+2).
- 기대 파일(정상): 215행. 행수 일치 확인.
- 분리된 두 케이스 erp코드·어드민옵션·수량/정산금액 분배 확인.

## 주의
- 기존 pytest 골든 테스트(4 passed)는 이 케이스가 없는 fixture라 영향 없음. 골든 테스트 재실행 필요(Reboot 후).
- `split_multiproduct_cells`의 erp코드 패턴 `\d{2}-\d{2}-\d{2}`: `31-05-001` 같은 3자리 끝 코드는 `31-05-00`으로 매칭되지만 단일 행이므로 2개 감지 조건 불만족 → 오발동 없음.
- import 모듈 변경이므로 Streamlit Reboot app 필요.

## 다음·상태
- 완료. Reboot 후 재실행 검증 필요 (사용자).
- 골든 테스트에 다른 상품 합포 케이스 추가는 나중에.
