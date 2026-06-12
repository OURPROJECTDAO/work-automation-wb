# 2026-06-12 — upload-monitor 코어 구현 + 실데이터 검증

## 무엇
- `core/workflows/upload_monitor.py` 신규: `resolve_identity` + 갭 빌더(uploaded 집합 → product_master 박스재고 조인 → 4분기·재고금액 desc).

## 변경
- 신규 모듈: `resolve_identity(코드,refs)->[상품코드]`(resolve_code 분류 분기 재사용·상품코드 반환, 합포 다중) · `_listing_codes`(listing CSV '코드' 컬럼) · `_load_exclude` · `build_uploaded_sets` · `build_gap_table`(노이즈/비판매 제외·재고금액 desc) · `channel_summary`(채널별 미업로드/품절 건수) · `gap_list_for_channel`.
- channel_margin_monitor에서 `_nfc·_num·load_references` import(중복 구현 안 함).
- **비판매 제외**: 중분류 `반품`·`파렛트`(EXCLUDE_MIDCAT) + 사용자 유지 `reference/upload_monitor_exclude.csv`(상품코드, 없으면 no-op).

## 검증 (실데이터)
- pm 4,340행 · 8채널 listing 전부 로드. ast.parse OK.
- **resolve_identity 4유형 환원 OK**: 박스 `26-08-02`→[005837]·낱개 `PC005902`→[005902]·소분 `BT10EA-25-40-02`→[001771]·합포 `31-03-08-CB-31-03-01`→[003612,002099].
- 채널 커버리지(업로드된 상품코드/ listing행): 스마트스토어 567/712·ESM 482/1193·식봄 473/522·캐시노트 502/544·배민 381/394·쿠팡 317/1306(로켓그로스 제외 영향)·올웨이즈 415/621·알리 285/322.
- 테이블 1,001행(반품·파렛트 19행 제외). 스마트스토어 업로드필요 362건·재고금액합 ~8.1억.
- **잡음 발견**: 부자재(포장박스 '3번(350*290*330)'·'16호뚱캔'·'랩(산업용)'·테이프)·회계('마트킹 환불 상계액')가 실분류(창고존, 예 '통조림-C동')에 섞여 카테고리로 못 거름. 일부는 관리코드 공백이나 그게 깨끗한 신호는 아님(실상품도 공백 가능, 부자재도 코드 보유). → 제외목록(상품코드)으로 발견 시 보완.
- 골든 직접 대조 불가: 골든 `★재고관리시트`가 외부참조 수식만·각 채널 결과페이지 캐시 없음 + 현재 listing 시점차. 로직 레벨 검증으로 갈음.

## 다음 · 상태
- **코어 구현·검증 완료, 미배포**(import 소비처 없음 → Reboot 불요).
- 다음 = ④ 독립 페이지(표·KPI·필터) → ⑤ L4 핸드오프(스마트스토어·ESM 입력폼 prefill / 6채널 CSV).
- 향후 제외목록 페이지 편집 UI, 부자재 1차 시드(사용자 마킹).
