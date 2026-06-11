# 2026-06-11 channel-margin-monitor — 식봄 가격변경 NameError 핫픽스

## 무엇
페이지 식봄 가격변경 분기에서 `_num(...)` 을 `cmm._num(...)` 으로 수정.

## 왜
배포 후 식봄 '가격 일괄변경 양식 생성' 클릭 시 `NameError: _num` (page 317). 코어 헬퍼 `_num`은 cmm 모듈 소속인데 페이지에서 prefix 없이 호출(같은 줄 정가 fallback). 페이지 내 다른 헬퍼는 cmm._nfc 처럼 prefix 사용 중이었음 — 이 한 줄만 누락.

## 변경
- `app/pages/6_채널마진모니터.py` (8699520): `_num(ro.get("정가"))` → `cmm._num(...)`. 페이지 내 bare 코어헬퍼 전수 점검 → 없음.

## 다음 · 상태
- 페이지 .py 변경 → **자동 반영**(Reboot 불필요, 새로고침). 식봄 가격변경 재시도 가능.
- 교훈: 페이지에서 코어 헬퍼는 항상 `cmm.` prefix.
