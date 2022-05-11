from flask import Blueprint, render_template, url_for, request, g, jsonify
from werkzeug.utils import redirect
from gtts import gTTS
from BeAwriter import db
from BeAwriter.models import Storybook, CoverImage, Rating, Pageimage

import datetime
from pytz import timezone
from sqlalchemy import and_
from sqlalchemy.sql import func

from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import tensor
from hanspell import spell_checker
import re

from PIL import Image
import torch
import torchvision
import clip
import torch.nn.functional as F
from BeAwriter.static.imgmodel.notebook_utils import TextEncoder, load_model, get_generated_images_by_texts

from krwordrank.sentence import summarize_with_sentences
import requests
from konlpy.tag import Okt

import torch.nn as nn
from torch import sigmoid
from torchvision import transforms
import matplotlib.pyplot as plt
import numpy as np

KST = timezone('Asia/Seoul')
now = datetime.datetime.utcnow()

def preprocessing(res):
    spelled_sent = spell_checker.check(res)
    hanspell_sent = spelled_sent.checked
    return hanspell_sent

def outputmodel(input):
    PATH = "../project/BeAwriter/static/storymodel/"
    model = AutoModelWithLMHead.from_pretrained(PATH)
    tokenizer = PreTrainedTokenizerFast.from_pretrained(PATH)
    
    # device = "cpu"
    device = "cuda:0"
    model = model.to(device)

    prompt_ids = tokenizer.encode(input)
    inp = tensor(prompt_ids)[None].cuda()
    preds = model.generate(inp,
                            use_cache=True,
                            pad_token_id=tokenizer.pad_token_id,
                            eos_token_id=tokenizer.eos_token_id,
                            bos_token_id=tokenizer.bos_token_id,
                            max_length=len(input)+30,
                            do_sample=True,
                            repetition_penalty=5.0,
                            temperature=0.9,
                            top_k=50,
                            top_p=0.92) 
    output = tokenizer.decode(preds[0].cpu().numpy())
    output = re.sub('[0-9:\n]','',output)
    return output

def keyword_translate(text):
    data = {'text': text,
            'source':'ko',
            'target':'en'}
    url = "https://openapi.naver.com/v1/papago/n2mt"
    header = {
        "X-Naver-Client-Id":'fQlpBVosQc_buCxfp_5V',
        "X-Naver-Client-Secret":'CEurYwz6Kl'
    }
    response = requests.post(url, headers=header, data= data)
    rescode = response.status_code
    
    if(rescode==200):
        t_text = response.json()
        return t_text['message']['result']['translatedText']
    else:
        return print("Error Code:" , rescode)

def extraction_keyword(texts):
    okt = Okt()
    stopwords = {'너무', '정말', '진짜', '그만', '갑자', '바로', '그때', '정말루', '정말로', '옛날',
                 '이제', '다시', '당장', '무슨', '분명', '어느', '우와', '하자', '이번에는', '깜짝', }
    keywords, sents = summarize_with_sentences(
                    [texts],
                    stopwords = stopwords,
                    diversity=0.5,
                    min_count=1,
                    num_keywords=10,
                    num_keysents=10,
    )
    keywords = list(keywords.keys())
    print(keywords)
    keywords = [j[0] for i in keywords for j in okt.pos(i) if j[1] == 'Noun' and len(j[0]) > 1]
    if len(keywords) == 0 :
        return 'nothing'
    return keyword_translate(keywords[0])

class ResidualBlock(nn.Module):
    def __init__(self, use_bias=False):
        super(ResidualBlock, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1, bias=use_bias)
        self.norm_1 = nn.InstanceNorm2d(256)
        self.conv_2 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1, bias=use_bias)
        self.norm_2 = nn.InstanceNorm2d(256)
        # self.norm_1 = nn.BatchNorm2d(256)
        # self.norm_2 = nn.BatchNorm2d(256)

    def forward(self, x):
        output = self.norm_2(self.conv_2(F.leaky_relu(self.norm_1(self.conv_1(x)))))
        return output + x

class Generator(nn.Module):
    def __init__(self, use_bias=False):
        super(Generator, self).__init__()
        self.conv_1 = nn.Conv2d(in_channels=3, out_channels=64, kernel_size=7, stride=1, padding=3, bias=use_bias)
        # self.norm_1 = nn.BatchNorm2d(64)
        self.norm_1 = nn.InstanceNorm2d(64)
        
        # down-convolution #
        self.conv_2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3, stride=2, padding=1,bias=use_bias)
        self.conv_3 = nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1,bias=use_bias)
        # self.norm_2 = nn.BatchNorm2d(128)
        self.norm_2 = nn.InstanceNorm2d(128)
        
        self.conv_4 = nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=2, padding=1,bias=use_bias)
        self.conv_5 = nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1,bias=use_bias)
        # self.norm_3 = nn.BatchNorm2d(256)
        self.norm_3 = nn.InstanceNorm2d(256)
        
        # residual blocks #
        residualBlocks = []
        for l in range(8):
            residualBlocks.append(ResidualBlock())
        self.res = nn.Sequential(*residualBlocks)
        
        # up-convolution #
        self.conv_6 = nn.ConvTranspose2d(in_channels=256, out_channels=128, kernel_size=3, stride=2, padding=1, output_padding=1, bias=use_bias)
        self.conv_7 = nn.ConvTranspose2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1, bias=use_bias)
        self.norm_4 = nn.InstanceNorm2d(128)
        # self.norm_4 = nn.BatchNorm2d(128)

        self.conv_8 = nn.ConvTranspose2d(in_channels=128, out_channels=64, kernel_size=3, stride=2, padding=1, output_padding=1, bias=use_bias)
        self.conv_9 = nn.ConvTranspose2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1, bias=use_bias)
        self.norm_5 = nn.InstanceNorm2d(64)
        # self.norm_5 = nn.BatchNorm2d(64)
        
        self.conv_10 = nn.Conv2d(in_channels=64, out_channels=3, kernel_size=7, stride=1, padding=3, bias=use_bias)
        

    def forward(self, x):
        x = F.leaky_relu(self.norm_1(self.conv_1(x)))
        x = F.leaky_relu(self.norm_2(self.conv_3(self.conv_2(x))))
        x = F.leaky_relu(self.norm_3(self.conv_5(self.conv_4(x))))
        
        x = self.res(x)

        x = F.leaky_relu(self.norm_4(self.conv_7(self.conv_6(x))))
        x = F.leaky_relu(self.norm_5(self.conv_9(self.conv_8(x))))

        x = self.conv_10(x)

        x = sigmoid(x)

        return x


bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/', methods=('GET','POST'))
def make():
    msg = None
    
    if request.method == 'POST':
        content = request.form['writecontent']
        if not content:
            msg = "키워드나 짧은 문장을 작성해주세요!"
        
        if msg is None:
            return render_template('book/makebook.html')
        
    return render_template('book/makebook.html', msg=msg)


@bp.route('/req', methods=['POST'])
def req():
    data = request.get_json()                 
    return jsonify(data)

@bp.route('/req_story', methods=['POST'])
def req_story():
    data = request.get_json()
    if data['inputdata']:
        hanspell_sent = preprocessing(data['inputdata'])
        res = outputmodel(hanspell_sent)
        outputdata = preprocessing(res)
        output = {'outputdata' : outputdata}
    else:
        output = {}        
    return jsonify(output)                

@bp.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    temp = "temp"
    if data['alldata']:
        book_contents = data['alldata']
        book_contents = re.sub('[.+]','.',book_contents)
        
        sb = Storybook(book_con=book_contents,
                    member_no=g.user.member_no,
                    book_title=temp,
                    book_date =  utc.localize(now).astimezone(KST))
        db.session.add(sb)
        db.session.commit()
        
        # 문장 분할   
        DIVN = 5
        split_content = []
        temp = ''
        storyArray = []
        
        split_content = book_contents.split('.')
        for idx, sentence in enumerate(split_content):
            if sentence:
                if idx % DIVN+1 < DIVN:
                    temp += sentence+'. '
                else:
                    temp += sentence+'. '
                    storyArray.append(temp)
                    temp = ''
        if temp:
            storyArray.append(temp)
        print('1 ok')
        # 모델 로드
        vqvae_path = '../project/BeAwriter/static/imgmodel/stage1/model.pt'
        model_vqvae, _ = load_model(vqvae_path)
        
        model_path = '../project/BeAwriter/static/imgmodel/stage2/model.pt'
        model_ar, config = load_model(model_path, ema=False)

        model_ar = model_ar.cuda().eval()
        model_vqvae = model_vqvae.cuda().eval()

        model_clip, preprocess_clip = clip.load("ViT-B/32", device='cuda')
        model_clip = model_clip.cuda().eval()
            
        text_encoder = TextEncoder(tokenizer_name=config.dataset.txt_tok_name, 
                            context_length=config.dataset.context_length)
        print('2 ok')
        print(storyArray)
        for idx, sa in enumerate(storyArray):
            # 키워드
            text_prompts = extraction_keyword(sa)
            text_prompts = 'Cartoon of ' + text_prompts
            print(text_prompts)

            # 이미지
            num_samples = 1
            temperature= 0.8
            top_k=2048
            top_p=0.95

            pixels = get_generated_images_by_texts(model_ar,
                                            model_vqvae,
                                            text_encoder,
                                            model_clip,
                                            preprocess_clip,
                                            text_prompts,
                                            num_samples,
                                            temperature,
                                            top_k,
                                            top_p)
            print('3 ok')
            images = [pixels.cpu().numpy() * 0.5 + 0.5]
            images = torch.from_numpy(np.array(images))
            images = torch.clamp(images, 0, 1)
            grid = torchvision.utils.make_grid(images)
            img = Image.fromarray(np.uint8(grid.numpy().transpose([1,2,0])*255))
            IMGPATH = f'{sb.book_no}_{idx}.jpg'
            img.save('../project/BeAwriter/static/pageimage/'+IMGPATH)   
            print('4 ok')
            pi = Pageimage(book_no=sb.book_no,
                        pageper_img_no=idx,
                        pageimg_path=IMGPATH)
            db.session.add(pi)
            db.session.commit()
            print('5 ok')
            
        book = {'bookn' : sb.book_no,
                'con' : sb.book_con}

    else:
        book = {}        
    return jsonify(book)

@bp.route('/cover/<int:book_no>/', methods=('GET','POST'))
def cover(book_no):
    msg1 = None
    msg = []  
    sb = Storybook.query.get(book_no)
    title = None
    isTitle = None
    if sb.book_title=="temp":
        isTitle = False
    else:
        isTitle = True

    if request.method == 'POST':
        if not isTitle and sb.book_title=="temp":
            title = request.form['title']
            if not title:
                msg1 = '제목을 입력해주세요!'
            else:
                sb.book_title = title
                db.session.commit()
                isTitle = True
                return render_template('book/bookcover.html', msg=msg, msg1=msg1, book_no=book_no, isTitle=isTitle)
        
        else:
            f = request.files['file']
            if not f:
                msg = ["파일을 넣고 제출 버튼을 눌러주세요.","생략 하시려면 생략하기 버튼을 눌러주세요."]
            else:
                extension=f.filename.split('.')[-1]
                filename=f'{g.user.member_no}_{sb.book_no}.{extension}'
                f.save('../project/BeAwriter/static/image/1/'+ filename)
                
                # 이미지 변환
                device = torch.device('cpu')
                if torch.cuda.is_available():
                    device = torch.device('cuda')
                    print("Train on GPU.")
                else:
                    print("No cuda available")
                checkpoint = torch.load('../project/BeAwriter/static/covermodel/best_checkpoint.pth', map_location=torch.device(device))
                G_inference = Generator()
                G_inference.load_state_dict(checkpoint['g_state_dict'])
                
                transformer = transforms.Compose([
                    transforms.Resize((350, 450)),
                    transforms.ToTensor()
                ])
                test_images = Image.open('../project/BeAwriter/static/image/1/'+filename).convert('RGB')
                test_images = transformer(test_images)[None,]
                result_images_best_checkpoint = G_inference(test_images)
                
                filename_new = f'{g.user.member_no}_{sb.book_no}.jpg'
                images = np.transpose(result_images_best_checkpoint[0].detach().numpy(), (1, 2, 0))
                plt.imsave('../project/BeAwriter/static/maked_image/'+filename_new,images)
                            
                img = CoverImage(book_no=sb.book_no,
                            img_path=filename,
                            maked_img_path=filename_new)
                db.session.add(img)
                db.session.commit()

        if len(msg)==0 and msg1 is None:
            return redirect(url_for('book.readbook', book_no=book_no))
            
    return render_template('book/bookcover.html', msg=msg, msg1=msg1, book_no=book_no, isTitle=isTitle)

@bp.route('/bookstar/<int:book_no>', methods=('GET','POST'))
def bookstar(book_no):
    error = None
    book = None
    isIt = None
    
    if request.method == 'POST':
        try:
            VALUE = request.form['rating']
            star = Rating(member_no=g.user.member_no,
                          book_no=book_no,
                          rating=int(VALUE))
            db.session.add(star)

            book = Storybook.query.get(book_no)

            if book.avg == 0:
                book.avg = VALUE

            else:
                book_avg =db.session.query(func.avg(Rating.rating))\
                    .join(Storybook)\
                    .filter(Rating.book_no == book.book_no)
                book.avg = book_avg
            db.session.commit()
            
            book = Storybook.query.get(book_no)
            
            if book.avg == 0:
                book.avg = VALUE
            else:
                book_avg = Rating.query.with_entities(Rating.book_no, func.avg(Rating.rating))\
                                 .filter(book.book_no == Rating.book_no)\
                                 .group_by(Rating.book_no).first()[1]
                book.avg = book_avg
            db.session.commit()
            
        except Exception:
            error = "평점을 매겨주세요!"
    
        if error is None:
            return redirect(url_for('main.index'))
    
    else:
        isIt = Rating.query.filter(and_(Rating.member_no==g.user.member_no,
                                        Rating.book_no==book_no)).first()
          
    return render_template("/book/bookstar.html", error=error, book_no=book_no, book=book, isIt=isIt)


@bp.route('/readbook/<int:book_no>/')
def readbook(book_no):
    book = Storybook.query.get_or_404(book_no)
    image = CoverImage.query.get(book_no)
    content = book.book_con

    DIVN = 5
    split_content = []
    temp = ''
    storyArray = []
    
    pageimagepath_list = []
    
    filename=str(book.book_no)+'.mp3'
    audio = 'audio/'+filename
    if not book.speak_path:
        tts=gTTS(text=content, lang='ko')
        audio_path = '../project/BeAwriter/static/audio/'+filename
        tts.save(audio_path)
        
        book.speak_path = audio_path
        db.session.commit()

    split_content = content.split('.')
    for idx, sentence in enumerate(split_content):
        if idx % DIVN+1 < DIVN:
            temp += sentence+'. '
        else:
            temp += sentence+'. '
            storyArray.append(temp)
            temp = ''

    if temp:
        storyArray.append(temp)

    pageimage_list = Pageimage.query.filter(Pageimage.book_no==book_no).all()
    for pi in pageimage_list:
        pageimagepath_list.append(pi.pageimg_path)
    print(pageimagepath_list)
    
    return render_template("/book/readbook.html", book=book, storyArray=storyArray, image=image, book_no=book_no, audio=audio, pageimagepath_list=pageimagepath_list)
    