# 2026-06-12 — upload-monitor 채널별 업로드제외(skip) + 등록/해제

## 무엇
- 새 상태 `업로드제외`(해당 채널 업로드x, 사용자 지정) + 등록/해제 UI + 전채널제외 행 숨김.

## 왜
- "업로드필요"로 잡히지만 실제로는 그 채널에 안 올릴 상품을 셀 단위로 표시. 예) 003601(비상품)=전채널 제외, 001591=캐시노트만 제외. 반대로 다시 업로드모드로 돌리는 해제도.

## 변경
- **core(upload_monitor.py)**: `ST_SKIP_CH="업로드제외"` + `parse_skip_text`/`build_skip_text`/`_load_skip`(상품코드,채널key 쌍) + `build_gap_table(skip_pairs=)` 오버라이드(셀 상태가 `업로드필요`일 때만 → `업로드제외`, 우선) + `channel_summary` 업로드제외 카운트. **skip_pairs 인자=페이지 라이브 read, 없으면 reference/upload_skip.csv.**
- **page(7_업로드감시.py)**: GitHub 헬퍼(_pat/_gh/_commit_skip) + `upload_skip.csv` 라이브 read(@cache_data ttl60)→build_gap_table 주입(frozenset 캐시키) + ALL_STATUS에 업로드제외 + **전채널제외 포함 토글**(기본 숨김: 8채널 전부 업로드제외인 행) + 채널별 건수표에 업로드제외 + **등록/해제 섹션**(표 다중선택 상품코드 × 체크채널 → upload_skip.csv append/diff 커밋, 미리보기 expander, _skip_text/_load cache clear+rerun).

## 검증 (실데이터, st 없이)
- 003601 전채널 skip → 8칸 전부 업로드제외·all()=True(기본 숨김 대상). 001591 캐시노트만 skip → 캐시노트=업로드제외·스마트스토어=업로드필요·all()=False(표시 유지).
- build/parse_skip_text 라운드트립 일치. 해제(차집합) → 001591 캐시노트 다시 업로드필요. 등록 쌍(상품×채널) 추가 정상.
- channel_summary 컬럼 [업로드필요·품절처리필요·업로드제외]. ast.parse OK(core+page).

## 우선순위 규칙
- 업로드제외 > 업로드필요 (셀). 이상없음·품절처리필요는 불변(이미 올라간 건 의미 없음).
- 전채널(8) 업로드제외 = 행 기본 숨김(토글로 표시). 부분 제외(001591)는 표시 유지.

## 다음 · 상태
- **core 수정 → Reboot app 1회 필요.** upload_skip.csv는 첫 등록 시 생성(없으면 빈 set).
- 다음 = L4 핸드오프(스마트스토어·ESM 등록폼 prefill / 6채널 CSV).
