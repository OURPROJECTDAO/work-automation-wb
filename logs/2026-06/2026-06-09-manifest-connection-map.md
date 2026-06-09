# 2026-06-09 연결 맵(manifest.md) 신설

## 무엇
공유 자산·워크플로우 의존을 한 장에 모은 역색인 manifest.md 신설. INDEX에 포인터 등록(상시읽기 아님 — 공유 reference/체인 건드릴 때만).

## 왜
KB 확장성 점검에서 "파일 연결성이 산문으로만 흩어져 있어 공유 파일 바꿀 때 영향범위(blast radius)를 한 번에 못 본다"가 약점으로 확인됨(에이전트 관점). ~10% 이관 시점에 미리 잡음.

## 내용 (워크플로우 10개 문서 실독 후 추출)
- A. 다중소비자 reference: product_master(logistics·dashboard·등록3채널), logistics_classification(logistics·cheonnyeon·dashboard) — 편집경로·깨짐주의 명시.
- A-2. 단일소비자 reference 소유 매핑.
- B. 의존 그래프: cheonnyeon←logistics(아카이브7열+분류표), dashboard⇄logistics(분류표), 등록3채널→common 상속, 등록채널←product_master, invoice-fill←송장마스터(openmarket 연결 미확정 플래그).
- C. 등록채널 자산위치(양식/카테고리=reference 정본, 소스/결과=Drive) + Drive 폴더ID. easyadmin 양식 미보관 명시.
- D. 공유 코드/페이지(1_파일처리.py 3워크플로우 공존 등).

## 검증
- 8개 워크플로우 문서 raw 일괄 재독 + esm/easyadmin 기독 내용으로 의존 추출. 추측 아님.

## 다음 / 상태
- 미적용(점검 제안 중 나머지): pitfalls 이분화(infra vs domain), state 상태 단일 진실원천화(행=포인터). 사용자 판단 대기.
- 신규 워크플로우/공유 reference 추가 시 manifest A·B·C 갱신 규율.
- invoice-fill 송장마스터 ↔ openmarket 송장출력 연결 확인 필요(B에 플래그).
