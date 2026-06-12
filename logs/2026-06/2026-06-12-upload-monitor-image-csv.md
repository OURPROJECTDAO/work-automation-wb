# 2026-06-12 — upload-monitor 이미지 포함 CSV (대표 A1 / 상세 B1 실검사)

## 무엇
- CSV 다운로드 디벨롭: 관리코드 기준 이미지 실검사(유무·확장자·URL)를 CSV에 추가.

## 왜
- 업로드필요 리스트를 받아 등록할 때, 각 상품의 이미지가 있는지·jpg/png·URL을 미리 알면 등록 준비가 끝남(L4 핸드오프 사전작업). 등록 워크플로우(smartstore/esm-register) 이미지 패턴 재사용.

## 변경
- **core(upload_monitor.py)**: `IMG_HOST`(gi.esmplus.com/td680708) + `IMG_COLS`(6) + `_img_url`·`_head_ok`(HEAD 200) + `probe_slot`(슬롯별 jpg→png) + `probe_image`(A1/B1 독립) + `probe_images`(ThreadPool 병렬·dedup·빈관리코드 제외). import urllib.request·concurrent.futures.
- **page(7_업로드감시.py)**: "🖼 이미지 확인 후 CSV 만들기" 버튼 → csv_src 관리코드 프로브 → 기본컬럼 + IMG_COLS(대표/상세 유무·확장자·URL) + 선택채널상태로 enrich → 이미지 포함 CSV. **관리코드별 세션 캐시**(um_img_cache, 재프로브 안 함) + summary(대표/상세 있음·없음) + download rerun 함정 회피(session_state 밖 렌더).

## 검증 (실데이터, 샌드박스)
- gi.esmplus.com HEAD 프로브 실동작: 200/404 판별, 대부분 jpg(.png fallback), **A1/B1 독립**(27-16 A1없고 B1있음). 33개 병렬 2.5s(workers24).
- enrich CSV 헤더 = 기본6 + 이미지6 + 채널. 빈 관리코드 공란. 대표/상세 유무 카운트 정상.

## ⚠️ 미검증
- **배포 Streamlit Cloud egress**: 샌드박스는 gi.esmplus.com 접근되나 Community Cloud 외부 egress 미확인 → 배포 후 버튼 눌러 '있음' 나오는지 확인. 전부 '없음'이면 egress 차단(페이지 안내문 포함).

## 다음 · 상태
- **core 수정 → Reboot app 1회 필요.**
- 다음 = L4 핸드오프(이 이미지 URL을 등록폼 prefill에 활용).
