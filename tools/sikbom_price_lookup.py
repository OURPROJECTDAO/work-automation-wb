#!/usr/bin/env python3
"""
식봄(foodspring) 경쟁가 조회 — 채팅 네이티브 헬퍼 (Claude 샌드박스에서 실행).
역공학 1회 완료분(GraphQL 엔드포인트+쿼리)을 박제. 매 세션 재탐색 불필요.

사용:
  python sikbom_price_lookup.py --keyword "진양 죽순 4호 400g 1개" [--cost 1700] [--our 2500]
  --keyword  검색어(필수). 우리 식봄 등재명 통짜로 줘도 됨 — 자동으로 일반화해 함께 검색.
  --cost     우리 매입가(낱개/박스, 식봄 정산마진 계산용·선택)
  --our      우리 현재 판매가(우리 마진 표시·선택)
  --extra    추가 검색어(쉼표 구분, 여러 개). 손으로 더 넓은/다른 표현 보태고 싶을 때.
  --exact    자동 일반화 끄기(준 검색어 그대로만 검색).
  --agg-comp 묶음배송(AggregateDelivery)도 경쟁사로 포함(기본=택배배송만).

★ 배송형태 규칙(경쟁사 판정 · 2026-06-29):
  vendor.delivery.__typename로 형태 구분 — ParcelDelivery=택배 / DirectDelivery=직배송 / AggregateDelivery=묶음.
  **경쟁최저 = 택배배송(ParcelDelivery)만.** 직배송 제외(사용자 규칙 — 직배송은 조건부 무료배송 등
  우리 실비택배 2,700과 경제구조가 달라 동일선상 비교 불가). 묶음도 기본 제외(--agg-comp로 포함 가능).
  표에 형태 컬럼 표시·제외행은 '✗제외' 표기·택배 경쟁최저보다 싼 비-택배 있으면 참고 안내.

★ 크롤링 규칙(검색 분절 방지·2026-06-29):
  식봄 검색은 ACCURACY 매칭이라 우리 통짜 등재명("진양 죽순 4호 400g 1개")으로 치면
  우리만 걸려 '경쟁없음'을 오판한다. 그래서 기본으로 검색어를 **일반화**해 같이 검색하고
  결과를 nid로 병합한다. 일반화 = 호수(4호)·낱개꼬리(1개/낱개)·괄호속성(상온/택배)을 떼고
  **브랜드+품목+규격(g/ml/kg/L)**은 보존(브랜드만 남기는 과일반화는 다른품목 오매칭이라 안 함).
  멀티팩(X24·24개입·*24개·box)은 보존(박스 listing이면 박스 경쟁이 잡혀야 함).

출력: 판매자별 (판매가 오름차순) 병합표 + (--cost 시) 최저가/우리가 기준 식봄 정산마진.
  · 규격 [..]에 멀티팩은 'x24' 식으로 표기 — 단캔/박스 구분용(AI가 동일규격만 비교).
  · 가격 비교 기준 = salePrice(판매가). 쿠폰/즉시할인가(−20%)는 마켓보로 부담이라 정산무관·미사용.
※ 같은 상품 판별/규격 매칭은 출력 보고 사람(AI)이 확정 — 스크립트는 후보만 제공.
※ 200 안 나오거나 빈 결과면 식봄이 쿼리/엔드포인트 바꾼 것 → 역공학 재실행 필요(workflows/sikbom-event-planning.md §크롤링).
"""
import sys, json, subprocess, urllib.parse, argparse, math, re

GQL_URL = "https://api.foodspring.co.kr/v2/graphql"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
COMM, SHIP_BUYER, REAL_SHIP, SF, FLOOR = 0.07, 3000, 2700, 0.967, 0.03
QUERY = r"""query SearchResultGoodsListPCPaginationQuery(
  $after: String = null
  $areaId: ID = null
  $first: Int = 80
  $input: GoodsSearchInput
  $isMobile: Boolean!
  $keyword: String!
) {
  ...SearchResultGoodsListPCFragment_2jQGSt
}

fragment BundlePurchaseMobileFragment on Goods {
  name
  nid
  vendor {
    nid
    name
    delivery {
      __typename
    }
    id
  }
  price {
    pricePerQuantity {
      quantity
      price
    }
  }
  goodsQuantity {
    minPerOrderQuantity {
      quantity
      activated
    }
  }
  deliveryFee {
    __typename
    ... on FreeDeliveryFee {
      __typename
      id
    }
    ... on ConditionalDeliveryFee {
      __typename
      condition
      id
    }
    ... on ArrivalDeliveryFee {
      id
    }
    ... on ChunkDeliveryFee {
      id
    }
    ... on PaidDeliveryFee {
      id
    }
    ... on QuantityDeliveryFee {
      id
    }
    ... on WeightVolumeDeliveryFee {
      id
    }
  }
  categoryNode {
    path
    id
  }
}

fragment BundlePurchasePCFragment on Goods {
  name
  nid
  vendor {
    nid
    name
    delivery {
      __typename
    }
    id
  }
  goodsQuantity {
    minPerOrderQuantity {
      activated
      quantity
    }
  }
  deliveryFee {
    __typename
    ... on FreeDeliveryFee {
      __typename
      id
    }
    ... on ConditionalDeliveryFee {
      __typename
      condition
      id
    }
    ... on ArrivalDeliveryFee {
      id
    }
    ... on ChunkDeliveryFee {
      id
    }
    ... on PaidDeliveryFee {
      id
    }
    ... on QuantityDeliveryFee {
      id
    }
    ... on WeightVolumeDeliveryFee {
      id
    }
  }
  price {
    pricePerQuantity {
      quantity
      price
    }
  }
  categoryNode {
    path
    id
  }
}

fragment DeliveryTagResFragment on Delivery {
  __isDelivery: __typename
  __typename
  ... on ParcelDelivery {
    __typename
  }
  ... on DirectDelivery {
    arrivalTag
  }
  ... on AggregateDelivery {
    arrivalTag
  }
}

fragment ItemCardCartControlResFragment on Goods {
  ...BundlePurchaseMobileFragment
  ...BundlePurchasePCFragment
  nid
  name
  goodsQuantity {
    minPerOrderQuantity {
      activated
      quantity
    }
    unitQuantity
  }
  price {
    pricePerQuantity {
      __typename
    }
    salePrice
  }
  vendor {
    name
    nid
    delivery {
      __typename
    }
    id
  }
  stock {
    __typename
    quantity
  }
  categoryNode {
    nid
    path
    id
  }
  isFreeDelivery
}

fragment ItemCardImageResFragment on Goods {
  ...SpecialPriceResFragment
  name
  images {
    primaryUrl
  }
}

fragment ItemCardQuantityCartButtonResFragment on Goods {
  ...useGoodsCountV2Fragment
  ...useGoodsNonPurchasableV2Fragment_1LTqib
  nid
  name
  cartCount
  vendor {
    nid
    name
    delivery {
      __typename
    }
    id
  }
  goodsQuantity {
    unitQuantity
    minPerOrderQuantity {
      activated
      quantity
    }
  }
  price {
    salePrice
  }
  categoryNode {
    path
    id
  }
  isFreeDelivery
}

fragment ItemCardResFragment_3ZwZC2 on Goods {
  ...useGoodsNonPurchasableV2Fragment_1LTqib
  ...SpecialPriceBadgeResFragment
  ...ItemCardImageResFragment
  ...ItemCardCartControlResFragment
  ...ItemCardQuantityCartButtonResFragment
  ...ItemCardRollingTagResFragment_3ZwZC2
  nid
  name
  vendor {
    nid
    name
    delivery {
      ...DeliveryTagResFragment
      __typename
      ... on DirectDelivery {
        arrivalTag
      }
      ... on AggregateDelivery {
        arrivalTag
      }
    }
    id
  }
  price {
    originalPrice
    salePrice
    appliedCoupon {
      price
    }
    discountRate
    pricePerQuantity {
      __typename
    }
  }
  goodsQuantity {
    minPerOrderQuantity {
      activated
      quantity
    }
    unitQuantity
  }
  categoryNode {
    path
    id
  }
  standard
  unit
  isFreeDelivery
}

fragment ItemCardRollingTagResFragment_3ZwZC2 on Goods {
  tag(type: CATEGORY) {
    __typename
    ... on CategoryGoodsTag {
      __typename
      text
      emphasis
    }
  }
  simpleReview {
    __typename
    ... on SimpleReviewRepurchase {
      quantity
    }
  }
}

fragment SearchResultCategoryFilterResFragment on SearchGoodsCategoryNode {
  id
  children {
    id
    name
    depth
    parentId
    totalCount
    children {
      id
      name
      depth
      parentId
      totalCount
      children {
        id
        name
        depth
        parentId
        totalCount
        children {
          id
          name
          depth
          parentId
          totalCount
        }
      }
    }
  }
}

fragment SearchResultCategoryFilterSectionPCFragment on GoodsFilterOption {
  categoryNode {
    children {
      __typename
      id
    }
    ...SearchResultCategoryFilterResFragment
    id
  }
}

fragment SearchResultDeliveryFilterSectionPCFragment on GoodsFilterOption {
  delivery
  ...SearchResultDeliveryFilterUniFragment
}

fragment SearchResultDeliveryFilterUniFragment on GoodsFilterOption {
  delivery
}

fragment SearchResultFilterPCFragment on GoodsFilterOption {
  delivery
  categoryNode {
    children {
      __typename
      id
    }
    id
  }
  vendor {
    inCart {
      totalCount
    }
    purchased {
      totalCount
    }
    favorites {
      totalCount
    }
  }
  origin {
    __typename
  }
  weight
  ...SearchResultDeliveryFilterSectionPCFragment
  ...SearchResultSellerFilterSectionPCFragment
  ...SearchResultPriceFilterSectionPCFragment
  ...SearchResultCategoryFilterSectionPCFragment
  ...SearchResultOriginFilterSectionPCFragment
  ...SearchResultWeightFilterSectionPCFragment
}

fragment SearchResultGoodsListPCFragment_2jQGSt on Query {
  pcFilterOption: goodsFilterOption(keyword: $keyword, areaId: $areaId) {
    ...SearchResultFilterPCFragment
    ...SearchResultSelectedChipListPCFragment
  }
  pcGoodsList: goodsSearch(areaId: $areaId, first: $first, after: $after, input: $input) {
    totalCount
    edges {
      node {
        ...ItemCardResFragment_3ZwZC2 @skip(if: $isMobile)
        id
        nid
        __typename
      }
      cursor
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

fragment SearchResultOriginFilterResFragment on GoodsFilterOption {
  origin {
    __typename
    value
    count
  }
}

fragment SearchResultOriginFilterSectionPCFragment on GoodsFilterOption {
  ...SearchResultOriginFilterResFragment
  origin {
    __typename
  }
}

fragment SearchResultPriceFilterSectionPCFragment on GoodsFilterOption {
  priceRange {
    min
    max
  }
}

fragment SearchResultSelectedChipListPCFragment on GoodsFilterOption {
  categoryNode {
    id
    name
    depth
    children {
      id
      name
      depth
      children {
        id
        name
        depth
        children {
          id
          name
          depth
          children {
            id
            name
            depth
          }
        }
      }
    }
  }
}

fragment SearchResultSellerFilterSectionPCFragment on GoodsFilterOption {
  ...SearchResultSellerFilterUniFragment
  vendor {
    inCart {
      totalCount
    }
    purchased {
      totalCount
    }
    favorites {
      totalCount
    }
  }
}

fragment SearchResultSellerFilterUniFragment on GoodsFilterOption {
  vendor {
    inCart {
      totalCount
      seller {
        id
        name
        searchCount
      }
    }
    purchased {
      totalCount
      seller {
        id
        name
        searchCount
      }
    }
    favorites {
      totalCount
      seller {
        id
        name
        searchCount
      }
    }
  }
}

fragment SearchResultWeightFilterResFragment on GoodsFilterOption {
  weight
}

fragment SearchResultWeightFilterSectionPCFragment on GoodsFilterOption {
  weight
  ...SearchResultWeightFilterResFragment
}

fragment SpecialPriceBadgeResFragment on Goods {
  gfoCode
}

fragment SpecialPriceResFragment on Goods {
  gfoCode
}

fragment useGoodsCountV2Fragment on Goods {
  nid
  goodsQuantity {
    minPerOrderQuantity {
      activated
      quantity
    }
    maxPerOrderQuantity {
      activated
      quantity
    }
    maxDayQuantity {
      activated
      quantity
    }
    maxPerPeriodQuantity {
      activated
      period {
        start
        end
      }
      quantity
      purchased
    }
    unitQuantity
  }
  stock {
    assignedQuantity
    quantity
  }
  todayPurchasedCount
  id
}

fragment useGoodsNonPurchasableV2Fragment_1LTqib on Goods {
  id
  reason_CARD: nonPurchasableReason {
    __typename
    ... on GoodsOutOfStockReason {
      __typename
      id
    }
    ... on GoodsStockNotEnoughReason {
      __typename
      id
    }
    ... on GoodsBlockedReason {
      __typename
      id
    }
    ... on SaleInactiveReason {
      __typename
      id
    }
    ... on GoodsByMinorsReason {
      id
    }
    ... on GoodsDeliveryFeeNotCalculableReason {
      id
    }
    ... on GoodsNonServiceableAreaReason {
      id
    }
    ... on GoodsQuantityAboveDailyMaximumReason {
      id
    }
    ... on GoodsQuantityAboveMaximumReason {
      id
    }
    ... on GoodsQuantityAbovePeriodMaximumReason {
      id
    }
    ... on GoodsQuantityBelowMinimumReason {
      id
    }
    ... on GoodsQuantityConstraintLimitReason {
      id
    }
    ... on GoodsQuantityNotDivisibleUnitQuantityReason {
      id
    }
  }
}
"""

def _curl(args):
    return subprocess.run(args, capture_output=True, text=True, timeout=40).stdout

def session_cookie(jar="fs_cj.txt"):
    _curl(["curl","-s","-m","20","-A",UA,"-c",jar,"https://www.foodspring.co.kr/","-o","/dev/null"])
    return jar

def crawl(keyword, jar):
    payload={"query":QUERY,"variables":{"keyword":keyword,"isMobile":False,
             "input":{"keyword":keyword,"sort":"ACCURACY_DESC"},"first":80,"after":None,"areaId":None}}
    open("_fs_p.json","w",encoding="utf-8").write(json.dumps(payload,ensure_ascii=False))
    ref="https://www.foodspring.co.kr/search/all?key="+urllib.parse.quote(keyword)
    out=_curl(["curl","-s","-m","30","-A",UA,"-b",jar,"-X","POST",GQL_URL,
        "-H","Content-Type: application/json","-H","Origin: https://www.foodspring.co.kr",
        "-H","Referer: "+ref,"-H","X-Device-Type: pc","-H","X-Client-Environment: production",
        "--data","@_fs_p.json"])
    try: d=json.loads(out)
    except Exception: return None
    if "errors" in d and not d.get("data"): return d
    def walk(o):
        if isinstance(o,dict):
            if o.get("__typename")=="Goods": yield o
            for v in o.values(): yield from walk(v)
        elif isinstance(o,list):
            for v in o: yield from walk(v)
    seen={}
    for g in walk(d): seen[g.get("nid")]=g
    res=[]
    for g in seen.values():
        pr=g.get("price") or {}
        df=g.get("deliveryFee") or {}
        ven=g.get("vendor") or {}
        vdeliv=(ven.get("delivery") or {}).get("__typename","")  # 배송형태(ParcelDelivery=택배/DirectDelivery=직배송/AggregateDelivery=묶음)
        res.append(dict(name=g.get("name",""), vendor=ven.get("name",""),
            sale=pr.get("salePrice"), orig=pr.get("originalPrice"),
            coupon=(pr.get("appliedCoupon") or {}).get("price"),
            stock=(g.get("stock") or {}).get("quantity"),
            deliv=df.get("__typename",""), cond=df.get("condition"), vdeliv=vdeliv))
    return res

def margin(price, cost):
    net=price*(1-COMM)+SHIP_BUYER*SF
    profit=net-cost-REAL_SHIP
    return net, profit, (profit/net if net else 0)

def floor_price(cost, M):
    return math.ceil(((cost+REAL_SHIP)/(1-M)-SHIP_BUYER*SF)/(1-COMM)/100)*100

def spec_hint(name):
    # 멀티팩 표기(X24·*24·24개입·24입)를 'x24'로 먼저 채집 — 단캔/박스 구분용
    packs=re.findall(r"(?:[xX*]\s*(\d+)|(\d+)\s*개입|(\d+)\s*입)", name)
    pk=[next(t for t in tup if t) for tup in packs]
    g=re.findall(r"(\d+(?:\.\d+)?)\s*(kg|g|ml|l)", name, re.I)
    parts=[f"{a}{b}" for a,b in g]
    parts+= [f"x{p}" for p in pk]
    return " ".join(parts)

_ATTR=re.compile(r"^(상온|실온|냉장|냉동|택배|택배배송|직배송|무료배송|대용량|업소용|벌크|낱개|개당|ea)$", re.I)
def _paren_sub(mo):
    inner=mo.group(1).strip()
    toks=[t for t in re.split(r"[\s,/]+", inner) if t]
    if toks and all(_ATTR.match(t) for t in toks):   # 괄호 안이 배송/보관/마케팅 속성뿐 → 제거
        return " "
    return " "+inner+" "                               # 브랜드/규격 등이 들었으면 언랩(괄호만 제거)

def normalize_keyword(raw):
    """우리 통짜 등재명 → 일반화 검색어. 호수·낱개꼬리·괄호속성만 제거, 코어(브랜드+품목+규격)·멀티팩 보존."""
    s=raw
    s=re.sub(r"[\(\[]([^\)\]]*)[\)\]]", _paren_sub, s)  # (상온)(택배)=제거 / (진양 400g)=언랩 보존
    s=re.sub(r"\d+\s*호"," ",s)                     # 캔 호수(4호 등) — 판매자 전용 표기·검색 분절
    s=re.sub(r"(?<![xX*\d])\b1\s*개\b"," ",s)        # 단독 '1개'(낱개 의미) 제거 — 멀티팩 X24/24개는 보존
    s=re.sub(r"낱\s*개"," ",s)
    s=re.sub(r"\s+"," ",s).strip()
    return s

def crawl_merge(keywords, jar):
    """여러 검색어를 각각 크롤해 nid로 병합(누락 방지). 반환 (rows, errinfo)."""
    merged={}; used=[]; err=None
    for kw in keywords:
        r=crawl(kw, jar)
        if r is None: err=err or "parse"; continue
        if isinstance(r,dict): err=err or "gql"; continue
        used.append((kw,len(r)))
        for row in r:
            k=(row["vendor"], row["name"], row["sale"])  # nid 동치 키(판매자+상품명+가격)
            merged[k]=row
    return list(merged.values()), used, err

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--cost", type=float, default=None)
    ap.add_argument("--our", type=float, default=None)
    ap.add_argument("--extra", default=None, help="추가 검색어(쉼표 구분)")
    ap.add_argument("--exact", action="store_true", help="자동 일반화 끄기")
    ap.add_argument("--agg-comp", dest="agg_comp", action="store_true", help="묶음배송도 경쟁사로 포함(기본=택배만)")
    a=ap.parse_args()
    # 검색어 집합 구성: 준 검색어 + (자동)일반화 + (수동)extra
    keywords=[a.keyword]
    if not a.exact:
        nk=normalize_keyword(a.keyword)
        if nk and nk!=a.keyword: keywords.append(nk)
    if a.extra:
        for e in a.extra.split(","):
            e=e.strip()
            if e and e not in keywords: keywords.append(e)
    jar=session_cookie()
    res, used, err = crawl_merge(keywords, jar)
    if not res:
        if err=="parse":
            print("[ERR] 응답 파싱 실패 — 엔드포인트/쿼리 변경 가능. 역공학 재실행 필요."); sys.exit(2)
        if err=="gql":
            print("[ERR] GraphQL 에러 — 역공학 재실행 필요."); sys.exit(2)
        print(f'검색어 {keywords} 결과 0건.'); return
    dmap={"FreeDeliveryFee":"무료","ConditionalDeliveryFee":"조건무료","PaidDeliveryFee":"유료",
          "QuantityDeliveryFee":"수량별","ArrivalDeliveryFee":"착불","ChunkDeliveryFee":"묶음"}
    fmap={"ParcelDelivery":"택배","DirectDelivery":"직배송","AggregateDelivery":"묶음","":"?"}
    def is_comp(r):
        # 경쟁사 = 택배배송(ParcelDelivery)만. 직배송 제외(사용자 규칙). 묶음은 --agg-comp 줄 때만 포함.
        f=r.get("vdeliv","")
        if "태동" in r["vendor"]: return False
        if f=="ParcelDelivery": return True
        if f=="AggregateDelivery" and a.agg_comp: return True
        return False
    rows=sorted(res, key=lambda x:x["sale"] if x["sale"] else 9e9)
    kwdesc=" + ".join(f'"{k}"({n})' for k,n in used)
    print(f'=== 식봄 검색 {kwdesc} → 병합 {len(rows)}건 (판매가 오름차순) ===')
    print(f'경쟁사 = 택배배송만 (직배송{"·묶음" if not a.agg_comp else ""} 제외{"·묶음 포함" if a.agg_comp else ""})')
    print(f'{"판매가":>8} {"정가":>7} {"재고":>8} {"형태":<4} {"배송비":<6} | {"판매자":<20} | 상품명[규격]')
    print("-"*108)
    for r in rows:
        sp=f'{int(r["sale"]):,}' if r["sale"] else "NA"
        op=f'{int(r["orig"]):,}' if r["orig"] else "-"
        st=r["stock"]; st=f'{int(st):,}' if isinstance(st,(int,float)) else "?"
        dv=dmap.get(r["deliv"],r["deliv"])
        if r["deliv"]=="ConditionalDeliveryFee" and r["cond"]: dv=f'{int(r["cond"]/10000)}만↑'
        fm=fmap.get(r.get("vdeliv",""),r.get("vdeliv",""))
        excl="" if (is_comp(r) or "태동" in r["vendor"]) else " ✗제외"  # 경쟁최저서 빠지는 행 표시
        hint=spec_hint(r["name"])
        print(f'{sp:>8} {op:>7} {st:>8} {fm:<4} {dv:<6} | {r["vendor"][:20]:<20} | {r["name"][:38]} [{hint}]{excl}')
    # 경쟁최저 = 택배배송만
    comp=[r for r in rows if r["sale"] and is_comp(r)]
    low=comp[0] if comp else None
    # 직배송/묶음 중 택배 경쟁최저보다 싼 게 있으면 참고 안내(규칙상 제외했음을 명시)
    excluded_cheaper=[r for r in rows if r["sale"] and "태동" not in r["vendor"] and not is_comp(r)
                      and (low is None or r["sale"]<low["sale"])]
    if a.cost is not None:
        print("\n--- 식봄 정산마진 (매입가 {:,}) ---".format(int(a.cost)))
        if a.our:
            n,p,m=margin(a.our, a.cost)
            print(f'  우리 현재가 {int(a.our):,} → 마진 {m*100:.1f}% (이익 {int(p):,})')
        if low:
            n,p,m=margin(low["sale"], a.cost)
            tag="✅3%이상" if m>=FLOOR else "⚠️3%미달"
            print(f'  경쟁최저(택배) {int(low["sale"]):,} ({low["vendor"]}) → 매칭시 마진 {m*100:.1f}% {tag}')
        else:
            print('  경쟁최저(택배) 없음 — 택배배송 경쟁사 없음(직배송/묶음만 존재하거나 우리 단독).')
        print(f'  3%하한가 {floor_price(a.cost,FLOOR):,} · 손익분기 {floor_price(a.cost,0):,}')
    elif low:
        print(f'\n경쟁최저(택배): {int(low["sale"]):,} ({low["vendor"]}) — 매입가(--cost) 주면 마진까지 계산')
    else:
        print('\n경쟁최저(택배) 없음 — 택배배송 경쟁사 없음.')
    if excluded_cheaper:
        e=excluded_cheaper[0]
        print(f'  ※ 더 싼 비-택배 존재(규칙상 제외): {int(e["sale"]):,} ({e["vendor"]}/{fmap.get(e.get("vdeliv",""),"?")}) '
              f'— 묶음도 경쟁으로 보려면 --agg-comp')

if __name__=="__main__":
    main()
