# 버전

| 버전 | 장 | 클래스 | 전처리 | 용도 |
|---|---:|---:|---|---|
| 원본 프로젝트 | 28,297 | 758 | 없음 | 소스 오브 트루스 |
| **v1** | 28,119 | ~694 | auto-orient, Front/Back·콘돔 omit, 대소문자·한영·Box/Blister 병합, filter-null 100% | SKU 단위 |
| v2 | — | — | 한글 remap 깨짐. **휴지통** | 쓰지 말 것 |
| **v3** | 28,119 | **75** | v1과 같은 omit/병합 + 소분류→중분류 remap, 증강 없음 | 학습용 |

v3에서 빠진 178장은 Front/Back·콘돔만 있던 이미지.

- v1 payload: [versions/v1-generate-payload.json](../versions/v1-generate-payload.json)
- v3 payload: [versions/v3-generate-payload.json](../versions/v3-generate-payload.json)
- 학습: RF-DETR Medium, [evaluation/3](https://app.roboflow.com/toyproject1/medicine-packaging-merged-v2/evaluation/3)
