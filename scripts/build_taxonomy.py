#!/usr/bin/env python3
"""Build 3-level taxonomy for remapped medicine-packaging classes."""
from __future__ import annotations

import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

ROOT = Path("/workspace/merged-v2-analysis")

MAJORS_ORDER = [
    "해열진통소염",
    "호흡기감기",
    "순환기",
    "당뇨",
    "항균항바이러스",
    "소화기",
    "신경정신",
    "호르몬내분비",
    "피부외용",
    "비타민영양",
    "피임산과",
    "정품위조",
    "한국식약처코드",
    "기타",
]

MIDS_ORDER = {
    "해열진통소염": ["Paracetamol계", "NSAID", "아스피린계", "통풍", "기타진통"],
    "호흡기감기": ["종합감기", "진해거담", "비염알레르기", "한방감기", "기타호흡기"],
    "순환기": None,
    "당뇨": None,
    "항균항바이러스": ["베타락탐", "세팔로스포린", "퀴놀론", "마크로라이드", "항진균", "항바이러스", "기타항균"],
    "소화기": ["제산궤양", "소화효소", "지사제", "기타소화"],
    "신경정신": ["항전간신경통", "항우울항정신", "편두통", "어지럼", "통풍", "기타신경"],
    "호르몬내분비": ["갑상선", "스테로이드", "여성호르몬", "기타내분비"],
    "비타민영양": ["종합비타민", "단일영양", "면역건강"],
    "피부외용": ["항진균외용", "스테로이드외용", "파스외용", "위생화장품", "기타외용"],
    "피임산과": ["경구피임", "산과기타"],
    "정품위조": None,
    "한국식약처코드": ["식약처품목허가번호"],
    "기타": ["성분명만", "브랜드미분류", "비의약품"],
}


def contains_any(text: str, needles) -> str | None:
    for n in needles:
        if n in text:
            return n
    return None


def fold(s: str) -> str:
    """Lowercase and strip Turkish/accent marks so RENNİE matches rennie."""
    s = s.replace("İ", "I").replace("ı", "i")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return s.lower()


PARA_KWS = [
    "paracetamol", "panadol", "crocin", "calpol", "tylenol", "tylolhot",
    "pamol", "biogesic", "biolgesic", "sumagesic", "novagesic", "fasidol",
    "pacetik", "mirasic", "sanmol", "parol", "dumin",
]
NSAID_KWS = [
    "ibuprofen", "naproxen", "naprex", "diclofenac", "mefenamic", "meloxicam",
    "piroxicam", "pirocam", "celecoxib", "etoricoxib", "etoricoxid",
    "apranax", "dolorex", "arveles", "majez", "cataflam", "voltaren",
    "poldan", "inza", "ponstan", "xidolac", "proris", "neorheumacyl",
    "benzydamine",
]
ASPIRIN_KWS = ["aspirin", "ecosprine"]

COLD_COMBO_KWS = [
    "neozep", "neozap", "bioflu", "decolgen", "medicol", "mixagrip",
    "ultraflu", "sanaflu", "actifed", "cheston", "coldaway", "a-ferin",
    "iburamin", "intunal", "bodrex", "procold", "oskadon", "saridon",
    "paramex", "fluanza", "판콜", "nalgestan",
]
COUGH_KWS = [
    "obh", "ob herbal", "cofsils", "ambroxol", "bromhexine", "bisolvon",
    "guaifenesin", "dextromethorphan", "acetylcysteine", "carbocisteine",
    "mucos", "mucopect", "transpulmin", "pectorin", "paratusin",
    "theophylline", "albuterol", "laserin", "exomuc", "terpin",
    "obat batuk", "nellco", "nelco", "komix", "vicks", "sptroches",
    "degirol", "amylmetacresol", "dichlorobenzyl",
]
ALLERGY_KWS = [
    "loratadine", "cetirizine", "fexofenadine", "bilastine", "telfast",
    "chlorpheniramine", "brompheniramine", "hydroxyzine", "diphenhydramine",
    "mepyramine", "chlorphenoxamine", "oxymetazoline", "phenylephrine",
    "naphazoline", "interhistin", "monas",
]
HERBAL_COLD_KWS = [
    "tolak angin", "antangin", "madu tj", "fa ta lai", "andrographis",
]

BETA_LACTAM_KWS = [
    "amoxicillin", "augmentin", "ampicillin", "dicloxacillin", "penicillin",
    "phenoxymethyl", "clavulanic",
]
CEPH_KWS = ["cefixim", "cefixin", "cef-3", "lostracef", "sefloc"]
QUIN_KWS = ["ciprofloxacin", "norfloxacin", "moxifloxacin"]
MACRO_KWS = ["azithromycin", "azee", "roxithromycin"]
ANTIFUNGAL_KWS = [
    "fluconazol", "ketoconazol", "ketokonazol", "clotrimazol",
    "itraconazol", "itrabat", "sporal", "mycoral", "mycostatin",
    "nocandis", "bifonazole",
]
ANTIVIRAL_KWS = ["acyclovir"]

ANTACID_KWS = [
    "simethicone", "mylanta", "gaviscon", "rennie", "promag", "polysilane",
    "omeprazole", "lomac", "esoral", "dexilend", "famotidine", "sucralfate",
    "plantacid", "lambucid", "aluminium hydroxide", "aluminum hydroxide",
    "magnesium hydroxide", "magnesium trisilicate", "dioctahedral", "smectite",
    "lansor", "polycrol", "sanmag",
]
ENZYME_KWS = ["베아제", "훼스탈", "pancreatin", "alpha choay"]
ANTIDIARR_KWS = ["loperamide", "entrostop", "diapet", "diatabs", "kaolin"]

THYROID_KWS = ["levothyroxine", "thyroxine", "methimazole"]
STEROID_KWS = [
    "prednison", "hydrocortisone", "betamethasone", "triamcinolone",
    "desoximetasone", "mometasone", "clobetasol", "budesonide",
    "fluticasone", "fluocinolone", "kenalog",
]
FEMALE_HORMONE_KWS = [
    "utrogestan", "cyclogest", "valiera", "femara", "misoprostol",
]

MULTI_VIT_KWS = [
    "berocca", "enervon", "neurobion", "sakatonik", "tonikum", "becom",
    "caviplex", "holisti", "scotts", "vitabion", "benexol", "renovit",
    "zegavit", "oxyvit", "nusaplex", "apialys", "curvit", "neurotropic",
    "neurosanbe", "neurodex", "cerebrofort", "vitamin b",
]
SINGLE_NUT_KWS = [
    "cevit", "folison", "folacid", "calci", "kalcoral", "coledan", "devit",
    "ipi vit", "redoxon", "sangobion", "natur-e", "folic", "biotin",
    "taurine", "prove d3", "vitacimin", "vicee", "dicaltrol", "ferlatum",
    "globifer", "cdr", "cal-95", "livron", "ever e", "vitabumin",
    "calcium", "vitamin c",
]
IMMUNE_KWS = ["imboost", "stimuno", "imunped"]

ANTIFUNGAL_TOP_KWS = [
    "canesten", "daktarin", "ketokonazole cream", "tolnaftate",
]
STEROID_TOP_KWS = ["gentrison"]
PLASTER_KWS = [
    "salonpas", "신신파스", "ben-gay", "hansaplast", "handsaplast",
    "counterpain", "koyo", "balsem", "hotin", "cooling 5", "freshcare",
    "minyak", "safecare", "medicated oil", "byebye fever", "plossa",
]
HYGIENE_KWS = [
    "betadine", "dettol", "selsun", "bio-oil", "lactacyd", "sterimar",
    "bepanthen", "herocyn", "caladine", "zambuk", "gpu", "polident",
    "dermatix", "callusol", "minosep", "y-rins", "sabun", "alco",
]
OTHER_TOP_KWS = [
    "peditox", "vital ear", "tretinoin", "minoxidil", "calamine",
    "benzoyl peroxide", "permethrin", "salep 88", "pi kang", "prodermis",
    "pasquam", "rohto", "cendo", "noroid", "salicyl",
]

INGREDIENT_ONLY = [
    "eugenol", "menthol", "levomenthol", "methyl salicylate", "phenyl salicylate",
    "salol", "zinc", "camphor", "quercetin", "eucalyptus", "spearmint",
    "mentha oil", "chamomile", "marigold", "bioflavonoid", "pontirus",
    "smilax", "lonrcera", "lonicera", "coptis", "phyllanthus", "zingiber",
    "glycyrrhiza", "asafoetida", "propolis", "licorice", "alumine", "magnesia",
    "l-cysteine", "escin", "aescin", "cassia siamea", "andrographis",
    "glucose anhydrous", "chloride", "citrate dihydrate", "polyethylene glycol",
    "propylene glycol", "hydroxypropyl", "povidone", "mucopolysaccharide",
    "hyaluronate", "lysozyme", "diosmin", "tranexamic", "caffeine",
    "lecithin", "collagen", "bilberry", "valeriana", "iodochlorhydroxyquin",
    "lodochlorhydroxyquin", "compound cardamom", "capsicum tincture",
    "ginger tincture", "tumeric", "curcuma",
]
NON_MEDICINE = [
    "su", "medicine-detection", "carbamate", "tissue lovers",
]

DIABETES_INNS = [
    ("metformin", "Metformin"),
    ("glimepiride", "Glimepiride"),
    ("glipizide", "Glipizide"),
    ("gliclazide", "Gliclazide"),
    ("glibenclamide", "Glibenclamide"),
    ("gliquidone", "Gliquidone"),
    ("sitagliptin", "Sitagliptin"),
    ("voglibose", "Voglibose"),
]
CARDIO_INNS = [
    ("amlodipine", "Amlodipine"),
    ("losartan", "Losartan"),
    ("telmisartan", "Telmisartan"),
    ("captopril", "Captopril"),
    ("ramipril", "Ramipril"),
    ("enalapril", "Enalapril"),
    ("bisoprolol", "Bisoprolol"),
    ("atenolol", "Atenolol"),
    ("propranolol", "Propranolol"),
    ("isosorbide", "Isosorbide"),
    ("furosemide", "Furosemide"),
    ("hidroklorotiazid", "Hydrochlorothiazide"),
    ("hydrochlorothiazide", "Hydrochlorothiazide"),
    ("methyldopa", "Methyldopa"),
    ("metildopa", "Methyldopa"),
    ("manidipine", "Manidipine"),
    ("simvastatin", "Simvastatin"),
    ("diosmin", "Diosmin"),
]


def mid_for_pain(low: str, name: str) -> str:
    if contains_any(low, ASPIRIN_KWS):
        return "아스피린계"
    if contains_any(low, NSAID_KWS):
        return "NSAID"
    if "dolo" in low and "dolorex" not in low:
        return "Paracetamol계"
    if contains_any(low, PARA_KWS) or "타이레놀" in name:
        return "Paracetamol계"
    if "판피린" in name:
        return "기타진통"
    return "기타진통"


def mid_for_resp(low: str, name: str) -> str:
    if contains_any(low, HERBAL_COLD_KWS) or "tolak angin" in low:
        return "한방감기"
    if contains_any(low, ALLERGY_KWS):
        return "비염알레르기"
    if contains_any(low, COUGH_KWS) or "obh" in low:
        return "진해거담"
    if contains_any(low, COLD_COMBO_KWS) or "판콜" in name:
        return "종합감기"
    if "seretide" in low or "salmeterol" in low:
        return "기타호흡기"
    return "기타호흡기"


def mid_for_abx(low: str) -> str:
    if contains_any(low, ANTIVIRAL_KWS):
        return "항바이러스"
    if contains_any(low, ANTIFUNGAL_KWS):
        return "항진균"
    if contains_any(low, MACRO_KWS):
        return "마크로라이드"
    if contains_any(low, QUIN_KWS):
        return "퀴놀론"
    if contains_any(low, CEPH_KWS):
        return "세팔로스포린"
    if contains_any(low, BETA_LACTAM_KWS):
        return "베타락탐"
    return "기타항균"


def mid_for_gi(low: str, name: str) -> str:
    if contains_any(low, ENZYME_KWS) or "베아제" in name or "훼스탈" in name:
        return "소화효소"
    if contains_any(low, ANTIDIARR_KWS):
        return "지사제"
    if contains_any(low, ANTACID_KWS):
        return "제산궤양"
    return "기타소화"


def mid_for_neuro(low: str) -> str:
    if contains_any(low, ["colchicine", "allopurinol"]):
        return "통풍"
    if contains_any(low, ["sumatriptan", "eletriptan", "ergotamine"]):
        return "편두통"
    if contains_any(low, [
        "flunarizine", "betahistine", "diphenidol", "dimenhydrinate",
        "cinnarizine", "nautamine", "antimo",
    ]):
        return "어지럼"
    if contains_any(low, [
        "lorazepam", "clorazepate", "amitriptyline", "tryptin", "fluoxetine",
        "aripiprazole", "epiclon", "selrotine",
    ]):
        return "항우울항정신"
    if contains_any(low, ["pregabalin", "pregaba", "gabapentin"]):
        return "항전간신경통"
    return "기타신경"


def mid_for_hormone(low: str) -> str:
    if contains_any(low, THYROID_KWS):
        return "갑상선"
    if contains_any(low, FEMALE_HORMONE_KWS):
        return "여성호르몬"
    if contains_any(low, STEROID_KWS):
        return "스테로이드"
    return "기타내분비"


def mid_for_vit(low: str) -> str:
    if contains_any(low, IMMUNE_KWS):
        return "면역건강"
    if contains_any(low, MULTI_VIT_KWS):
        return "종합비타민"
    if "vitamin" in low and ("plus" in low or ("vitamin c" in low and "vitamin d" in low)):
        return "종합비타민"
    if contains_any(low, SINGLE_NUT_KWS) or "vitamin" in low:
        return "단일영양"
    return "단일영양"


def mid_for_topical(low: str, name: str) -> str:
    if contains_any(low, ANTIFUNGAL_TOP_KWS) or "ketokonazole cream" in low:
        return "항진균외용"
    if contains_any(low, STEROID_TOP_KWS):
        return "스테로이드외용"
    if contains_any(low, PLASTER_KWS) or "신신파스" in name:
        return "파스외용"
    if contains_any(low, HYGIENE_KWS):
        return "위생화장품"
    if contains_any(low, OTHER_TOP_KWS):
        return "기타외용"
    return "기타외용"


def mid_for_obgyn(low: str) -> str:
    if contains_any(low, ["mercilon", "marvelon"]):
        return "경구피임"
    return "산과기타"


def mid_for_inn_or_brand(low: str, inns) -> str:
    for kw, inn in inns:
        if kw in low:
            return inn
    return "브랜드"


def mid_for_etc(low: str, name: str) -> str:
    if name.strip().lower() in {"su", "medicine-detection", "tissue lovers"} or contains_any(low, NON_MEDICINE):
        return "비의약품"
    if contains_any(low, INGREDIENT_ONLY):
        return "성분명만"
    if re.search(
        r"\b(L\.|roxb\.|officinalis|japonica|chinensis|glabra|emblica|paniculata|trifoliata)\b",
        name,
        re.I,
    ):
        return "성분명만"
    return "브랜드미분류"


EXTRA = {
    "Simvastatin": ("순환기", "Simvastatin"),
    "Diosmin": ("순환기", "Diosmin"),
    "Loratadine": ("호흡기감기", "비염알레르기"),
    "Cetirizine": ("호흡기감기", "비염알레르기"),
    "Cetirizine Dihydrochloride": ("호흡기감기", "비염알레르기"),
    "Fexofenadine": ("호흡기감기", "비염알레르기"),
    "Bilastine": ("호흡기감기", "비염알레르기"),
    "bilastine 20": ("호흡기감기", "비염알레르기"),
    "Telfast 180mg": ("호흡기감기", "비염알레르기"),
    "Chlorpheniramine": ("호흡기감기", "비염알레르기"),
    "Chlorpheniramine maleate": ("호흡기감기", "비염알레르기"),
    "Brompheniramine": ("호흡기감기", "비염알레르기"),
    "Hydroxyzine": ("호흡기감기", "비염알레르기"),
    "Diphenhydramine HCI": ("호흡기감기", "비염알레르기"),
    "Mepyramine": ("호흡기감기", "비염알레르기"),
    "Chlorphenoxamine": ("호흡기감기", "비염알레르기"),
    "Oxymetazoline": ("호흡기감기", "비염알레르기"),
    "Phenylephrine": ("호흡기감기", "비염알레르기"),
    "Phenylephrine HCl": ("호흡기감기", "비염알레르기"),
    "Naphazoline": ("호흡기감기", "비염알레르기"),
    "Interhistin": ("호흡기감기", "비염알레르기"),
    "Monas": ("호흡기감기", "비염알레르기"),
    "Nalgestan": ("호흡기감기", "종합감기"),
    "Exomuc 20mg": ("호흡기감기", "진해거담"),
    "Bisolvon": ("호흡기감기", "진해거담"),
    "Bisolvon Extra": ("호흡기감기", "진해거담"),
    "Terpin Hydrate": ("호흡기감기", "진해거담"),
    "Nellco": ("호흡기감기", "진해거담"),
    "Nelco": ("호흡기감기", "진해거담"),
    "Komix Jahe": ("호흡기감기", "진해거담"),
    "Obat Batuk Ibu dan Anak": ("호흡기감기", "진해거담"),
    "Vicks Vaporup": ("호흡기감기", "진해거담"),
    "Vicks Inhealer": ("호흡기감기", "진해거담"),
    "SPTroches": ("호흡기감기", "진해거담"),
    "Degirol": ("호흡기감기", "진해거담"),
    "Amylmetacresol": ("호흡기감기", "진해거담"),
    "Dichlorobenzyl Alcohol": ("호흡기감기", "진해거담"),
    "SERETIDE ACCU": ("호흡기감기", "기타호흡기"),
    "Antangin": ("호흡기감기", "한방감기"),
    "Madu TJ": ("호흡기감기", "한방감기"),
    "OB Herbal": ("호흡기감기", "한방감기"),
    "Fa Ta Lai Jone": ("호흡기감기", "한방감기"),
    "Andrographis Paniculata": ("호흡기감기", "한방감기"),
    "LANSOR": ("소화기", "제산궤양"),
    "Polycrol": ("소화기", "제산궤양"),
    "Sanmag": ("소화기", "제산궤양"),
    "Neosanmag": ("소화기", "제산궤양"),
    "Magnesium Trisilicate": ("소화기", "제산궤양"),
    "No Spa Forte 80mg": ("소화기", "기타소화"),
    "Alpha Choay 4200IU": ("소화기", "소화효소"),
    "Activated Charcoal": ("소화기", "기타소화"),
    "Kaolin": ("소화기", "지사제"),
    "Diatabs": ("소화기", "지사제"),
    "Antiflatulence": ("소화기", "기타소화"),
    "omidon": ("소화기", "기타소화"),
    "Norvom": ("소화기", "기타소화"),
    "Lacto-B": ("소화기", "기타소화"),
    "Curcuma Plus": ("소화기", "기타소화"),
    "Peptisol": ("소화기", "기타소화"),
    "Microlax": ("소화기", "기타소화"),
    "Cinnarizine": ("신경정신", "어지럼"),
    "Nautamine 90mg": ("신경정신", "어지럼"),
    "Antimo": ("신경정신", "어지럼"),
    "Antimo Anak": ("신경정신", "어지럼"),
    "Beklo": ("신경정신", "기타신경"),
    "Tolperisone": ("신경정신", "기타신경"),
    "Tolperisone Hydrochloride": ("신경정신", "기타신경"),
    "Orphenadrine Citrate": ("신경정신", "기타신경"),
    "Ergotamine": ("신경정신", "편두통"),
    "Selrotine": ("신경정신", "항우울항정신"),
    "valeriana officinalis": ("신경정신", "기타신경"),
    "Fluocinolone Acetonide": ("호르몬내분비", "스테로이드"),
    "Kenalog": ("호르몬내분비", "스테로이드"),
    "Obimin": ("피임산과", "산과기타"),
    "Sensitif Uji Kehamilan": ("피임산과", "산과기타"),
    "Andalan Ovulation Test": ("피임산과", "산과기타"),
    "Lactaboost": ("피임산과", "산과기타"),
    "BENEXOL B12": ("비타민영양", "종합비타민"),
    "Dicaltrol": ("비타민영양", "단일영양"),
    "Ferlatum 15ml": ("비타민영양", "단일영양"),
    "GlobiFer plus": ("비타민영양", "단일영양"),
    "CDR": ("비타민영양", "단일영양"),
    "CDR Fortos": ("비타민영양", "단일영양"),
    "Calcium Ascorbate": ("비타민영양", "단일영양"),
    "Vitamin CVitamin D plus": ("비타민영양", "종합비타민"),
    "Renovit Gold": ("비타민영양", "종합비타민"),
    "Zegavit": ("비타민영양", "종합비타민"),
    "Oxyvit": ("비타민영양", "종합비타민"),
    "Nusaplex": ("비타민영양", "종합비타민"),
    "Apialys Sirup": ("비타민영양", "종합비타민"),
    "Apialys Drop": ("비타민영양", "종합비타민"),
    "Curvit": ("비타민영양", "종합비타민"),
    "Livron": ("비타민영양", "단일영양"),
    "Imunped": ("비타민영양", "면역건강"),
    "Neurodex": ("비타민영양", "종합비타민"),
    "Ever E250": ("비타민영양", "단일영양"),
    "Cal-95": ("비타민영양", "단일영양"),
    "Vitabumin": ("비타민영양", "단일영양"),
    "Cerebrofort": ("비타민영양", "종합비타민"),
    "Nephrisol-D": ("비타민영양", "단일영양"),
    "Sporal 100mg": ("항균항바이러스", "항진균"),
    "Mycoral": ("항균항바이러스", "항진균"),
    "Mycostatin": ("항균항바이러스", "항진균"),
    "Nocandis": ("항균항바이러스", "항진균"),
    "Bifonazole": ("항균항바이러스", "항진균"),
    "Combantrin": ("항균항바이러스", "기타항균"),
    "Combantrin Jeruk": ("항균항바이러스", "기타항균"),
    "Nifuroxazide": ("항균항바이러스", "기타항균"),
    "Gentamicin": ("항균항바이러스", "기타항균"),
    "Gentamicin Sulfate": ("항균항바이러스", "기타항균"),
    "Neomycin Sulfate": ("항균항바이러스", "기타항균"),
    "Polymyxin B Sulfate": ("항균항바이러스", "기타항균"),
    "Clavulanic Acid": ("항균항바이러스", "베타락탐"),
    "Ace XR": ("해열진통소염", "기타진통"),
    "Parol": ("해열진통소염", "Paracetamol계"),
    "Dumin": ("해열진통소염", "Paracetamol계"),
    "Naprex": ("해열진통소염", "NSAID"),
    "Proris": ("해열진통소염", "NSAID"),
    "Pirocam": ("해열진통소염", "NSAID"),
    "Neorheumacyl Neuro": ("해열진통소염", "NSAID"),
    "Benzydamine": ("해열진통소염", "NSAID"),
    "Coparcetin": ("해열진통소염", "기타진통"),
    "ByeBye Fever": ("해열진통소염", "기타진통"),
    "Calamine": ("피부외용", "기타외용"),
    "Benzoyl Peroxide": ("피부외용", "기타외용"),
    "Permethrin": ("피부외용", "기타외용"),
    "Salep 88": ("피부외용", "기타외용"),
    "Pi Kang Shuang": ("피부외용", "기타외용"),
    "Prodermis": ("피부외용", "기타외용"),
    "Pasquam": ("피부외용", "기타외용"),
    "Gentrison": ("피부외용", "스테로이드외용"),
    "Rohto": ("피부외용", "기타외용"),
    "Rohto Dry Fresh": ("피부외용", "기타외용"),
    "Cendo Eyefresh": ("피부외용", "기타외용"),
    "Cendo Protagenta": ("피부외용", "기타외용"),
    "Minosep": ("피부외용", "위생화장품"),
    "Minosep Hijau": ("피부외용", "위생화장품"),
    "Y-rins": ("피부외용", "위생화장품"),
    "Sabun JF": ("피부외용", "위생화장품"),
    "Noroid": ("피부외용", "기타외용"),
    "Salicyl Talk": ("피부외용", "기타외용"),
    "Nebacetin": ("피부외용", "기타외용"),
    "Alco": ("피부외용", "위생화장품"),
    "Alcoplus": ("피부외용", "위생화장품"),
    "Safecare": ("피부외용", "파스외용"),
    "Safecare Strong": ("피부외용", "파스외용"),
    "Medicated Oil": ("피부외용", "파스외용"),
    "Tolnaftate": ("피부외용", "항진균외용"),
    "Iodochlorhydroxyquin": ("피부외용", "항진균외용"),
    "Lodochlorhydroxyquin": ("피부외용", "항진균외용"),
    "Cefixine": ("항균항바이러스", "세팔로스포린"),
    "RENNIE": ("소화기", "제산궤양"),
    "IBURAMINCOLD": ("호흡기감기", "종합감기"),
    "Antazoline": ("호흡기감기", "비염알레르기"),
    "Antazoline HCl": ("호흡기감기", "비염알레르기"),
    "Tetryzoline": ("호흡기감기", "비염알레르기"),
    "Tetryzoline HCl": ("호흡기감기", "비염알레르기"),
    "Plossa": ("피부외용", "파스외용"),
    "Tolak Linu Herbal": ("호흡기감기", "한방감기"),
}


def classify(name: str):
    low = fold(name)

    if re.fullmatch(r"\d{9}", name):
        return "한국식약처코드", "식약처품목허가번호"

    m = re.match(r"^(authentic|counterfeit)[\s\-_*]*", name, re.I)
    if m:
        stem = name[m.end():].strip(" -_*")
        stem = re.sub(r"\s+", " ", stem)
        return "정품위조", stem

    if contains_any(low, ["counterpain", "salonpas", "ben-gay", "hansaplast", "handsaplast"]) or "신신파스" in name:
        return "피부외용", mid_for_topical(low, name)

    if contains_any(low, ["nautamine", "antimo"]):
        return "신경정신", "어지럼"

    if "ketokonazole cream" in low or re.search(r"clotrimazol\w*\s+cream", low):
        return "피부외용", "항진균외용"

    if "seretide" in low:
        return "호흡기감기", "기타호흡기"

    if contains_any(low, [
        "metformin", "glimepiride", "glipizide", "gliclazide",
        "glibenclamide", "gliquidone", "sitagliptin", "voglibose",
        "glycediab", "linatin", "diabetes",
    ]):
        return "당뇨", mid_for_inn_or_brand(low, DIABETES_INNS)

    if contains_any(low, [
        "amlodipine", "amlopine", "losartan", "telmisartan", "captopril",
        "ramipril", "enalapril", "bisoprolol", "atenolol", "propranolol",
        "prenolol", "nifelat", "cilacar", "manidipine", "isosorbide",
        "furosemide", "hidroklorotiazid", "hydrochlorothiazide",
        "betacor", "pencor", "olmetime", "metildopa", "methyldopa",
        "agidopa", "hipertensi",
    ]):
        return "순환기", mid_for_inn_or_brand(low, CARDIO_INNS)

    if contains_any(low, [
        "paracetamol", "panadol", "crocin", "calpol", "dolo", "tylenol",
        "tylolhot", "pamol", "biogesic", "biolgesic", "sumagesic",
        "novagesic", "fasidol", "pacetik", "mirasic", "sanmol",
        "ibuprofen", "naproxen", "diclofenac", "mefenamic", "meloxicam",
        "piroxicam", "celecoxib", "etoricoxib", "etoricoxid", "aspirin",
        "ecosprine", "apranax", "dolorex", "arveles", "majez", "cataflam",
        "voltaren", "poldan", "inza", "ponstan", "xidolac",
    ]) or "타이레놀" in name or "판피린" in name:
        return "해열진통소염", mid_for_pain(low, name)

    if contains_any(low, [
        "neozep", "neozap", "bioflu", "decolgen", "medicol", "mixagrip",
        "ultraflu", "sanaflu", "actifed", "cheston", "coldaway", "a-ferin",
        "iburamin", "intunal", "bodrex", "procold", "obh", "tolak angin",
        "laserin", "cofsils", "ambroxol", "bromhexine", "guaifenesin",
        "dextromethorphan", "acetylcysteine", "carbocisteine", "theophylline",
        "albuterol", "mucopect", "transpulmin", "pectorin", "paratusin",
        "oskadon", "saridon", "paramex", "fluanza",
    ]) or "판콜" in name or re.search(r"\bmucos\b", low):
        return "호흡기감기", mid_for_resp(low, name)

    if contains_any(low, [
        "amoxicillin", "augmentin", "cefixim", "cefixin", "cef-3", "azithromycin",
        "azee", "ciprofloxacin", "clindamycin", "metronidazol", "doxycycl",
        "ampicillin", "dicloxacillin", "norfloxacin", "roxithromycin",
        "fluconazol", "ketoconazol", "ketokonazol", "clotrimazol",
        "itraconazol", "itrabat", "moxifloxacin", "penicillin",
        "phenoxymethyl", "sefloc", "sulorim", "lostracef", "impurin",
        "kalmicetine", "chloramphenicol", "thiamphenicol", "oxytetracycline",
        "tinidazole", "nitrofurazone", "mupirocin", "acyclovir",
    ]):
        return "항균항바이러스", mid_for_abx(low)

    if contains_any(low, [
        "simethicone", "mylanta", "gaviscon", "rennie", "promag",
        "polysilane", "omeprazole", "lomac", "esoral", "dexilend",
        "famotidine", "loperamide", "entrostop", "diapet", "domperidone",
        "hyoscine", "mebeverine", "pancreatin", "sucralfate", "plantacid",
        "lambucid", "dulcolax", "lactulax", "aluminium hydroxide",
        "aluminum hydroxide", "magnesium hydroxide", "dioctahedral",
        "smectite",
    ]) or "베아제" in name or "훼스탈" in name:
        return "소화기", mid_for_gi(low, name)

    if contains_any(low, [
        "pregabalin", "pregaba", "gabapentin", "lorazepam", "clorazepate",
        "amitriptyline", "tryptin", "fluoxetine", "aripiprazole", "tramadol",
        "sumatriptan", "eletriptan", "flunarizine", "betahistine",
        "diphenidol", "dimenhydrinate", "colchicine", "allopurinol",
        "epiclon", "flavoxate",
    ]):
        return "신경정신", mid_for_neuro(low)

    if contains_any(low, [
        "levothyroxine", "thyroxine", "methimazole", "prednison",
        "hydrocortisone", "betamethasone", "triamcinolone", "utrogestan",
        "cyclogest", "valiera", "femara", "misoprostol", "desoximetasone",
        "mometasone", "clobetasol", "budesonide", "fluticasone", "salmeterol",
    ]):
        return "호르몬내분비", mid_for_hormone(low)

    if contains_any(low, [
        "mercilon", "marvelon", "fluomizin", "neotergynan", "pregnabion",
        "folamil", "prenatal", "ovulation", "kehamilan",
    ]):
        return "피임산과", mid_for_obgyn(low)

    if contains_any(low, [
        "berocca", "vitabion", "cevit", "folison", "folacid", "calci",
        "kalcoral", "coledan", "devit", "ipi vit", "enervon", "redoxon",
        "neurobion", "sangobion", "natur-e", "vitamin", "calcium", "folic",
        "biotin", "taurine", "imboost", "stimuno", "sakatonik", "tonikum",
        "scotts", "prove d3", "holisti", "becom", "caviplex", "vitacimin",
        "vicee", "neurotropic", "neurosanbe",
    ]):
        return "비타민영양", mid_for_vit(low)

    if contains_any(low, [
        "canesten", "salonpas", "ben-gay", "hansaplast", "handsaplast",
        "freshcare", "minyak", "callusol", "dermatix", "polident",
        "tretinoin", "minoxidil", "counterpain", "koyo", "balsem", "hotin",
        "daktarin", "betadine", "dettol", "selsun", "bio-oil", "lactacyd",
        "sterimar", "bepanthen", "herocyn", "caladine", "zambuk", "gpu",
        "peditox", "cooling 5", "vital ear",
    ]) or "신신파스" in name:
        return "피부외용", mid_for_topical(low, name)

    if name in EXTRA:
        return EXTRA[name]
    for k, v in EXTRA.items():
        if k.lower() == low:
            return v

    return "기타", mid_for_etc(low, name)


def apply_remap(raw_classes: dict, remap: dict) -> dict:
    drop = set(remap["drop"])
    merge = remap["merge"]
    out = {}
    for name, cnt in raw_classes.items():
        if name in drop:
            continue
        new = merge.get(name, name)
        out[new] = out.get(new, 0) + cnt
    return out


def build(classes: dict) -> dict:
    assigned = {}
    unmapped = []
    for name, cnt in classes.items():
        major, mid = classify(name)
        if major not in MAJORS_ORDER:
            unmapped.append(name)
            major, mid = "기타", "브랜드미분류"
        assigned[name] = (major, mid, cnt)

    tree = {m: defaultdict(list) for m in MAJORS_ORDER}
    for name, (major, mid, cnt) in assigned.items():
        tree[major][mid].append({"name": name, "count": cnt})

    majors = []
    for mname in MAJORS_ORDER:
        mids_map = tree[mname]
        mid_names = list(mids_map.keys())
        preferred = MIDS_ORDER.get(mname)
        if preferred:
            mid_names_sorted = [x for x in preferred if x in mids_map]
            mid_names_sorted += sorted(
                [x for x in mid_names if x not in preferred],
                key=lambda x: (-sum(c["count"] for c in mids_map[x]), x),
            )
        else:
            mid_names_sorted = sorted(
                mid_names,
                key=lambda x: (x == "브랜드", -sum(c["count"] for c in mids_map[x]), x),
            )
        mids = []
        for mid in mid_names_sorted:
            items = sorted(mids_map[mid], key=lambda x: (-x["count"], x["name"]))
            mids.append({
                "name": mid,
                "n_classes": len(items),
                "n_instances": sum(c["count"] for c in items),
                "classes": items,
            })
        majors.append({
            "name": mname,
            "n_classes": sum(m["n_classes"] for m in mids),
            "n_instances": sum(m["n_instances"] for m in mids),
            "mids": mids,
        })

    return {
        "n_classes": len(classes),
        "n_instances": sum(classes.values()),
        "majors": majors,
        "unmapped_check": unmapped,
    }


def pct(n, d):
    return 0.0 if d == 0 else 100.0 * n / d


def write_md(tax: dict, path: Path) -> None:
    n_cls = tax["n_classes"]
    n_ins = tax["n_instances"]
    lines = []
    lines.append("# 의약품 포장 클래스 3단계 분류체계")
    lines.append("")
    lines.append(
        f"리맵 후 **{n_cls}개** 소분류(클래스)를 **14개 대분류**로 나눴다. "
        f"인스턴스 합계는 {n_ins:,}건이다. 소분류 이름은 리맵 후 클래스명 그대로이다."
    )
    lines.append("")
    lines.append("## 대분류 요약")
    lines.append("")
    lines.append("| 대분류 | 클래스수 | 인스턴스 | 클래스비율 | 인스턴스비율 |")
    lines.append("|---|---:|---:|---:|---:|")
    for m in tax["majors"]:
        lines.append(
            f"| {m['name']} | {m['n_classes']} | {m['n_instances']:,} | "
            f"{pct(m['n_classes'], n_cls):.1f}% | {pct(m['n_instances'], n_ins):.1f}% |"
        )
    lines.append(
        f"| **합계** | **{n_cls}** | **{n_ins:,}** | **100%** | **100%** |"
    )
    lines.append("")

    etc = next(m for m in tax["majors"] if m["name"] == "기타")
    if pct(etc["n_classes"], n_cls) >= 30:
        lines.append(
            f"> **주의:** 기타가 클래스의 {pct(etc['n_classes'], n_cls):.1f}% "
            f"({etc['n_classes']}/{n_cls})로 30%를 넘는다. "
            "성분명만·미확인 브랜드·비의약품이 섞여 있다. 다음 라운드에서 중분류를 더 쪼개거나 "
            "브랜드 사전을 보강하는 편이 좋다."
        )
        lines.append("")
    else:
        lines.append(
            f"기타는 클래스 {etc['n_classes']}개({pct(etc['n_classes'], n_cls):.1f}%), "
            f"인스턴스 {etc['n_instances']:,}건({pct(etc['n_instances'], n_ins):.1f}%)이다."
        )
        lines.append("")

    lines.append("## 대분류별 중분류")
    lines.append("")
    for m in tax["majors"]:
        lines.append(f"### {m['name']}")
        lines.append("")
        lines.append(
            f"클래스 {m['n_classes']}개, 인스턴스 {m['n_instances']:,}건 "
            f"(전체 클래스 {pct(m['n_classes'], n_cls):.1f}%)."
        )
        lines.append("")
        lines.append("| 중분류 | 클래스수 | 인스턴스 | 소분류 예시 |")
        lines.append("|---|---:|---:|---|")
        for mid in m["mids"]:
            examples = ", ".join(c["name"] for c in mid["classes"][:5])
            if mid["n_classes"] > 5:
                examples += " …"
            lines.append(
                f"| {mid['name']} | {mid['n_classes']} | {mid['n_instances']:,} | {examples} |"
            )
        lines.append("")

    lines.append("## 분류 메모")
    lines.append("")
    lines.append("- 우선순위: 식약처 9자리 숫자 → 정품/위조 → 당뇨 → 순환기 → 해열진통 → 호흡기 → 항균 → 소화기 → 신경정신 → 호르몬 → 피임산과 → 비타민 → 피부외용 → 기타.")
    lines.append("- Counterpain / Salonpas / 신신파스 / BEN-GAY / Handsaplast는 해열진통이 아니라 피부외용(파스)으로 둔다.")
    lines.append("- Nautamine·Antimo는 멀미약이므로 소화기가 아니라 신경정신(어지럼)으로 둔다.")
    lines.append("- Allopurinol·Colchicine은 통풍으로 신경정신 중분류에 둔다.")
    lines.append("- SERETIDE 같은 복합 흡입제는 호흡기감기, 단독 스테로이드/살메테롤은 호르몬내분비.")
    lines.append("- 한국식약처코드는 약 정체를 추정하지 않고 `식약처품목허가번호` 하나로만 묶는다.")
    lines.append("- 애매한 브랜드는 기타/브랜드미분류로 보수적으로 둔다.")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main():
    raw = json.loads((ROOT / "classes.json").read_text())["classes"]
    remap = json.loads((ROOT / "remap.json").read_text())
    classes = apply_remap(raw, remap)
    tax = build(classes)

    out = {
        "n_classes": tax["n_classes"],
        "majors": tax["majors"],
        "unmapped_check": tax["unmapped_check"],
    }
    (ROOT / "taxonomy.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    write_md(tax, ROOT / "TAXONOMY.md")

    print("n_classes=%s n_instances=%s" % (tax["n_classes"], tax["n_instances"]))
    print("unmapped_check=%s" % tax["unmapped_check"])
    print()
    print("%-16s %5s %8s" % ("major", "cls", "inst"))
    for m in tax["majors"]:
        print("%-16s %5d %8d" % (m["name"], m["n_classes"], m["n_instances"]))
    print()
    etc = next(m for m in tax["majors"] if m["name"] == "기타")
    print("=== 기타 detail ===")
    for mid in etc["mids"]:
        print("  [%s] %d cls / %d inst" % (mid["name"], mid["n_classes"], mid["n_instances"]))
        for c in mid["classes"]:
            print("    %5d  %s" % (c["count"], c["name"]))


if __name__ == "__main__":
    main()
