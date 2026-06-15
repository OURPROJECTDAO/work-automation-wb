# 2026-06-15 intelligence-layer 첫 브릭 — 수정로그 가격이력 적재

## 무엇 / 왜
지능 레이어 Phase 1 1a (ADR 0018). 상품수정삭제로그의 매입단가/매출단가 변경 이력을 private repo에 적재 → 마진 이력의 토대(역재생). 사용자 제공 export 1건(최대).

## ★ 스코프 정정 (실측)
- KB 가정 "3년치 export 가능" = **거짓**. ERP는 **조회일 기준 ~1년 롤링만 보관.** 실파일(Exp260615): 2025-06-16~2026-05-29, 4,663행. 그 이전은 영구 조회 불가(사용자 확인).
- 2026-06분은 이 export에 없음(다음 수신 시 dedup으로 합류).
- 결론: 3년 소급 불가 → **월 1회 재수신·dedup 누적이 필수**(ERP가 잊으니 우리가 보존). 이력 엔진의 존재 이유가 더 분명해짐.

## 변경
- work-automation-app: `core/intelligence/price_history.py`(+__init__) — parse_price_log(openpyxl read_only금지, 매입단가/매출단가만, NFC 상품코드 문자열키·콤마제거 float·처리자 PII 제외) + read_history/ingest(GitHub parquet R/W, dedup키=(상품코드·수정항목·수정일자) keep=last 멱등) + as_of_value(역재생, 앵커는 호출자 공급).
- work-automation-data: `history/price_changes.parquet` 첫 적재 — 2,567행(매입2009/매출558), 81KB.

## 검증
- 파서 실파일: keep 2,567 · 숫자 파싱 실패 0 · dedup키 중복 0 · 상품코드 937(앞자리0 보존) · 날짜 2025-06-16~2026-05-29.
- 모듈 compile OK. 적재 PUT 201. **읽기-재검증 행수 일치.**
- 미검증: 역재생 앵커(product_master 낱개[8] vs 박스[9] 매입단가) — 다음 수.

## 다음 / 상태
- 다음(★): 역재생 앵커 확정 — 매입단가 변경의 최신 수정후가 product_master 낱개/박스 어느 컬럼과 일치하는지 실데이터 대조 → as_of_value에 결선. 이후 대시보드 온라인마진 실측·마진 침식 경보로 확장.
- 운영: 월 1회 수정로그 재수신 → ingest()로 dedup 누적(현재 채팅/수동; 추후 §5.6 이력 적립 페이지).
- 상태: 지능 레이어 status=design 유지(아직 사용자向 운영 기능 없음). 첫 브릭(적재) 완료.
