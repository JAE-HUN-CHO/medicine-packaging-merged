# versions

Roboflow `versions_generate` 페이로드와 생성·학습 기록.

| 파일 | 내용 |
|---|---|
| [v1-generate-payload.json](v1-generate-payload.json) | SKU 정리 버전 |
| [v3-generate-payload.json](v3-generate-payload.json) | 중분류 75 버전 (학습용) |
| [v3-generate-result.json](v3-generate-result.json) | v3 생성 결과. v2는 한글 깨져서 휴지통 |
| [train-v3-result.json](train-v3-result.json) | RF-DETR Medium job (`2c3b3ee56385c34d5926`) |

한글 remap 타깃은 이 JSON 바이트 그대로 보낸다. MCP나 에디터 재인코딩하면 v2처럼 깨진다.
