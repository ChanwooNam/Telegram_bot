from flask import Flask, render_template, request
from decouple import config
import requests
import random

app = Flask(__name__)

api_url = 'https://api.telegram.org'
token = config('TELEGRAM_BOT_TOKEN')
chat_id = config('CHAT_ID')

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/write')
def write():
    return render_template('write.html')

@app.route('/send')
def send():
    text = request.args.get('message')
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    return '<h1>전송이되는지 확인 !!</h1>'

# token 정보를 경로에 주어서 노출되지 않는한 해킹 당하지 않게 한다
# webbook을 걸어둔 서버가 있으면 거기로 계속 정보를 보낸다 
# 텔레그램 서버가 우리 서버에게 HTTP POST 요청을 통해
# 사용자 메세지 정보를 받아라고 전달해주는 것
# 우리가 status 200을 리턴해줘야 텔레그램측이 더이상의 전송을 중단한다.
# 200을 안돌려주면 계속~~ POST 요청을 여러번 보낸다.
@app.route(f'/{token}', methods=['POST'])
def telagram():
    # 1. 메아리(Echo) 기능
    # 1.1 request.get_json() 구조 확인하기
    print(request.get_json())
    # 1.2 [실습] 사용자 아이디, 텍스트 가져오기
    chat_id = request.get_json().get('message').get('from').get('id')
    text = request.get_json()['message']['text']
    # 1.3 [실습] 텔레그램 API에게 요청을 보내서 답변해주기
    #requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

   
    if text == '/로또':
         # 1. [기본] 로또 기능 (random...?)
         #    사용자가 '/로또'라고 말하면 랜덤으로 번호 6개 뽑아서 돌려주기!
         #    나머지 경우엔 전부 메아리 칩시다
        rotto_num = random.sample(range(1,46),6)
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={rotto_num}')
    elif text[0:7] == '/vonvon' and len(text) > 7: 
        # 2. [심화] vonvon 기능
        #    사용자가 '/vonvon 이름'이라고 말하면 신이 나를 만들었을 때 요소 돌려주기 
        
        # 2.1 사용자가 입력한 데이터를 가져온다. 
        user_name = text[7:]
        # 2.2 사용자에게 보여줄 여러가지 재밌는 특성들 리스트를 만든다. 
        first_list = ['잘생김', '못생김', '많이 못생김', '그냥 존잘..', '다비드 조각상', '그냥 정우성..', '개존잘..']
        second_list = ['순수함', '변태', '착함', '바보', '천재']
        third_list = ['허세', '물욕', '식욕', '수면욕', ]
        # 2.3 리스트에서 랜덤으로 하나씩을 선택한다. 
        first = random.choice(first_list)
        second = random.choice(second_list)
        third = random.choice(third_list)

        text = f'{user_name}님은 {first}한 스푼 넣고.. {second} 두 스푼 넣고.. {third} 너무 많이 넣었다...'
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')
    else :
        # 메아리 
        requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}')

    
    # 정상적으로 받으면 200 ok를 보내준다
    return '', 200


if __name__ == '__main__':
    app.run(debug=True)