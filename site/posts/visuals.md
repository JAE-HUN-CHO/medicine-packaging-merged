---
title: 그림으로 보기
date: 2026-08-18
dek: 차트와 평가 사진을 한 페이지에 모아 둔다. 숫자는 docs/EVAL.md, data/sources.json, taxonomy.json, v3 split과 같다.
order: 0
---

이 글은 문서 캔버스다. 표와 문장 사이에 묻혀 있던 그림만 꺼내 놓는다. 새 점수는 없다.

<nav class="toc" aria-label="차례">

1. [소스 14개](#소스-14개)
2. [대분류 14](#대분류-14)
3. [v3 분할](#v3-분할)
4. [원본 758 롱테일](#원본-758-롱테일)
5. [재확인한 클래스](#재확인한-클래스)
6. [평가 다섯 장](#평가-다섯-장)

</nav>

## 소스 14개

`data/sources.json`의 장수. 합 28,297.

![소스 14개의 이미지 수](../charts/chart-sources.png)

*소스 14개의 장수. medicine_52가 4,869장으로 가장 크고, medicine-Aeye가 321장으로 가장 작다.*

## 대분류 14

`taxonomy/taxonomy.json` 각 대분류의 `n_instances`. 합 49,242(드롭 28개 제외).

![대분류 14개 박스 수](../charts/chart-majors.png)

*taxonomy.json 대분류 14개. 순환기 7,052, 해열진통소염 6,898.*

## v3 분할

학습 버전 v3. 22,715 / 2,983 / 2,421. 합 28,119.

![v3 train/valid/test 분할](../charts/chart-split.png)

*v3 split 22,715 / 2,983 / 2,421. 빠진 178장은 Front/Back·콘돔만 있던 이미지다.*

## 원본 758 롱테일

원본 프로젝트(라벨 버전 0) 클래스 분포. `docs/STATS.md`.

![원본 758 클래스 롱테일 버킷](../charts/chart-buckets.png)

*인스턴스 수 구간별 클래스 수. 싱글톤 114(15.0%), 5개 이하 298(39.3%).*

![상위 15 클래스](../charts/chart-top15.png)

*상위 15. 빨간 막대 Front/Back은 약 이름이 아니다. Back 1,353, Paracetamol 1,142, Amlodipine 1,066, Front 889.*

## 재확인한 클래스

테스트셋에서 다시 본 클래스만 그린다. 75개 전부가 아니다. `docs/EVAL.md`.

![재확인한 클래스 F1과 mAP50](../charts/chart-eval-f1.png)

*F1: 식약처품목허가번호 0.97, 정품위조 브랜드(Alaxan / Bioflu / Decolgen / Medicol / Neozep) ≈ 1.0, Paracetamol계 0.69, Sitagliptin 0.54. mAP50: Amlodipine 0.41, 테스트 전체 83.8(그림에는 0.838). NSAID는 정확한 F1이 없어 생략.*

테스트 헤드라인은 mAP50 83.8, mAP50-95 69.0, precision 84.9, recall 79.5. 권고 confidence 0.42.

## 평가 다섯 장

아래 캡션은 [학습과 평가를 직접 보니](/medicine-packaging-merged/posts/eval/)와 같다. 장마다 개별 mAP를 새로 재지는 않았다.

### Sitagliptin — Januvia 100 mg

![Januvia 상자, sitagliptin phosphate 100 mg](../eval/sitagliptin.jpg)

*손이 MSD Januvia(sitagliptin phosphate) 100 mg 상자를 들고 있다. 흰 상자, 오른쪽 청록 원 패턴.*

Sitagliptin 중분류는 소분류 2개, 494박스다. F1 0.54, Metformin 혼동 21회.

### TYLOLHOT — 종합감기인데 Paracetamol계

![TYLOLHOT 상자](../eval/tylol-hot.jpg)

*Nobel TYLOLHOT. 표시 용량 500 mg + 60 mg + 4 mg / 20 g. 성분 Parasetamol, Psödoefedrin HCl, Klorfeniramin maleat. 12포.*

파라세타몰+슈도에페드린+클로르페니라민 종합감기. v3 remap은 **Paracetamol계**에 남겨 두었다.

### Telmisartan — 상자 위에 블리스터

![TEMLUS-H 80 상자와 블리스터](../eval/telmisartan.jpg)

*Leeford TEMLUS-H 80. 라벨은 Telmisartan & Hydrochlorothiazide Tablets IP, 10×10. 앞에 10정 은박 블리스터.*

순환기/Telmisartan 중분류는 소분류 1개, 477박스. 상자와 블리스터가 한 프레임에 있는 전형적인 팩이다.

### 은박 블리스터 — Asthalin-4

![Asthalin-4 블리스터 앞뒤](../eval/i20.jpg)

*Cipla Asthalin-4, Salbutamol Sulphate 4 mg. 왼쪽은 은박 뒷면, 오른쪽은 30정 앞면. 은박에 제품명이 세로로 반복된다.*

평가 메모의 “작은 블리스터·은박 글자 반복에서 과검출”이 가리키는 유형이다.

### Paracetamol계 — 어수선한 배경의 PARACIP-650

![PARACIP-650 블리스터](../eval/paracetamol26.jpg)

*Cipla PARACIP-650, Paracetamol Tablets IP 650 mg. 한쪽 정이 빠진 블리스터. 아래는 초록 플라스틱, 위는 QR 용지, 바닥에는 발.*

Paracetamol계는 소분류 24개, 4,159박스. 테스트 F1 0.69, miss 47, background FP 223.
