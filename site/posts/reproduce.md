---
title: 이 레포로 재현하는 법
date: 2026-08-15
dek: 이미지와 라벨은 Roboflow에 있다. 이 레포에는 페이로드와 택소노미만 있다. 한글은 재인코딩하지 말 것.
order: 6
---

워크스페이스 `toyproject1`, 프로젝트 `medicine-packaging-merged-v2`. 순서의 원문은 레포 [`docs/REPRODUCE.md`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/docs/REPRODUCE.md)다. 이 글은 그 순서를 레포 파일에 붙여 쓴다.

원본 758 클래스는 건드리지 않는다. 항상 `versions_generate` remap으로 새 버전을 만든다.

## 전제

- 이미지·라벨은 Roboflow에 있다. 레포에는 페이로드와 택소노미, 소스 표, 차트만 있다.
- 한글 클래스 이름은 JSON **파일 바이트 그대로** 보낸다. 중간 재인코딩하면 깨진다. v2가 그 휴지통이다.
- remap 키는 라이브 클래스명과 1:1. `pepfamin`이지 `pepsfamin`이 아니다.

## 1. v1 — SKU 정리

1. [`data/remap.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/data/remap.json)의 `drop` 28개(Front, Back, 콘돔) → omit.
2. 같은 파일의 `merge` 74→47 (대소문자, `_Box`/`_Blister`/`_Pack`, 타이레놀→Tylenol).
3. preprocessing: auto-orient, filter-null 100%, 리사이즈·증강 없음.
4. 페이로드: [`versions/v1-generate-payload.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/versions/v1-generate-payload.json).

결과: 28,119장, 약 694 클래스.

## 2. v3 — 중분류 75

1. v1 canon 이름에 [`data/mid-remap.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/data/mid-remap.json)의 `map`을 적용한다.
2. 페이로드: [`versions/v3-generate-payload.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/versions/v3-generate-payload.json) (758키, omit 28, 타깃 75).
3. 생성 후 샘플: `pepfamin`→제산궤양, `Glycediab`→당뇨-브랜드.
4. v2는 쓰지 말 것.

결과: 28,119장 (train 22,715 / valid 2,983 / test 2,421), 클래스 75. 생성 기록은 [`versions/v3-generate-result.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/versions/v3-generate-result.json).

한글 타깃(`제산궤양`, `당뇨-브랜드`)은 에디터에서 다시 저장하지 말고, 레포에 있는 바이트를 그대로 `versions_generate`에 넣는다.

## 3. 학습

- 모델: RF-DETR Medium. NAS(`rfdetr-nas-parent`)는 trial 플랜에서 `nas_not_available_for_plan`으로 거절됨. 재시도하지 말 것.
- job: `2c3b3ee56385c34d5926`
- 기록: [`versions/train-v3-result.json`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/versions/train-v3-result.json)
- 모니터: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3

## 4. 평가

- 페이지: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3
- 메모: [`docs/EVAL.md`](https://github.com/jae-hun-cho/medicine-packaging-merged/blob/main/docs/EVAL.md)
- 권고 confidence **0.42**. 기본 0.20은 쓰지 않는다.
- 평가 UI가 한글을 대시로 바꾸더라도 모델 클래스 이름은 한글이다.

## packv2만 따로

instance-seg COCO에서 `segmentation`을 제거하고 `bbox`만 남긴 뒤 `medicine-packv2-od`로 올려 합쳤다. 이미 합본에 들어 있으므로 재현 때는 이 변환을 다시 할 필요가 없다. 같은 소스를 다른 프로젝트에 넣을 때만 반복한다.

## 이 블로그를 로컬에서

`site` 폴더로 이동한 뒤 패키지를 설치하고 빌드 스크립트를 실행한다. 산출물은 `site/dist/`다. 페이지 경로는 `/medicine-packaging-merged/`를 전제로 한다. Pages 워크플로는 레포 루트 `.github/workflows/pages.yml`이다. `docs/`, `taxonomy/`, `data/`, `versions/`, `charts/`, `scripts/`는 그대로 둔다.
