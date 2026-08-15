---
title: 학습과 평가를 직접 보니
date: 2026-08-14
dek: RF-DETR Medium, 테스트 mAP50 83.8. 쉬운 클래스가 점수를 끌어올리고, Sitagliptin과 파라세타몰은 그렇지 않다.
order: 5
---

모델은 RF-DETR Medium이다. 처음에 요청한 것은 `rfdetr-nas-parent`였으나 trial 플랜에서 거절됐다. 에러 코드 `nas_not_available_for_plan`, 메시지 그대로 *Neural Architecture Search is not available on your current plan*. NAS는 다시 시도하지 않고 medium으로 한 번 폴백했다.

`training_id`는 `2c3b3ee56385c34d5926`. 모델 표시 이름은 `toyproject1/medicine-packaging-merged-v2-3-rfdetr-medium-t1`. 학습 기록은 [`versions/train-v3-result.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/versions/train-v3-result.json), 모니터는 [version 3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3), 평가는 [evaluation/3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3) (`eval` `mgmZOi2hagpAgLeF9Boh`). 메모는 [`docs/EVAL.md`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/docs/EVAL.md).

COCO export는 6,857 MB, 폴링 중 progress 0.2 → 0.79 → 1.

## 헤드라인

| split | mAP50 | mAP50-95 | P | R |
|---|---:|---:|---:|---:|
| test | 83.8 | 69.0 | 84.9 | 79.5 |
| valid | 79.3 | — | 77 | 75.2 |

Roboflow가 권고하는 confidence는 **0.42**. 평가 화면 기본값 0.20은 허위 박스가 많다. 배포 임계값은 0.42를 쓴다.

valid의 mAP50-95는 평가 메모에 없다. 그래서 비워 둔다.

## 점수를 올리는 클래스

식약처품목허가번호는 테스트 F1 **0.97**(998 중 994). 상자 위주, 라벨 형식이 비슷하다. 필리핀 정품·위조 박스 — Alaxan, Bioflu, Decolgen, Medicol Advance, Neozep Forte — 는 클래스마다 약 **1.0**. 큰 상자만 있는 이미지가 많다.

이 두 축이 평균을 끌어올린다. 83.8을 “포장 일반이 잘 된다”로 읽으면 안 된다.

## 약한 곳

- **Sitagliptin** F1 0.54. Metformin으로 21회 혼동.
- **Amlodipine** mAP50 0.41.
- **Paracetamol계** F1 0.69. miss 47, background FP 223.
- NSAID와 종합감기 상자끼리 혼동.
- 작은 블리스터, 은박에 같은 글자가 반복되는 장면에서 과검출.

아래 다섯 장은 그 약점과 냄새를 보기 위한 것이다. 장마다 개별 mAP를 새로 재지는 않았다.

## 다섯 장

### Sitagliptin — Januvia 100 mg

![Januvia 상자, sitagliptin phosphate 100 mg](../eval/sitagliptin.jpg)

*손이 MSD Januvia(sitagliptin phosphate) 100 mg 상자를 들고 있다. 흰 상자, 오른쪽 청록 원 패턴.*

Sitagliptin 중분류는 소분류 2개, 494박스다. Metformin은 3개 소분류, 1,123박스. 둘 다 당뇨 대분류의 흰 상자다. F1 0.54, Metformin 혼동 21회는 그 겹침과 맞다. 브랜드 로고를 읽지 못하면 계열이 무너진다.

### TYLOLHOT — 종합감기인데 Paracetamol계

![TYLOLHOT 상자](../eval/tylol-hot.jpg)

*Nobel TYLOLHOT. 표시 용량 500 mg + 60 mg + 4 mg / 20 g. 성분 Parasetamol, Psödoefedrin HCl, Klorfeniramin maleat. 12포.*

파라세타몰+슈도에페드린+클로르페니라민이다. 적응증은 종합감기. v3 remap은 이 클래스를 **Paracetamol계**에 남겨 두었다. 택소노미 글에서 말한 알려진 냄새다. 검증 25건에는 넣지 않았다. 평가에서 NSAID↔종합감기 혼동과 같은 줄에 놓인다.

### Telmisartan — 상자 위에 블리스터

![TEMLUS-H 80 상자와 블리스터](../eval/telmisartan.jpg)

*Leeford TEMLUS-H 80. 라벨은 Telmisartan & Hydrochlorothiazide Tablets IP, 10×10. 앞에 10정 은박 블리스터.*

순환기/Telmisartan 중분류는 소분류 1개, 477박스. 이 장은 객체감지 셋이 노리는 전형적인 팩이다. 상자와 블리스터가 한 프레임에 있다. 점수가 약한 예로 든 것이 아니라, 학습이 본 포장 형태를 보여 주기 위한 장이다.

### 은박 블리스터 — Asthalin-4

![Asthalin-4 블리스터 앞뒤](../eval/i20.jpg)

*Cipla Asthalin-4, Salbutamol Sulphate 4 mg. 왼쪽은 은박 뒷면, 오른쪽은 30정 앞면. 은박에 제품명이 세로로 반복된다.*

평가 메모의 “작은 블리스터·은박 글자 반복에서 과검출”이 가리키는 유형이다. 같은 문자열이 포일 한 장에 여러 번 찍혀 있으면 모델이 박스를 쪼개기 쉽다. 권고 confidence 0.42가 기본 0.20보다 나은 이유이기도 하다.

### Paracetamol계 — 어수선한 배경의 PARACIP-650

![PARACIP-650 블리스터](../eval/paracetamol26.jpg)

*Cipla PARACIP-650, Paracetamol Tablets IP 650 mg. 한쪽 정이 빠진 블리스터. 아래는 초록 플라스틱, 위는 QR 용지, 바닥에는 발.*

Paracetamol계는 소분류 24개, 4,159박스로 해열진통소염에서 가장 크다. 그런데 테스트 F1은 0.69, miss 47, background FP 223. 흰 은박과 흰 종이가 한 장에 있으면 배경을 약 상자로 집는다. 이 장이 그 장면이다.

## 평가 UI가 한글을 대시로 바꾼다

Roboflow 평가 화면은 한글 중분류 이름을 글자 수만큼 대시로 보여 준다. `Paracetamol계`는 `Paracetamol-`. 모델은 한글 이름으로 학습됐다. 깨지는 쪽은 평가 API/UI다. 클래스 이름을 리포트에서 찾을 때 대시로 접힌 줄을 한글 원명과 맞춰 읽어야 한다.

## 읽는 법

테스트 mAP50 83.8은 맞다. 식약처 상자와 필리핀 정품·위조 상자가 그 숫자를 만든다. Sitagliptin 0.54, Amlodipine 0.41, Paracetamol계 0.69, 그리고 TYLOLHOT가 Paracetamol계에 남아 있는 사실이 같은 평가의 다른 면이다. 임계값은 0.42.
