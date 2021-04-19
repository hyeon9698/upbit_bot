import pyupbit
import time
from datetime import datetime
from pytz import timezone
import telegram
from dotenv import load_dotenv
import os

# 필요 API KEY load
load_dotenv()
access = os.getenv('UPBIT_API_ACCESS_KEY')
secret = os.getenv('UPBIT_API_SECRET_KEY')
upbit = pyupbit.Upbit(access, secret)
token = os.getenv('TELEGRAM_API_TOKEN_KEY')
mc = os.getenv('TELEGRAM_API_MC')
bot = telegram.Bot(token)

# 필요 변수 초기화
coin_list = ["KRW-ENJ", "KRW-SAND", "KRW-DOGE", "KRW-BTT", "KRW-XRP", "KRW-DKA", "KRW-MED", "KRW-BTC", "KRW-ADA", "KRW-ETH"]
n = len(coin_list)
prices_open = [0]*(n)
prices_prev = [0]*(n)
prices_now = [0]*(n)
prices_high_5 = [0]*(n)
prices_high_15 = [0]*(n)
prices_low_5 = [0]*(n)
prices_low_15 = [0]*(n)
save = True
save_high = True
save_low = True
now = datetime.now(timezone('Asia/Seoul'))
prev_day = now.day

# 실행하면 바로 업데이트
for i in range(n):
    prices_open[i] = pyupbit.get_ohlcv(coin_list[i], "day").iloc[-1]['open']
    print(prices_open[i], coin_list[i])
    prices_prev[i] = pyupbit.get_current_price(coin_list[i])
    prices_high_5[i] = prices_prev[i] + prices_prev[i] * 0.05
    prices_high_15[i] = prices_open[i] + prices_open[i] * 0.15
    prices_low_5[i] = prices_prev[i] - prices_prev[i] * 0.05
    prices_low_15[i] = prices_open[i] - prices_open[i] * 0.15
    time.sleep(0.1)

while True:
    # 지금 한국 시간
    now = datetime.now(timezone('Asia/Seoul'))
        
    # 하루에 한번 작동하는 save
    if prev_day != now.day:
        prev_day = now.day
        save = True
        msg = "save 변수가 True로 업데이트 됐습니다.\nsave: " + str(save)
        print(msg)
        bot.sendMessage(mc,msg)
    
    # 매 시간 가격
    msg = f'----------{now.strftime("%Y-%m-%d %H:%M:%S")}----------\n'
    for i in range(n):
        prices_now[i] = pyupbit.get_current_price(coin_list[i])
        msg += f'{"%10s"%coin_list[i]} {prices_now[i]}원\n'
        time.sleep(0.1)
    print(msg)

    # 아침 9시에 prices_open 변수 새로 설정
    if now.hour == 9 and now.minute == 0 and now.second > 30 and save:
        save = False
        msg = "시가가 바꼈습니다.\n"
        for i in range(n):
            prices_open[i] = pyupbit.get_ohlcv(coin_list[i], "day").iloc[-1]['open']
            prices_high_15[i] = prices_open[i] + prices_open[i] * 0.15
            prices_low_15[i] = prices_open[i] - prices_open[i] * 0.15
            msg += f'4%s{coin_list} -> {prices_open[i]}원\n'
            time.sleep(0.1)
        print(msg)
        bot.sendMessage(mc,msg)

    # where the magic happens - main code
    for i in range(n):
        if prices_now[i] >= prices_high_5[i]:
            msg = f'{coin_list[i]} {prices_prev[i]}원 -> {prices_now[i]}원 됨. \n5프로 올랐음 확인 바람\n'
            print(msg)
            bot.sendMessage(mc,msg)
            prices_prev[i] = prices_now[i]
            prices_high_5[i] = prices_now[i] + prices_now[i] * 0.05
            prices_low_5[i] = prices_now[i] - prices_now[i] * 0.05
        if prices_now[i] <= prices_low_5[i]:
            msg = f'{coin_list[i]} {prices_prev[i]}원 -> {prices_now[i]}원 됨. \n5프로 내려감 확인 바람\n'
            print(msg)
            bot.sendMessage(mc,msg)
            prices_prev[i] = prices_now[i]
            prices_high_5[i] = prices_now[i] + prices_now[i] * 0.05
            prices_low_5[i] = prices_now[i] - prices_now[i] * 0.05
        if prices_now[i] >= prices_high_15[i] and save_high:
            save_high = False
            msg = f'!!!!!!!!!!{coin_list[i]} {prices_now[i]}원\n시가 대비 15프로나 올라갔음!!!!!!!!!!\n'
            print(msg)
            bot.sendMessage(mc,msg)
        if prices_now[i] <= prices_low_15[i] and save_low:
            save_low = False
            msg = f'!!!!!!!!!!{coin_list[i]} {prices_now[i]}원\n시가 대비 15프로나 떨어졌음!!!!!!!!!!\n'
            print(msg)
            bot.sendMessage(mc,msg)
    time.sleep(1)
