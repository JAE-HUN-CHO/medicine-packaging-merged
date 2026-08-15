---
title: 소스 14개와 라이선스
date: 2026-08-14
dek: 이미지별 원본이 이긴다. packv2와 SevaMeds만 Public Domain, 나머지는 CC BY 4.0.
order: 2
---

라이선스는 2026-08-14 Universe 페이지에서 확인했다. 합친 셋을 CC BY 4.0으로 불러도, 상업 사용 때는 아래 저작자 표시를 남기고 **원본 라이선스를 따른다**. Public Domain 소스는 그대로 Public Domain이다.

기계용 목록은 레포 [`data/sources.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/data/sources.json), 표는 [`docs/SOURCES.md`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/docs/SOURCES.md)다. 장수를 더하면 4,869 + 3,348 + 2,970 + 2,961 + 2,781 + 2,756 + 2,495 + 2,171 + 1,511 + 779 + 521 + 447 + 367 + 321 = **28,297**.

![소스별 이미지 수](../charts/chart-sources.png)

*소스 14개의 장수. medicine_52가 4,869장으로 가장 크고, medicine-Aeye가 321장으로 가장 작다.*

## 14개

| 소스 | 장 | 라이선스 | Universe |
|---|---:|---|---|
| medicine_52 | 4,869 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [project-pd1ub/medicine_52](https://universe.roboflow.com/project-pd1ub/medicine_52) |
| Hithesh | 3,348 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [medicine-detection-1tu11](https://universe.roboflow.com/hitheshs-workspace-wogjn/medicine-detection-1tu11) |
| Drug2 | 2,970 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [drug-2-test1-r5drk](https://universe.roboflow.com/product-nq3cy/drug-2-test1-r5drk) |
| rk6cb | 2,961 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [medicines-rk6cb](https://universe.roboflow.com/data-dmf9w/medicines-rk6cb) |
| Aiden | 2,781 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [pill-detection-vc79k](https://universe.roboflow.com/aiden-knqrf/pill-detection-vc79k) |
| medicine packv2 | 2,756 | [Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) | [medicine-packv2-gnn8b](https://universe.roboflow.com/hfghfg-wzmb7/medicine-packv2-gnn8b) |
| Pasus | 2,495 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [medicine_name_detection](https://universe.roboflow.com/pasus-workspace/medicine_name_detection) |
| AIMedisina | 2,171 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [final-aimedisina](https://universe.roboflow.com/laitsugas/final-aimedisina) |
| SmartVision | 1,511 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [smartvision-nbnsq](https://universe.roboflow.com/obat/smartvision-nbnsq) |
| Indonesian Medicines | 779 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [indonesian-medicines-poft7](https://universe.roboflow.com/abdi-btu08/indonesian-medicines-poft7) |
| SevaMeds | 521 | [Public Domain](https://creativecommons.org/publicdomain/zero/1.0/) | [sevameds](https://universe.roboflow.com/sevameds-z0xbx/sevameds) |
| Teknofest | 447 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [medicine-d7ttn](https://universe.roboflow.com/teknofest-r4zmp/medicine-d7ttn) |
| ConvenienceMedicinesProject | 367 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [conveniencemedicinesproject](https://universe.roboflow.com/yolov5labeling/conveniencemedicinesproject) |
| medicine-Aeye | 321 | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | [medicine-aeye](https://universe.roboflow.com/gongjuhyeon/medicine-aeye) |

원본 fork는 워크스페이스에 유지했다.

## 소스마다 다른 것

**medicine_52** (4,869). 한국 식약처 9자리 품목허가번호가 클래스 이름이다. 제품명이 아니다. 원본 758 중 MFDS 9자리 클래스가 53개, 인스턴스는 4,974박스다. v3에서는 중분류 `식약처품목허가번호` 하나로 접힌다.

**Hithesh** (3,348). 같은 약의 상자와 블리스터가 섞여 있다.

**Aiden** (2,781). 클래스 이름은 알약처럼 보이지만 이미지는 포장이다.

**medicine packv2** (2,756, Public Domain). instance-seg → bbox. COCO에서 `segmentation`을 제거하고 `bbox`만 남겨 `medicine-packv2-od`로 올린 뒤 합쳤다.

**AIMedisina** (2,171). Front/Back 뷰 라벨이 있다. 원본 상위 클래스 `Back` 1,353 · `Front` 889가 여기서 온다. 학습 버전에서는 omit했다. 약 이름이 아니기 때문이다.

**Indonesian Medicines** (779). 콘돔 SKU가 섞여 있다. Sutra, Fiesta, Durex, Kondom Andalan 등 26개 클래스를 v1에서 드롭했다. 박스 수는 많지 않다. `Sutra OK 12` 3박스부터 `Fiesta Black Coffee 3` 1박스까지.

**SevaMeds** (521, Public Domain). 아유르베다 포장이다. 서양 성분명 택소노미에 잘 안 맞는다.

**ConvenienceMedicinesProject** (367). 웹 캡처가 섞여 있다. 카메라로 찍은 팩과 화면을 다시 찍은 팩이 한 셋에 있다.

## 합칠 때 버린 것, 남긴 것

버린 것은 두 종류다. AIMedisina Front/Back, 그리고 인도네시아 콘돔. 둘 다 v1 `drop` 28개에 들어 있고, 그 이미지만 있으면 통째로 빠진다. 178장.

남긴 것은 식약처 코드, 정품·위조 쌍, 아유르베다, 웹 캡처다. 코드는 제품명이 아님을 카드에 적었고, 정품·위조는 제품명 중분류로 유지했다. 라이선스 표시는 소스 단위로 남긴다.
