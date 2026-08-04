# 2026-08-04 온누리 발주서 NaN 크래시 — 근본원인=참조 CSV 붙여넣기 개행 오염

## 무엇 / 왜
사용자 앱 실행 시 `ValueError: cannot convert float NaN to integer`
(`onnuri_order.py:86 int(val)`). 발주서(260804_발주서_태동마트.xlsx) 12행 중
마지막 행(밀리원 삼계탕, 수량 3)이 SKU 단가표에 없어서 발생.

사용자가 SKU를 추가한 뒤에도 동일 오류 재발 → 조사 결과 **추가는 됐으나
값에 개행문자가 딸려 저장**된 것이 진짜 원인.

## 근본원인 (2단)
1. **참조 CSV 오염** — 엑셀에서 셀을 복사해 `st.data_editor` 에 붙여넣으면
   셀 끝 개행(`\n`)이 값에 그대로 들어온다. CSV 는 따옴표로 감싸 보존하므로
   파일은 멀쩡해 보이지만 lookup 이 조용히 전부 실패한다.
   `'PC005982\n' != 'PC005982'`
   - 게다가 **마지막 열에 개행이 남으면 재읽기 때 유령 빈 행이 생긴다.**
     그 빈 행이 다시 저장되며 행수가 매 저장마다 1씩 증가(122→123→…).
     `_edit_with_search` 의 `result[key_col].astype(str).str.strip() != ""`
     필터가 못 잡는 이유 = **pandas 3 에서 `astype(str)` 이 결측을 'nan'
     문자열로 안 만들고 NaN 으로 남긴다**(pitfalls 기등재 항목과 동일 계열).
     `NaN.strip()` → NaN, `NaN != ""` → True → 살아남음.
2. **워크플로우 취약성** — `CalcTotal._calc` 가 미매칭 행에 `None` 반환.
   같은 컬럼에 정수가 하나라도 섞이면 pandas 가 float64 로 추론하며
   None → **NaN**. `_patch_column_values` 가드는 `val is None` 만 봐서
   NaN 이 통과 → `int(nan)` 폭발.
   ★ 전건 미매칭이면 object dtype 이라 None 이 살아남아 오히려 안 터짐 —
   **"일부만 미매칭"일 때만 터지는** 구멍이었다.

## 변경 (work-automation-app, 7파일)
- `core/base.py` — **신규 `clean_cell` / `sanitize_ref_df(df, key_col=None)`**.
  전 문자열 셀 개행·탭→공백 + strip + NFC, 전열 빈 행 제거, key_col 빈 행 제거.
  ★ pandas 3 는 `dtype=str` 열이 object 가 아니라 str dtype 이라
  `dtype == object` 검사로 거르면 조용히 통과 → **전 컬럼에 map** 으로 처리.
  (1차 구현에서 이 함정에 걸려 테스트3 실패 → 수정)
- `core/workflows/onnuri_order.py` —
  ① `_patch_column_values` NaN 가드(`isinstance(val,float) and math.isnan(val)`)
  ② `LoadSKU` 가 관리코드에 `clean_cell` 적용(더러운 CSV 여도 매칭)
  ③ `_calc` 가 발주서 관리코드에도 동일 적용(양쪽 정규화)
- `app/pages/2_기준데이터관리/` **4개 페이지 전부** — 저장 함수 안
  `to_csv` 직전 `df = sanitize_ref_df(df)`. 4파일이 각자 저장 함수를
  복제해 갖고 있어 한 곳만 고치면 안 됨
  (`_gh_put_csv`×2 · `_save_csv` · `_commit_csv`).
  ※ p1 은 다운로드 버튼용 `to_csv` 가 하나 더 있어 앵커로 저장 경로만 겨냥.
- `reference/sku_list.csv` — 개행 제거 + 유령 빈행 삭제(123→122행) +
  신규 2행(PC005981 가마치 / PC005982 밀리원 삼계탕) 규격 `1kg*1` ·
  내품수량 `1.0` · 운영 `-` 를 기존 소분행 관례대로 보정.

## 검증
- 앱 코어 원본 그대로 로컬 실행해 **동일 traceback 재현**(base.py:48 → :191 → :86).
- 테스트1: **깨진 HEAD CSV 그대로** 워크플로우 실행 → 12행 전건 채움, 총 235,400원.
  (LoadSKU 의 clean_cell 방어 덕분)
- 테스트2: SKU 진짜 미등재로 만들고 실행 → **예외 없이 완주**, 미매칭 1행만 빈칸.
- 테스트3: `sanitize_ref_df` → 123행 → 122행, 잔여 오염 셀 0.
- 테스트4: **멱등성** 122→122→122, `a.equals(b)` — 유령 행 증식 정지.
- 테스트5: 타 참조 CSV 무손상 — logistics_classification 1557행(값 2셀 정리)·
  sub_list 388(1)·bm_commission 780(2)·unit_list 417(8). **행 삭제 0**.
  → 다른 CSV 들도 이미 같은 오염을 갖고 있었고 다음 저장 때 자동 청소됨.
- diff: 기존 120행 값 변경 0건. 삭제 키 = 유령 빈행(`''`) 1건뿐.
- 커밋 후 원격 재fetch: sku_list 122행·오염 0·PC005982 존재, 6개 .py 전부 ast OK.
- 산출물 `260804_발주서_태동마트(확인).xlsx` 사용자 전달
  (sharedStrings 보존 확인 — inlineStr 0개).

## 다음 / 상태
- ⚠️ **재배포(1~2분) + Reboot app 1회 필요.**
  core 2종(`base.py` 신규 함수 추가 · `onnuri_order.py`) 변경 →
  기존 import 모듈이라 `sys.modules` 캐시. 페이지는 새 core 함수를 참조하므로
  Reboot 없으면 `ImportError: cannot import name 'sanitize_ref_df'` 가 난다.
- Reboot 후 사용자 확인 대기: ① 온누리 발주서 재실행 정상 ② 기준데이터관리
  4개 탭 저장 정상(행수 안 늘어남).
- 미완: 온누리 회귀 pytest 부재(기존 백로그). 이번 케이스
  (일부 미매칭 → NaN)는 **fixture 로 박제할 가치 큼** — 빈 G셀 fixture 백로그와 묶어서.
