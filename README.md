# medicine-packaging-merged

## 블로그

작업 기록을 GitHub Pages에 정리했습니다.

- 주소: https://jae-hun-cho.github.io/medicine-packaging-merged/
- 로컬: `cd site && npm i && npm run build` 후 `site/dist/`를 연다.

원본 문서와 택소노미·페이로드는 아래 폴더에 그대로 있습니다.

상업용 의약품 **포장**(상자·블리스터·병) 객체감지 데이터셋의 재현 레포입니다. 알약이 아니라 팩 단위이고, 클래스는 제품명·성분명·식약처 코드입니다.

- Roboflow: [toyproject1/medicine-packaging-merged-v2](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2)
- 학습 버전: [v3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3) (중분류 75)
- 평가: [evaluation/3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3)
- 라이선스: 이미지별 원본이 우선. 합친 셋은 CC BY 4.0, packv2·SevaMeds는 Public Domain.

## 한 줄

Universe에서 상업 사용 가능한 포장 OD 14개를 fork → 합침 → packv2 폴리곤을 박스로 변환 → 노이즈 클래스 정리 → 치료 중분류 75개로 접어 RF-DETR Medium 학습.

## 숫자

| | 원본 | v3 (학습) |
|---|---:|---:|
| 이미지 | 28,297 | 28,119 |
| 클래스 | 758 | 75 |
| split | 22,890 / 2,984 / 2,423 | 22,715 / 2,983 / 2,421 |

v3 test (RF-DETR Medium): mAP50 **83.8**, precision **84.9**, recall **79.5**. 쉬운 클래스(식약처 박스, 필리핀 정품·위조)가 점수를 끌어올립니다. 메모는 [docs/EVAL.md](docs/EVAL.md).

## 폴더

```
docs/        카드, 재현, 버전, 소스, 평가
taxonomy/    14 / 75 / 694 트리와 JSON
data/        remap · 클래스 · 소스 JSON
versions/    v1 · v3 generate payload와 학습 기록
charts/      소스·롱테일 그림
scripts/     로컬 분석
examples/    hosted inference 예제
site/        한국어 블로그 (Pages)
```

| 가고 싶은 곳 | 파일 |
|---|---|
| 데이터셋 카드 | [docs/DATASET-CARD.md](docs/DATASET-CARD.md) |
| 재현 순서 | [docs/REPRODUCE.md](docs/REPRODUCE.md) |
| 소스·라이선스 | [docs/SOURCES.md](docs/SOURCES.md) |
| 중분류 75 | [taxonomy/mids.csv](taxonomy/mids.csv) · [taxonomy/tree.md](taxonomy/tree.md) |
| v3 페이로드 | [versions/v3-generate-payload.json](versions/v3-generate-payload.json) |

## 재현

원본 758 클래스는 건드리지 않습니다. 항상 `versions_generate` remap으로 새 버전을 만듭니다.

1. v1 SKU 정리: `versions/v1-generate-payload.json`
2. v3 중분류: `versions/v3-generate-payload.json`
3. 한글 타깃은 파일 바이트 그대로 전송. 중간 재인코딩하면 깨집니다 (v2는 휴지통).

검증에서 옮긴 25건은 [taxonomy/taxonomy-audit.md](taxonomy/taxonomy-audit.md).

## 주의

- 클래스 롱테일: 원본 중앙값 17장, singleton 114
- 식약처 9자리는 제품명이 아님
- 상업 사용 시 이미지별 원본 라이선스·저작자 표시
