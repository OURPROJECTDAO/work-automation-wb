# 2026-06-12 — upload-monitor 설계확정 + 실물검증 (KB 기록)

## 무엇
- 신규 워크플로우 **upload-monitor(업로드감시)** 설계확정 + product_master/resolve_code/listing 실물검증 + KB 기록.

## 왜
- 골든 `★재고관리시트`(박스재고 있는데 채널 미업로드 감시)를 **코드기반 자동 매칭 + 등록 인계 + 대시보드 커버리지**로 발전. 발주 재고 ↔ 등록 ↔ 마진모니터를 잇는 허브.

## 변경
- workflows/upload-monitor.md 생성
- decisions/0017-upload-monitor.md 생성
- state.md: 워크플로우 인덱스 +1행, 다음 한 수 추가, 갱신
- roadmap.md: 다음(우선순위) 추가
- manifest.md: product_master·product_attributes 소비자 +upload-monitor, listing 공유 표기, 의존그래프 추가
- INDEX.md: 현재 워크플로우 목록 +upload-monitor

## 검증 (실물)
- **product_master.csv 4,340행**: 상품코드[3] 유니크(빈0) → **키=상품코드**. 관리코드[4] 빈114+충돌2(`27-08`,`27-01-05`) → 키 부적합. 박스재고=[14]("박스")·박스매입단가[9]·상품명[5]·규격[6]·박스내품[7] 위치 확정. utf-8-sig.
- **resolve_code** 반환 (유형,매입가,재고,규격,비고) — 정체 미반환 → 얇은 `resolve_identity` 래퍼 필요(분기 재사용·상품코드 반환). refs `pm_by_mgmt`(관리코드→행)·`pm_by_prod`(상품코드→행) 존재.
- **listing_*.csv 8채널 전부 존재**(ali·allways·baemin·cashnote·coupang·esm·sikbom·smartstore), 관리코드 컬럼명="코드"(빈값 가능).

## 설계 확정 (ADR 0017)
- base 정체 collapse(키=상품코드) → "하나라도 업로드=OK" 자동. 재고=박스재고, 우선순위=재고금액 desc. 품절 단일판정. listing 마진모니터 스냅샷 그대로.
- MVP = L1(매트릭스)+L2(갭)+L4(스마트스토어·ESM 자동폼 / 6채널 CSV)+L6(건수 KPI). 제외=L5 채널확장·추이·6채널 자동폼·예상마진·품절정밀화.

## 다음 · 상태
- **설계확정 MVP, 미구현.** 다음 = ③코어 모듈(`resolve_identity` 래퍼 + 갭 빌더) 구현 → 독립 페이지 → L4 핸드오프.
