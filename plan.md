# 업무 자동화 시스템 — 구현 청사진

_작성: 2026-06-01 · 결정 근거: decisions/0002_

---

## 0. 한 장 요약

오픈마켓 발주 정제 업무(현재 VBA 매크로 엑셀)를 **원격·클라우드 기반 Python 시스템**으로 옮긴다.
입력과 출력은 Excel 그대로, 내부 처리 로직만 VBA → Python으로 재구현한다.
일상 실행은 Web UI(무료·토큰 0), 코드 수정·개발은 채팅(Claude)으로 한다.

```
입력 Excel 업로드 →  [Python 처리 코어]  → 출력 Excel 다운로드
                          ↑        ↑
                     Web UI    Claude 채팅
                    (일상 실행)  (수정/개발)
```

---

## 1. 아키텍처 (4계층)

### 1계층 — 처리 코어 (Python 패키지)
- pandas + openpyxl로 VBA 워크플로우를 함수로 재구현.
- **로직과 데이터 분리**: 참조 데이터(도서산간/필터링/미배송 리스트)는 코드에서 빼서 csv로 관리. 데이터 갱신이 코드 수정 없이 가능.
- **워크플로우 = 플러그인**: 모든 템플릿이 "입력 읽기 → 단계들 실행 → 출력 쓰기" 패턴. 공통 베이스 + 템플릿별 모듈. 새 템플릿 = 모듈 1개 추가.

### 2계층 — Web UI (Streamlit)
- 파일 처리(업로드→실행→다운로드)와 대시보드를 한 앱에. 멀티 페이지로 분리.
- **역할 분담**: Web UI = 런타임(반복 실행, LLM 안 거침 → 토큰 0). 채팅 = 수정·개발.

### 3계층 — 코드 저장소 (채팅 수정 경로)
- KB와 **분리된** 새 repo `work-automation-app`.
- 수정 흐름: 채팅으로 요청 → Claude가 repo 코드 편집·커밋 → 서버 자동 재배포.

### 4계층 — 호스팅
- Streamlit Community Cloud (무료, 비공개 앱 1개 + 뷰어 허용명단).
- 리소스 부족·동료 확대·데이터 통제 필요 시 Railway(~$5/mo)로 이전. 코드 그대로 재사용.

---

## 2. 핵심 설계 원칙 (4가지)

1. **로직/데이터 분리** — 참조 데이터는 csv. 코드는 데이터를 "불러다" 쓴다.
2. **워크플로우 = 플러그인** — 공통 인터페이스에 맞춘 모듈. 추가·교체가 독립적.
3. **골든 파일 검증** — 기존 VBA 출력 결과물을 정답지로 두고, Python 출력이 일치하는지 자동 대조. 이관의 안전벨트.
4. **Streamlit 분리 규율** — 처리 로직을 Streamlit 파일에 절대 넣지 않는다. 화면 파일은 "그리기 + 코어 함수 호출"만. → 나중에 Railway/FastAPI 이전이 무통증.

---

## 3. 코드 구조 (work-automation-app)

```
work-automation-app/
├── core/                       # 1계층: 처리 코어 (프레임워크 무관)
│   ├── base.py                 # Workflow/Step 인터페이스, 공통 IO
│   ├── io_excel.py             # 엑셀 읽기/쓰기 헬퍼
│   └── workflows/
│       ├── registry.py         # 워크플로우 등록부 (이름 → 클래스)
│       └── openmarket_merge.py # 첫 템플릿
├── reference/                  # 참조 데이터 (로직과 분리)
│   ├── dosan_list.csv          # 도서산간리스트
│   ├── filter_list.csv         # 필터링리스트
│   └── undelivered_list.csv    # 미배송지리스트
├── tests/
│   ├── golden/                 # VBA 출력 결과물 = 정답지
│   ├── fixtures/               # 입력 샘플
│   └── test_openmarket_merge.py
├── app/                        # 2계층: Streamlit
│   ├── streamlit_app.py        # 진입점
│   └── pages/
│       ├── 1_파일처리.py
│       └── 2_대시보드.py
├── requirements.txt
├── .streamlit/config.toml
└── README.md
```

핵심은 `core/`가 `app/`을 모른다는 점. Streamlit은 `core`를 호출만 한다. 호스팅·UI가 바뀌어도 `core`는 그대로다.

---

## 4. 첫 템플릿 워크플로우 (오픈마켓합포도서산간확인V7)

버튼 순서 = 처리 단계. Python 워크플로우로 옮길 단계 목록:

| 순서 | VBA 매크로 | Python 단계 (재구현 대상) |
|---|---|---|
| 0 | ProcessMergedCells | 병합 셀 해제 + 상품명 줄바꿈 합치기 (전처리) |
| 0.5 | SaveSheetToNewFile | 정제된 송장 별도 출력 |
| 1 | CopyDuplicatesToSummary | 주소 중복 → 합포확인 |
| 2 | SortColumnBDescending | 합포확인 주소 정렬 |
| 3 | HighlightColumnC | 합포확인 색상 구분 |
| 4 | FilterAndCopyRows | 상품명 ↔ 필터링리스트 → 필터링확인 |
| — | FasterCopyRows | 주소 ↔ 도서산간리스트 → 지역확인 |
| — | mbCopyRows | 주소 ↔ 미배송지리스트 → 미배송지역확인 |

- 미사용 `OC_Module`은 이관 대상 아님.
- 출력물: 정제 송장 + 합포확인 + 지역확인 + 미배송지역확인 + 필터링확인 (멀티 시트 xlsx).

---

## 5. 단계별 구현 계획

### Phase 0 — 기반 셋업
- [ ] GitHub private repo `work-automation-app` 생성 (사용자)
- [ ] PAT 권한을 두 repo(`-wb` + `-app`)로 확장 (사용자, Claude 안내)
- [ ] 프로젝트 구조 스캐폴딩 (위 3장 디렉토리)
- 산출물: 빈 골격 repo

### Phase 1 — 첫 템플릿 Python 이관 (핵심)
- [ ] 참조 데이터 3종을 xlsm에서 csv로 추출 → `reference/`
- [ ] `core/base.py` 워크플로우 인터페이스 구현
- [ ] `openmarket_merge.py` 8단계 재구현 (주소 매칭 전 NFC 정규화, csv는 UTF-8-sig)
- [ ] 기존 출력 결과물을 `tests/golden/`에 배치
- [ ] 골든 파일 대조 테스트 통과
- 산출물: CLI로 "입력 xlsx → 출력 xlsx"가 VBA와 동일 결과

### Phase 2 — Streamlit 앱 골격 + 배포
- [ ] `app/streamlit_app.py`: 업로드 → 워크플로우 선택 → 실행 → 다운로드
- [ ] Community Cloud 배포 + 뷰어 허용명단 설정
- 산출물: 웹에서 파일 넣고 결과 받는 동작

### Phase 3 — 나머지 템플릿 이관
- [ ] 템플릿 1종씩 분석 → 워크플로우 모듈 추가 → 골든 대조
- 산출물: 10종 전부 웹에서 선택 실행 가능

### Phase 4 — 대시보드
- [ ] `2_대시보드.py`: 매출/현황 등 데이터 뷰 (차트·필터)
- 산출물: Power BI 유사 뷰

### 나중
- 입력 자동 수집 (스마트스토어/쿠팡/ESM API or 크롤링)
- 동료 접근 확대 / 필요 시 Railway 이전

---

## 6. 위험 / 주의

- **데이터 통제**: 주문 데이터가 무료 외부 서버(Community Cloud) 경유. 비공개 허용명단이지만 통제권 밖임을 인지. 께름칙하면 Phase 2에서 바로 Railway로.
- **VBA 정확 재현**: VBA의 미묘한 동작(병합 처리, 부분 문자열 매칭 등)을 그대로 옮겨야 함. 골든 파일 대조가 이걸 잡아줌.
- **VBA 직접 수정 보류**: xlsm 내 VBA를 코드로 수정하는 건 위험(OLE 바이너리). 미사용 모듈 삭제는 Excel 수동으로.
- **PII**: KB·로그에 고객정보 금지. 식별자(주문번호 등)만.

---

## 7. 한국어 처리 (전 구간 필수)

엑셀 내용·주소·상품명·시트명이 대부분 한글. 다음을 기본값으로 박는다.

1. **인코딩 일관성** — 전 구간 UTF-8. 특히 `reference/` csv는 **UTF-8-sig(BOM)**로 저장 → Excel에서 직접 열어도 안 깨짐. base64 디코딩 시 Latin-1 절대 금지(모지바케).
2. **유니코드 정규화(NFC)** — 주소 매칭 **전에 NFC 정규화 필수**(`unicodedata.normalize("NFC", s)`). 출처가 다른 데이터가 NFD(자모 분리) 형태면 같은 글자라도 부분일치 매칭이 실패. 도서산간·미배송 매칭(주소 부분 포함 검사)이 핵심 로직이라 이 버그는 치명적.
3. **대시보드 차트 폰트** — matplotlib는 한글 폰트 미설치 시 □□□로 깨짐. Plotly/Altair(브라우저 폰트 사용) 권장. matplotlib 쓸 거면 나눔고딕 등 한글 폰트 설치·지정 필요.
4. **정렬 순서** — VBA의 xlPinYin 정렬과 Python 기본 정렬(유니코드 코드포인트)이 가나다 순서에서 미묘하게 다를 수 있음. 골든 파일 대조로 확인하고, 어긋나면 로케일 기반 정렬 적용.
5. **시트명/파일명 한글** — openpyxl는 한글 시트명 OK. 출력 파일명 한글도 대체로 OK(서버 파일시스템 UTF-8 확인).

> 검증 연결: 위 1·2·4는 골든 파일 대조 테스트에서 자동으로 드러난다. 결과가 한 글자라도 다르면 인코딩/정규화/정렬 중 하나를 의심.

---

## 8. 다음 한 수

**Phase 0**의 repo 생성 + PAT 확장. 이 두 가지(사용자 작업)가 끝나면 Phase 1 착수.
