# **의존 구문 코퍼스 변환 도구**(모두의 말뭉치)

본 프로그램은 국립국어원에서 배포한 모두의 말뭉치 중  구문 분석 코퍼스를 CoNLL 포맷으로 변환해주고 학습 / 개발 / 평가 데이터로 나누어주는 툴입니다.

툴을 사용하기에 앞서 모두의 말뭉치에서 구문 분석 말뭉치와 형태 분석 말뭉치 중 문어 버전을 필요로 합니다.

다운로드 링크: https://corpus.korean.go.kr

구문 분석 말뭉치 파일명: NXDP1902008051.json

형태 분석 말뭉치 파일명: NXMP1902008040.json



# CoNLL-U Format

*예제:* 세금 감면은 경기를 자극하는 데 별로 효과가 없습니다.

|  ID  |   FORM    |    LEMMA    | UPOSTAG |   XPOSTAG   | FEATS | HEAD | DEPREL | DEPS | MISC |
| :--: | :-------: | :---------: | :-----: | :---------: | :---: | :--: | :----: | :--: | :--: |
|  1   |   세금    |    세금     |    _    |     NNG     |   _   |  2   |   NP   |  _   |  _   |
|  2   |  감면은   |   감면 은   |    _    |   NNG+JX    |   _   |  8   | NP_SBJ |  _   |  _   |
|  3   |  경기를   |   경기 를   |    _    |   NNG+JKO   |   _   |  4   | NP_OBJ |  _   |  _   |
|  4   | 자극하는  | 자극 하 는  |    _    | NNG+XSV+ETM |   _   |  5   | VP_MOD |  _   |  _   |
|  5   |    데     |     데      |    _    |   NP_AJT    |   _   |  8   | NP_AJT |  _   |  _   |
|  6   |   별로    |    별로     |    _    |     AP      |   _   |  8   |   AP   |  _   |  _   |
|  7   |  효과가   |   효과 가   |    _    |   NNG+JKS   |   _   |  8   | NP_SBJ |  _   |  _   |
|  8   | 없습니다. | 없 습니다 . |    _    |  VA+EF+SF   |   _   |  0   |   VP   |  _   |  _   |



# 요구사항

- python 3.6

  

# 실행 방법

> python main.py --dependency_file **NXDP1902008051.json** --morphology_file **NXMP1902008040.json** --train_ids ids/train_ids.txt --valid_ids ids/valid_ids.txt --eval_ids ids/eval_ids.txt --output_path conlls/

```
Paramters
dependency_file: 모두의 말뭉치 구문 분석 파일
morphology_file: 모두의 말뭉치 형태 분석 파일
train_ids: 학습 코퍼스
valid_ids: 개발 코퍼스
eval_ids: 평가 코퍼스
output_path: 변환한 파일 저장할 폴더 경로
```



# 코퍼스 통계

| 모두의 말뭉치(ver 1.0) | 문장 수 | 평균 어절 수 |
| ---------------------- | ------- | ------------ |
| 학습 코퍼스            | 119,500 | 13.29        |
| 개발 코퍼스            | 15,000  | 13.41        |
| 평가 코퍼스            | 15,000  | 13.33        |

