#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 API 기본 사용 예제
"""

import os
import json
from kiwoom_api import KiwoomClient

# 환경변수에서 API 키 가져오기
# 실제 사용 시에는 환경변수 설정 필요: export kiwoom_appkey=개인키
# export kiwoom_secretkey=시크릿키
appkey = os.environ.get('kiwoom_appkey')
secretkey = os.environ.get('kiwoom_secretkey')

def main():
    # 모의투자 환경으로 클라이언트 초기화
    client = KiwoomClient(appkey, secretkey, is_mock=True)
    
    # 현재가 조회
    stock_code = '005930'  # 삼성전자
    response = client.price.get_current_price(stock_code)
    print_response('현재가 조회', response)
    
    # 계좌잔고 조회
    response = client.account.get_account_balance()
    print_response('계좌잔고 조회', response)
    
    # 주문 예제 (실행 전 주석 해제 필요)
    # 시장가 매수 주문
    # response = client.order.buy_order(
    #     stk_cd='005930',  # 삼성전자
    #     ord_qty='1',      # 1주
    #     trde_tp='3'       # 시장가
    # )
    # print_response('시장가 매수 주문', response)

def print_response(title, response):
    """응답 데이터 출력 헬퍼 함수"""
    print('-' * 50)
    print(f'[{title}]')
    print('-' * 50)
    print(f'Status Code: {response["status_code"]}')
    
    # 헤더 정보 출력
    print('\n[Headers]')
    for key, value in response['headers'].items():
        if value:
            print(f'{key}: {value}')
    
    # 데이터 출력 (예쁘게 출력)
    print('\n[Response Data]')
    print(json.dumps(response['data'], indent=2, ensure_ascii=False))
    print('-' * 50)
    print()

if __name__ == '__main__':
    main() 