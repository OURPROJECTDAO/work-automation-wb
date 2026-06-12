# 2026-06-12 channel-margin-monitor: ESM 다중파일 업로드 (수기병합 제거)

## 무엇
ESM 상품관리 갱신 업로더를 **다중파일**로 — 500상품 한도 배치 다운로드(11/22/33)를 한 번에 올리면 자동 병합.

## 왜
ESM 다운로드는 1회 500상품 한도라 여러 배치. '전체 교체'(가격변동 반영 유일 경로)는 파일 1개만 받아 → 사용자가 한 시트로 수기 병합해야 했음. 그 수작업 제거.

## 변경
- core CHANNEL_CONFIG['esm']: **`multi_file`: True**.
- `app/pages/6_채널마진모니터.py`: `multi_file` 채널이면 `st.file_uploader(accept_multiple_files=True)`. 여러 파일 각각 parse(파일내 지마켓필터·dedup) → 이어붙이기 → `dedup_key`(A) 교차 중복제거 → '전체 교체'/'신규만 추가'. **multi 채널은 raw 저장 생략**(모니터 전용, price_form 없음 → raw 미사용). '신규만 추가' help에 "기존 상품 가격변동 미반영 → 갱신은 전체 교체" 명시.
- 타 채널 영향 없음(multi 기본 False, 단일파일 경로 동일).

## 검증
- 11+22+33 각각 parse→concat→교차 dedup = **1193**(사용자 중복제거 동일), 상품번호 유니크.
- ast.parse OK (cmm.py, page6.py).

## 다음·상태
- **⚠️ core+page 수정 → Reboot app 1회 필요.**
- ESM 갱신 워크플로: 배치 3개 한꺼번에 드래그 → '전체 교체'(가격변동 반영) 또는 '신규만 추가'(신규 상품번호만). 수기 병합·중복제거 불요.
- 미검증: 실제 앱 다중파일 업로드 동작 사용자 확인.
