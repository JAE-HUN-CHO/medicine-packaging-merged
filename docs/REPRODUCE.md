# 재현

원본 758 클래스는 건드리지 않는다. 항상 Roboflow `versions_generate` remap으로 새 버전을 만든다.

Workspace `toyproject1` / project `medicine-packaging-merged-v2`.

## 0. 전제

- 이미지·라벨은 Roboflow에 있다. 이 레포에는 페이로드와 택소노미만 있다.
- 한글 클래스 이름은 JSON 파일 바이트 그대로 보낸다. 중간 재인코딩하면 깨진다 (v2 휴지통).
- remap 키는 **라이브 클래스명**과 1:1. `pepfamin`이지 `pepsfamin`이 아님.

## 1. v1 — SKU 정리

1. [data/remap.json](../data/remap.json)의 `drop` 28개(Front, Back, 콘돔) → omit
2. 같은 파일의 `merge` 74→47 (대소문자, `_Box`/`_Blister`/`_Pack`, 타이레놀→Tylenol)
3. preprocessing: auto-orient, filter-null 100%, 리사이즈·증강 없음
4. payload: [versions/v1-generate-payload.json](../versions/v1-generate-payload.json)

결과: 28,119장, 약 694 클래스.

## 2. v3 — 중분류 75 (학습용)

1. v1 canon 이름에 [data/mid-remap.json](../data/mid-remap.json)의 `map`을 적용
2. payload: [versions/v3-generate-payload.json](../versions/v3-generate-payload.json) (758키, omit 28, 타깃 75)
3. 생성 후 샘플: `pepfamin`→제산궤양, `Glycediab`→당뇨-브랜드
4. v2는 쓰지 말 것

결과: 28,119장 (train 22,715 / valid 2,983 / test 2,421), 클래스 75.

## 3. 학습

- 모델: RF-DETR Medium. NAS(`rfdetr-nas-parent`)는 trial 플랜에서 거절됨
- job: `2c3b3ee56385c34d5926`
- 기록: [versions/train-v3-result.json](../versions/train-v3-result.json)
- 모니터: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/3

## 4. 평가

- 페이지: https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3
- 메모: [EVAL.md](EVAL.md)
- 권고 confidence 0.42

## packv2만 따로

instance-seg COCO에서 `segmentation`을 제거하고 `bbox`만 남긴 뒤 `medicine-packv2-od`로 올려 합쳤다.
