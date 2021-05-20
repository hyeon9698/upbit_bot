import pandas as pd
import time
import numpy as np
import pyupbit
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import telegram # pip install python-telegram-bot
import json
from dotenv import load_dotenv # pip install python-dotenv
import os

load_dotenv()
access = os.getenv('UPBIT_API_ACCESS_KEY')
secret = os.getenv('UPBIT_API_SECRET_KEY')
upbit = pyupbit.Upbit(access, secret)

coin_list = ["KRW-BTC", "KRW-ETH", "KRW-DOGE"]

days = 14
k_range = [0.4,0.5,0.6]
ma_range = [0,5,10,15]
total_list = []
values = []
dfs = []
not_1 = []
not_1_cnt = 0
not_1_total = 0
stay_total_list = []
for coin in coin_list:
    time.sleep(0.5)
    dfs.append(pyupbit.get_ohlcv(coin, count=days))#, to="20201019"))
print(days, "days")
for k in k_range:
    for ma in ma_range:
        total = 0
        stay_total = 0
        for idx, coin in enumerate(coin_list):
            # print(coin)
            # time.sleep(0.1)
            df = dfs[idx] # pyupbit.get_ohlcv(coin, count=days)
            time.sleep(0.01)
            df2 = pyupbit.get_ohlcv(coin, count=days+ma+1)#, to="20201019")
            # print(coin)
            time.sleep(0.01)
            df2['range1'] = (df2['high'] - df2['low']) * k
            df['target1'] = df2['open'] + df2['range1'].shift(1)
            # df['ror1'] = np.where(df['high'] >= df['target1'],
            #         df['close']*0.997 / df['target1'] ,
            #         1)
            # df2 = pyupbit.get_ohlcv(coin, count=days+ma)
            time.sleep(0.05)
            close = df2['close']
            df_ma = close.rolling(window=ma).mean()
            df['ma15'] = df_ma.shift(1)
            df['ma15ortarget'] = np.where(df['target1'] >= df['ma15'], df['target1'], df['ma15'])
            df['ror1'] = np.where(df['high'] >= df['ma15ortarget'],
                (df['close'])*0.995/df['ma15ortarget'],
                1
            )
            if ma == 0:
                df['ma15'] = 0
                df['ma15ortarget'] = np.where(df['target1'] >= df['ma15'], df['target1'], df['ma15'])
                df['ror1'] = np.where(df['high'] >= df['ma15ortarget'],
                    (df['close'])*0.995/df['ma15ortarget'],
                    1
                )
        


            df['hpr1'] = df['ror1'].cumprod()
            hpr1 = df['hpr1'][-1]
            total += hpr1
            df['hpr2'] = df['close'][-1]*0.995/df['open'][0]
            hpr2 = df['hpr2'][-1]
            stay_total += hpr2
            # if hpr1 != 1:
            #     # print(f'{"%5s"%coin} ---- {hpr1} -> {hpr1*100 - 100}')
            #     not_1.append((hpr1, coin))
            #     not_1_cnt += 1
            #     not_1_total += hpr1
        total_list.append((total/len(coin_list),k,ma,stay_total/len(coin_list)))
s = sorted(total_list, key = lambda x: (x[0]))
# for i in sorted(not_1, key = lambda x: x[0]):
#     print(f'{"%9s"%i[1]} -> {"%2.3f"%(i[0]*100-100)}%')
for i in s:
    print(f'{"%  3.2f"%(i[0]*100-100)}% |||    k  {"%2.2f"%i[1]}    |||    ma  {"%2d"%i[2]}    |||    존버  {"%2.2f"%(i[3]*100-100)}%')
# print(f'"예상 평균 손익 %는 "{not_1_total/not_1_cnt*100-100}%')
# df.to_csv('testing2.csv')
