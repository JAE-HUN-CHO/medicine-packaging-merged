# v3 평가 메모 (2026-08-14)

모델: `toyproject1/medicine-packaging-merged-v2-3-rfdetr-medium-t1`  
eval: `mgmZOi2hagpAgLeF9Boh`  
페이지: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3

## 헤드라인

| split | mAP50 | mAP50-95 | P | R |
|---|---:|---:|---:|---:|
| test | 83.8 | 69.0 | 84.9 | 79.5 |
| valid | 79.3 | — | 77 | 75.2 |

Roboflow 권고 confidence는 **0.42**. 평가 기본 0.20은 허위 박스가 많습니다.

## 잘 되는 것

- 식약처품목허가번호: test F1 0.97 (998 중 994)
- 필리핀 정품·위조 박스: Alaxan, Bioflu, Decolgen, Medicol Advance, Neozep Forte ≈ 1.0
- 큰 상자 위주

## 약한 것

- Sitagliptin F1 0.54, Metformin으로 21회 혼동
- Amlodipine mAP50 0.41
- Paracetamol계 F1 0.69 (miss 47, background FP 223)
- NSAID ↔ 종합감기 박스
- 작은 블리스터·은박 글자 반복에서 과검출

## 평가 UI

한글 중분류 이름이 글자 수만큼 대시로 깨집니다. `Paracetamol계`는 `Paracetamol-`. 모델은 한글 이름으로 학습됐고 평가 API/UI만 깨집니다.

## 택소노미 냄새

`TYLOLHOT`는 파라세타몰+슈도에페드린+클로르페니라민 종합감기인데 v3 remap이 Paracetamol계로 넣었습니다.
