# medicine-packaging-merged-v2 data-quality report

Project: `toyproject1/medicine-packaging-merged-v2` (object-detection).
Computed from Roboflow `projects_get` class counts and splits.
No training. Project was not modified.

## Headline numbers

| metric | value |
| --- | --- |
| n_images | 28297 |
| unannotated | 0 |
| train / valid / test | 22890 / 2984 / 2423 |
| split percents | 80.89% / 10.55% / 8.56% |
| n_classes | 758 |
| total annotation instances | 51520 |
| annotations per image | 1.821 |
| MFDS 9-digit classes | 53 |
| Korean Hangul classes | 7 |
| noise/non-medicine candidate classes | 142 (3662 instances) |
| case-collision groups | 8 |
| Box/Blister/Pack multi-form groups | 27 |
| Authentic/Counterfeit groups | 6 |

## Splits

| split | n_images | percent |
| --- | --- | --- |
| train | 22890 | 80.89% |
| valid | 2984 | 10.55% |
| test | 2423 | 8.56% |
| **sum** | 28297 | 100.00% |

## Class-count distribution

| stat | instances per class |
| --- | --- |
| min | 1 |
| p25 | 2.00 |
| median | 17.00 |
| p75 | 91.00 |
| max | 1353 |
| mean | 67.97 |

| bucket | n_classes | % of classes | n_instances |
| --- | --- | --- | --- |
| 1 | 114 | 15.0% | 114 |
| 2-5 | 184 | 24.3% | 527 |
| 6-20 | 96 | 12.7% | 1067 |
| 21-100 | 188 | 24.8% | 11006 |
| 101-500 | 166 | 21.9% | 30216 |
| 500+ | 10 | 1.3% | 8590 |

Long tail is severe: **114 classes have a single instance** (15.0% of classes) and 298 classes have ≤5 instances (39.3%).

## Top 20 classes by instance count

| rank | class | count | % of instances |
| --- | --- | --- | --- |
| 1 | Back | 1353 | 2.63% |
| 2 | Paracetamol | 1142 | 2.22% |
| 3 | Amlodipine | 1066 | 2.07% |
| 4 | Front | 889 | 1.73% |
| 5 | Crocin | 840 | 1.63% |
| 6 | Metformin | 755 | 1.47% |
| 7 | Allopurinol | 690 | 1.34% |
| 8 | Naproxen | 666 | 1.29% |
| 9 | Glimepiride | 624 | 1.21% |
| 10 | Simethicone | 565 | 1.10% |
| 11 | Telmisartan | 477 | 0.93% |
| 12 | Losartan | 458 | 0.89% |
| 13 | Isosorbide Dinitrate | 452 | 0.88% |
| 14 | Calpol | 436 | 0.85% |
| 15 | Glipizide | 431 | 0.84% |
| 16 | Dicloxacillin | 418 | 0.81% |
| 17 | Tumeric 500 | 410 | 0.80% |
| 18 | Dolo-650 | 391 | 0.76% |
| 19 | sefloc | 386 | 0.75% |
| 20 | Simvastatin | 385 | 0.75% |

`Front` + `Back` alone are 2242 instances (4.35% of all annotations) and are view labels, not medicines.

## Bottom 30 classes (long-tail / likely noise)

| class | count |
| --- | --- |
| Andalan Ovulation Test | 1 |
| Antiflatulence | 1 |
| Bepanthen | 1 |
| Bio-Oil | 1 |
| Biolgesic Paracetamol | 1 |
| Bodrexin | 1 |
| CIPROFLOXACIN | 1 |
| Cal-95 | 1 |
| Carbamate Insecticides | 1 |
| Citrate Dihydrate | 1 |
| Combantrin | 1 |
| Counterpain Cool | 1 |
| Curvit | 1 |
| Diapet | 1 |
| Dichlorobenzyl Alcohol | 1 |
| Dipsamol | 1 |
| Dulcolax | 1 |
| Durex Extra Safe | 1 |
| Durex Extra Safe 12 | 1 |
| Durex Invisible 3 | 1 |
| Durex Performa 3 | 1 |
| Elzsa | 1 |
| Ever E250 | 1 |
| Fiesta Banana 3 | 1 |
| Fiesta Black Coffee 3 | 1 |
| Fiesta Bubble Gum 3 | 1 |
| Fiesta Delay 3 | 1 |
| Fiesta Grape 3 | 1 |
| Fiesta Party Pack 12 | 1 |
| Fiesta Strawberry 12 | 1 |

All 30 are singletons. Many are condom SKUs, toiletries, incomplete names, or one-off brand fragments — not usable as a medicine-pack taxonomy.

## Case-collision pairs

Same string ignoring case, different Roboflow class IDs. Examples called out in the brief: Losartan/losartan, Ibuprofen/ibuprofen, Metformin/metformin.

| normalized | n_variants | combined | variants |
| --- | --- | --- | --- |
| metformin | 2 | 817 | Metformin (755), metformin (62) |
| losartan | 2 | 677 | Losartan (458), losartan (219) |
| ibuprofen | 2 | 429 | Ibuprofen (226), ibuprofen (203) |
| ketoconazole | 2 | 346 | Ketoconazole (255), ketoconazole (91) |
| hydrocortisone | 2 | 146 | hydrocortisone (131), Hydrocortisone (15) |
| poldan mig | 2 | 101 | Poldan MIG (100), Poldan Mig (1) |
| propolis extract | 2 | 18 | Propolis Extract (17), Propolis extract (1) |
| licorice extract | 2 | 4 | Licorice Extract (3), Licorice extract (1) |

## Near-duplicate groups

### Box vs Blister vs Pack (same drug stem)

27 stems have 2+ of `_Box` / `_Blister` / `_Pack`. These should usually be one product class (or an explicit form attribute), not separate SKUs.

| stem | n_forms | combined | counts |
| --- | --- | --- | --- |
| Marvelon | 2 | 152 | Box=90; Blister=—; Pack=62 |
| Pac-Control | 2 | 136 | Box=86; Blister=—; Pack=50 |
| Cefixim 200mg | 2 | 136 | Box=90; Blister=46; Pack=— |
| Doxycyclin 100mg | 2 | 132 | Box=82; Blister=50; Pack=— |
| Augmentin 1g | 2 | 130 | Box=93; Blister=—; Pack=37 |
| Voltaren 100mg | 2 | 129 | Box=88; Blister=41; Pack=— |
| No Spa Forte 80mg | 2 | 127 | Box=84; Blister=43; Pack=— |
| Mercilon | 2 | 125 | Box=87; Blister=—; Pack=38 |
| Nabifar 5g | 2 | 124 | Box=82; Blister=—; Pack=42 |
| Cyclogest 400mg | 2 | 124 | Box=77; Blister=47; Pack=— |
| GlobiFer plus | 2 | 123 | Box=82; Blister=41; Pack=— |
| Nautamine 90mg | 2 | 122 | Box=82; Blister=—; Pack=40 |
| Metronidazol 250mg | 2 | 121 | Box=73; Blister=48; Pack=— |
| Fluomizin 10mg | 2 | 120 | Box=71; Blister=49; Pack=— |
| Daikyn 0.5mg | 2 | 120 | Box=80; Blister=40; Pack=— |
| Cataflam 50mg | 2 | 120 | Box=71; Blister=49; Pack=— |
| Calci Briozcal Tablets | 2 | 118 | Box=74; Blister=44; Pack=— |
| Folacid 5mg | 2 | 116 | Box=87; Blister=29; Pack=— |
| Sporal 100mg | 2 | 116 | Box=74; Blister=42; Pack=— |
| Valiera 2mg | 2 | 115 | Box=74; Blister=41; Pack=— |
| Aspirin 81mg | 2 | 109 | Box=79; Blister=30; Pack=— |
| Neotergynan | 2 | 103 | Box=67; Blister=—; Pack=36 |
| Misoprostol200 | 2 | 99 | Box=68; Blister=31; Pack=— |
| Telfast 180mg | 2 | 97 | Box=65; Blister=32; Pack=— |
| Exomuc 20mg | 2 | 97 | Box=62; Blister=—; Pack=35 |
| Lomac 20mg | 2 | 96 | Box=67; Blister=29; Pack=— |
| Prednison 5mg | 2 | 92 | Box=64; Blister=28; Pack=— |

### Authentic-X vs Counterfeit-X

| stem | authentic | counterfeit | plain leftover | combined |
| --- | --- | --- | --- | --- |
| Decolgen | Authentic-Decolgen (200) | Counterfeit-Decolgen (170) | Decolgen (68) | 438 |
| Medicol Advance | Authentic -Medicol Advance (44) | Counterfeit-Medicol Advance (357) | — | 401 |
| Biogesic | Authentic_Biogesic (274) | Counterfeit_Biogesic (113) | Biogesic (2) | 389 |
| Alaxan | Authentic-Alaxan (181) | Counterfeit-Alaxan (202) | — | 383 |
| Neozep Forte | Authentic-Neozep Forte (170) | Counterfeit-Neozep Forte (201) | Neozep Forte (3) | 374 |
| Bioflu | Authentic-Bioflu (149) | Counterfeit-Bioflu (192) | — | 341 |

Separator inconsistency: hyphen (`Authentic-Alaxan`), underscore (`Authentic_Biogesic`), and spaced hyphen (`Authentic -Medicol Advance`).

### Korean Hangul vs English (same product)

7 Hangul class names, 485 instances. Only 타이레놀 has a clear English twin (`Tylenol`).

| korean | count | english / related | note |
| --- | --- | --- | --- |
| 타이레놀 | 113 | Tylenol (228), TYLOLHOT (48) | Same acetaminophen brand family (Tylenol / 타이레놀). |
| 베아제정 | 65 | 닥터베아제정 (68) | Bearse digestive tablets; 닥터베아제정 is a sibling SKU, no English class. |
| 닥터베아제정 | 68 | 베아제정 (65) | Doctor Bearse; sibling of 베아제정. |
| 훼스탈플러스정 | 48 | — | Festal Plus; no English class present. |
| 신신파스 아렉스 | 86 | — | Sinsinpas Arex plaster; no English class present. |
| 판피린티정 | 41 | — | Panpyrin-T; no English class present. |
| 판콜에이내복액 | 64 | — | Pancol-A liquid; no English class present. |

Hangul classes:

| class | count |
| --- | --- |
| 타이레놀 | 113 |
| 신신파스 아렉스 | 86 |
| 닥터베아제정 | 68 |
| 베아제정 | 65 |
| 판콜에이내복액 | 64 |
| 훼스탈플러스정 | 48 |
| 판피린티정 | 41 |

### Other spelling / brand families (extra, not in the three requested patterns)

| group | combined | members | note |
| --- | --- | --- | --- |
| Neozep/Neozap Forte | 162 | Neozep Forte (3), Neozap Forte (159) | Likely same brand, spelling drift |
| Cefixime family | 387 | Cefixime (215), Cefixim 200mg_Box (90), Cefixim 200mg_Blister (46), Cefixine (36) | Same API, three spellings + form split |
| Ketoconazole family | 348 | Ketoconazole (255), ketoconazole (91), Ketokonazole (1), Ketokonazole Cream (1) | Case + spelling (k/c) + cream SKU |
| Etoricoxib | 72 | Etoricoxib (59), Etoricoxid (13) | Spelling typo |
| Biogesic | 390 | Biogesic (2), Authentic_Biogesic (274), Counterfeit_Biogesic (113), Biolgesic Paracetamol (1) | Auth/counterfeit plus typo Biolgesic |
| Hansaplast | 4 | Hansaplast (2), Handsaplast Koyo Panas (2) | Brand typo + plaster (toiletry-adjacent) |
| Nellco/Nelco | 7 | Nellco (6), Nelco (1) | Spelling drift |
| Aluminum hydroxide | 64 | Aluminium Hydroxide (61), Aluminum Hydroxide (3) | UK/US spelling; ingredient-only |
| Panadol family | 376 | Panadol (4), Panadol Paracetamol (120), Panadol Extra Paracetamol (97), Panadol Extra (7), Panadol Cold Flu (138), Panadol Flu Batuk (7), Panadol Anak (3) | Same brand fragmented across SKUs/languages |
| Amlodipine family | 1762 | Amlodipine (1066), amlopine (280), amlodipine 5mg hipertensi (196), amlodipine 10mg hipertensi (220) | Generic + dose/indication + typo amlopine |
| Metformin family | 1123 | Metformin (755), metformin (62), metformin 500mg diabetes (194), metformin 850mg diabetes (112) | Case collision plus dose-split Indonesian labels |
| Losartan family | 727 | Losartan (458), losartan (219), Losartan Potassium (50) | Case collision plus salt form |
| Ibuprofen | 429 | Ibuprofen (226), ibuprofen (203) | Pure case collision |
| Glimepiride family | 1244 | Glimepiride (624), glimepiride 1mg diabetes (116), glimepiride 2mg diabetes (220), glimepiride 3mg diabetes (142), glimepiride 4mg diabetes (142) | Generic plus Indonesian dose/indication splits |

## Noise / non-medicine class candidates

**142 classes / 3662 instances** flagged. Heuristics: condom brand needles (Durex, Fiesta, Sutra, Kondom); explicit `Front` / `Back` / `Polident` / `Medicine-detection`; pregnancy tests; toiletries (shampoo/soap/oil/plaster/mouthwash-like); obvious ingredient-only / botanical / excipient labels that are not pack SKUs; degenerate label `su`.

| family | n_classes | n_instances |
| --- | --- | --- |
| explicit | 4 | 2251 |
| ingredient-only | 70 | 1128 |
| degenerate-label | 1 | 129 |
| toiletry | 39 | 115 |
| condom | 26 | 36 |
| pregnancy-test | 2 | 3 |

| class | count | reasons |
| --- | --- | --- |
| Back | 1353 | explicit:Back |
| Front | 889 | explicit:Front |
| su | 129 | degenerate-label |
| Eugenol | 125 | ingredient-only |
| Methyl Salicylate | 123 | ingredient-only |
| Levomenthol | 104 | ingredient-only |
| Menthol | 63 | ingredient-only |
| Aluminium Hydroxide | 61 | ingredient-only |
| Aescin | 51 | ingredient-only |
| Zinc | 47 | ingredient-only |
| Salol and Menthol | 38 | ingredient-only |
| Cassia Siamea | 36 | ingredient-only |
| Calcium | 32 | ingredient-only |
| Camphor | 29 | ingredient-only |
| Magnesium Hydroxide | 29 | ingredient-only |
| Clavulanic Acid | 22 | ingredient-only |
| Escin | 19 | ingredient-only |
| Eucalyptus oil | 19 | ingredient-only |
| Quercetin | 19 | ingredient-only |
| Magnesium Trisilicate | 17 | ingredient-only |
| Propolis Extract | 17 | ingredient-only |
| Kaolin | 16 | ingredient-only |
| Activated Charcoal | 15 | ingredient-only |
| Andrographis Paniculata | 15 | ingredient-only |
| Asafoetida and Alcohol | 15 | ingredient-only |
| L-cysteine | 14 | ingredient-only |
| Taurine | 14 | ingredient-only |
| Herocyn | 13 | toiletry:herocyn |
| Minyak Tawon | 12 | toiletry:minyak |
| Strong Ginger Tincture | 12 | ingredient-only |
| Caffeine | 10 | ingredient-only |
| Compound Cardamom Tincture | 10 | ingredient-only |
| Strong Capsicum Tincture | 10 | ingredient-only |
| Vitamin C | 9 | ingredient-only |
| Balsem Otot Geliga | 8 | toiletry:balsem |
| Chamomile Extract | 8 | ingredient-only |
| Dioctahedral smectite | 8 | ingredient-only |
| Hydroxypropyl Methylcellulose | 8 | ingredient-only |
| Polident | 8 | explicit:Polident |
| Lemon Bioflavonoid Complex | 7 | ingredient-only |
| Marigold Extract | 7 | ingredient-only |
| MyBaby Minyak Telon | 7 | toiletry:minyak |
| Phenyl Salicylate | 7 | ingredient-only |
| Biotin | 6 | ingredient-only |
| Calcium Ascorbate | 5 | ingredient-only |
| Coptis Chinensis | 5 | ingredient-only |
| Minyak Angin Cap Kapak | 5 | toiletry:minyak |
| Pontirus Trifoliata | 5 | ingredient-only |
| Smilax Glabra | 5 | ingredient-only |
| Vitamin B group | 5 | ingredient-only |
| Alumine | 4 | ingredient-only |
| Collagen | 4 | ingredient-only |
| Dettol | 4 | toiletry:dettol |
| Freshcare Hot | 4 | toiletry:freshcare |
| Lecithin | 4 | ingredient-only |
| Magnesia | 4 | ingredient-only |
| Sabun JF | 4 | toiletry:sabun |
| Vicks Vaporup | 4 | toiletry:vicks |
| Aluminum Hydroxide | 3 | ingredient-only |
| Freshcare Lavender | 3 | toiletry:freshcare |
| Freshcare Smash | 3 | toiletry:freshcare |
| Lactacyd Baby | 3 | toiletry:lactacyd |
| Licorice Extract | 3 | ingredient-only |
| Lonicera japonica | 3 | ingredient-only |
| Medicated Oil | 3 | toiletry:medicated oil |
| Mentha oil | 3 | ingredient-only |
| Mucopolysaccharide | 3 | ingredient-only |
| Spearmint oil | 3 | ingredient-only |
| Sutra 12 | 3 | condom:sutra |
| Sutra 3 | 3 | condom:sutra |
| Sutra OK 12 | 3 | condom:sutra |
| Vital Ear Oil | 3 | toiletry:vital ear oil |
| Balsem lang | 2 | toiletry:balsem |
| Bepanthen Baby | 2 | toiletry:bepanthen baby |
| Betadine Feminime Hygiene | 2 | toiletry:feminime |
| Bilberry Extract | 2 | ingredient-only |
| Caladine | 2 | toiletry:caladine |
| Chloride | 2 | ingredient-only |
| Durex Close Fit 3 | 2 | condom:durex |
| Fiesta Durian 3 | 2 | condom:fiesta |
| Folic Acid | 2 | ingredient-only |
| Freshcare Citrus | 2 | toiletry:freshcare |
| Freshcare Kayu Putih | 2 | toiletry:freshcare |
| Handsaplast Koyo Panas | 2 | toiletry:handsaplast |
| Hansaplast | 2 | toiletry:hansaplast |
| Kondom Andalan 12 | 2 | condom:kondom |
| Koyo Cabe | 2 | toiletry:koyo |
| Lonrcera Japonica | 2 | ingredient-only |
| Minyak Kayu Putih Cap Ayam | 2 | toiletry:minyak |
| Minyak Kayu Putih Sierra | 2 | toiletry:minyak |
| Minyak Telon Lang | 2 | toiletry:minyak |
| Polyethylene Glycol | 2 | ingredient-only |
| Povidone | 2 | ingredient-only |
| Propylene Glycol | 2 | ingredient-only |
| Selsun | 2 | toiletry:selsun |
| Sensitif Uji Kehamilan | 2 | pregnancy-test |
| Sutra Gerigi 12 | 2 | condom:sutra |
| Zambuk | 2 | toiletry:zambuk |
| valeriana officinalis | 2 | ingredient-only |
| Andalan Ovulation Test | 1 | pregnancy-test |
| Antiflatulence | 1 | ingredient-only |
| Bio-Oil | 1 | toiletry:bio-oil |
| Carbamate Insecticides | 1 | ingredient-only |
| Citrate Dihydrate | 1 | ingredient-only |
| Dichlorobenzyl Alcohol | 1 | ingredient-only |
| Durex Extra Safe | 1 | condom:durex |
| Durex Extra Safe 12 | 1 | condom:durex |
| Durex Invisible 3 | 1 | condom:durex |
| Durex Performa 3 | 1 | condom:durex |
| Fiesta Banana 3 | 1 | condom:fiesta |
| Fiesta Black Coffee 3 | 1 | condom:fiesta |
| Fiesta Bubble Gum 3 | 1 | condom:fiesta |
| Fiesta Delay 3 | 1 | condom:fiesta |
| Fiesta Grape 3 | 1 | condom:fiesta |
| Fiesta Party Pack 12 | 1 | condom:fiesta |
| Fiesta Strawberry 12 | 1 | condom:fiesta |
| Fiesta Strawberry 3 | 1 | condom:fiesta |
| Fiesta Ultra Safe | 1 | condom:fiesta |
| Fiesta Ultra Thin 3 | 1 | condom:fiesta |
| Freshcare Eucalyptus | 1 | toiletry:freshcare |
| Glucose Anhydrous | 1 | ingredient-only |
| Glycyrrhiza glabra L. | 1 | ingredient-only |
| Hyaluronate | 1 | ingredient-only |
| Licorice extract | 1 | ingredient-only |
| Medicine-detection | 1 | explicit:Medicine-detection |
| Minyak Angin Cap lang | 1 | toiletry:minyak |
| Minyak Telon Sierra | 1 | toiletry:minyak |
| Phyllanthus emblica L. | 1 | ingredient-only |
| Propolis extract | 1 | ingredient-only |
| Rohto | 1 | toiletry:rohto |
| Rohto Dry Fresh | 1 | toiletry:rohto |
| Sterimar Bouche | 1 | toiletry:sterimar |
| Sterimar Hygiene | 1 | toiletry:sterimar |
| Sterimar Hygiene Baby | 1 | toiletry:sterimar |
| Sutra 24 | 1 | condom:sutra |
| Sutra Gerigi 3 | 1 | condom:sutra |
| Sutra OK | 1 | condom:sutra |
| Sutra OK 24 | 1 | condom:sutra |
| Sutra OK 3 | 1 | condom:sutra |
| Tissue Lovers | 1 | toiletry:tissue lovers |
| Vicks Inhealer | 1 | toiletry:vicks |
| Zingiber officinale roxb. | 1 | ingredient-only |

## MFDS 9-digit codes (medicine_52 style)

**53 classes**, **4974 instances**. These are Korean MFDS item-permit numbers (9 digits), not brand names.

| code | count |
| --- | --- |
| 201206715 | 252 |
| 200902301 | 198 |
| 199801026 | 188 |
| 200906877 | 164 |
| 201204389 | 142 |
| 200806191 | 138 |
| 201204330 | 134 |
| 201203128 | 130 |
| 200102527 | 124 |
| 200801645 | 118 |
| 200810700 | 118 |
| 202106092 | 113 |
| 201706946 | 108 |
| 198900672 | 104 |
| 200400463 | 104 |
| 201003989 | 104 |
| 201300035 | 104 |
| 199901559 | 102 |
| 200710782 | 102 |
| 200901257 | 102 |
| 201301591 | 102 |
| 201500673 | 102 |
| 200400485 | 101 |
| 197900277 | 100 |
| 198700405 | 99 |
| 196800036 | 98 |
| 198902527 | 98 |
| 199400883 | 98 |
| 202106954 | 98 |
| 199600571 | 96 |
| 200300406 | 93 |
| 199303109 | 91 |
| 200700547 | 89 |
| 201802210 | 88 |
| 202107327 | 86 |
| 199902738 | 84 |
| 201300036 | 84 |
| 201300045 | 84 |
| 200008591 | 72 |
| 200610765 | 59 |
| 201603303 | 58 |
| 200102499 | 56 |
| 197000053 | 51 |
| 202001495 | 50 |
| 201803439 | 48 |
| 200202423 | 45 |
| 201602703 | 45 |
| 201300034 | 40 |
| 200900740 | 32 |
| 202008370 | 28 |
| 200201403 | 26 |
| 202003060 | 18 |
| 200903973 | 6 |

## Source composition (known image counts only)

Image counts below are the provided known totals. No other source sizes were inferred. Qualitative notes are from prior visual review, not new counts.

| source | n_images | % of 28297 | known quality note |
| --- | --- | --- | --- |
| medicine_52 | 4869 | 17.21% | MFDS 9-digit item-permit codes; Korean packs |
| Convenience | 367 | 1.30% | QUALITATIVE: web screenshots mixed in |
| Aeye | 321 | 1.13% | — |
| packv2 | 2756 | 9.74% | — |
| SevaMeds | 521 | 1.84% | QUALITATIVE: Ayurvedic products |
| Drug2 | 2970 | 10.50% | — |
| Aiden | 2781 | 9.83% | QUALITATIVE: class names are pills but images are packs |
| Indonesian | 779 | 2.75% | QUALITATIVE: condom SKUs mixed in |
| rk6cb | 2961 | 10.46% | — |
| Pasus | 2495 | 8.82% | — |
| Hithesh | 3348 | 11.83% | QUALITATIVE: mixed box + blister of same drug |
| AIMedisina | 2171 | 7.67% | QUALITATIVE: Front/Back view labels |
| SmartVision | 1511 | 5.34% | — |
| Teknofest | 447 | 1.58% | — |
| **total** | 28297 | 100.00% | matches n_images |

## Qualitative sample-review notes (not new counts)

- Convenience: web screenshots rather than pack photography.
- Indonesian: condoms (Durex / Fiesta / Sutra / Kondom) inside a medicine project.
- AIMedisina: `Front` / `Back` view labels (largest non-drug classes).
- Hithesh: mixed box + blister annotations for the same drug.
- SevaMeds: Ayurvedic / herbal products.
- Aiden: names look like pill/API labels but the images are packaging.

## Top issues

1. **Class explosion + long tail.** 758 classes for 28297 images; median class has only 17 instances; 114 singletons. A detector cannot learn most of these labels.
2. **Duplicate identity.** Case collisions (Losartan/losartan, Ibuprofen/ibuprofen, Metformin/metformin, …), 27 Box/Blister/Pack splits, 6 Authentic/Counterfeit pairs, and 타이레놀 vs Tylenol. Same product is many classes.
3. **Non-drug classes.** `Front`/`Back` (view), condoms, pregnancy tests, denture cream (`Polident`), toiletries, botanical/ingredient fragments, `Medicine-detection`, and `Carbamate Insecticides`.
4. **Heterogeneous taxonomies merged.** MFDS 9-digit codes, Indonesian `drug Nmg indication` strings, brand SKUs, API generics, and Hangul brand names coexist without a join key.
5. **Source-level contamination** (qualitative): screenshots, Ayurvedic, condom catalog, Front/Back views, box/blister double-labeling, pill-named pack photos.

## Files

- `/workspace/merged-v2-analysis/classes.json`
- `/workspace/merged-v2-analysis/STATS.md`
- `/workspace/merged-v2-analysis/stats.json`
- `/workspace/merged-v2-analysis/analyze.py`
