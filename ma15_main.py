import pyupbit
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import telegram # pip install python-telegram-bot
import json
from dotenv import load_dotenv # pip install python-dotenv
import os

def printall():
    msg = f"------------------------------{now.strftime('%Y-%m-%d %H:%M:%S')}------------------------------\n"
    for i in range(n):
        msg += f"{'%10s'%coin_list[i]} ma15: {'%11.2f'%ma15[i]} 현재가: {'%11.2f'%price_now[i]} 매수금액: {'%7d'%money_list[i]} hold: {'%5s'%hold[i]}\n"
    print(msg)
def buy(ticker, money):
    time.sleep(0.1)
    b = upbit.buy_market_order(ticker, money)
    try:
        if b['error']:
            b = upbit.buy_market_order(ticker, 50000)
            msg = "돈 좀 부족해서 " + str(ticker)+" "+str(50000)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    except:
        msg = str(ticker)+" "+str(money)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)
def sell(ticker):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker)
    s = upbit.sell_market_order(ticker, balance)
    msg = str(ticker)+" 매도 시도"+"\n"+json.dumps(s, ensure_ascii = False)
    print(msg)
    bot.sendMessage(mc,msg)
def get_ma15_high(ticker):
    df_get_ma15 = pyupbit.get_ohlcv(ticker, interval="minute15")
    close = df_get_ma15['close']
    ma = close.rolling(window=15).mean()
    high = df_get_ma15['high']
    return ma[-2], high[-2]

load_dotenv()
access = os.getenv('UPBIT_API_ACCESS_KEY')
secret = os.getenv('UPBIT_API_SECRET_KEY')
upbit = pyupbit.Upbit(access, secret)
token = os.getenv('TELEGRAM_API_TOKEN_KEY')
mc = os.getenv('TELEGRAM_API_MC')
bot = telegram.Bot(token)
df = pd.read_csv('dataset.csv')

# 32 coins
coin_list = ["KRW-ENJ", "KRW-SAND", "KRW-TRX", "KRW-BTT", "KRW-XRP", "KRW-DKA", "KRW-MLK", "KRW-AQT", "KRW-MED", "KRW-BTC", 
            "KRW-ADA", "KRW-ETH", "KRW-BCH", "KRW-PCI", "KRW-BORA", "KRW-XLM", "KRW-XEM", "KRW-EOS", "KRW-STRAX", "KRW-PUNDIX", 
            "KRW-MANA", "KRW-STRK", "KRW-QTUM", "KRW-HBAR", "KRW-SNT", "KRW-VET", "KRW-STX", "KRW-SC", "KRW-CRO", "KRW-NEO",
            "KRW-GAS", "KRW-DOGE"]
# percent_list = [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]

n = len(coin_list)
coin_waiting_15 = [True]*n
hold = [True]*n
money_list = [100000]*n
save = False
ma15 = [0]*n
high = [0]*n
price_now = [0]*n
time_save = True
df = pd.read_csv('ma15_main.csv')

#############새롭게 시작하는거면 이 부분 주석처리하기###################
for i in range(n):
    hold[i] = df.loc[i, 'hold']
    coin_waiting_15[i] = df.loc[i, 'coin_waiting_15']
#####################################################################

for i in range(n):
    time.sleep(0.1)
    ma15[i], high[i] = get_ma15_high(coin_list[i])

while True:
    # 지금 한국 시간
    now = datetime.now(timezone('Asia/Seoul'))

    if not time_save:
        if (now.hour-1) % 6 == 0:
            time_save = True

    if save and (now.minute-1) % 15 == 0:
        save = False
    
    if not save and now.minute % 15 == 0 and now.second >= 20:
        for i in range(n):
            time.sleep(0.1)
            ma15[i], high[i] = get_ma15_high(coin_list[i])
            coin_waiting_15[i] = False
            df.loc[i, 'coin_waiting_15'] = False
            df.to_csv('ma15_main.csv', index=None)
        save = True
        print("------------------------------ma15와 high 갱신------------------------------")
    
    for i in range(n):
        time.sleep(0.1)
        price_now[i] = pyupbit.get_current_price(coin_list[i])

    for i in range(n):
        if not hold[i] and ma15[i] <= price_now[i]:
            buy(coin_list[i], money_list[i])
            hold[i] = True
            coin_waiting_15[i] = True
            df.loc[i, 'hold'] = True
            df.loc[i, 'coin_waiting_15'] = True
            df.to_csv('ma15_main.csv', index=None)
    
    for i in range(n):
        if hold[i] and ma15[i] > high[i] and not coin_waiting_15[i]:
            sell(coin_list[i])
            hold[i] = False
            coin_waiting_15[i] = True
            df.loc[i, 'hold'] = False
            df.loc[i, 'coin_waiting_15'] = True
            df.to_csv('ma15_main.csv', index=None)
    printall()

    if (now.hour % 6) == 0 and time_save:
        time_save = False
        msg = f"지금 {now.hour}시입니다. 코드가 잘 실행되고 있습니다."
        bot.sendMessage(mc,msg)
        
    # time.sleep(0.1)
