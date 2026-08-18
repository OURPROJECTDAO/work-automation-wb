# coupang-register — 쿠팡 신규 상품 등록 (로컬 API 배치)

## 개요
쿠팡 마켓플레이스(판매자배송) 신규 상품을 **OPEN API로 배치 등록**. 2026-07-08 확립(파일럿 DOLE 1건→70건 배치 성공).

## 경로 결정 (왜 로컬 API인가)
- WING 엑셀 일괄등록이 막힌 상황에서 API 채택.
- **쿠팡 OPEN API는 IP 화이트리스트 필수** → Anthropic 클라우드 IP는 동적(호출마다 34.x 상이)이라 등록 불가 → **대화창에서 직접 호출 불가**.
- **해결=로컬 실행**(nadl 패턴). 사용자 PC 고정 공인IP를 WING(판매자정보>추가판매정보>OPEN API 키)에 등록 후, AI가 만든 스크립트를 `C:\claudeworkautolocal\coupang\`에서 실행.
- 참고: 엑셀 일괄등록본(셀러툴 xlsm)도 완성되어 있음(WING 일괄 막힘 해제 시 대안). 셀러툴 규칙은 하단 [부록].

## 인프라 (HMAC/엔드포인트/키)
- HOST=https://api-gateway.coupang.com
- **서명**: dt=UTC `%y%m%dT%H%M%SZ`; msg=dt+method+path+query(‘?’제외); sig=HMAC_SHA256(secret,msg).hexdigest(); 헤더 `Authorization: CEA algorithm=HmacSHA256, access-key={A}, signed-date={dt}, signature={sig}`. gzip 응답 decompress 필요.
- **상품생성**: POST `/v2/providers/seller_api/apis/api/v1/marketplace/seller-products` (※`apis`—`apps` 오타 시 400 "Provider id is not specified correctly"). 초당 10건 제한(sleep~0.15).
- **카테고리 메타**: GET `/v2/providers/seller_api/apis/api/v1/marketplace/meta/category-related-metas/display-category-codes/{code}`
- **출고지 조회**: GET `/v2/providers/marketplace_openapi/apis/api/v1/vendor/shipping-place/outbound` (v4 outboundShippingCenters는 410 retired).
- **반품지 조회**: GET `/v2/providers/openapi/apis/api/v4/vendors/{vendorId}/returnShippingCenters`. 주소는 응답 최상위 아님 → **`placeAddresses[0]`**(returnZipCode/returnAddress/returnAddressDetail/companyContactNumber).
- 키: 프로젝트 지식 `쿠팡api`(ACCESS_KEY/SECRET_KEY/VENDOR_ID=A00083972/VENDOR_USER_ID=td2684). 로컬은 같은 폴더 `쿠팡api`(.txt 허용). **KB·출력 노출 금지**.

## 고정 준비물 (태동유통 기준)
- 출고지 **23482844**(한진2025) · 반품지 **1002309412**(2025한진) · 택배사 **HANJIN**.
- 무료배송(deliveryChargeType FREE·deliveryCharge 0) · 초도배송비(deliveryChargeOnReturn) **5000** · 반품배송비(returnCharge) **5000**.

## 상품 규칙 (사용자 확정)
- **마진 10%** · **박스 단위** · **과세(taxType TAX)** · 재고 maximumBuyCount **9999** · 출고리드타임 **5** · 성인/병행/해외 N.
- **판매가** = ceil((박스매입가+2700)/((1−수수료/100)(1−0.10))/100)×100. 수수료=카테고리 판매대행수수료(대개 10.6).
- **상품명/옵션명 분리**(중요): 쿠팡 노출 상품명=정제명에서 **규격 제거**(예 "스팸 클래식"), 옵션명(itemName)=**규격**(예 "300g 20개"). 정제명 소스=listing_esm(관리코드)+goods-list 관리코드기입본. 규격 첫 위치(숫자+kg/g/ml/L) 기준 분리.
- **구조화옵션(attributes)**: 카테고리 메타 필수(MANDATORY)만. 개당중량(g) vs 개당용량(ml)은 group택1 → 규격단위로 결정(kg/g→중량, L/ml→용량). 수량="박스내품수+개". 값=숫자+단위 통째("3000g","6개").
- **고시(notices)**: 카테고리 메타 **`noticeCategories`**(필드명 주의, notices 아님)에서 유형 1개 선택(가공식품 우선)→항목 전부. content="상세설명 참조", 전화 항목만 010-6291-9345.
- **이미지**: images[].vendorPath에 gi.esmplus URL 직접(png 포함 OK). 상세=contents `{contentsType:TEXT, contentDetails:[{content:"<img src='B1URL' />", detailType:TEXT}]}`. 규칙 `https://gi.esmplus.com/td680708/{관리코드}/{관리코드}_{A1|B1}.{ext}`(확장자는 업로드감시_이미지 파일에 실검사값).
- 바코드 없음: barcode ""·emptyBarcode true·emptyBarcodeReason "상품확인불가_바코드없음".
- 브랜드=상품명 첫 토큰(자동). requested=False(임시저장)→WING 확인 후 승인요청.

## 카테고리 매핑
- 소스=참조표 `식품.xlsx`(카테고리 zip, data 시트 [코드]경로+수수료. 이건 등록템플릿 아닌 참조표). 상품명 키워드→카테고리 leaf 코드. 4862 카테고리라 AI 1차 매핑→사용자 검수(CSV).
- 확정 매핑 예: 과일통조림58569·기타농산물통조림73169(버섯/죽순)·콩통조림73168·꽁치58561·번데기59879·햄58564·가미참치58556·피클59849·퓨어올리브유73022·참기름58499·고추씨기름58501·굴소스72979·토마토소스59083·기타소스72986(데미그라스)·기타중화요리소스72983(두반장/쌍노두)·핫소스59866(캡사이신)·땅콩버터잼58751·일반꿀58900·유자차58869·양조간장58471·미림73015·기타식초58520·후추58524·분말조미료73027·농축액원액110731·녹차음료58781·기타탄산58768·과자쿠키59628(새우칩/메밀칩).
- 세제 등 비식품은 제외(카테고리 부적합).

## 스크립트 (로컬)
- `coupang_batch.py`: 배치 데이터 CSV 읽어 등록. 카테고리 메타캐시·build_attributes(필수·group택1)·build_notices(noticeCategories)·초당10건·requested=False·batch_result.csv 로깅. `python coupang_batch.py [N]`(N=소량 테스트).
- `coupang_batch_data.csv`: code/name(상품명)/itemName(옵션명)/category/optType/optValue/qty/price/A1/B1.
- 생성 파이프라인(AI): 업로드감시_이미지(관리코드·상품명·박스매입가·A1/B1 URL) + product_master(규격·박스내품) + 카테고리매핑 + 정제명(listing_esm/goods-list) → 배치 데이터 CSV.

## 절차 (세션)
1. 등록대상 확보(업로드감시_5채널_이미지: 쿠팡 '업로드필요' + A1/B1 URL).
2. 카테고리 매핑 CSV 생성→사용자 검수(비식품/애매 카테고리 확인).
3. 배치 데이터 CSV 생성(상품명/옵션명 분리·옵션·판매가·이미지).
4. 사용자 로컬 실행: `query`(출고지/반품지/메타 확인, 필요시)→`coupang_batch.py 3`(소량)→전체.
5. WING서 확인 후 승인요청. 실패건 batch_result.csv error로 보정.

## 함정
- 경로 `apis`≠`apps`. 출고지 v4 retired→marketplace_openapi. 반품지 주소=placeAddresses[0]. 고시 필드=noticeCategories(≠notices). IP 화이트리스트(로컬 필수). 대표이미지 JPG 권장이나 URL이면 png도 통과. 검색옵션은 필수 아니면 생략. `(택N)` 옵션은 실제 1개만.

## [부록] 엑셀 일괄등록(셀러툴 xlsm) — 대안
- 셀러툴 V4.x xlsm '2.식품' 탭 r5부터. 옵션유형=참조표 셀 `(택N) ` 접두만 제거 통째로(`\n[필수]\n[기본단위]` 포함)·값 단위포함·검색옵션 생략. 고시 c89=가공식품·값 "상세설명 참조". 이미지 URL 가능(가이드 9-1-1). 파일명 영문·1~4행 보존. openpyxl keep_vba 저장. (logs/2026-07-08-coupang-register-pilot 참조)

## ★ 선물세트 전용 규칙 (2026-08-13 확립)
- **한 상품에 1~박스내품 세트를 옵션으로** 묶는다(별도 상품 아님). 옵션 최대치 = **박스내품**
  (1박스 분량까지가 묶음배송 한 건). 기존 관행과 동일 — 예: 스팸12k호 1~4세트, NH2호 1~3세트.
- 판매자상품코드 = **관리코드**(PC 없음). itemName = `{N}세트`. 구매옵션 `수량` = `{N}개`.
- 카테고리 **59882** = 식품>가공/즉석식품>캔/통조림류>**통조림선물세트**. 고시 = 가공식품(실측 확인).
  ★ 카테고리 코드는 셀러툴 원본 `sellertool_upload.xlsm`의 **`hidden` 시트**에 `[코드] 경로` 형태로 있다
  (`data` 시트만 있는 파일에는 없음 — 외부링크로만 걸려 값이 안 딸려온다).
- **무료배송**(`deliveryChargeType FREE`) → 수량별 배송비 설정 불필요. 실택배 2,700원은 판매가에 흡수.
- ★ **등록 후 hapo_multiplier에 옵션ID 키로 N 등록 필수**(`n_source:"ref"`).
  N = **세트수 ÷ 박스내품**. 세트수==박스내품 옵션은 N=1이라 생략. 옵션ID는 `price_inventory_*.xlsx` 3열.
  미등록 시 마진 −169~−371%. (바코드 칸이 아님 — 바코드 폴백은 스마트스토어 전용)
- 배치 실적: **선물세트 신규 4종 15옵션(2026-08-13)** — 45-07-06 J호(1~3세트)·45-07-05 I호(1~4)·
  45-07-08 L-3호(1~5)·45-07-09 L-2호(1~3). 마진 5%·수수료 10.6% 가정. 전건 승인완료·판매중.
  ⚠️ cmm의 쿠팡 수수료는 **12%**라 실현 마진은 3.5~4.0%로 잡힌다(등록 시 가정 10.6%와 차이).
