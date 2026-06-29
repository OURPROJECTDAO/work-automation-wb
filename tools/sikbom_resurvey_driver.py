"""식봄 신규등록 재조사 드라이버 — 배치별 크롤 결과를 누적 CSV에 적립."""
import sys, json, csv, os, importlib.util, math
spec=importlib.util.spec_from_file_location('sk','sikbom_price_lookup.py')
sk=importlib.util.module_from_spec(spec); spec.loader.exec_module(sk)

RESULTS="resurvey_2026-06-29.csv"
FIELDS=["no","gubun","sno","mcode","pcode","name","spec","N","cost","cur_sheet",
        "our_live","comp_low","comp_seller","comp_form","comp_match_margin","our_live_margin",
        "floor3","verdict","newtag","propose","note","n_taekbae_comp"]

import re as _re
_PROMO=_re.compile(r"행사품목|행사가|초특가|타임특가|한정수량|즉시배송|기획전")
def _is_promo(r): return bool(_PROMO.search(str(r.get("name",""))))

def run_item(it, jar):
    name=str(it["name"]); cost=float(it["cost"])
    kws=[name]; nk=sk.normalize_keyword(name)
    if nk and nk!=name: kws.append(nk)
    rows,used,err=sk.crawl_merge(kws, jar)
    rows=[r for r in rows if r.get("sale")]
    fmap={"ParcelDelivery":"택배","DirectDelivery":"직배송","AggregateDelivery":"묶음"}
    # 우리 live가
    ours=[r for r in rows if "태동" in r["vendor"]]
    our_live=min((r["sale"] for r in ours), default=None)
    # 택배 경쟁
    comp_all=[r for r in rows if "태동" not in r["vendor"] and r.get("vdeliv")=="ParcelDelivery"]
    # 음료(박스 등재)는 낱개 리스팅 오염 제거 — 박스 가격대 필터(우리가×0.5 이상). 7차 학습.
    if str(it.get("gubun"))=="음료" and our_live:
        comp_all=[r for r in comp_all if r["sale"]>=our_live*0.5]
    # 행사품목/초특가 제외(사용자 규칙 — 일시 행사가는 따라붙지 않음)
    comp=[r for r in comp_all if not _is_promo(r)]
    comp=sorted(comp, key=lambda x:x["sale"])
    promo_cheaper=[r for r in comp_all if _is_promo(r) and our_live and r["sale"]<our_live]
    promo_note=(f' [행사제외: {promo_cheaper[0]["vendor"]} {int(promo_cheaper[0]["sale"])}]' if promo_cheaper else "")
    low=comp[0] if comp else None
    def mg(p): 
        net=p*(1-sk.COMM)+sk.SHIP_BUYER*sk.SF; return (net-cost-sk.REAL_SHIP)/net if net else 0
    floor3=sk.floor_price(cost, sk.FLOOR)
    rec=dict(no=it["no"],gubun=it["gubun"],sno=it["sno"],mcode=it["mcode"],pcode=it["pcode"],
        name=name,spec=it["spec"],N=it["N"],cost=int(cost),cur_sheet=it["cur"],
        our_live=our_live, comp_low=(low["sale"] if low else ""),
        comp_seller=(low["vendor"] if low else ""), comp_form=("택배" if low else ""),
        comp_match_margin=(round(mg(low["sale"])*100,1) if low else ""),
        our_live_margin=(round(mg(our_live)*100,1) if our_live else ""),
        floor3=floor3, n_taekbae_comp=len(comp))
    # 판정
    if our_live is None:
        rec["verdict"]="우리등재없음"; rec["newtag"]="확인필요"; rec["propose"]=""; rec["note"]="크롤에 우리 행 없음"
    elif low is None:
        rec["verdict"]="우리단독(택배경쟁없음)"; rec["newtag"]="우리 최저/택배경쟁없음"; rec["propose"]=""; rec["note"]=""
    elif our_live <= low["sale"]:
        rec["verdict"]="우리최저"; rec["newtag"]=("단독최저" if our_live<low["sale"] else "공동최저")
        rec["propose"]=""; rec["note"]=f'차순위 {low["vendor"]} {int(low["sale"])}'
    else:
        # 경쟁이 더 쌈. 경쟁−100 단독최저가 3%하한 이상이면 '인하', 아니면 '결정'(못 맞춤)
        under=int(low["sale"])-100
        if under>=floor3:
            rec["verdict"]="인하"; rec["newtag"]="경쟁더쌈→인하"; rec["propose"]=under
            rec["note"]=f'경쟁최저 {low["vendor"]} {int(low["sale"])} < 우리 {int(our_live)} → 단독최저 {under}(마진 {round(mg(under)*100,1)}%)'
        else:
            rec["verdict"]="결정(3%하한>경쟁)"; rec["newtag"]="경쟁더쌈·매칭불가"; rec["propose"]=floor3
            rec["note"]=f'경쟁 {low["vendor"]} {int(low["sale"])} < 우리 {int(our_live)}, 3%하한 {floor3}>경쟁−100 → 가격경쟁 불가·사용자판단'
    rec["note"]=(rec.get("note","") or "")+promo_note
    return rec

def main():
    lo,hi=int(sys.argv[1]),int(sys.argv[2])  # No 범위 (포함)
    items=json.load(open("items_all.json")) if os.path.exists("items_all.json") else json.load(open("items_1_10.json"))
    batch=[it for it in items if lo<=int(it["no"])<=hi]
    jar=sk.session_cookie()
    recs=[]
    import time; t0=time.time()
    for it in batch:
        recs.append(run_item(it, jar))
    # 누적 append (헤더 1회)
    new=not os.path.exists(RESULTS)
    with open(RESULTS,"a",newline="",encoding="utf-8-sig") as f:
        w=csv.DictWriter(f, fieldnames=FIELDS); 
        if new: w.writeheader()
        for r in recs: w.writerow(r)
    print(f"No{lo}~{hi}: {len(recs)}건 적립 ({time.time()-t0:.1f}s) → {RESULTS}")
    for r in recs:
        v=r["verdict"]
        flag="⚠️인하" if v=="인하" else ("🟡결정" if v.startswith("결정") else "✅"+r["newtag"])
        print(f'  No{r["no"]:>2} {r["name"][:24]:<24} live {r["our_live"]} | 택배경쟁 {r["comp_low"] or "-"}({r["comp_seller"][:10]}) | {flag} {r["propose"] or ""}')

if __name__=="__main__": main()
