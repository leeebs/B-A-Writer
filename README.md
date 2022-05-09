# B-A-Writer
***
![81d4a71985f947f2da56658ffdcf58e2](https://user-images.githubusercontent.com/28862384/167350120-3ef5ca6d-d6a2-444b-b2c0-ce42567c22a6.jpg)

+ ## 동화를 만들어주는 AI 창작 서비스
COVID로 야외 활동이 제한된 시기, 아이들과 함께 할 수 있는 서비스.<br>
아이들과 함께 동화를 만들며 좋은 추억을 쌓아보세요.<br>
직접 동화를 만들어봄으로 아이들의 창의력이 쑥쑥 올라갑니다.

노션 주소 : (https://bewriter.notion.site/B-a-Writer-9f4e32bc9d3646ab8ae52f81388001fe)

+ ## 조원 소개
조수빈(조장), 송영근, 안서연, 이반석, 정희창, 조우리

+ ## 작업 환경
> Visual Studio Code <br> Colab

+ ## 사용 언어
+ ### Front
+ #### Language
> HTML <br> CSS <br> Javascript
+ #### Framework
> Bootstrap5

+ ### Back
+ #### Language
> Python
+ #### Framework
> Flask

+ ## AI
> KoGPT-2 <br> RQ-Transformer <br> GAN

+ ## API
> GTTS <br> Papago <br> Han-spell

+ ## DB
> SQLite

+ ## 구동 방법
1. Anaconda Prompt activate <br>
2. project 폴더로 이동 <br>
3. start.py에 등록되어 있는 set FLASK_APP=BeAwriter, set FLASK_ENV=development 를 각각 cmd 창에 입력<br>
윈도우에서 실행시 set, 리눅스에서 실행 시 export로 적어주세요.
4. flask run 입력

+ ## 구동 시 설치 프로그램
pip install flask_migrate <br>
pip install flask_admin<br>
pip install git+https://github.com/ssut/py-hanspell.git<br>
pip install flask_wtf<br>
pip install gtts<br>
pip install pytz<br>
pip install regex<br>
pip install transformers<br>
pip install fastai==2.2.5<br>

pip install git+https://github.com/openai/CLIP.git<br>
pip install omegaconf<br>
pip install EasyDict<br>

pip install krwordrank<br>
pip install konlpy<br>

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
└──
```
+ ## 주의사항
Cuda를 사용하기 때문에 GPU가 필요합니다.
