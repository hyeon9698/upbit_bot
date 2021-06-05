# upbit_bot 가상화폐 변동성 돌파 전략 프로그램 (업비트용)
(필요한 코드가 있으시면 이슈 써주세요! 해당 부분 만들어 드리겠습니다.)
## 가상화폐 매매 자동화 프로그램
- 참고 책: [파이썬을 이용한 비트코인 자동매매 (개정판)](https://wikidocs.net/book/1665) ![image](https://user-images.githubusercontent.com/41141851/115146002-a4c3e080-a08f-11eb-85bc-122ee056a2c0.png)
- 참고 코드: [파이썬을 이용한 비트코인 자동매매](https://github.com/sharebook-kr/book-cryptocurrency) (Apache License 2.0)
1. main.py -> 비트코인 + 알트코인을 자동으로 매매해 주는 봇 + 실시간 진행 상황을 Telegram으로 문자 전송 + 데이터를 쌓아서 실제로 얼마를 벌었는지 비교
2. check.py -> 봇을 못 믿는 사람을 위해 실시간으로 변동성을 파악해서 알려주는 봇, 매수 매도는 사용자가 하기
3. compair.py -> 실재로 존버를 했을 경우와 변동성 돌파 전략을 사용했을 경우를 비교하는 코드
### 실행방법

[https://www.upbit.com/service_center/open_api_guide](https://www.upbit.com/service_center/open_api_guide) 사이트에서 upbit API key를 가지고 옵니다. (구글에 upbit api 치시면 바로 나옵니다.)

![test](https://user-images.githubusercontent.com/41141851/118991825-080e9e80-b9bf-11eb-9f74-8e9bb6584138.png)


Open API 사용하기를 클릭해서 로그인을 합니다.

![test](https://user-images.githubusercontent.com/41141851/118991974-2b394e00-b9bf-11eb-8df7-a4d5e6cbd7c2.png)

코드에 필요한 권한을 체크합니다. 출금하기와 입금하기는 안 해도 됩니다.

특정IP에서만 실행 부분에서 자신의 IP를 넣습니다.

그러면 upbit Access key와 upbit Secret key를 받고 메모에 써놓습니다. 이 값들은 다른 사람에게 절대 보여주면 안 됩니다.

[텔레그램 봇 참고 사이트](https://co-vision.gitbook.io/co-vision/how-to-build/sw-build/4.-required-api#telegram-api) 여기에 들어가서 해당 사이트에서 Telegram API부분을 참고하여 upbit 봇을 만듭니다. 

![test](https://user-images.githubusercontent.com/41141851/118992220-676cae80-b9bf-11eb-9961-9131f2b94696.png)

해당 사이트 "3. HTTP API를 받는다" 부분에서 HTTP API 값을 메모에 저장을 합니다. 

해당 사이트 "4. user number ID를 구한다" 부분에서 user id를 메모에 저장을 합니다. 추후에 telegram-mc-key에 넣을 것 입니다.

참고로 해당 사이트는 예전 제가 했던 프로젝트입니다.

vscode 또는 pythonanywhere 사이트에서 아래 코드를 진행을 합니다.

### main.py
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

```

에디터를 이용해서 main.py로 들어갑니다.

![test](https://user-images.githubusercontent.com/41141851/118992432-9aaf3d80-b9bf-11eb-8843-d3cca4b3673c.png)

아까 써놓았던 upbit-api-key에서 access key와 secret key를 넣고, telegram-api-key에서 telegram token key와 telegram mc key를 넣습니다.

그리고 coin_list에서 자신이 투자할 코인을 적어두고

percent_list에는 가진 돈의 몇 프로를 한 코인에 투자할 것인지에 대한 변수를 수정합니다.

```python
# 메인 코드 실행
python main.py
```

참고로 해당 코드는 k값은 0.5이고 이동평균은 5일을 보고 지금 가격이 target을 넘었을 경우 & 지금 가격이 이동평균 보다 높을 경우 구매를 합니다.

### check.py
```python
# 메인 코드 실행
python check.py
```
실시간으로 몇 프로 올랐고 내렸고를 확인 할 수 있습니다.

### compair.py (backtesting)
![test](https://user-images.githubusercontent.com/41141851/118996709-0f37ab80-b9c3-11eb-9824-5e8a48d87688.png)
compair.py 코드를 통해 2주동안 존버를 했을 경우와 변동성 돌파를 사용한 결과를 비교를 해 봤습니다. (2021.05.20 기준)
존버를 했을 경우 -22.92% 손해를 입고
변동성 돌파를 사용한 경우 적절한 k값과 이동평균 값을 사용한다면 최저 -0.51% 손해를 본 것을 알 수 있습니다.
하락장에서는 확실히 방어를 하는 매매 방법인 것 같습니다.

### dataset.csv
코드가 갑자기 종료될 경우 바로 다시 실행 가능하게 csv 파일을 읽어서 실행을 하게 만들었습니다.

### saved_data.csv
날짜, 존버 했을 경우와 안 했을 경우를 비교해서 정리하는 데이터 파일 입니다.

### 코인을 추가하고 싶을 때
- coin_list 정보 갱신
- reset_dataset.csv 파일 정보 갱신
- dataset.csv 파일 정보 갱신

#### 투자의 책임은 투자자 본인에게 있습니다.
