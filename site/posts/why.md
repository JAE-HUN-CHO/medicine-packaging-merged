---
title: 왜 이 데이터셋인가
date: 2026-08-14
dek: 알약이 아니라 상자다. 상업 사용이 되는 포장 객체감지 14개를 합친 이유.
order: 1
---

알약 한 알을 위에서 찍은 사진이 아니다. 약국 선반과 가정 서랍에 실제로 놓이는 **상자·블리스터·병**을 박스로 잡는 객체감지 데이터셋이다. 클래스 이름에는 제품명, 성분명, 한국 식약처 9자리 품목허가번호가 들어 있다.

Roboflow 워크스페이스는 `toyproject1`, 프로젝트는 [medicine-packaging-merged-v2](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2)다. 원본(라벨 버전 0) 숫자는 이렇다.

| | 값 |
|---|---|
| 이미지 | 28,297 |
| 클래스 | 758 |
| 박스 | 51,520 (장당 1.82) |
| split | train 22,890 / valid 2,984 / test 2,423 |

미라벨 이미지는 0장이다. 원본 클래스는 그대로 둔다. 정리는 라이브 758을 고치는 방식이 아니라 `versions_generate` remap으로만 한다.

## 상업 사용이 되는 것만

Universe에는 포장 사진이 많지만 라이선스가 갈린다. 이 셋은 상업 사용이 되는 소스만 골랐다. 2026-08-14 Universe 페이지 기준으로 packv2와 SevaMeds는 Public Domain, 나머지 12개는 CC BY 4.0이다. 합친 셋은 CC BY 4.0으로 보면 되고, **이미지별 원본 라이선스가 우선**이다.

1차 합본 `medicine-packaging-merged`는 packv2를 빼면 25,541장이다. packv2는 instance-seg COCO에서 `segmentation`을 버리고 `bbox`만 남긴 뒤 `medicine-packv2-od`로 올려 합쳤다. 그 2,756장이 더해져 28,297장이 된다.

## 758개는 학습 타깃이 되기 어렵다

원본 클래스 분포의 중앙값은 장수가 아니라 인스턴스 17이다. 싱글톤은 114개(15.0%), 5개 이하가 298개(39.3%)다. 상위는 `Back` 1,353, `Paracetamol` 1,142, `Amlodipine` 1,066, `Front` 889이다. `Front`와 `Back`만 합쳐도 2,242박스(4.35%)인데, 약 이름이 아니라 AIMedisina의 뷰 라벨이다.

같은 약을 대소문자로 쪼갠 쌍도 있다. `Metformin` 755 + `metformin` 62, `Losartan` 458 + `losartan` 219. `_Box` / `_Blister` / `_Pack`로 갈라 놓은 줄기도 27개다. 이 상태 그대로 758-way를 돌리면 롱테일이 점수를 삼킨다.

그래서 학습은 중분류 75개로 접은 v3에서 했다. 원본 28,297 → v3 28,119(22,715 / 2,983 / 2,421). 빠진 178장은 Front/Back·콘돔만 있던 이미지다.

## 이 글의 범위

이어지는 글은 소스 14개의 라이선스, 14 / 75 / 694 택소노미, v1·깨진 v2·v3를 만든 방법, RF-DETR Medium 평가, 이 레포로 같은 버전을 다시 만드는 순서다. 차트와 JSON은 레포 `charts/` · `data/` · `taxonomy/` · `versions/`에 있다. 이 블로그는 그 숫자를 옮긴다.
