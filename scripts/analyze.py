#!/usr/bin/env python3
"""Data-quality stats for toyproject1/medicine-packaging-merged-v2.

Reads classes.json (classes dict + splits) and writes STATS.md + stats.json.
Does not train or modify the Roboflow project.
"""
from __future__ import annotations

import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path("/workspace/merged-v2-analysis")
CLASSES_PATH = ROOT / "classes.json"
STATS_MD = ROOT / "STATS.md"
STATS_JSON = ROOT / "stats.json"

HANGUL_RE = re.compile(r"[\uac00-\ud7a3]")
MFDS_RE = re.compile(r"^\d{9}$")
FORM_RE = re.compile(r"^(?P<stem>.+)_(?P<form>Box|Blister|Pack)$", re.I)
AUTH_RE = re.compile(
    r"^(?P<kind>authentic|counterfeit)[\s_\-]+(?P<stem>.+)$", re.I
)

# Known Korean product <-> English / sibling names (qualitative mapping).
KO_EN_PAIRS = [
    {
        "korean": "타이레놀",
        "english": ["Tylenol"],
        "related": ["TYLOLHOT"],
        "note": "Same acetaminophen brand family (Tylenol / 타이레놀).",
    },
    {
        "korean": "베아제정",
        "english": [],
        "related": ["닥터베아제정"],
        "note": "Bearse digestive tablets; 닥터베아제정 is a sibling SKU, no English class.",
    },
    {
        "korean": "닥터베아제정",
        "english": [],
        "related": ["베아제정"],
        "note": "Doctor Bearse; sibling of 베아제정.",
    },
    {
        "korean": "훼스탈플러스정",
        "english": [],
        "related": [],
        "note": "Festal Plus; no English class present.",
    },
    {
        "korean": "신신파스 아렉스",
        "english": [],
        "related": [],
        "note": "Sinsinpas Arex plaster; no English class present.",
    },
    {
        "korean": "판피린티정",
        "english": [],
        "related": [],
        "note": "Panpyrin-T; no English class present.",
    },
    {
        "korean": "판콜에이내복액",
        "english": [],
        "related": [],
        "note": "Pancol-A liquid; no English class present.",
    },
]

# Curated obvious ingredient / excipient / botanical labels that are not pack SKUs.
INGREDIENT_ONLY = {
    "Aluminium Hydroxide",
    "Aluminum Hydroxide",
    "Magnesium Hydroxide",
    "Magnesium Trisilicate",
    "Methyl Salicylate",
    "Phenyl Salicylate",
    "Levomenthol",
    "Eugenol",
    "Menthol",
    "Salol and Menthol",
    "Zinc",
    "Camphor",
    "Caffeine",
    "Calcium",
    "Folic Acid",
    "Collagen",
    "Lecithin",
    "Taurine",
    "L-cysteine",
    "Chloride",
    "Citrate Dihydrate",
    "Glucose Anhydrous",
    "Hyaluronate",
    "Povidone",
    "Kaolin",
    "Clavulanic Acid",
    "Compound Cardamom Tincture",
    "Strong Capsicum Tincture",
    "Strong Ginger Tincture",
    "Eucalyptus oil",
    "Spearmint oil",
    "Mentha oil",
    "Chamomile Extract",
    "Marigold Extract",
    "Licorice Extract",
    "Licorice extract",
    "Propolis Extract",
    "Propolis extract",
    "Bilberry Extract",
    "Lemon Bioflavonoid Complex",
    "Andrographis Paniculata",
    "Cassia Siamea",
    "Pontirus Trifoliata",
    "Smilax Glabra",
    "Lonrcera Japonica",
    "Coptis Chinensis",
    "Phyllanthus emblica L.",
    "Zingiber officinale roxb.",
    "Glycyrrhiza glabra L.",
    "Lonicera japonica",
    "valeriana officinalis",
    "Polyethylene Glycol",
    "Propylene Glycol",
    "Hydroxypropyl Methylcellulose",
    "Mucopolysaccharide",
    "Dichlorobenzyl Alcohol",
    "Asafoetida and Alcohol",
    "Alumine",
    "Magnesia",
    "Vitamin C",
    "Vitamin B group",
    "Biotin",
    "Calcium Ascorbate",
    "Activated Charcoal",
    "Antiflatulence",
    "Carbamate Insecticides",
    "Quercetin",
    "Escin",
    "Aescin",
    "Dioctahedral smectite",
}

# Toiletry / household / non-pack-medicine keywords (name contains, case-insensitive).
TOILETRY_NEEDLES = [
    "listerine",
    "selsun",
    "sabun",
    "shampoo",
    "dettol",
    "lactacyd",
    "bio-oil",
    "tissue lovers",
    "hansaplast",
    "handsaplast",
    "sterimar",
    "feminime",
    "feminine",
    "freshcare",
    "minyak",
    "vicks",
    "bepanthen baby",
    "rohto",
    "caladine",
    "herocyn",
    "zambuk",
    "vital ear oil",
    "medicated oil",
    "balsem",
    "koyo",
]

CONDOM_NEEDLES = ["durex", "fiesta", "sutra", "kondom"]
PREGNANCY_NEEDLES = ["kehamilan", "ovulation"]
EXPLICIT_NOISE = {"Front", "Back", "Polident", "Medicine-detection"}

SOURCES = [
    ("medicine_52", 4869, "MFDS 9-digit item-permit codes; Korean packs"),
    ("Convenience", 367, "QUALITATIVE: web screenshots mixed in"),
    ("Aeye", 321, ""),
    ("packv2", 2756, ""),
    ("SevaMeds", 521, "QUALITATIVE: Ayurvedic products"),
    ("Drug2", 2970, ""),
    ("Aiden", 2781, "QUALITATIVE: class names are pills but images are packs"),
    ("Indonesian", 779, "QUALITATIVE: condom SKUs mixed in"),
    ("rk6cb", 2961, ""),
    ("Pasus", 2495, ""),
    ("Hithesh", 3348, "QUALITATIVE: mixed box + blister of same drug"),
    ("AIMedisina", 2171, "QUALITATIVE: Front/Back view labels"),
    ("SmartVision", 1511, ""),
    ("Teknofest", 447, ""),
]


def percentile(sorted_vals: list[int], p: float) -> float:
    """Linear-interpolation percentile (inclusive, Excel PERCENTILE.INC)."""
    if not sorted_vals:
        return float("nan")
    if len(sorted_vals) == 1:
        return float(sorted_vals[0])
    k = (len(sorted_vals) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return float(sorted_vals[int(k)])
    return sorted_vals[f] * (c - k) + sorted_vals[c] * (k - f)


def pct(n: int, d: int) -> float:
    return (100.0 * n / d) if d else 0.0


def has_hangul(name: str) -> bool:
    return bool(HANGUL_RE.search(name))


def is_mfds(name: str) -> bool:
    return bool(MFDS_RE.fullmatch(name))


def needle_hit(name: str, needles: list[str]) -> str | None:
    low = name.lower()
    for n in needles:
        if n in low:
            return n
    return None


def classify_noise(name: str) -> list[str]:
    reasons: list[str] = []
    if name in EXPLICIT_NOISE:
        reasons.append("explicit:" + name)
    hit = needle_hit(name, CONDOM_NEEDLES)
    if hit:
        reasons.append("condom:" + hit)
    if needle_hit(name, PREGNANCY_NEEDLES):
        reasons.append("pregnancy-test")
    hit = needle_hit(name, TOILETRY_NEEDLES)
    if hit:
        reasons.append("toiletry:" + hit)
    if name in INGREDIENT_ONLY:
        reasons.append("ingredient-only")
    if name == "su":
        reasons.append("degenerate-label")
    return reasons


def md_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def main() -> None:
    raw = json.loads(CLASSES_PATH.read_text(encoding="utf-8"))
    classes: dict[str, int] = raw["classes"]
    splits: dict[str, int] = raw["splits"]
    n_images = int(raw["n_images"])
    n_classes = len(classes)
    total_ann = sum(classes.values())
    ann_per_image = total_ann / n_images if n_images else 0.0

    counts = sorted(classes.values())
    dist = {
        "min": counts[0],
        "p25": percentile(counts, 25),
        "median": percentile(counts, 50),
        "p75": percentile(counts, 75),
        "max": counts[-1],
        "mean": total_ann / n_classes,
    }

    buckets_def = [
        ("1", lambda c: c == 1),
        ("2-5", lambda c: 2 <= c <= 5),
        ("6-20", lambda c: 6 <= c <= 20),
        ("21-100", lambda c: 21 <= c <= 100),
        ("101-500", lambda c: 101 <= c <= 500),
        ("500+", lambda c: c >= 500),
    ]
    buckets = {}
    for label, pred in buckets_def:
        names = [n for n, c in classes.items() if pred(c)]
        buckets[label] = {
            "n_classes": len(names),
            "n_instances": sum(classes[n] for n in names),
            "pct_classes": pct(len(names), n_classes),
        }

    top20 = sorted(classes.items(), key=lambda kv: (-kv[1], kv[0]))[:20]
    bottom30 = sorted(classes.items(), key=lambda kv: (kv[1], kv[0]))[:30]

    # Case-collision: identical when lowercased, different original strings.
    by_lower: dict[str, list[str]] = defaultdict(list)
    for name in classes:
        by_lower[name.lower()].append(name)
    case_pairs = []
    for key, names in sorted(by_lower.items()):
        if len(names) > 1:
            case_pairs.append(
                {
                    "normalized": key,
                    "variants": [
                        {"name": n, "count": classes[n]}
                        for n in sorted(names, key=lambda x: -classes[x])
                    ],
                    "n_variants": len(names),
                    "combined_count": sum(classes[n] for n in names),
                }
            )
    case_pairs.sort(key=lambda g: -g["combined_count"])

    # Box / Blister / Pack groups
    form_map: dict[str, dict[str, str]] = defaultdict(dict)
    for name in classes:
        m = FORM_RE.match(name)
        if m:
            form_map[m.group("stem")][m.group("form")] = name
    form_groups = []
    for stem, forms in form_map.items():
        if len(forms) >= 2:
            form_groups.append(
                {
                    "stem": stem,
                    "forms": {
                        form: {"name": nm, "count": classes[nm]}
                        for form, nm in forms.items()
                    },
                    "n_forms": len(forms),
                    "combined_count": sum(classes[nm] for nm in forms.values()),
                }
            )
    form_groups.sort(key=lambda g: -g["combined_count"])

    # Authentic vs Counterfeit (+ leftover plain SKU if present)
    auth_map: dict[str, dict[str, str]] = defaultdict(dict)
    for name in classes:
        m = AUTH_RE.match(name)
        if m:
            stem = re.sub(r"\s+", " ", m.group("stem")).strip()
            auth_map[stem][m.group("kind").lower()] = name
    # attach leftover plain names (Biogesic, Decolgen, Neozep Forte)
    leftover_keys = {n: n for n in classes if n not in EXPLICIT_NOISE}
    auth_groups = []
    for stem, kinds in auth_map.items():
        group = {
            "stem": stem,
            "kinds": {
                k: {"name": nm, "count": classes[nm]} for k, nm in kinds.items()
            },
            "plain": None,
            "combined_count": sum(classes[nm] for nm in kinds.values()),
        }
        if stem in leftover_keys:
            group["plain"] = {"name": stem, "count": classes[stem]}
            group["combined_count"] += classes[stem]
        auth_groups.append(group)
    auth_groups.sort(key=lambda g: -g["combined_count"])

    # Korean hangul classes + KO/EN pairs
    hangul_classes = sorted(
        ((n, classes[n]) for n in classes if has_hangul(n)),
        key=lambda kv: -kv[1],
    )
    ko_en = []
    for pair in KO_EN_PAIRS:
        kname = pair["korean"]
        entry = {
            "korean": {"name": kname, "count": classes.get(kname, 0)},
            "english": [
                {"name": e, "count": classes.get(e, 0)} for e in pair["english"]
            ],
            "related": [
                {"name": r, "count": classes.get(r, 0)} for r in pair["related"]
            ],
            "note": pair["note"],
            "combined_count": classes.get(kname, 0)
            + sum(classes.get(e, 0) for e in pair["english"])
            + sum(classes.get(r, 0) for r in pair["related"] if r != kname),
        }
        # avoid double-counting related that is another hangul already listed
        ko_en.append(entry)

    mfds = sorted(
        ((n, classes[n]) for n in classes if is_mfds(n)),
        key=lambda kv: -kv[1],
    )

    noise_items = []
    for name, cnt in classes.items():
        reasons = classify_noise(name)
        if reasons:
            noise_items.append(
                {"name": name, "count": cnt, "reasons": reasons}
            )
    noise_items.sort(key=lambda x: (-x["count"], x["name"]))

    # Extra spelling / brand near-dups (not case, not form suffix)
    extra_near = [
        {
            "group": "Neozep/Neozap Forte",
            "members": ["Neozep Forte", "Neozap Forte"],
            "note": "Likely same brand, spelling drift",
        },
        {
            "group": "Cefixime family",
            "members": ["Cefixime", "Cefixim 200mg_Box", "Cefixim 200mg_Blister", "Cefixine"],
            "note": "Same API, three spellings + form split",
        },
        {
            "group": "Ketoconazole family",
            "members": ["Ketoconazole", "ketoconazole", "Ketokonazole", "Ketokonazole Cream"],
            "note": "Case + spelling (k/c) + cream SKU",
        },
        {
            "group": "Etoricoxib",
            "members": ["Etoricoxib", "Etoricoxid"],
            "note": "Spelling typo",
        },
        {
            "group": "Biogesic",
            "members": ["Biogesic", "Authentic_Biogesic", "Counterfeit_Biogesic", "Biolgesic Paracetamol"],
            "note": "Auth/counterfeit plus typo Biolgesic",
        },
        {
            "group": "Hansaplast",
            "members": ["Hansaplast", "Handsaplast Koyo Panas"],
            "note": "Brand typo + plaster (toiletry-adjacent)",
        },
        {
            "group": "Nellco/Nelco",
            "members": ["Nellco", "Nelco"],
            "note": "Spelling drift",
        },
        {
            "group": "Aluminum hydroxide",
            "members": ["Aluminium Hydroxide", "Aluminum Hydroxide"],
            "note": "UK/US spelling; ingredient-only",
        },
        {
            "group": "Panadol family",
            "members": [
                "Panadol",
                "Panadol Paracetamol",
                "Panadol Extra Paracetamol",
                "Panadol Extra",
                "Panadol Cold Flu",
                "Panadol Flu Batuk",
                "Panadol Anak",
            ],
            "note": "Same brand fragmented across SKUs/languages",
        },
        {
            "group": "Amlodipine family",
            "members": [
                "Amlodipine",
                "amlopine",
                "amlodipine 5mg hipertensi",
                "amlodipine 10mg hipertensi",
            ],
            "note": "Generic + dose/indication + typo amlopine",
        },
        {
            "group": "Metformin family",
            "members": [
                "Metformin",
                "metformin",
                "metformin 500mg diabetes",
                "metformin 850mg diabetes",
            ],
            "note": "Case collision plus dose-split Indonesian labels",
        },
        {
            "group": "Losartan family",
            "members": ["Losartan", "losartan", "Losartan Potassium"],
            "note": "Case collision plus salt form",
        },
        {
            "group": "Ibuprofen",
            "members": ["Ibuprofen", "ibuprofen"],
            "note": "Pure case collision",
        },
        {
            "group": "Glimepiride family",
            "members": [
                "Glimepiride",
                "glimepiride 1mg diabetes",
                "glimepiride 2mg diabetes",
                "glimepiride 3mg diabetes",
                "glimepiride 4mg diabetes",
            ],
            "note": "Generic plus Indonesian dose/indication splits",
        },
    ]
    extra_resolved = []
    for g in extra_near:
        members = [
            {"name": m, "count": classes[m]}
            for m in g["members"]
            if m in classes
        ]
        extra_resolved.append(
            {
                "group": g["group"],
                "note": g["note"],
                "members": members,
                "combined_count": sum(x["count"] for x in members),
            }
        )

    source_rows = []
    source_total = sum(n for _, n, _ in SOURCES)
    for name, n, note in SOURCES:
        source_rows.append(
            {
                "source": name,
                "n_images": n,
                "pct_images": pct(n, n_images),
                "note": note,
            }
        )

    split_rows = []
    split_sum = sum(splits.values())
    for k in ("train", "valid", "test"):
        split_rows.append(
            {
                "split": k,
                "n_images": splits[k],
                "pct_images": pct(splits[k], n_images),
            }
        )

    noise_by_reason: dict[str, dict] = defaultdict(
        lambda: {"n_classes": 0, "n_instances": 0}
    )
    for item in noise_items:
        # bucket by primary family
        family = item["reasons"][0].split(":")[0]
        # if multiple, attribute to each family
        families = {r.split(":")[0] for r in item["reasons"]}
        for fam in families:
            noise_by_reason[fam]["n_classes"] += 1
            noise_by_reason[fam]["n_instances"] += item["count"]

    stats = {
        "project_id": raw.get("project_id", "toyproject1/medicine-packaging-merged-v2"),
        "n_images": n_images,
        "unannotated": raw.get("unannotated", 0),
        "splits": {
            "counts": splits,
            "percents": {r["split"]: r["pct_images"] for r in split_rows},
            "sum": split_sum,
        },
        "n_classes": n_classes,
        "total_annotation_instances": total_ann,
        "annotations_per_image": ann_per_image,
        "class_count_distribution": dist,
        "class_count_buckets": buckets,
        "top20_classes": [{"name": n, "count": c} for n, c in top20],
        "bottom30_classes": [{"name": n, "count": c} for n, c in bottom30],
        "case_collision_pairs": case_pairs,
        "near_duplicates": {
            "box_blister_pack": form_groups,
            "authentic_counterfeit": auth_groups,
            "korean_english": ko_en,
            "other_spelling_or_brand_families": extra_resolved,
        },
        "noise_non_medicine_candidates": {
            "items": noise_items,
            "n_classes": len(noise_items),
            "n_instances": sum(x["count"] for x in noise_items),
            "by_family": dict(noise_by_reason),
        },
        "mfds_9digit": {
            "n_classes": len(mfds),
            "n_instances": sum(c for _, c in mfds),
            "classes": [{"name": n, "count": c} for n, c in mfds],
        },
        "korean_hangul": {
            "n_classes": len(hangul_classes),
            "n_instances": sum(c for _, c in hangul_classes),
            "classes": [{"name": n, "count": c} for n, c in hangul_classes],
        },
        "source_composition": {
            "rows": source_rows,
            "sum_images": source_total,
            "expected_total": 28297,
            "matches_n_images": source_total == n_images,
        },
        "qualitative_sample_review": [
            "Convenience: web screenshots (not pack photos).",
            "Indonesian: condom products mixed into a medicine project.",
            "AIMedisina: Front/Back view classes instead of product identity.",
            "Hithesh: same drug split across box + blister classes.",
            "SevaMeds: Ayurvedic / herbal products.",
            "Aiden: class names look like pill/API names but images are packs.",
        ],
    }

    STATS_JSON.write_text(
        json.dumps(stats, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # ---- STATS.md ----
    lines: list[str] = []
    a = lines.append
    a("# medicine-packaging-merged-v2 data-quality report")
    a("")
    a("Project: `toyproject1/medicine-packaging-merged-v2` (object-detection).")
    a("Computed from Roboflow `projects_get` class counts and splits.")
    a("No training. Project was not modified.")
    a("")
    a("## Headline numbers")
    a("")
    a(
        md_table(
            ["metric", "value"],
            [
                ["n_images", n_images],
                ["unannotated", raw.get("unannotated", 0)],
                [
                    "train / valid / test",
                    f"{splits['train']} / {splits['valid']} / {splits['test']}",
                ],
                [
                    "split percents",
                    f"{pct(splits['train'], n_images):.2f}% / "
                    f"{pct(splits['valid'], n_images):.2f}% / "
                    f"{pct(splits['test'], n_images):.2f}%",
                ],
                ["n_classes", n_classes],
                ["total annotation instances", total_ann],
                ["annotations per image", f"{ann_per_image:.3f}"],
                ["MFDS 9-digit classes", len(mfds)],
                ["Korean Hangul classes", len(hangul_classes)],
                [
                    "noise/non-medicine candidate classes",
                    f"{len(noise_items)} ({sum(x['count'] for x in noise_items)} instances)",
                ],
                ["case-collision groups", len(case_pairs)],
                ["Box/Blister/Pack multi-form groups", len(form_groups)],
                ["Authentic/Counterfeit groups", len(auth_groups)],
            ],
        )
    )
    a("")
    a("## Splits")
    a("")
    a(
        md_table(
            ["split", "n_images", "percent"],
            [
                [r["split"], r["n_images"], f"{r['pct_images']:.2f}%"]
                for r in split_rows
            ]
            + [["**sum**", split_sum, f"{pct(split_sum, n_images):.2f}%"]],
        )
    )
    a("")
    a("## Class-count distribution")
    a("")
    a(
        md_table(
            ["stat", "instances per class"],
            [
                ["min", dist["min"]],
                ["p25", f"{dist['p25']:.2f}"],
                ["median", f"{dist['median']:.2f}"],
                ["p75", f"{dist['p75']:.2f}"],
                ["max", dist["max"]],
                ["mean", f"{dist['mean']:.2f}"],
            ],
        )
    )
    a("")
    a(
        md_table(
            ["bucket", "n_classes", "% of classes", "n_instances"],
            [
                [
                    label,
                    buckets[label]["n_classes"],
                    f"{buckets[label]['pct_classes']:.1f}%",
                    buckets[label]["n_instances"],
                ]
                for label, _ in buckets_def
            ],
        )
    )
    a("")
    a(
        f"Long tail is severe: **{buckets['1']['n_classes']} classes have a single instance** "
        f"({buckets['1']['pct_classes']:.1f}% of classes) and "
        f"{buckets['1']['n_classes'] + buckets['2-5']['n_classes']} classes have ≤5 instances "
        f"({pct(buckets['1']['n_classes'] + buckets['2-5']['n_classes'], n_classes):.1f}%)."
    )
    a("")
    a("## Top 20 classes by instance count")
    a("")
    a(
        md_table(
            ["rank", "class", "count", "% of instances"],
            [
                [i, n, c, f"{pct(c, total_ann):.2f}%"]
                for i, (n, c) in enumerate(top20, 1)
            ],
        )
    )
    a("")
    a(
        f"`Front` + `Back` alone are {classes.get('Front', 0) + classes.get('Back', 0)} instances "
        f"({pct(classes.get('Front', 0) + classes.get('Back', 0), total_ann):.2f}% of all annotations) "
        "and are view labels, not medicines."
    )
    a("")
    a("## Bottom 30 classes (long-tail / likely noise)")
    a("")
    a(
        md_table(
            ["class", "count"],
            [[n, c] for n, c in bottom30],
        )
    )
    a("")
    a(
        "All 30 are singletons. Many are condom SKUs, toiletries, incomplete names, "
        "or one-off brand fragments — not usable as a medicine-pack taxonomy."
    )
    a("")
    a("## Case-collision pairs")
    a("")
    a(
        "Same string ignoring case, different Roboflow class IDs. "
        "Examples called out in the brief: Losartan/losartan, Ibuprofen/ibuprofen, Metformin/metformin."
    )
    a("")
    if case_pairs:
        rows = []
        for g in case_pairs:
            variants = ", ".join(
                f"{v['name']} ({v['count']})" for v in g["variants"]
            )
            rows.append(
                [g["normalized"], g["n_variants"], g["combined_count"], variants]
            )
        a(md_table(["normalized", "n_variants", "combined", "variants"], rows))
    else:
        a("None found.")
    a("")
    a("## Near-duplicate groups")
    a("")
    a("### Box vs Blister vs Pack (same drug stem)")
    a("")
    a(
        f"{len(form_groups)} stems have 2+ of `_Box` / `_Blister` / `_Pack`. "
        "These should usually be one product class (or an explicit form attribute), not separate SKUs."
    )
    a("")
    form_rows = []
    for g in form_groups:
        parts = []
        for form in ("Box", "Blister", "Pack"):
            if form in g["forms"]:
                parts.append(f"{form}={g['forms'][form]['count']}")
            else:
                parts.append(f"{form}=—")
        form_rows.append([g["stem"], g["n_forms"], g["combined_count"], "; ".join(parts)])
    a(md_table(["stem", "n_forms", "combined", "counts"], form_rows))
    a("")
    a("### Authentic-X vs Counterfeit-X")
    a("")
    auth_rows = []
    for g in auth_groups:
        kinds = g["kinds"]
        auth = kinds.get("authentic")
        ctr = kinds.get("counterfeit")
        plain = g["plain"]
        auth_rows.append(
            [
                g["stem"],
                f"{auth['name']} ({auth['count']})" if auth else "—",
                f"{ctr['name']} ({ctr['count']})" if ctr else "—",
                f"{plain['name']} ({plain['count']})" if plain else "—",
                g["combined_count"],
            ]
        )
    a(
        md_table(
            ["stem", "authentic", "counterfeit", "plain leftover", "combined"],
            auth_rows,
        )
    )
    a("")
    a(
        "Separator inconsistency: hyphen (`Authentic-Alaxan`), underscore (`Authentic_Biogesic`), "
        "and spaced hyphen (`Authentic -Medicol Advance`)."
    )
    a("")
    a("### Korean Hangul vs English (same product)")
    a("")
    a(
        f"{len(hangul_classes)} Hangul class names, {sum(c for _, c in hangul_classes)} instances. "
        "Only 타이레놀 has a clear English twin (`Tylenol`)."
    )
    a("")
    a(
        md_table(
            ["korean", "count", "english / related", "note"],
            [
                [
                    e["korean"]["name"],
                    e["korean"]["count"],
                    ", ".join(
                        f"{x['name']} ({x['count']})"
                        for x in e["english"] + e["related"]
                    )
                    or "—",
                    e["note"],
                ]
                for e in ko_en
            ],
        )
    )
    a("")
    a("Hangul classes:")
    a("")
    a(
        md_table(
            ["class", "count"],
            [[n, c] for n, c in hangul_classes],
        )
    )
    a("")
    a("### Other spelling / brand families (extra, not in the three requested patterns)")
    a("")
    a(
        md_table(
            ["group", "combined", "members", "note"],
            [
                [
                    g["group"],
                    g["combined_count"],
                    ", ".join(f"{m['name']} ({m['count']})" for m in g["members"]),
                    g["note"],
                ]
                for g in extra_resolved
            ],
        )
    )
    a("")
    a("## Noise / non-medicine class candidates")
    a("")
    a(
        f"**{len(noise_items)} classes / {sum(x['count'] for x in noise_items)} instances** flagged. "
        "Heuristics: condom brand needles (Durex, Fiesta, Sutra, Kondom); "
        "explicit `Front` / `Back` / `Polident` / `Medicine-detection`; "
        "pregnancy tests; toiletries (shampoo/soap/oil/plaster/mouthwash-like); "
        "obvious ingredient-only / botanical / excipient labels that are not pack SKUs; "
        "degenerate label `su`."
    )
    a("")
    a(
        md_table(
            ["family", "n_classes", "n_instances"],
            [
                [fam, v["n_classes"], v["n_instances"]]
                for fam, v in sorted(
                    noise_by_reason.items(), key=lambda kv: -kv[1]["n_instances"]
                )
            ],
        )
    )
    a("")
    a(
        md_table(
            ["class", "count", "reasons"],
            [
                [x["name"], x["count"], ", ".join(x["reasons"])]
                for x in noise_items
            ],
        )
    )
    a("")
    a("## MFDS 9-digit codes (medicine_52 style)")
    a("")
    a(
        f"**{len(mfds)} classes**, **{sum(c for _, c in mfds)} instances**. "
        "These are Korean MFDS item-permit numbers (9 digits), not brand names."
    )
    a("")
    a(
        md_table(
            ["code", "count"],
            [[n, c] for n, c in mfds],
        )
    )
    a("")
    a("## Source composition (known image counts only)")
    a("")
    a(
        "Image counts below are the provided known totals. "
        "No other source sizes were inferred. Qualitative notes are from prior visual review, not new counts."
    )
    a("")
    a(
        md_table(
            ["source", "n_images", "% of 28297", "known quality note"],
            [
                [
                    r["source"],
                    r["n_images"],
                    f"{r['pct_images']:.2f}%",
                    r["note"] or "—",
                ]
                for r in source_rows
            ]
            + [
                [
                    "**total**",
                    source_total,
                    f"{pct(source_total, n_images):.2f}%",
                    "matches n_images" if source_total == n_images else "MISMATCH",
                ]
            ],
        )
    )
    a("")
    a("## Qualitative sample-review notes (not new counts)")
    a("")
    a("- Convenience: web screenshots rather than pack photography.")
    a("- Indonesian: condoms (Durex / Fiesta / Sutra / Kondom) inside a medicine project.")
    a("- AIMedisina: `Front` / `Back` view labels (largest non-drug classes).")
    a("- Hithesh: mixed box + blister annotations for the same drug.")
    a("- SevaMeds: Ayurvedic / herbal products.")
    a("- Aiden: names look like pill/API labels but the images are packaging.")
    a("")
    a("## Top issues")
    a("")
    a(
        "1. **Class explosion + long tail.** "
        f"{n_classes} classes for {n_images} images; median class has only {dist['median']:.0f} instances; "
        f"{buckets['1']['n_classes']} singletons. A detector cannot learn most of these labels."
    )
    a(
        "2. **Duplicate identity.** Case collisions (Losartan/losartan, Ibuprofen/ibuprofen, Metformin/metformin, …), "
        f"{len(form_groups)} Box/Blister/Pack splits, {len(auth_groups)} Authentic/Counterfeit pairs, "
        "and 타이레놀 vs Tylenol. Same product is many classes."
    )
    a(
        "3. **Non-drug classes.** `Front`/`Back` (view), condoms, pregnancy tests, denture cream (`Polident`), "
        "toiletries, botanical/ingredient fragments, `Medicine-detection`, and `Carbamate Insecticides`."
    )
    a(
        "4. **Heterogeneous taxonomies merged.** MFDS 9-digit codes, Indonesian `drug Nmg indication` strings, "
        "brand SKUs, API generics, and Hangul brand names coexist without a join key."
    )
    a(
        "5. **Source-level contamination** (qualitative): screenshots, Ayurvedic, condom catalog, "
        "Front/Back views, box/blister double-labeling, pill-named pack photos."
    )
    a("")
    a("## Files")
    a("")
    a("- `/workspace/merged-v2-analysis/classes.json`")
    a("- `/workspace/merged-v2-analysis/STATS.md`")
    a("- `/workspace/merged-v2-analysis/stats.json`")
    a("- `/workspace/merged-v2-analysis/analyze.py`")
    a("")

    STATS_MD.write_text("\n".join(lines), encoding="utf-8")
    print("n_images", n_images)
    print("n_classes", n_classes)
    print("total_ann", total_ann)
    print("ann_per_image", f"{ann_per_image:.3f}")
    print("mfds", len(mfds), sum(c for _, c in mfds))
    print("hangul", len(hangul_classes), sum(c for _, c in hangul_classes))
    print("case_pairs", len(case_pairs))
    print("form_groups", len(form_groups))
    print("auth_groups", len(auth_groups))
    print("noise_classes", len(noise_items), sum(x["count"] for x in noise_items))
    print("source_sum", source_total)
    print("wrote", STATS_MD, STATS_JSON)


if __name__ == "__main__":
    main()
