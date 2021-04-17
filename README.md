# upbit_bot 가상화폐 변동성 돌파 전략 프로그램 (업비트용)
## 가상화폐 매매 자동화 프로그램
- [참고 책](https://wikidocs.net/book/1665)
- 비트코인 + 알트코인을 자동으로 매매해 주는 봇 + 실시간 진행 상황을 Telegram으로 문자 전송 + 데이터를 쌓아서 실제로 얼마를 벌었는지 비교
### 실행방법
- [virtualenv 코드 참고 사이트](https://dgkim5360.tistory.com/entry/python-virtualenv-on-linux-ubuntu-and-windows)
- 24시간 코드 돌리는 것은 pythonanywhere 사이트를 이용했음
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
### 코인을 추가할 때
- own_coin_list_04_08 정보 갱신
- coin_list 정보 갱신
- percent_list 정보 갱신
- reset_dataset.csv 파일 정보 갱신
- dataset.csv 파일 정보 갱신
- pythonanywhere 에서 main.py, dataset.csv, reset_dataset.csv 업데이트
