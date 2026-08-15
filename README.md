# medicine-packaging-merged

상업용 의약품 **포장**(상자·블리스터·병) 객체감지 데이터셋의 재현 레포입니다. 알약이 아니라 팩 단위이고, 클래스는 제품명·성분명·식약처 코드입니다.

- Roboflow: [toyproject1/medicine-packaging-merged-v2](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2)
- 학습 버전: [v3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3) (중분류 75)
- 평가: [evaluation/3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3)
- 라이선스: 이미지별 원본이 우선. 합친 셋은 CC BY 4.0, packv2·SevaMeds는 Public Domain.

자세한 카드는 [DATASET-CARD.md](DATASET-CARD.md), 소스 URL·라이선스는 그 마지막 섹션에 있습니다.

## 한 줄

Universe에서 상업 사용 가능한 포장 OD 14개를 fork → 합침 → packv2 폴리곤을 박스로 변환 → 노이즈 클래스 정리 → 치료 중분류 75개로 접어 RF-DETR Medium 학습.

## 숫자

| | 원본 | v3 (학습) |
|---|---:|---:|
| 이미지 | 28,297 | 28,119 |
| 클래스 | 758 | 75 |
| split | 22,890 / 2,984 / 2,423 | 22,715 / 2,983 / 2,421 |

v3 test (RF-DETR Medium): mAP50 **83.8**, precision **84.9**, recall **79.5**. 쉬운 클래스(식약처 박스, 필리핀 정품·위조)가 점수를 끌어올립니다. 메모는 [EVAL.md](EVAL.md).

## 재현

원본 758 클래스는 건드리지 않습니다. 항상 `versions_generate` remap으로 새 버전을 만듭니다.

1. v1 SKU 정리: `generate-payload.json` (`remap.json`의 drop·merge)
2. v3 중분류: `generate-v2-payload.json` (`mid-remap.json`)
3. 한글 타깃은 파일 바이트 그대로 전송. 중간 재인코딩하면 깨집니다 (v2는 휴지통).

택소노미는 `taxonomy.json` / [TAXONOMY.md](TAXONOMY.md) (14 대 / 75 중 / 694 소). 검증에서 옮긴 25건은 [taxonomy-audit.md](taxonomy-audit.md).

## 주의

- 클래스 롱테일: 원본 중앙값 17장, singleton 114
- 식약처 9자리는 제품명이 아님
- 상업 사용 시 이미지별 원본 라이선스·저작자 표시
