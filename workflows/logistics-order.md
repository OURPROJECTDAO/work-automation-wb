# 워크플로우: 발주서출력업무 (logistics-order)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md.

## 요약
- 원본 `물류팀프로그램v5_2.xlsm` 16단계 매크로를 **2-phase + 게이트**로 재구현 (decisions/0003).
- HTML 매출통계 입력 → 물류팀 시트(프린트용) + 품절목록 + 발주자료 아카이브.
- Phase 3 (2번째 템플릿). 운영 중. 구현+디자인+테스트 완료.

## 처리 모델 (2-phase + 게이트)
- Phase1: 정제 · 셀나누기 · 구분분류 · 중복제거 · 규격 → **GATE A**(구분 미분류 코드).
- Phase2: 자리바꿈 · 정렬 · 통합 · 재고대조 → **GATE B**(낱개 원코드 미매칭).
- 에러 없으면 클릭 2번으로 끝. 있으면 그 지점 정지 → 기준데이터에 추가 후 재실행 → 다음번 자동 통과.
- 게이트 시 미매칭은 기준데이터(분류표 / 낱개처리목록)에 자동 추가.

## 코드 / 데이터
- `core/workflows/logistics_order.py` (run_phase1 → 4-tuple 반환[archive_df 포함], run_phase2, generate_*_xlsx)
- 기준데이터 (`reference/`, 고정):
  - `logistics_classification.csv` (1012행, 멸치쇼핑 분류표)
  - `unit_list.csv` (383행, 낱개처리목록)
  - `spec_master.csv` (4366행, 규격파일)
- 연동데이터: `product_master.csv` (상품관리, 박스재고 — **매일 갱신**, 연동데이터관리 페이지 + 타임스탬프)
- UI:
  - `app/pages/1_파일처리.py` (발주서출력업무 탭, Phase1/2 + GATE A/B)
  - `app/pages/2_기준데이터관리/3_발주서출력업무.py` (분류표 / 낱개목록 / 규격파일)
  - `app/pages/3_연동데이터관리/1_상품관리.py` (상품관리 업로드 + 타임스탬프)
- 테스트: `tests/test_logistics_order.py`, fixtures `tests/fixtures/logistics/`.

## 전용 함정
- **HTML 매출통계 노이즈**: .xls 안에 서브테이블(품절 사전경고)이 있어 `pd.read_html[0]` 앞에 'col0만 값, 나머지 NaN'인 노이즈 행이 섞임 → 'erp관리코드' 헤더 행을 찾아 그 위를 전부 skip.
- **셀나누기(합포 1건 묶음) — 같은 상품**: HTML rowspan 병합셀 → 두 번째 행의 총수량·정산금액이 NaN. 감지 후 위 행 값 ÷2를 두 행에 분배, 판매처그룹·선결제비·평균단가는 복사. `split_merged_cells` 처리.
- **셀나누기(합포 1건 묶음) — 다른 상품** ★2026-06-04 발견★: 두 서로 다른 상품이 합포된 경우, `pd.read_html`이 어드민옵션·옵션추가항목1을 **한 셀에 이어붙여** 파싱함. 예) `옵션추가항목1='31-03-0531-22-02'`, `어드민옵션='코카콜라355...[31-03-05]코카콜라제로355...[31-22-02]'`. 두 번째 행의 총수량이 NaN이 아니므로 `split_merged_cells`가 감지 못 함. → `split_multiproduct_cells`로 처리: `옵션추가항목1`에서 `\d{2}-\d{2}-\d{2}` 패턴 2개 이상 감지 시 수량/정산금액 ÷ 2, 어드민옵션을 첫 번째 `[erp코드]` 기준으로 분리. `run_phase1`에서 `fill_management_code` 전에 실행.
- **발주자료 아카이브 = 원본 8열, 중복제거 전**(개별주문 보존). 완성 phase1(10열·구분/규격·중복제거 후) 아님. `run_phase1`이 archive_df를 별도 반환. 헤더는 '어드민 옵션'(띄어쓰기).
- **상품관리(product_master) 컬럼 위치참조**: `iloc[:,4]`=관리코드, `iloc[:,14]`=박스재고.
- **낱개처리목록**: 낱개코드→원코드 매핑. 원코드로 상품관리 재고 조회. 원코드가 상품관리에 없으면 GATE B(사용자가 낱개목록에 추가).
- **수치 컬럼 float 명시**: `_필요수량` 등은 `.astype(float)`. 안 하면 낱개 배수곱(예 10×0.125=1.25) 대입 시 `Invalid value for dtype int64` 에러.
- **재고 계산**: 재고 = 박스재고(상품관리) − 필요수량(낱개는 총수량×배수). 음수 = 품절목록. round 후 int.

## 출력 디자인 (프린트용 — 물류팀 전달)
- 타이틀 바: 남색(2F5496) 배경 + 흰 글씨, 날짜 "YYYY년 M월 D일 X요일".
- 섹션 헤더: 연파랑(D9E1F2) + 남색 글씨.
- 구분 카테고리 색: 선물세트=FFF3CD, 식품=E2EFF7, 음료=E3F1E5.
- 규격: 가운데정렬 + 연속 동일값 병합.
- 총수량: 낱개("낱" 접두) 파란글씨(0B5394), 일반 검정.
- 재고(품절, 음수): 빨강(C00000) + 분홍배경(FDE7E7).
- 어드민옵션 좌측, 재고 우측. 테두리 회색(999999).
- 열 순서: 구분 / 규격 / erp(C열 숨김) / 어드민옵션 / 총수량 / 재고.
- 품절목록 시트도 동일 톤(헤더색, 현재고 빨강).

## 검증 (골든 대조)
- pytest 4 passed (`tests/test_logistics_order.py`):
  1. archive 8열·중복제거 전 검증
  2. 물류팀 102행 erp별 (총수량,재고) 1:1
  3. 품절목록 10행 1:1
  4. 셀나누기 ÷2 단위테스트
- fixtures: sales_input.xls, product_master.csv(골든 스냅샷), classification/unit_list/spec_master.csv, golden_물류팀.csv, golden_품절목록.csv.
- 테스트는 pm_df/cls_df/spec_df/unit_df를 fixture로 명시 주입 → 라이브 기준데이터 편집과 무관하게 결정적.
- 골든 내장 상품관리(4222행)로 재실행 시 품절 10/10 일치. (업로드 상품관리는 다른 시점이라 품절 행수 다를 수 있음 — 정상.)
- 주의: 다른 상품 합포(split_multiproduct_cells) 케이스는 골든 테스트 fixture에 아직 미포함. 필요 시 추가.

## 관련 로그 / 결정
- decisions/0003-logistics-order-2phase-gate.md
- logs/2026-06/2026-06-02-phase3-logistics-order.md (구현)
- logs/2026-06/2026-06-02-logistics-bugfix.md (int64·아카이브 8열)
- logs/2026-06/2026-06-02-logistics-print-design.md (프린트 디자인)
- logs/2026-06/2026-06-02-logistics-golden-test.md (골든 테스트)
- logs/2026-06/2026-06-02-streamlit-infra-fixes.md (nav·모듈캐시 — 전역, pitfalls.md)
- logs/2026-06/2026-06-04-logistics-multiproduct-fix.md (다른 상품 합포 버그픽스)
