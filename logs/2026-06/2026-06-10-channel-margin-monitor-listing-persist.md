# 2026-06-10 channel-margin-monitor — 상품관리(listing) 연동데이터화 (저장+갱신)

## 무엇
매번 다운로드 업로드 → **저장본 자동 로드**로 변경(사용자 요청). 다운로드는 '상품관리 갱신'에서 전체 교체/신규 추가 시에만 갱신.

## 변경 (app repo)
- core (7c0c51e7): CHANNEL_CONFIG에 `key`(저장 파일명) + `LISTING_COLS`·`recs_to_csv`·`csv_text_to_recs`·`merge_listing`·`compute_listing`(recs→결과)·`_stats` 추가. `run()`=parse_download+compute_listing 리팩터.
- page (396f92de): 저장본 `reference/listing_<key>.csv` API 직읽기 자동 로드 → 표 즉시. `📥 상품관리 갱신` expander: 새 .xlsx → [전체 교체](최신 전체로 덮어쓰기) / [신규만 추가](merge_listing, 새 상품번호만) → API 커밋 + 메타(갱신일 KST·건수) + cache.clear. 커밋 직후엔 in-memory 표시(read-after-write 지연 회피). _gh PAT는 st.secrets GITHUB_PAT.
- 시드: `reference/listing_smartstore.csv`(712, c0c2e9de) + `.meta.json`(0cd496ba). → 페이지 즉시 동작.

## 검증
- 라운드트립: parse→recs_to_csv→csv_text_to_recs→compute_listing stats 동일(712·평균10.28%). merge(기존5+신규712→707추가). ast 양쪽 OK.

## 다음 / 상태
- ⚠️ core 모듈 변경(신규 함수) → **Reboot app 1회** 후 페이지에서 인식(미리부트 시 AttributeError 가능).
- 저장 위치 = app repo reference/(public). listing = 상품번호·코드·상품명·판매가·배송비·즉시할인·포인트·바코드(고객 PII 없음, product_master 가격과 동급).
- '전체 교체'가 기본(신규+가격변동 반영). '신규만 추가'는 기존 가격 유지 → 가격변동 미반영(주의).
- 타 채널: CHANNEL_CONFIG `key` + 컬럼맵 추가하면 동일 저장/갱신.
