<div align="center">
<img src='https://user-images.githubusercontent.com/63540952/167678218-fb084e34-ff3c-4661-b3c1-f879ac6af2e1.jpeg' height='400' width='400'>
  <h4>노션에는 스크럼기록과 추가적인 설명이 나와있으니 참고하시길 바랍니다 <br>
(https://bewriter.notion.site/B-a-Writer-9f4e32bc9d3646ab8ae52f81388001fe)
  </h4>
 <h1 style='text-align:center; font-size: 60px; '>BAWRITER</h1>
 <p align="center">
  <h3>동화를 만들어주는 AI 창작 서비스</h3>
  <h6>개발기간 : 2022/04/11 ~ 2022/05/11</h6>
</div>


## 1. 조원 소개
조수빈(조장), 송영근, 안서연, 이반석, 정희창, 조우리

<br>

## 2. 서비스 소개
<div align="center">
<img src='https://user-images.githubusercontent.com/61009770/167703483-af59df25-7a51-4240-b457-d226c84456fc.png'>
</div>


## 3. 작업 환경
> <img src="https://img.shields.io/badge/Visual Studio code-007ACC?style=flat&logo=Visual Studio code&logoColor=white"/> <br> <img src="https://img.shields.io/badge/Google Colab-F9AB00?style=flat&logo=Google Colab-&logoColor=white"/>

+ ## 사용 언어
+ ### Front
<img src="https://img.shields.io/badge/HTML-E34F26?style=flat&logo=html5&logoColor=white"/> <img src="https://img.shields.io/badge/css-1572B6?style=flat&logo=css3&logoColor=white"/> <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=JavaScript&logoColor=white"/> <img src="https://img.shields.io/badge/Bootstrap5-7952B3?style=flat&logo=Bootstrap&logoColor=white"/> 

+ ### Back
<img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white"/> <img src="https://img.shields.io/badge/Flask-000000?style=flat&logo=Flask&logoColor=white"/> 

+ ### DB
<img src="https://img.shields.io/badge/SQLite-003B57?style=flat&logo=SQLite&logoColor=white"/>

## 4. ERD
![dba PNG](https://user-images.githubusercontent.com/63540952/167684479-e447fdcb-725e-435f-8ada-9276978587e8.png)

## 5. 기능 설명

### 일반 사용자

- 회원가입
- 로그인
- qna 작성 및 수정,삭제 가능
- 동화책 만들기 
- 동화책 내용 음성출력
- 별점
- 타 유저 동화책 읽기 및 평점

### 관리자
- 관리자 페이지에서 데이터베이스 관리 가능
- qna 댓글에 대한 답변 



## 6. AI 기능
+ ## 중요 모델
> KoGPT-2 <br> RQ-Transformer <br> CartoonGAN

+ ## 사용 API
> GTTS <br> Papago <br> Han-spell


## 7. 구동 방법
1. Anaconda Prompt activate <br>
2. requirements.txt 를 이용해 설치 폴더를 작성해주세요.
3. project 폴더로 이동 <br>
4. start.py에 등록되어 있는 `set FLASK_APP=BeAwriter`, `set FLASK_ENV=development` 를 각각 cmd 창에 입력.<br>
윈도우에서 실행시 `set`, 리눅스에서 실행 시 `export`로 적어주세요.
5. flask run 입력


+ ## AI Model
+ ### KoGPT-2
[link](https://drive.google.com/uc?export=download&id=1-1DGCLsrqViL7GNJPsXpivPHptn1MwEm) <br>
pytorch_model.bin 파일을 다운받아 static > storymodel 폴더에 넣기

+ ### RQ-Transformer
[link](https://arena.kakaocdn.net/brainrepo/models/RQVAE/dcd95e8f08408e113aab6451fae895f5/cc3m.tar.gz) <br>
+ #### stage 1
압축을 풀고 stage 1 폴더 내의 model.pt 를 다운받아 static > imagemodel > stage1 폴더에 넣기
+ #### stage 2
압축을 풀고 stage 2 폴더 내의 model.pt 를 다운받아 static > imagemodel > stage2 폴더에 넣기

```
├── imgmodel
│   ├── stage1
│   │   ├── config.yaml
│   │   └── model.pt
│   └── stage2
│       ├── config.yaml
│       └── model.pt
│
├── storymodel
│   ├── config.json
│   ├── special_tokens_map.json
│   ├── tokenizer_config.json
│   ├── tokenizer.json
│   └── pytorch_model.bin
│ 
│ 
└── covermodel
    └── best_checkpoint.pth

```
+ ## 주의사항
Cuda를 사용하기 때문에 GPU가 필요합니다.

