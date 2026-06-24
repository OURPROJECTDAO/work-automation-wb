#!/usr/bin/env python3
"""
식봄(foodspring) 경쟁가 조회 — 채팅 네이티브 헬퍼 (Claude 샌드박스에서 실행).
역공학 1회 완료분(GraphQL 엔드포인트+쿼리)을 박제. 매 세션 재탐색 불필요.

사용:
  python sikbom_price_lookup.py --keyword "명가꽈배기" [--cost 4200] [--our 5000]
  --keyword  검색어(필수)
  --cost     우리 매입가(낱개/박스, 식봄 정산마진 계산용·선택)
  --our      우리 현재 판매가(우리 마진 표시·선택)

출력: 판매자별 (판매가 오름차순) 표 + (--cost 시) 최저가/우리가 기준 식봄 정산마진.
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
        res.append(dict(name=g.get("name",""), vendor=(g.get("vendor") or {}).get("name",""),
            sale=pr.get("salePrice"), orig=pr.get("originalPrice"),
            coupon=(pr.get("appliedCoupon") or {}).get("price"),
            stock=(g.get("stock") or {}).get("quantity"),
            deliv=df.get("__typename",""), cond=df.get("condition")))
    return res

def margin(price, cost):
    net=price*(1-COMM)+SHIP_BUYER*SF
    profit=net-cost-REAL_SHIP
    return net, profit, (profit/net if net else 0)

def floor_price(cost, M):
    return math.ceil(((cost+REAL_SHIP)/(1-M)-SHIP_BUYER*SF)/(1-COMM)/100)*100

def spec_hint(name):
    g=re.findall(r"(\d+(?:\.\d+)?)\s*(kg|g|ml|l|개|입|ea)", name, re.I)
    return " ".join(f"{a}{b}" for a,b in g) if g else ""

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--keyword", required=True)
    ap.add_argument("--cost", type=float, default=None)
    ap.add_argument("--our", type=float, default=None)
    a=ap.parse_args()
    jar=session_cookie()
    res=crawl(a.keyword, jar)
    if res is None:
        print("[ERR] 응답 파싱 실패 — 엔드포인트/쿼리 변경 가능. 역공학 재실행 필요."); sys.exit(2)
    if isinstance(res,dict):
        print("[ERR] GraphQL 에러:", json.dumps(res.get("errors"),ensure_ascii=False)[:300]); sys.exit(2)
    if not res:
        print(f'"{a.keyword}" 검색결과 0건.'); return
    dmap={"FreeDeliveryFee":"무료","ConditionalDeliveryFee":"조건무료","PaidDeliveryFee":"유료",
          "QuantityDeliveryFee":"수량별","ArrivalDeliveryFee":"착불","ChunkDeliveryFee":"묶음"}
    rows=sorted(res, key=lambda x:x["sale"] if x["sale"] else 9e9)
    print(f'=== 식봄 "{a.keyword}" {len(rows)}건 (판매가 오름차순) ===')
    print(f'{"판매가":>8} {"정가":>7} {"재고":>8} {"배송":<6} | {"판매자":<20} | 상품명[규격]')
    print("-"*104)
    for r in rows:
        sp=f'{int(r["sale"]):,}' if r["sale"] else "NA"
        op=f'{int(r["orig"]):,}' if r["orig"] else "-"
        st=r["stock"]; st=f'{int(st):,}' if isinstance(st,(int,float)) else "?"
        dv=dmap.get(r["deliv"],r["deliv"])
        if r["deliv"]=="ConditionalDeliveryFee" and r["cond"]: dv=f'{int(r["cond"]/10000)}만↑'
        hint=spec_hint(r["name"])
        print(f'{sp:>8} {op:>7} {st:>8} {dv:<6} | {r["vendor"][:20]:<20} | {r["name"][:40]} [{hint}]')
    # 최저(우리 제외 추정: 이름에 태동/우리 키워드 없으면 경쟁)
    comp=[r for r in rows if r["sale"] and "태동" not in r["vendor"]]
    low=comp[0] if comp else None
    if a.cost is not None:
        print("\n--- 식봄 정산마진 (매입가 {:,}) ---".format(int(a.cost)))
        if a.our:
            n,p,m=margin(a.our, a.cost)
            print(f'  우리 현재가 {int(a.our):,} → 마진 {m*100:.1f}% (이익 {int(p):,})')
        if low:
            n,p,m=margin(low["sale"], a.cost)
            tag="✅3%이상" if m>=FLOOR else "⚠️3%미달"
            print(f'  경쟁최저 {int(low["sale"]):,} ({low["vendor"]}) → 매칭시 마진 {m*100:.1f}% {tag}')
        print(f'  3%하한가 {floor_price(a.cost,FLOOR):,} · 손익분기 {floor_price(a.cost,0):,}')
    elif low:
        print(f'\n경쟁최저: {int(low["sale"]):,} ({low["vendor"]}) — 매입가(--cost) 주면 마진까지 계산')

if __name__=="__main__":
    main()
