# 현재 상태 (스냅샷)
> 워크플로우 상세 = workflows/<name>.md · 작업 이력 = logs/ · 백로그 = roadmap.md · 전역 함정 = pitfalls.md · 결정 = decisions/

## 운영 인프라
- KB 기억 시스템: GitHub OURPROJECTDAO/work-automation-wb (main).
- 코드 저장소: GitHub OURPROJECTDAO/work-automation-app (main, public).
- 엑셀 작업물: Google Drive 업무자동화-KB/templates·inputs·outputs.
- 웹 앱: Streamlit Community Cloud 배포·운영 중.

## 워크플로우 인덱스 (이관 완료 = 운영 중)
> 상태는 통제어휘(운영중/진행중/이슈/개념doc). **상세·검증·미해결·자산은 각 workflows/<name>.md**. 연결=manifest.md. **구조화 정본(노드 status·로드맵·연결)=systemmap.json (ADR 0019); 아래 표·다음 한 수는 사람용 서사 미러.**

| 워크플로우 (내부명) | Phase | 상태 | 상세 |
|---|---|---|---|
| openmarket-merge (오픈마켓합포도서산간확인V7) | 1 | 운영중 | workflows/openmarket-merge.md |
| onnuri-order (온누리양식_발주서/제이티발주) | 3 | 운영중 | workflows/onnuri-order.md |
| logistics-order (발주서출력업무) | 3 | 운영중 | workflows/logistics-order.md |
| cheonnyeon-upload (천년경영업로드V15) | 3 | 운영중 | workflows/cheonnyeon-upload.md |
| invoice-fill (송장처리) | 3 | 운영중 (4채널) | workflows/invoice-fill.md |
| dashboard (영업이익현황) | 4 | 운영중 (이익률·물류량 점진) | workflows/dashboard.md |
| product-registration-common (등록 공통) | — | 개념doc | workflows/product-registration-common.md |
| smartstore-register (스마트스토어) | — | 운영중 (챗) | workflows/smartstore-register.md |
| easyadmin-register (이지어드민·정산채널) | — | 운영중 (챗) | workflows/easyadmin-register.md |
| esm-register (ESM=G마켓) | — | 운영중 (챗) | workflows/esm-register.md |
| channel-margin-monitor (채널 가격·마진 모니터) | — | 운영중 (8채널 모니터 / 7채널 가격변경) | workflows/channel-margin-monitor.md |
| upload-monitor (업로드감시) | — | 운영중(업로드제외 등록/해제, L4 대기) | workflows/upload-monitor.md |
| intelligence-layer (지능 레이어·이력엔진+두뇌) | — | 진행중 (1a·1b·두뇌①·주문적재(전기간 2023-03~2026-05)·판매가검증·P2 송장실배분·**매입현황 전기간 적재(2022-01~2026-05)** 완료)·**두뇌① 탭D**·**두뇌② 재고 지능(품절·재발주)** | workflows/intelligence-layer.md |

## 완료된 Phase
- Phase 0: 코드 repo 스캐폴딩. 2026-06-01.
- Phase 1: openmarket_merge 8단계 + pytest. 2026-06-01.
- Phase 2: Streamlit 앱 + Community Cloud 배포 + 기준데이터 관리 UI. 2026-06-01.
- Phase 3 (진행 중): 4종 완료 (onnuri-order, logistics-order, cheonnyeon-upload, invoice-fill). 나머지 템플릿 대기.
- Phase 4 (운영 최소): 대시보드 — 데이터계층+저장어댑터+3개년 적재(313K행)+최소 페이지(매출 집계)+증분 업로더([데이터 추가] 탭) 배포. 차트/물류량/이익률/거래처그룹 점진추가. 2026-06-08. (decisions/0006)

## 막힌 것 / 이슈
- 없음. (B2 인프라 완료 — repo·PAT R/W·st.secrets 검증됨 2026-06-08.)

## 다음 한 수
- **★★ 재개점 (2026-06-15): 주문 백필 완료 ✅(2023-03~2026-05·398,873행·2023 여름 갭만). 데이터현황 페이지 1단계 ✅(통합 데이터 관리·적재 범위/갭·가격이력 포함·x축 YYYY-MM). **2단계 업로드=나중에 일괄**(매입현황 등 적재 대상 다 갖춘 뒤·사용자 확정). **두뇌①·② 완료(2026-06-15)** → 다음=**두뇌③ 채널 가격 A/B**(채널명 정규화 선행) or 상품360카드. 로드맵 정본=systemmap.json. ⚠️ 두뇌① core 수정 → Reboot app 1회.**
  - **P2 완료**: core `ship_alloc.py` — EA 송장그룹 박스배분÷매출낱개=택배강도 + (상호명,월) 00-12 정합, 대시보드 온라인마진 탭 추정송장·k 교체(토글 use_actual 기본 ON·EA 미경유 6채널 추정 fallback). 골든 reconcile 채널 총택배==00-12 정확(diff0)·rate 커버 100%·기존추정 +28% 과대. ★단위=매출낱개≠EA판매단위. ⚠️core→**Reboot app 1회**.
  - **적재 완료**: orders/easyadmin_2026-{01~05}.parquet 51,641행(PII제거·송장그룹 해시·발주일 기준·core `orders.py`). velocity+송장그룹 토대. 다음 백필=2025(컨테이너, Streamlit 1GB 회피).
  - **판매가 신뢰도 검증 완료**(3중: 매출자료 gross/net·현재 listing·정산서/원장 — 상세 logs/2026-06-15-easyadmin-price-reliability.md): EasyAdmin 판매가 = "주문 시점 실제가"로 **신뢰**. 채널별 — 알리 원장 89% 정확·보조금 없음(가설 기각)·**고가 세트/번들만 EA 과소**(예 스팸세트 EA 35,600 vs 진실 136,500); 식봄 정산서 쿠폰 0건(사용자 기억 할인=마켓보로 *플랫폼 즉시할인* → EasyAdmin/정산서 미포착=정상)·15% 갭=가격 인하 drift; 올웨이즈 EA<listing=수수료 변동 가격 선인상(시간차); 나머지 신뢰. **수수료 가정 검증**=알리 9%(ERP 0.91·모니터 0.09, 실측 8.8%)·식봄 7%(실측 6.6%) 둘 다 정확·보수적.
  - **보정 보류(백로그)**: 고가 세트/번들 EA 판매가 과소 → velocity/A/B에서 listing 보정. 사용자: "나중에 숫자 이상하면 맞추자"(지금 안 함).
  - **현재 순서(ADR 0020 재배열·정본=systemmap.json)**: ① 두뇌① 강화 ✅(3렌즈+velocity, velocity는 두뇌①에 흡수) → ② ✅**두뇌② 재고 지능**(현재고÷소진율 품절·재발주 4구간·9_재고지능) → ③ **두뇌③ 채널 가격 A/B**[next] → 상품 360도 카드. 토대(이력엔진·P2 송장실배분·주문 398K 백필·매입현황 66K 적재) 모두 완료.
- **★ intelligence-layer(지능 레이어·이력엔진+두뇌) 설계확정·미구현(ADR 0018, 2026-06-12)**: 관찰↔실행 사이 두뇌(진단·추천·측정) 신설. 매일/3년 데이터를 private repo 이력으로 적립 → ①마진 침식·제시 ②입고·품절 예측 ③채널 가격 A/B. ★정산 진실=매출자료(EasyAdmin/erp 정산은 raw), 택배 실배분=송장번호 그룹(추정송장·k 대체), 매입가=master(수정로그). 데이터 카탈로그 9종·단계별 구현 = workflows/intelligence-layer.md. **이력 엔진 1a(수정로그 가격이력 적재+역재생)·1b(상품관리 재고 스냅샷 적립) 완료(2026-06-15).** 1b=업로드 훅이 새 업로드 df를 날짜본으로 `snapshots/stock_YYYY-MM.parquet` 적립(dedup 멱등·전이탐지 0↔양수), core `stock_history.py`, **forward 축적**(과거 소급 불가), ⚠️core→Reboot. **두뇌① 마진 침식 v1 완료(2026-06-15)** — 신규 `8_마진침식.py`+`margin_erosion.py`. **채널 baseline 기준**(매익률=오프라인이라 폐기, 사용자 확정)·최근 3개월 매입인상∩채널 미달·이미 재설정분 자동제외·8채널 통합·권장가(cmm 재사용). 검증 89관리코드 인상→침식 50건(게토레이 4채널·동원참치 +30%). 한계=합성코드 미조인. ⚠️core→Reboot. **EasyAdmin 주문 적재 1차 완료(2026-06-15)** — orders/easyadmin_2026-{03,04,05}.parquet 25,821행(PII제거·송장그룹 해시·**발주일 기준**, core `orders.py`). velocity·송장그룹 토대 확보. **2026 전체(1~5월) 51,641행 적재 완료.** 다음=2025 백필(컨테이너·Streamlit 1GB 회피). ★정확도 함정=EasyAdmin≠매출자료 100% 아님(발주후 일괄입력·취소송장 00-12 미차감) → velocity는 월/주 단위, 정산진실=매출자료. velocity 연결 후보=두뇌① 정렬(침식×판매량)·두뇌③ 가격 A/B·P2 송장배분(진짜 마진). 운영=월1회 수정로그 재수신 ingest(침식 정확도).
- **Phase 4 대시보드 점진 확장**: 매출집계·증분업로더·거래처그룹·구분분류·기간 날짜범위·일/월/연 추이·**이익 모드(택배비=ERP 00-12 라인, 3000/2500 보정 토글, 이익률=이익/매입가, 전체 거래처)** 배포 완료(decisions/0008). 다음 후보 — ① 물류량(수량÷박스내품) ② 이익/물류량 콤보(이중축). 상세 workflows/dashboard.md.
- core/ 신규 모듈을 페이지가 import → 첫 배포 후 Reboot app 필요(pitfalls 모듈캐시).
- **상품등록 운영 중**(챗 네이티브, ADR 0009): smartstore·esm·easyadmin. **멀티채널 배치 입력폼 v2**(`reference/product_input_form_v2.xlsx`, 대상 채널=스마트스토어/G마켓/둘 다) 배포 완료(2026-06-10) — smartstore·esm 공용, 구 v1 deprecated. 이미지확장자=URL 실검사 자동판별 확정. 미해결 — 결정적 엔진/캐시 미구현. 상세 workflows/product-registration-common.md·*-register.md.
- **대시보드 product_attributes**: ✅ 슬림화(ADR 0011, 2026-06-10) — 4컬럼(식품음료·합포수량·최종분류). 차원=세분류만 + 식품음료 구분 3차 fallback(브랜드·b2b 폐기). **Reboot app 필요.** 451 합포수량 채우면 병합. 상세 workflows/dashboard.md.
- **상품마진(온라인) 탭**: ✅ 신설(ADR 0012, 2026-06-10) — 합포×내품 택배배분 추정 + 채널 보정계수(실제송장÷추정송장). 온라인 거래처 자동스코프. page-only. 상세 workflows/dashboard.md.
- **channel-margin-monitor**(채널 가격·마진 모니터, 운영중): 스마트스토어·식봄·**캐시노트** 모니터. 스마트스토어·식봄은 가격변경도. 표준 정산식=스마트스토어형(2700·ceil), 수수료만 채널별(스마트스토어/캐시노트 6%·식봄 7%). **캐시노트 추가 완료(2026-06-11, ADR 0014)** — 골든 513/513 입력 일치(N·배송비 전건). 신규 축: `ship_fee_policy`(배송정책코드 조건부 배송비)·`_pid`(상품번호 숫자셀 정수정규화). 행사 차등수수료는 무시(소스 없음). **캐시노트 가격변경 완료(2026-06-11)** — '(캐시노트)양식' append(A=OFR·D=SKU 다운로드 Q/R `extra_cols` 보존, F=수정·L=Y·N=9999 고정, G=권장가·H=정가). 식봄 append 로직 `build_append_items` 헬퍼로 공용화. **⚠️ core 수정분 Reboot app 필요**. 미해결 — baseline↔product_master 조인 갭. **배민상회 추가 완료(2026-06-11, 모니터)** — 골든 394/394 입력 일치(수수료·정산가 전건). 신규 축: **상품별 수수료**(`commission_source="download"` — 다운로드 BU/100+0.03, 채널 단일값 아님)·listing CSV 스키마 유연화(extra_cols 자동 보존). **배민상회 가격변경도 완료(2026-06-11)** — '(배민)양식' append, J=변경판매가(권장가)·H=변경소비자가=무늬용 가짜(표준 FAKE_JEONG). 옵션번호/옵션명 extra_cols 보존. **무늬용 가짜정가=전 채널 표준 단일화**(권장가+20~30% 랜덤·100원, jeong_field 있으면 기본) — 식봄·배민도 적용(2026-06-11). **쿠팡 추가 완료(2026-06-11, 모니터+가격변경)** — 골든 1989/1989(정산가·N·판매가). 수수료 12% 단일·배송비 0·키=옵션ID. 가격변경은 **filter형 신설**(다운로드 자체가 조회+변경요청 컬럼형 → 원본 P/Q 기입, build_filter_price_xlsx). 5채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡) 전부 모니터+가격변경. **쿠팡 로켓그로스(바코드 E열) 모니터 제외 완료(2026-06-11)** — `exclude_row_if_col_filled`:5, parse 단계 행 제외(기존 listing은 '전체 교체' 재파싱 필요). **배민 가격변경 양식 외부링크 경고 수정(2026-06-11)** — 템플릿 고아 externalLinks 제거 + `_strip_external_links`(append/bulk/filter 전 빌더). 옵션번호 float `510609.0`→정수(`_pid` extra_cols·`_deflo` 라운드트립). **쿠팡 가격변경 filter 네이티브 zip 수술 완료(2026-06-11)** — openpyxl 저장이 inlineStr로 변질→쿠팡 업로드 거부 → `build_filter_price_xlsx`를 원본 네이티브 zip 수술로 교체(골든 바이트 일치). **쿠팡은 '전체 교체'로 raw 네이티브 유지 필수.** **⚠️ core 수정분 Reboot app 필요.** **쿠팡 raw inlineStr 오염 치유 + filter형 '신규만 추가' 비활성 가드 완료(2026-06-11)** — 저장 raw가 과거 '신규만 추가'로 inlineStr 오염→수술 출력도 inlineStr(업로드 거부) → raw 무손실 네이티브 역변환 커밋 + page 가드(price_form.mode=filter면 신규만추가 disabled). Reboot 불필요. **쿠팡 수술 출력 sharedStrings 정규화 완료(2026-06-11, 최종)** — 치유 후에도 실패 재현(앱이 캐시/stale 옛 오염 raw 사용) → `build_filter_price_xlsx`가 남긴 행을 항상 `t="s"`로 변환+sst 재구성(`_inline_cells_to_shared`). **raw가 inlineStr이든 native이든 출력 항상 네이티브** → 캐시/배포 무관 업로드 성공(엑셀 '값붙' 동치). 검증: 오염 raw 입력→출력 inlineStr 0·값 무손실. **⚠️ core 수정 → Reboot app 1회 필요.** **✅ Reboot+재생성 후 쿠팡 업로드 성공 사용자 확인(2026-06-11) — 가격변경 5채널 전부 완료·검증.** **올웨이즈(올팜) 추가 완료(2026-06-12, 모니터+가격변경)** — 6번째 채널. 판매가=팀구매가(K)·정가=개인구매가(J)·수수료10.5% 단일·배송비0·N=hapo(올팜ObjectId 748/748). 골든 입력 판매가/N 621/621·정산617/619. **가격변경=append('(올웨이즈)양식')** — K=권장가·J=FAKE_JEONG, extra_cols(카테고리·판매상태·옵션명/값·재고)+int_fields, 양식 end-to-end 검증. 페이지 무수정(mode append 자동). 미검증=올웨이즈 실업로드 inlineStr 허용. **⚠️ core 수정 → Reboot app 필요.** **6채널(스마트스토어·식봄·캐시노트·배민상회·쿠팡·올웨이즈) 모니터+가격변경. 알리(AliExpress) 모니터 추가 완료(2026-06-12)** — 7번째. **다중시트 export 자동정제(consolidate, 매크로 ALI상품매크로V2 흡수)** — 보이는 카테고리 시트만 통합·r2 라벨조회·숫자ID 필터, 별도 정제 업무 불요. 수수료9%·배송0·N=hapo(알리상품번호). 골든 입력 관리코드/상품명/판매가/N 전부 322/322. ⚠️ core+page 수정 → Reboot 필요. 알리 가격변경 미구현(AliExpress 다중시트 양식 별도). **ESM(G마켓) 모니터 추가 완료(2026-06-12, ADR 0015)** — 8번째. 17.5% 단일(골든 정산 가격×0.825 재현, O열 판매이용료 미사용)·키=A마스터상품번호·N=hapo(A·채널무관). G마켓+옥션 통합 다운로드(500상품 한도 다회배치)를 **F=='지마켓' 필터+A중복제거 parse 자동화**(신규 knob `include_row_if_col_value`·`dedup_key`, 수기 합치기 불필요)·`_num` 콤마 허용(배송비 '3,000'/'무료'). 골든 입력 판매가/배송비 1193/1193·정산액 1189/1193·base 1170/1187. consolidation 1193/1193. 골든 N=#REF! 대조불가. 가격변경 미구현(알리처럼). **다중파일 업로드(multi_file)** — 500상품 한도 배치를 한번에 올려 자동 병합(수기병합 불요). **가격변경(append) 추가(2026-06-12)** — '(ESM)양식'에 B=사이트상품번호(extra_cols 보존·모니터키 A와 다름)·C=권장가·A=순번(seq_col), 정가칸 없어 jeong 없음. esm_price_template.xlsx. 양식 30표본 전건 일치. **8채널 모니터/7채널 가격변경(알리만 가격변경 미구현).** ⚠️ core 수정 → Reboot. **ESM 실업로드 성공 사용자 확인(2026-06-12).** **8채널 모니터 / 6채널 가격변경. 다음: 알리·ESM 가격변경 or 추가 채널.** 상세 workflows/channel-margin-monitor.md.
- **기준마진율 편집(현재 마진율→기준) 추가 완료(2026-06-12, ADR 0016)** — 전 채널 공통. 모니터 표 선택→버튼 1개→**새 기준 인라인 편집(data_editor, 기본값=현재 마진율, 직접 수정)**·충돌은 후보표시+직접입력·0.1%p. (offset 라디오 폐기 2026-06-12) 그 채널 baseline_col 컬럼만 수정(타채널 보존). **baseline을 GitHub 라이브read(compute_listing override)로 바꿔 저장 즉시 반영**(재배포 불요). 미달 상품 목표 인정→미달 해제(검증: 미달 10→0, 전체 49→29). 향후 ②인라인 ③일괄. ⚠️ core+page → Reboot.
- **upload-monitor(업로드감시) 설계확정·미구현(ADR 0017, 2026-06-12)**: 박스재고 있는데 채널 미업로드 탐지 → 등록 인계. base 정체 collapse(resolve_code 재사용 `resolve_identity`, 키=**상품코드**), listing 8채널 공유(마진모니터 스냅샷), 재고=박스재고·우선순위=재고금액 desc, 품절 단일판정. MVP = L1매트릭스+L2갭+L4(스마트스토어·ESM 자동폼/6채널 CSV)+L6 건수KPI. 제외=L5 채널확장(11번가·셀러허브·자사몰·토마토)·추이·예상마진. 코어+페이지 운영 — 8채널 매트릭스·KPI·채널 체크박스+컬럼별 상태필터(AND)·채널별 업로드제외(skip) 등록/해제(전채널제외 숨김·해제=다시 업로드필요)·**이미지 포함 XLSX(대표A1/상세B1 실검사 6컬럼·jpg→png)**·**박스재고/재고금액 임계값 필터**·**다운로드 XLSX(코드 텍스트 서식)**. 이미지 egress 배포 확인 OK(사용자). **L4 핸드오프 = 후순위(사용자 2026-06-15: 일괄 업로드 가능 채널 프로세스 완비 후 재논의 — 미장착 채널 多, 지금 만들 단계 아님)** — (스마트스토어·ESM 입력폼 prefill: 관리코드·박스모드·합포장(product_attributes)·과세디폴트 + 이미지URL / 6채널 CSV). 상세 workflows/upload-monitor.md.
- (백로그) Phase 3 나머지 템플릿 이관 — 사용자 실물 파일 제공 대기.
- (백로그) 온누리 빈 G셀 회귀 fixture/pytest.

_갱신: 2026-06-12 (ESM(G마켓) 모니터+다중파일+가격변경(append), 8채널 모니터/7채널 가격변경. B=사이트상품번호·seq_col순번·jeong없음. core → Reboot 필요)_

_갱신: 2026-06-12 (기준마진율 편집 추가 — 현재 마진율→기준, 전 채널 공통, baseline 라이브read 즉시반영. ADR 0016. core+page → Reboot)_

_갱신: 2026-06-12 (기준마진율 새 기준 인라인 편집(data_editor) — offset 라디오 제거, 기본값=현재·직접 수정. page만 → Reboot)_

_갱신: 2026-06-12 (upload-monitor(업로드감시) 신규 워크플로우 설계확정·미구현 — base 정체 collapse·키=상품코드·재고금액 우선·L4 등록 인계. ADR 0017)_

_갱신: 2026-06-12 (intelligence-layer 신규 워크플로우 설계확정 — 이력엔진+두뇌, 데이터 카탈로그 9종, 정산진실=매출자료·택배=송장. 첫 브릭=수정로그 적재. ADR 0018)_

_갱신: 2026-06-15 (systemmap.json 신설 — 지도+로드맵 단일 진실원천. 스키마 계약·권한 경계(JSON=상태/로드맵/연결 정본·.md=디테일/서사)·갱신 트리거·검증3종. ADR 0019. 렌더러=outputs/system-map.html, 인앱 페이지 예정)_

_갱신: 2026-06-15 (intelligence-layer 첫 브릭 — 수정로그 가격이력 적재 완료. 2,567건(매입2009/매출558)·**1년 롤링(3년 소급 불가 정정)**·dedup키 중복0. work-automation-data:history/price_changes.parquet + core/intelligence/price_history.py(파서+dedup적재+역재생). 다음=역재생 앵커 확정. ADR 0018)_

_갱신: 2026-06-15 (intelligence-layer 역재생 결선 — 수정로그 '매입단가' 앵커=product_master 낱개[8] 확정(95.4%). current_purchase_price+as_of_value 실증 완료(as-of 매입가). 1a 완료, 다음=1b 상품관리 스냅샷. ADR 0018)_

_갱신: 2026-06-15 (intelligence-layer 1b 상품관리 재고 스냅샷 적립 완료 — 업로드 훅·stock_history.py·dedup 멱등·전이탐지. core→Reboot. 다음=두뇌① 마진 침식)_

_갱신: 2026-06-15 (두뇌① 마진 침식 v1 — 채널 baseline·최근3개월 매입인상∩미달·8채널 통합·권장가. 신규 8_마진침식.py+margin_erosion.py. intelligence-layer status→진행중. Reboot 필요)_

_갱신: 2026-06-15 (EasyAdmin 주문 적재 1차 — 2026 3~5월 25,821행·PII제거·송장그룹·발주일기준. core orders.py. 다음 Jan-Feb로 2026 완료. velocity→두뇌①정렬·③A/B·P2)_

_갱신: 2026-06-15 (EasyAdmin 주문 2026 적재 완료 — 1~5월 51,641행. 정확도 함정 기록(매출자료≠EasyAdmin, velocity 월/주). 다음 2025 백필)_

_갱신: 2026-06-15 (★세션 핸드오프 — EasyAdmin 주문 2026 적재(51,641행)+판매가 신뢰도 3중 검증 완료. 알리/식봄/올웨이즈 전부 해명·수수료 가정 정확. 재개점=velocity 활용 갈림길(두뇌①가중/P2/③A/B/2025백필). 보정=세트 판매가 백로그)_

_갱신: 2026-06-15 (velocity 갈림길 해소 — 사용자 확정 순서 P2 송장실배분(최우선)→2025 주문백필→두뇌③ A/B, velocity 가중 후순위. systemmap.json 정본 갱신)_

_갱신: 2026-06-15 (P2 송장 실배분 완료 — EA 송장그룹 박스배분÷매출낱개 강도 + 00-12 정합, 대시보드 온라인마진 실측 교체. core ship_alloc.py·⚠️Reboot. 단위=매출낱개≠EA판매단위. 다음=2025 백필)_

_갱신: 2026-06-15 (upload-monitor L4 등록 핸드오프 후순위 — 채널 일괄업로드 프로세스 완비 후 재논의. systemmap next→later)_

_갱신: 2026-06-15 (EasyAdmin 주문 2025 하반기 백필 — 7~12월 70,455행·발주일 기준 클린·PII0·멱등. <tr> 스트리밍 파싱(86MB·컨테이너). 누적 122K행. 다음=2025 상반기)_

_갱신: 2026-06-15 (EasyAdmin 주문 과거 백필 완료 — 통파일 .xlsx 2023-03~2025-06 276,777행·헤더명 매핑(Source.Name 시프트). 전 기간 2023-03~2026-05·398,873행. 2023 여름 갭. 다음=두뇌③ A/B)_

_갱신: 2026-06-15 (데이터현황 페이지 1단계 — 통합 데이터 관리, 시계열 누적 자료 적재 범위/갭 한눈에. core coverage.py(디렉토리목록만)+2_데이터현황.py+nav. 재고스냅샷=현황만, 매입/발주=예정. ⚠️Reboot. 다음=2단계 업로드)_

_갱신: 2026-06-15 (데이터현황 후속 — 가격이력 타임라인 포함(single 1파일 range read)·x축 YYYY-MM. 2단계 업로드=나중에 일괄(매입현황 등 적재 후) 결정. 다음=두뇌③)_

_갱신: 2026-06-15 (유형별매입현황 전기간 적재 — 통파일 72컬럼 헤더명 매핑·53파티션 2022-01~2026-05·65,999행·합계액=진실·PII0·멱등. core purchases.py(orders 동형). 거래처코드 2025+ 편중(리드타임 과거 위주)·2C/입고신호 전기간. 다음=두뇌③ A/B)_

_갱신: 2026-06-15 (로드맵 재배열 ADR 0020 — backbone 완성→신호결합. 두뇌① 강화(2C+velocity) next1·두뇌② 승격 next2·두뇌③ planned·상품360카드 신규. 착수=두뇌① 강화)_

_갱신: 2026-06-15 (두뇌① 강화 완료 — 3렌즈(이미침식/곧침식2C/실판매이상)+velocity 월손실액. margin_erosion.py+5함수·8_마진침식.py 3탭. ⚠️Reboot. 다음=두뇌②)_

_갱신: 2026-06-15 (두뇌① 탭D 당일 점검 — 당일 천년경영 output+송장출력+master 3파일로 당일 실현마진 이상치 즉시 탐지. 매출=실제기입단가(net)·택배=채널flat×실박스(송장)×물류량. core daily_margin.py·8_마진침식 4탭. 실파일0615 조인100%·택배정합diff0·이상28. ⚠️Reboot. 다음=두뇌②)_

_갱신: 2026-06-15 (탭D 정정 — 택배 실송장 단위 배분[채널 물류량 비례배분 과다계상 버그, 사용자 지적]·해소기 강화. 이상 28→9. ⚠️Reboot)_

_갱신: 2026-06-15 (두뇌② 재고 지능 v1 — 현재고(최종재고 낱개)÷소진율(매출 전채널)=소진예측일·매입 입고주기 리드타임 proxy로 재발주. 4구간(품절임박/곧재발주/충분/사장재고). 신규 stockout.py+9_재고지능.py. 매출 base 직조인(합성코드 한계 없음)·택배비/음수재고 처리. ⚠️Reboot. 다음=두뇌③ A/B)_

_갱신: 2026-06-16 (탭D 택배 배분 합포 2시나리오 정확화 — ① 250/355 H열 콤마 다품목 전체추출(둘째 품목 누락 버그) ② 175~200ml 30개입 수령자 그룹 ceil(팩/3) 물리합포(reference/hapo_175_190.csv 60종 관리코드). 거짓 역마진 해소. ⚠️core→Reboot. 다음=master+0616 이상치 before/after 사용자 확인 → 두뇌③)_
