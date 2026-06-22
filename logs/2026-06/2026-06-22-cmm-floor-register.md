# 채널마진모니터 — 제한 상품 등록/해제 UI (권장가 ↔ 제한)

## 무엇
표에서 상품 선택 → "🔒 제한 상품 등록/해제" 섹션에서 **제한내용 입력→저장**으로 그 관리코드를
`reference/margin_floor.csv`에 등록(=권장가 칸이 제한 문구로 바뀜). 비우고 저장=해제. 전 채널 공통.

## 출처 (사용자 질문 답)
- 권장가/제한 컬럼: 제한(margin_floor.csv에 그 관리코드 있으면 '제한내용' 텍스트) > 미매칭 비고 > 기준미설정 > 권장가(역산).
- compute: `fl = refs["floor"].get(rec["코드"])` if apply_floor → row["제한"]=제한내용 or 비고. 키=listing 관리코드 원본.
- 두뇌④ load_locked()도 같은 파일 읽어 작업목록 제외. KB margin-optimizer §22 "제한 등록/해제는 채널마진모니터 쪽 관리" 충족.

## 변경
- **core**:
  - `compute_listing(..., floor_override=None)` — floor_override 있으면 refs["floor"] 교체(즉시 반영). compute 무수정(refs["floor"]만 씀).
  - `parse_floor_dict(text)` — margin_floor.csv text → {관리코드:{상품명,비고,제한내용}}(라이브 read).
  - `update_floor_csv(text, upserts, removes)` — 등록/수정(upsert)·해제(remove). 헤더/열순서/BOM(utf-8-sig)/CRLF 보존(update_baseline_csv 패턴).
- **page**:
  - `_load_floor_text()`(@cache 라이브) + `_commit_floor()`. compute_listing에 floor_override=parse_floor_dict 주입(편집 즉시 반영, baseline과 동일).
  - **제한 등록/해제 섹션**(기준마진율 설정과 같은 인라인+cmm_tblver 패턴): 선택 상품 data_editor(관리코드·상품명·현재·제한내용✏️). 입력=등록/수정·비움(기존 제한)=해제·빈칸+무제한=무변경. 저장→commit→clear→tblver+1→rerun(체크박스 풀림·즉시 반영).

## 검증
- update_floor_csv 골든: 원본 48 제한 → 신규1+수정1 등록/2, 해제1. BOM·CRLF·헤더·타 관리코드 전부 보존. 재파싱 일치.
- parse_floor_dict 48건. ast OK. 커밋 core f8726dcd · page 18af7eb4.

## 다음 / 상태
- ⚠️ **core(compute_listing 시그니처·새 함수 2개) → Reboot 1회 필요**(이번 세션 canonical_code Reboot에 묶임).
- 제한내용 기본=빈칸(선택분 일괄 오등록 방지) — 입력한 행만 등록. 비고는 "마진율 민감 상품" 자동.
