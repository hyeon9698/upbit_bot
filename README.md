# upbit_bot
## 비트코인 매매 자동화 프로그램
- [참고 책](https://wikidocs.net/book/1665)
- [virtualenv 코드 관련 사이트](https://dgkim5360.tistory.com/entry/python-virtualenv-on-linux-ubuntu-and-windows)
- pythonanywhere 사이트를 이용했음
- 순서대로 코드 작성하기
- git clone https://github.com/hyeon9698/upbit_bot
- cd upbit_bot
- pip3 install virtualenv
- virtualenv upbit --python=python3.8
- source upbit/bin/activate
- pip install -r requirements.txt
- python main.py
## 코인을 추가할 때
- own_coin_list_04_08 정보 갱신
- coin_list 정보 갱신
- percent_list 정보 갱신
- reset_dataset.csv 파일 정보 갱신
- dataset.csv 파일 정보 갱신
- pythonanywhere 에서 main.py, dataset.csv, reset_dataset.csv 업데이트
