# medicine-packaging-merged-v2

상업용 의약품 **포장**(상자·블리스터·병) 객체감지 데이터셋. 알약이 아니라 팩 단위이고, 클래스에 실제 제품명·성분명·식약처 코드가 들어 있다.

- Workspace: `toyproject1`
- Project: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2
- Type: object-detection
- License: 원본을 따른다. 합친 셋은 **CC BY 4.0**으로 보면 되고, 이미지별 원본 라이선스가 우선이다. SevaMeds만 **CC0**.
- Date: 2026-08-14

## 한 줄 요약

Universe에서 상업 사용 가능한 포장 OD 14개를 fork → 합침 → packv2 폴리곤을 박스로 변환해 추가 → 노이즈 클래스 정리 → 치료 중분류 75개로 접어 학습.

## 원본 (dataset, 미라벨 0)

| | 값 |
|---|---|
| 이미지 | 28,297 |
| 클래스 | 758 |
| 박스 | 51,520 (장당 1.82) |
| split | train 22,890 / valid 2,984 / test 2,423 |

원본 클래스는 그대로 둔다. 정리는 버전 remap으로만 한다.

## 소스 (14)

| 소스 | 장 | 비고 |
|---|---:|---|
| medicine_52 | 4,869 | 한국 식약처 9자리 품목허가번호 |
| Hithesh | 3,348 | 같은 약의 상자+블리스터 혼재 |
| Drug2 | 2,970 | |
| rk6cb | 2,961 | |
| Aiden | 2,781 | 클래스명은 알약, 이미지는 포장 |
| packv2 | 2,756 | instance-seg → bbox 변환 후 합침 (CC0/Public Domain) |
| Pasus | 2,495 | |
| AIMedisina | 2,171 | Front/Back 뷰 라벨 |
| SmartVision | 1,511 | |
| Indonesian | 779 | 콘돔 SKU 혼입 |
| SevaMeds | 521 | 아유르베다, CC0 |
| Teknofest | 447 | |
| Convenience | 367 | 웹 캡처 혼입 |
| Aeye | 321 | |

원본 fork는 워크스페이스에 유지. 1차 합본은 `medicine-packaging-merged` (25,541장, packv2 제외).

## 버전

| 버전 | 장 | 클래스 | 전처리 | 용도 |
|---|---:|---:|---|---|
| 원본 프로젝트 | 28,297 | 758 | 없음 | 소스 오브 트루스 |
| **v1** | 28,119 | ~694 | auto-orient, Front/Back·콘돔 omit, 대소문자·한영·Box/Blister 병합, filter-null 100% | SKU 단위 |
| v2 | — | — | 한글 remap 깨짐. **휴지통** | 쓰지 말 것 |
| **v3** | 28,119 | **75** | v1과 같은 omit/병합 + 소분류→중분류 remap, 증강 없음 | 학습용 |

v3 split: train 22,715 / valid 2,983 / test 2,421. 빠진 178장은 Front/Back·콘돔만 있던 이미지.

학습: `rfdetr-medium` (`training_id` `2c3b3ee56385c34d5926`). NAS(`rfdetr-nas-parent`)는 trial 플랜이라 불가. 모니터: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3

## 중분류 75개 (v3) — 14 대분류

| 대분류 | 소분류 | 박스 | 대표 중분류 |
|---|---:|---:|---|
| 해열진통소염 | 53 | 6,898 | Paracetamol계, NSAID, 아스피린계 |
| 호흡기감기 | 109 | 5,397 | 종합감기, 진해거담, 비염알레르기 |
| 순환기 | 32 | 7,052 | Amlodipine, Losartan, 순환기-브랜드 |
| 당뇨 | 20 | 4,845 | Glimepiride, Metformin, 당뇨-브랜드 |
| 항균항바이러스 | 58 | 4,878 | 베타락탐, 세팔로스포린, 기타항균 |
| 소화기 | 49 | 2,375 | 제산궤양, 소화효소 |
| 신경정신 | 33 | 3,549 | 항우울항정신, 항전간신경통, 통풍 |
| 호르몬내분비 | 11 | 1,157 | 갑상선, 스테로이드(전신) |
| 피부외용 | 98 | 1,282 | 스테로이드외용, 파스외용, 위생화장품 |
| 비타민영양 | 68 | 2,015 | 단일영양, 종합비타민, 면역건강 |
| 피임산과 | 11 | 510 | 경구피임, 산과기타 |
| 정품위조 | 12 | 2,253 | Alaxan, Bioflu 등 제품명 쌍 |
| 한국식약처코드 | 53 | 4,974 | 식약처품목허가번호 |
| 기타 | 87 | 2,057 | 브랜드미분류, 성분명만 |

정품·위조 쌍은 제품명 중분류로 유지. Atova(아토르바스타틴/아토바쿠온 모호), Immucept(면역억제제)는 기타.

## 재현

원본 758 클래스는 건드리지 않는다. 항상 `versions_generate` remap으로 새 버전을 만든다.

### v1 — SKU 정리

1. `remap.json`의 `drop` 28개(Front, Back, 콘돔) → 빈 문자열(omit)
2. `remap.json`의 `merge` 74→47 (대소문자, `_Box`/`_Blister`/`_Pack`, 타이레놀→Tylenol)
3. preprocessing: `auto-orient`, `filter-null: 100%`, 리사이즈·증강 없음
4. payload: `generate-payload.json`

### v3 — 중분류 75

1. v1 canon 이름에 `mid-remap.json`의 `map`을 적용. 키는 **라이브 클래스명**과 1:1이어야 한다 (`pepfamin`이지 `pepsfamin`이 아님)
2. 한글 타깃(`제산궤양`, `당뇨-브랜드`)은 파일 바이트 그대로 전송. MCP 중간 재인코딩하면 v2처럼 깨진다
3. payload: `generate-v2-payload.json` (758키, omit 28, 타깃 75)
4. 생성 후 remap 샘플 확인: `pepfamin`→제산궤양, `Glycediab`→당뇨-브랜드

### 분류 검증에서 옮긴 25건

감기 복합(Panadol Cold Flu, Panadol Flu Batuk, 판피린티정), 흡입제(Salmeterol, Budesonide, Fluticasone Propionate), 외용 스테로이드 7개, 파스 성분(멘톨·캄파 등), pepfamin(파모티딘), Angenta(항우울), Ace XR(파라세타몰 665mg ER), Tumeric 500, Leflunomide, ByeBye Fever. 목록은 `taxonomy-audit.md`.

### packv2 변환

instance-seg COCO에서 `segmentation`을 제거하고 `bbox`만 남긴 뒤 `medicine-packv2-od`로 올려 합침.

## 이 레포의 파일

- [docs/DATASET-CARD.md](DATASET-CARD.md) — 이 카드
- [docs/STATS.md](STATS.md) / [data/stats.json](../data/stats.json) — 원본 758 분석
- [data/remap.json](../data/remap.json) / [docs/REMAP.md](REMAP.md) — v1 drop·merge
- [taxonomy/](../taxonomy/) — 14/75/694
- [data/mid-remap.json](../data/mid-remap.json) — 소분류→중분류
- [versions/v1-generate-payload.json](../versions/v1-generate-payload.json) — v1
- [versions/v3-generate-payload.json](../versions/v3-generate-payload.json) — v3
- [versions/v3-generate-result.json](../versions/v3-generate-result.json) — v3 생성 기록
- [versions/train-v3-result.json](../versions/train-v3-result.json) — 학습 job
- [docs/EVAL.md](EVAL.md) — v3 평가 메모
- [docs/SOURCES.md](SOURCES.md) — 소스 14개 attribution
- [docs/REPRODUCE.md](REPRODUCE.md) — 재현 순서

## 주의

- 클래스 롱테일: 원본 중앙값 17장, singleton 114
- Convenience는 웹 캡처, SevaMeds는 아유르베다
- 식약처 9자리는 제품명이 아님
- 상업 사용 시 이미지별 원본 라이선스·저작자 표시

## 소스·라이선스 (attribution)

이미지별 원본 라이선스가 우선이다. 합친 셋은 CC BY 4.0으로 보면 되고, Public Domain 소스는 그대로 Public Domain이다. 상업 사용 시 아래 저작자 표시를 남긴다.

| 소스 | 장 | 라이선스 | Universe |
|---|---:|---|---|
| medicine_52 | 4,869 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/project-pd1ub/medicine_52 |
| Hithesh (Medicine detection) | 3,348 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/hitheshs-workspace-wogjn/medicine-detection-1tu11 |
| Drug2 (Drug 2 Test1) | 2,970 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/product-nq3cy/drug-2-test1-r5drk |
| rk6cb (Medicines) | 2,961 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/data-dmf9w/medicines-rk6cb |
| Aiden (Pill Detection) | 2,781 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/aiden-knqrf/pill-detection-vc79k |
| medicine packv2 | 2,756 | [Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) | https://universe.roboflow.com/hfghfg-wzmb7/medicine-packv2-gnn8b |
| Pasus (medicine_name_detection) | 2,495 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/pasus-workspace/medicine_name_detection |
| AIMedisina (Final AIMedisina) | 2,171 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/laitsugas/final-aimedisina |
| SmartVision | 1,511 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/obat/smartvision-nbnsq |
| Indonesian Medicines | 779 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/abdi-btu08/indonesian-medicines-poft7 |
| SevaMeds | 521 | [Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) | https://universe.roboflow.com/sevameds-z0xbx/sevameds |
| Teknofest medicine | 447 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/teknofest-r4zmp/medicine-d7ttn |
| ConvenienceMedicinesProject | 367 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/yolov5labeling/conveniencemedicinesproject |
| medicine-Aeye | 321 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://universe.roboflow.com/gongjuhyeon/medicine-aeye |

라이선스는 2026-08-14 Universe 페이지에서 확인했다. packv2·SevaMeds만 Public Domain, 나머지 12개는 CC BY 4.0.
