# 신규 PC낱개 일괄 등록 (스마트스토어 갭 기준 3개 reference 채움)

## 무엇 / 왜
- 신규 상품이 매출에 잡힐 때마다 낱개처리목록·규격파일·천년경영 소분목록에 PC낱개 코드를
  하나씩 등록하던 수작업을, **스마트스토어 listing 기준으로 미등록분을 한 번에** 채움.
- 사용자 요청: 식품/음료 분류(logistics_classification)는 본인이 함. **PC코드만** 3개 파일에 추가.
- ★가장 중요 = 천년경영(sub_list). 소분목록 누락 시 낱개가 전체(박스) 시트로 새어 ERP에
  박스 매출로 오등록됨. **PC코드 낱개개수는 반드시 1**(사용자 재확인).

## 재사용 레시피 (다음에 또 "한 번에" 할 때)
1. app repo reference/ 에서 unit_list.csv·sub_list.csv·spec_master.csv·listing_smartstore.csv·
   product_master.csv 를 raw로 받는다.
2. listing_smartstore 의 `코드`(col1) 중 `PC` 접두 코드 집합 = 현재 스토어 PC낱개 전체.
3. 각 파일의 기존 PC행과 대조 → **파일별 누락분**을 따로 계산(부분 등록 흔함 — 빠진 파일에만 넣음).
4. 각 PC코드 해소: `상품코드 = PC접두 제거 후 leading-zero strip` → product_master 에서 매칭.
   - 원코드 = product_master[4] 관리코드
   - 박스내품 = product_master[7]
   - 규격 = product_master[6] (박스규격)
5. 파일별 신규 행 형식(기존 PC행과 동일):
   - **unit_list**: `{PC코드},,,PC,{1/박스내품},{원코드}`  (상품명·박스내품칸 공백)
   - **sub_list** : `{PC코드},1,{원코드},낱개1개`             (낱개개수=1 고정)
   - **spec_master**: `{PC코드},,{PC규격}`
6. PC규격 파생(박스규격→낱개규격):
   - `(N입*...)` → `1입`  (예 (12입*210g)→1입)
   - 그 외: **최상위(괄호 depth0) 마지막 `*` 뒤를 `1`로** (130g*48→130g*1, (140+20)*4→(140+20)*1,
     200g*(10입*3)→200g*1). 전체가 `(...*N)`로 감싸였으면 겉괄호 벗기고 처리 ((240g*6)→240g*1).
   - 박스규격 공백이면 상품명에서 용량 유추(플래그) — 이번 PC005814(루글리오 포마스 5L)=`5L*1` 사용자 확인.
7. 커밋 전 검증(ERP 안전): sub_list 추가분 전건 낱개개수=1 · 원코드가 product_master 관리코드로
   실재(박스데이터 유무) · 원코드가 unit_list와 100% 정합. 커밋 후 재fetch 재대조.
8. 파일 3개 UTF-8-sig(BOM)·LF·trailing newline — append 시 BOM 보존(앞) + `\n` 종료.

## 변경 (app repo work-automation-app)
- reference/unit_list.csv  +17행 (커밋 2eb7ec85)
- reference/sub_list.csv   +16행 (커밋 0b51b498)
- reference/spec_master.csv +20행 (커밋 71dfd01f)
- 신규 PC코드 20건: PC004898/005071/005128/005246/005321/005632/005696/005699/005738/
  005812/005813/005814/005830/005832/005875/005899/005900/005902/005959/005960.
  (일부는 부분 등록돼 있어 빠진 파일에만 추가 — unit 17·sub 16·spec 20)

## 검증
- product_master 미해소 0건(전건 상품코드→관리코드 해소).
- sub_list 추가 16건: 낱개개수 전건 1 · 원코드 전건 PM 관리코드 실재+박스데이터 有 · unit_list 원코드 100% 일치.
- 기존 sub_list PC 167건도 낱개개수≠1 = 0건(불변식 성립).
- 커밋 후 재fetch: 추가분 20건 전건 정상 반영·값 일치, 내가 만든 중복 0.

## 다음 / 상태
- 완료. 앱 자동 재배포로 반영(reference라 Reboot 불필요·cmm/logistics 캐시 후 반영).
- ★관찰(기존 데이터 중복, 내가 만든 것 아님·전부 무해): sub_list PC004898 ×2(낱개개수·원코드
  동일, 구분칸만 공백 차이 — 첫출현 우선이라 ERP 무해) / unit_list PC005548·005201·005237 완전동일행 /
  spec_master PC004850·005201·005723·005237 완전동일행. **정리하려면 별건 승인 필요**(행 삭제라 미실행).
- 식품/음료 분류(logistics_classification)는 사용자 몫 — 미변경.
