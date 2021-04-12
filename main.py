import pyupbit
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import telegram # pip install python-telegram-bot
import json
from dotenv import load_dotenv # pip install python-dotenv
import os

def cal_target(ticker):
    time.sleep(0.1)
    df_cal_target = pyupbit.get_ohlcv(ticker, "day")
    yesterday = df_cal_target.iloc[-2]
    today = df_cal_target.iloc[-1]
    yesterday_range = yesterday['high'] - yesterday['low']
    target = today['open'] + yesterday_range * 0.5
    return target
def sell(ticker):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker)
    s = upbit.sell_market_order(ticker, balance)
    msg = str(ticker)+"매도 시도"+"\n"+json.dumps(s, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)
def buy(ticker, money):
    time.sleep(0.1)
    b = upbit.buy_market_order(ticker, money)
    msg = str(ticker)+" "+str(money)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)
def printall():
    print(f"------------------------------{now.strftime('%Y-%m-%d %H:%M:%S')}------------------------------" )
    for i in range(n):
        print(f"{'%8s'%coin_list[i]} 목표가: {'%11.1f'%target[i]} 현재가: {'%11.1f'%prices[i]} 매수금액: {'%7d'%money_list[i]} hold: {'%5s'%hold[i]} status: {op_mode[i]}")
def save_data(krw_balance):
    own_coin_list_04_08 = [
        380.92350925, # enj
        1830.30246740, # sand
        0, # trx
        164545.48742559, # btt
        0, # xrp
        3060.94093686, # dka
        173.66460848, # mlk
        0.47666666, # aqt
        1855.12241723, #med
        0.00550091, #btc
        250.37281553, #ada
        0.09961308, # eth
        0.14317678, # bch
        0, # pci
        0, # bora
        0 #xlm
    ]
    now_prices = [-1]*(n) 
    jonbeo = "----------들고만 있었으면----------\n"
    total_jonbeo = 0
    auto_upbit = "----------자동화----------\n"
    auto_upbit += "자동화 총 금액 -> " + str(krw_balance) + "\n"
    for i in range(n):
        now_prices[i] = pyupbit.get_current_price(coin_list[i])
        total_jonbeo += now_prices[i]*own_coin_list_04_08[i]
        jonbeo += coin_list[i] + " 현 가격: " + str(now_prices[i]) + "이 코인의 총 가격" + str(now_prices[i]*own_coin_list_04_08[i]) + "\n"
        time.sleep(0.3)
    total_jonbeo += 1610370
    jonbeo += "지금까지 존버했으면 총 금액 -> " + str(total_jonbeo) + "\n"
    msg = jonbeo + auto_upbit + "존버와의 금액 차이 -> " + str(krw_balance - total_jonbeo) + "원 벌었음(-이면 잃은거)"
    df2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])
    df2 = df2.append({'date':now.strftime('%Y-%m-%d %H:%M:%S'), 'jonbeo':total_jonbeo, 'auto_upbit': krw_balance, 'difference_jonbeo_autoupbit':krw_balance - total_jonbeo}, ignore_index=True)
    df2.to_csv('saved_data.csv', mode='a', header=False)
    print(msg)
    bot.sendMessage(mc,msg)
def get_yesterday_ma5(ticker):
    df_get_yesterday_ma5 = pyupbit.get_ohlcv(ticker)
    close = df_get_yesterday_ma5['close']
    ma = close.rolling(window=5).mean()
    return ma[-2]
# 객체 생성
load_dotenv()
access = os.getenv('UPBIT_API_ACCESS_KEY')
secret = os.getenv('UPBIT_API_SECRET_KEY')
upbit = pyupbit.Upbit(access, secret)
token = os.getenv('TELEGRAM_API_TOKEN_KEY')
mc = os.getenv('TELEGRAM_API_MC')
bot = telegram.Bot(token)
df = pd.read_csv('dataset.csv')
df2 = pd.DataFrame(columns=['date','jonbeo','auto_upbit','difference_jonbeo_autoupbit'])

# 변수 설정
# 총 16개
# ENJ 엔진코인 18%
# SAND 샌드박스 18%
# TRX 트론 18%
# BTT 비트토렌트 10%
# XRP 리플 3%
# DKA 디카르고 3%
# MLK 밀크 3%
# AQT 알파쿼크 3%
# MED 메디블록 3%
# BTC 비트코인 3%
# ADA 에이다 3%
# ETH 이더리움 3%
# BCH 비트코인캐시 3%
# PCI 페이코인 3%
# BORA 보라 3%
# XLM 스텔라루멘 3%

INF = 1000000000000
coin_list = ["KRW-ENJ", "KRW-SAND", "KRW-TRX", "KRW-BTT", "KRW-XRP", "KRW-DKA", "KRW-MLK", "KRW-AQT", "KRW-MED", "KRW-BTC", "KRW-ADA", "KRW-ETH", "KRW-BCH", "KRW-PCI", "KRW-BORA", "KRW-XLM"]
percent_list = [0.18, 0.18, 0.18, 0.10, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03, 0.03]
n = len(coin_list)
money_list = [0]*(n)
op_mode = [False] * (n) # 당일 9시에 코드를 시작하지 않았을 경우를 위한 변수
hold = [False] * (n) # 해당 코인을 가지고 있는지
target = [INF]*(n)
prices = [-1]*(n)
save1 = True
save2 = True
krw_balance = 0
now = datetime.now(timezone('Asia/Seoul'))
prev_day = now.day
yesterday_ma5 = [0]*(n)

# 중간에 시작하더라도 아침 9시에 보유한 코인들을 팔 수 있게 만들었음
print("----------현재 보유중인 코인 개수----------")
for i in range(n):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker=coin_list[i])
    print("%8s"%coin_list[i]," -> ", balance, "개")
    if balance > 0:
        df.loc[i, 'hold'] = True
        df.to_csv('dataset.csv', index=None)
        hold[i] = True
print("----------어제 ma5 가격----------")
for i in range(n):
    time.sleep(0.1)
    yesterday_ma5[i] = get_yesterday_ma5(coin_list[i])
    print(f"{'%8s'%coin_list[i]} -> {'%11.1f'%yesterday_ma5[i]} 원")

# 중간에 시작하더라도 target 데이터와 money_list 데이터 op_mode, hold데이터 가지고 옴
for i in range(n):
    target[i] = df.loc[i,'target']
    money_list[i] = df.loc[i,'money_list']
    hold[i] = df.loc[i,'hold']
    op_mode[i] = df.loc[i,'op_mode']

# 만약 코드를 실행할때 지금이 아침 8시가 지났을 경우 9시까지 거래를 안한다.
## 추후에 수정 필요 이걸 할지 안 할지 밤 새서 코드가 돌아가는 확신이 있으면 없애도 될듯
## 밑에 코드는 밤사이 코드가 멈췄을때를 위한 장치, 사는 것을 멈춤
if now.hour == 8:
    print("8시에 코드를 실행했으므로 save guard가 실행됩니다.")
    print("만약 이게 없었으면 당신은: ")
    time.sleep(0.1)
    flag = True
    for i in range(n):
        if op_mode[i] and not hold[i]:
            time.sleep(0.1)
            if target[i] < pyupbit.get_current_price(coin_list[i]):
                flag = False
                print(f"{coin_list[i]} 를 {money_list[i]} 만큼 구매 예정이었습니다. 그리고 오전 9시에 팔았을 겁니다.")
    if flag:
        print("아무일도 일어나지 않았습니다. save guard가 실행됩니다. 9시가 되면 리셋 됩니다.")
    for i in range(n):
        op_mode[i] = False
        df.loc[i,'op_mode'] = False

while True:
    # 지금 한국 시간
    now = datetime.now(timezone('Asia/Seoul'))
    
    # 하루에 한번 작동하는 save
    if prev_day != now.day:
        prev_day = now.day
        save1 = True
        save2 = True
        msg = "save 변수가 True로 업데이트 됐습니다.\nsave1: " + str(save1) + " save2 -> " + str(save2)
        bot.sendMessage(mc,msg)

    # 매도 시도
    if now.hour == 8 and now.minute == 59 and save1:
        time.sleep(1)
        for i in range(n):
            sell(coin_list[i])
            hold[i] = False
            df.loc[i, 'hold'] = False
            df.to_csv('dataset.csv', index=None)
            op_mode[i] = False
            df.loc[i, 'op_mode'] = False
            df.to_csv('dataset.csv', index=None)
        print('----------전부 매도 완료----------')

        # 매도가 다 되고 나서
        time.sleep(0.1)
        krw_balance = upbit.get_balance("KRW")
        for i in range(n):
            money_list[i] = int(krw_balance * (percent_list[i]+0.10))
            df.loc[i, 'money_list'] = money_list[i]
            df.to_csv('dataset.csv', index=None)
        msg = "----------매수할 돈 정보 갱신(money_list)----------\n"
        for i in range(n):
            msg += coin_list[i] + " " + str(money_list[i])+"원"+"\n"
        print(msg)
        bot.sendMessage(mc,msg)
        save_data(krw_balance)
        save1 = False        

    # 09:00:00 목표가 갱신
    if now.hour == 9 and now.minute == 0 and save2:
        for i in range(n):            
            target[i] = cal_target(coin_list[i])
            df.loc[i, 'target'] = target[i]
            df.to_csv('dataset.csv', index=None)
            op_mode[i] = True
            df.loc[i, 'op_mode'] = True
            df.to_csv('dataset.csv', index=None)
        msg = "----------목표가 갱신(target)----------\n"
        for i in range(n):
            msg += coin_list[i] + " " + str(target[i])+"원"+"\n"
        print(msg)
        bot.sendMessage(mc,msg)
        save2 = False
        print("어제 ma5 가격 갱신")
        for i in range(n):
            time.sleep(0.1)
            yesterday_ma5[i] = get_yesterday_ma5(coin_list[i])
            print(f"{'%8s'%coin_list[i]} -> {'%11.1f'%yesterday_ma5[i]} 원")
        msg = ""
        for i in range(n):
            if yesterday_ma5[i] > target[i]:
                msg += str(coin_list[i]) + "는 yesterday_ma5가 target보다 커서 안 사질 수도 있음 yesterday_ma5 -> " yesterday_ma5[i] + " target -> "+target[i]+"\n"
        if msg:
            bot.sendMessage(mc,msg)
            

    # 현 가격 가져오기
    for i in range(n):
        prices[i] = pyupbit.get_current_price(coin_list[i])
        time.sleep(0.1)  # 실행할때는 주석처리하기

    # 매초마다 조건을 확인한 후 매수 시도
    for i in range(n):
        if op_mode[i] and not hold[i] and prices[i] >= target[i] and prices[i] >= yesterday_ma5[i]:
            # 매수
            buy(coin_list[i], money_list[i])
            hold[i] = True
            df.loc[i, 'hold'] = True
            df.to_csv('dataset.csv', index=None)
            print('----------매수 완료------------')

    # 상태 출력
    printall()
msg = "while문 밖으로 나왔습니다 확인해주세요"
bot.sendMessage(mc,msg)
