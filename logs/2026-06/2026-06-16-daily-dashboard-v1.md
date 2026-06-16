# 2026-06-16 — 데일리 대시보드 v1 (당일 점검 승격 + 세션 자동 파일 인계)

## 무엇
마진침식 탭D(당일 점검)를 독립 페이지 '데일리 대시보드'로 승격(네비 첫 그룹·지도·로드맵 아래) + 매일 출력하는 천년경영 output·송장출력을 이전 워크플로우(파일처리)에서 **세션 자동 인계** → 재업로드 불요. 사용자 비전='매일 반복 업무 산출물로 당일 인사이트(당일점검의 확장판)' 첫 브릭.

## 왜
탭D는 매번 2파일 수동 업로드 필요. 둘 다 사용자가 매일 파일처리에서 이미 생산. 클릭 한 번에 보게.

## 변경 (코드 — app repo)
- 신규 `core/intelligence/daily_inbox.py` — 세션 인박스 push/get + 슬롯 상수(SLOT_CHEONNYEON/SLOT_INVOICE). core는 streamlit 비의존(session_state 인자).
- 신규 `app/pages/0b_데일리대시보드.py` — 당일 마진(daily_margin 재사용) + 인박스 상태표시 + 슬롯 수동 갱신(override). 상품관리=reference 라이브.
- 수정 `app/pages/1_파일처리.py` — `import _inbox` + 오픈마켓(invoice_bytes=★★송장)·천년경영(out=output) 생성 직후 inbox.push.
- 수정 `app/pages/8_마진침식.py` — 탭D 제거(3탭)·`daily_margin import` 제거.
- 수정 `app/streamlit_app.py` — nav 지도·로드맵 다음에 데일리 대시보드.
- 커밋: daily_inbox e2b0707·0b 7124c7b·1_파일처리 1b2430b·8_마진침식 7fa0cea·streamlit_app 3a3cfd8.

## 검증
- 코드 5종 `ast.parse` 전부 통과(편집 anchor assert·8_마진침식 tabD/dm 잔여 0 확인).
- 호환성: 오픈마켓 generate_invoice_xlsx(★★송장) 송장출력 시트 = 탭D parse_invoice_shipping 위치(판매처[3]·수령자[5]·주소[6]·상품명[7]·송장번호[9])·탭D 0615 실파일 검증 형식과 동일 → 자동 인계 호환 확정(코드 읽어 대조). 천년경영 out=parse_cheonnyeon_sales 입력 동일.
- ★ 인박스=세션 휘발성(송장 PII로 디스크/repo 미저장) → 같은 세션 자동·새 세션 수동. 사용자 수용(일일 업무 한 세션).

## 다음 · 상태
- 상태: v1 배포 커밋 완료. **새 core(daily_inbox) 첫 배포 → 데일리 대시보드 안 보이면 Reboot app 1회.** 실사용(자동 인계 동작) 사용자 확인 대기.
- KB: systemmap daily-dashboard 노드 신설(meta n)·edges(오픈마켓/천년경영→데일리)·state 인덱스/다음·workflows/daily-dashboard.md·intel §5.6·INDEX·ADR 0023.
- 다음 한 수 = **확장판**(추가 데일리 인사이트 — 품절/발주/업로드 등 반복업무 결합, 사용자와 설계).
