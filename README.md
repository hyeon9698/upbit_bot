# upbit_bot 가상화폐 변동성 돌파 전략 프로그램 (업비트용)
(필요한 코드가 있으시면 이슈 써주세요! 해당 부분 만들어 드리겠습니다.)
## 가상화폐 매매 자동화 프로그램
- 참고 책: [파이썬을 이용한 비트코인 자동매매 (개정판)](https://wikidocs.net/book/1665) ![image](https://user-images.githubusercontent.com/41141851/115146002-a4c3e080-a08f-11eb-85bc-122ee056a2c0.png)
- 참고 코드: [파이썬을 이용한 비트코인 자동매매](https://github.com/sharebook-kr/book-cryptocurrency) (Apache License 2.0)
1. main.py -> 비트코인 + 알트코인을 자동으로 매매해 주는 봇 + 실시간 진행 상황을 Telegram으로 문자 전송 + 데이터를 쌓아서 실제로 얼마를 벌었는지 비교
2. check.py -> 봇을 못 믿는 사람을 위해 실시간으로 변동성을 파악해서 알려주는 봇, 매수 매도는 사용자가 하기
3. compair.py -> 실재로 존버를 했을 경우와 변동성 돌파 전략을 사용했을 경우를 비교하는 코드
### 실행방법

[https://www.upbit.com/service_center/open_api_guide](https://www.upbit.com/service_center/open_api_guide) 사이트에서 로그인을 한 후 (구글에 upbit api 치시면 바로 나옵니다.)

Open API 사용하기를 클릭해서 로그인을 합니다.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4ff57bc1-3159-4068-844c-92b4f0908d61/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/4ff57bc1-3159-4068-844c-92b4f0908d61/Untitled.png)

코드에 필요한 권한을 체크합니다. 출금하기와 입금하기는 안 해도 됩니다.

특정IP에서만 실행 부분에서 자신의 IP를 넣습니다.

그러면 upbit Access key와 upbit Secret key를 받고 메모에 써놓습니다. 이 값들은 다른 사람에게 절대 보여주면 안 됩니다.

[텔레그램 봇 참고 사이트]([https://co-vision.gitbook.io/co-vision/how-to-build/sw-build/4.-required-api#telegram-api](https://co-vision.gitbook.io/co-vision/how-to-build/sw-build/4.-required-api#telegram-api))

해당 사이트에서 Telegram API부분을 참고하여 upbit 봇을 만듭니다. 해당 사이트 "3. HTTP API를 받는다" 부분에서 HTTP API 값을 메모에 저장을 합니다. 

해당 사이트 "4. user number ID를 구한다" 부분에서 user id를 메모에 저장을 합니다. 추후에 telegram-mc-key에 넣을 것 입니다.

참고로 해당 사이트는 예전 제가 했던 프로젝트입니다.

vscode 또는 pythonanywhere 사이트에서 아래 코드를 진행을 합니다.

### [main.py](http://main.py/)

```
# 깃허브 클론
git clone <https://github.com/hyeon9698/upbit_bot>
cd upbit_bot
# 가상 환경 세팅
pip3 install virtualenv
virtualenv upbit --python=python3.8
source upbit/bin/activate
# 필요한 requirments 다운
pip install -r requirements.txt

```

에디터를 이용해서 main.py로 들어갑니다.

아까 써놓았던 upbit-api-key에서 access key와 secret key를 넣고, telegram-api-key에서 telegram token key와 telegram mc key를 넣습니다.

그리고 coin_list에서 자신이 투자할 코인을 적어두고

percent_list에는 가진 돈의 몇 프로를 한 코인에 투자할 것인지에 대한 변수를 수정합니다.

![https://s3-us-west-2.amazonaws.com/secure.notion-static.com/823b9039-1317-4f8c-8ea9-c0271258296c/Untitled.png](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/823b9039-1317-4f8c-8ea9-c0271258296c/Untitled.png)

```
# 메인 코드 실행
python main.py
```

참고로 해당 코드는 k값은 0.5이고 이동평균은 5일을 보고 지금 가격이 target을 넘었을 경우 & 지금 가격이 이동평균 보다 높을 경우 구매를 합니다.
#### main.py
```python
# 깃허브 클론
git clone https://github.com/hyeon9698/upbit_bot
cd upbit_bot
# 가상 환경 세팅
pip3 install virtualenv
virtualenv upbit --python=python3.8
source upbit/bin/activate
# 필요한 requirments 다운
pip install -r requirements.txt
# 메인 코드 실행
python main.py
```
#### check.py
```python
# 깃허브 클론
git clone https://github.com/hyeon9698/upbit_bot
cd upbit_bot
# 가상 환경 세팅
pip3 install virtualenv
virtualenv upbit --python=python3.8
source upbit/bin/activate
# 필요한 requirments 다운
pip install -r requirements.txt
# 메인 코드 실행
python check.py
```
### 코인을 추가할 때
- own_coin_list_04_08 정보 갱신
- coin_list 정보 갱신
- percent_list 정보 갱신
- reset_dataset.csv 파일 정보 갱신
- dataset.csv 파일 정보 갱신
- pythonanywhere 에서 main.py, dataset.csv, reset_dataset.csv 업데이트

#### 투자의 책임은 투자자 본인에게 있습니다.
