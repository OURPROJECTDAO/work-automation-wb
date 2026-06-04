# 워크플로우: 온누리양식_발주서 (onnuri-order)

> 이 워크플로우를 건드리기 전 이 파일을 읽는다. 전역 함정은 pitfalls.md.

## 요약
- `_2-a_온누리양식v2.xlsm` 발주서 처리. 입력 발주서 → 합계:판매가 열 역기입 → (확인).xlsx 저장.
- Phase 3 (1번째 템플릿). 운영 중.
- 원본 VBA 모듈: `OC_JT_FillG_And_SaveConfirm`. 사용자 내부 명칭: **제이티발주 업무**.

## 코드 / 데이터
- `core/workflows/onnuri_order.py` (162줄)
- 참조: `reference/sku_list.csv` (109 SKU, UTF-8-sig)
- UI: 기준데이터관리 > **SKU단가표** 탭 (sku_list.csv 인라인 편집, key_col=관리코드, large=False — 기존 탭 렌더링 로직 재사용).

## 핵심 수식
합계 = 공급가 × 수량 + ceil(수량 / 최대합포수량) × 배송비
- VBA 원식: `F2 = E2*C2*B2 + G2` → 합계 = 공급가 × 수량 × 합포 + 배송비나누기 × 배송비기본.
- 최대합포수량 = SKU!F열 (배송비 부과 규칙). 코카콜라500=1, 일반음료=2~3.
- 배송비나누기 N = ROUNDUP(수량 / 최대합포수량) = `math.ceil(qty / max_bundle)`. 배송비는 합포수량 초과 시 1배송당 1회 추가.
- 골든 15행 전수 역추적 후 구현.

## 출력 방식 (2026-06-04 수정)
- **zipfile 직접 조작**: 원본 xlsx를 zipfile로 열어 `sheet1.xml`의 합계 열만 패치 후 저장.
- 기존 방식(`shutil.copy2` + openpyxl save)은 모든 문자열 셀을 sharedString(`t="s"`) → inlineStr(`t="inlineStr"`)으로 변환 → 외부 시스템 헤더 인식 불가 문제 발생하여 교체.
- zipfile 방식은 sharedStrings.xml 구조를 원본 그대로 유지. 헤더 및 모든 문자열 셀 `t="s"` 보존.

## 전용 함정
- **openpyxl read_only 셀 값은 숫자도 str로 읽힐 수 있음** → `int()` 명시 변환 필수.
- **SKU 테이블 동일 관리코드 중복 존재** (예: 23-18 × 2) → `drop_duplicates('관리코드', keep='first')` 필수.
- 우편번호는 입력 xlsx에 이미 문자열 `"08206"` 형태로 저장 → 별도 처리 불필요.
- **★ openpyxl save 금지**: `_save`에서 openpyxl의 `Workbook.save()` 사용 시 sharedString → inlineStr 변환 발생. 합계 열 수정은 반드시 zipfile 직접 조작 방식 사용. (2026-06-04 확인)

## 검증 (골든 대조)
- 골든 15/15 행 전수 일치 (`골든 일치: True`).
- (전용 pytest 파일은 아직 별도 없음 — 회귀 테스트화는 백로그.)

## 관련 로그 / 결정
- logs/2026-06/2026-06-01-phase3-onnuri-order.md (구현)
- logs/2026-06/2026-06-01-phase3-sku-tab.md (SKU단가표 탭)
- logs/2026-06/2026-06-04-onnuri-sharedstring-fix.md (sharedString 버그픽스)
