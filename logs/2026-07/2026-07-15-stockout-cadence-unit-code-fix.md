# 2026-07-15 — 품절목록·품절 알림판 낱개/소분 코드 cadence 미연동 버그픽스

## 무엇 / 왜
사용자 보고: 발주서 출력 시 **품절목록 E/F/G(최근입고일·평균매입주기·입고횟수)가 낱개 품목만 공백**.
확인 결과 발주서(logistics-order)뿐 아니라 **데일리 대시보드 품절 알림판(stockout_board)에도 동일 결함**,
알림판 쪽은 표시 누락에 더해 **재입고 자동삭제가 영구 미작동**이었음(더 심각).

## 원인 (실측 확정)
- **매입현황(buyin)·상품관리 박스재고는 전부 박스 관리코드 기준.** 최근 13개월 buyin 17,116행 중 `PC*` 접두 **0행**,
  product_master 관리코드 4,377개 중 낱개/소분 매핑코드 319개 가운데 **3개만 존재**.
- `generate_result_xlsx`는 cadence를 `erp관리코드` 그대로 조회 → 낱개/소분은 무조건 미매칭.
  `stockout_board.board_to_frame`/`reconcile`도 `_nfc(code)` 그대로 조회.
- ★ **정합 깨짐**: 같은 행의 재고(`reconcile_stock`)는 이미 unit_list 원코드로 계산하는데 cadence만 낱개코드 기준이었음.
- 낱개코드 그대로 cadence 보유 = **0건** / 원코드로 치환 시 **319개 중 255개** 보유.

## 변경
1. `core/workflows/logistics_order.py` (df674755)
   - 신규 `unit_origin_map(unit_df=None)` — unit_list.csv 기반 {낱개/소분코드: 원코드} NFC 맵(자기자신 92건 제외 → 319건).
   - `generate_result_xlsx(..., cadence=None, unit_df=None)` — 품절목록 cadence 조회를
     `cadence.get(code) or cadence.get(원코드)` 폴백으로. unit_df 미지정 시 load_unit_list() 폴백
     (페이지·챗 네이티브 실행 모두 자동 커버 — 호출부 무수정).
2. `core/intelligence/stockout_board.py` (8e5181c1)
   - 신규 `_key(code, code_map)` 헬퍼. `reconcile(..., code_map=None)`·`board_to_frame(..., code_map=None)`가
     box_stock·cadence 조회 시 원코드로 치환. code_map 미주입 시 기존 동작(하위호환).
3. `app/pages/0b_데일리대시보드.py` (c9699393)
   - `logistics_order` import + `_unit_origin_map()` 캐시(ttl 1800) → reconcile·board_to_frame에 code_map 주입.
   - 캡션에 "낱개/소분은 원코드=박스 기준" 명시.

## 검증 (실데이터 골든 대조)
- **품절목록** — 사용자 업로드 `물류팀_0715.xlsx` 5건 재현. unit 매핑 없는 실행(=수정 전 동치)이 업로드 파일과
  값 전건 일치(회귀 기준선 확보) → 수정 후 낱개 2건 채워짐, 박스 3건 불변:
  - PC002764 → 원코드 17-02 : 2026-03-16 · 81일 · 4회
  - PC004739 → 원코드 306-33-30-01 : 2026-05-08 · 31일 · 4회
- **품절 알림판** — 라이브 board 11건 before/after: 낱개/소분 3건(GB140G12EA-10-02·PC002764·PC004739) E/F/G+현재박스재고
  채워짐, 박스 8건 불변.
- **★ 재입고 자동삭제 실증**: `GB140G12EA-10-02`(유동 골뱅이 소분, 품절시작 07-10)는 원코드 `10-02` **박스재고 122**로
  이미 재입고됐는데 5일째 알림판에 박제돼 있었음 → 수정 후 reconcile이 입고로그(품절일수 5·입고시재고 122) 기록 후
  자동삭제. before 0건 → after 1건.
- pytest `tests/test_logistics_order.py` 4 passed(골든 무변). 나머지 테스트 오류는 컨테이너 미설치 패키지
  (xlrd·msoffcrypto·python-calamine)로 사전 존재·무관.
- ast.parse 3파일 OK.

## 다음 / 상태
- ⚠️ **core 2종(logistics_order·stockout_board) 변경 → 재배포 후 Reboot app 1회 필요.** 0b는 page-only(자동반영)지만
  새 core 함수(unit_origin_map·code_map 인자)를 참조하므로 Reboot 전에는 TypeError 가능 → Reboot 필수.
- Reboot 후 사용자 확인 대기: (a) 발주서 재출력 시 낱개 행 E/F/G 표시 (b) 데일리 대시보드 품절 알림판에서
  GB140G12EA-10-02 재입고 자동처리 토스트+자동삭제(=data repo 커밋 발생).
- 잔여: 알림판 seed는 여전히 낱개코드 그대로 등록(표시는 발주 코드 유지가 맞음 — 조회 시점 치환이라 의도된 설계).
  같은 원코드의 박스코드 건이 별도 등록되면 알림판에 두 줄(원코드 재고 동일)로 보일 수 있음 — 현재 사례 없음·관찰만.
