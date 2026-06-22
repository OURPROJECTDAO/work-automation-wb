# 2026-06-22 데일리 이상치 표 — 콤마·월마진% 컬럼·페이지 폭

## 무엇 (3건, app `0b_데일리대시보드.py`)
1. **콤마(가독성)** — 이상치/전체 표 금액 컬럼(매출(net)·원가·택배·마진 + 신규 월매출)을 `NumberColumn(format="localized")`로 → 천단위 콤마. (낱개=%d, 박스/마진율/기준%=%.1f 유지.) ★이 표는 선택그리드(CheckboxColumn·on_select)라 Styler 불가 → column_config format으로 처리. streamlit>=1.36이라 'localized' 지원.
2. **월 마진% 컬럼 추가** — 기존 4월매출·5월매출 옆에 **4월마진%·5월마진%**. = 그 (채널×관리코드)의 정산 **총마진율(판매이익÷판매금액, 택배 전 gross)**. `_recent_month_sales` agg에 gp(판매이익) 추가, lk값 (매출, 판매이익) 튜플. 매출 0인 달은 마진%=None(—). 컬럼 순서=…상품명·[월매출들]·[월마진%들]·매출(net)·낱개….
3. **데일리 페이지 폭 풀기** — 컬럼 많아짐. 원인=core/ui.py `.block-container{max-width:1180px}` 전역(layout=wide인데도 1180 캡). 이 페이지만 page-scoped `st.markdown(<style>.block-container{max-width:none}</style>)`로 해제(진입점 1180 뒤에 와서 override·타 페이지는 1180 유지·디자인 의도 보존).

## 검증 (실데이터 골든)
- 월 총마진율 합리적·gross>net 관계 일관: 스스 10-01 4.3%→4.1%·식봄 11-16 7.1%→7.1%·스스 08-28 8.8%(gross) vs 화면 daily net 2.1%(택배 차감). ESM 52-55. 38.7%→13.1%=4월 소액(10,395) 노이즈(소표본 마진% 흔들림·매출 옆에 같이 보여 식별 가능).
- ast.parse OK·src.count 전건 1. 커밋 db7eb50.

## 다음·상태
- **page-only → 재배포 자동반영·Reboot 불요.** 화면 확인 대기(콤마·월마진%·풀폭).
- ★ 월마진%=gross(택배 전)라 오늘 net 마진%와 **수준 다름**(추세용). 진짜 net 월마진율은 orders+ship_alloc 택배배분 필요(무거움·미적용) — 요청 시 별건.
- master 5월까지라 6월은 7월초 [데이터추가] 적재 후 반영.
