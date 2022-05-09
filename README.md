# B-A-Writer
***
![ddf8ce96f606f](https://user-images.githubusercontent.com/28862384/167321907-3f9d3edc-aeed-4135-9b70-932274ce853c.jpg)
+ ## 동화를 만들어주는 AI 창작 서비스
COVID로 야외 활동이 제한된 시기, 아이들과 함께 할 수 있는 서비스.<br>
아이들과 함께 동화를 만들며 좋은 추억을 쌓아보세요.<br>
직접 동화를 만들어봄으로 아이들의 창의력이 쑥쑥 올라갑니다.

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
https://drive.google.com/drive/folders/19M-dN7ui3LVTfs3KYqyrTE8OzuJSJu7a?usp=sharing <br>
pytorch_model.bin 파일을 다운받아 static > storymodel 폴더에 넣기

+ ### RQ-Transformer
+ #### stage 1
https://drive.google.com/drive/folders/19GscvzbL550c7r3fv-EXv715U9qC3DoY <br>
model.pt 를 다운받아 static > imagemodel > stage1 폴더에 넣기

+ #### stage 2
https://drive.google.com/drive/folders/1ihFHo__HTJzNIDek5UhQGnXNlIyqD8SF <br>
model.pt 를 다운받아 statc > imagemodel > stage2 폴더에 넣기

+ ## 주의사항
Cuda를 사용하기 때문에 GPU가 필요합니다.
