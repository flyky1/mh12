#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 신용주문 모듈 사용 예제
"""

import os
import sys
import json
from pprint import pprint

# 상위 디렉토리 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom import KiwoomOpenAPI

def main():
    """신용주문 모듈 사용 예제"""
    # API 키 설정
    app_key = os.environ.get('kiwoom_appkey')
    app_secret = os.environ.get('kiwoom_secretkey')

    if not app_key or not app_secret:
        print("환경 변수에 API 키가 설정되어 있지 않습니다.")
        print("환경 변수를 설정하거나 직접 키를 입력해주세요.")
        return

    # Kiwoom Open API 객체 생성
    api = KiwoomOpenAPI(app_key, app_secret)

    # 로그인
    auth_result = api.auth_login()
    print("로그인 결과:")
    pprint(auth_result)

    # 신용매수주문 예제
    print("\n신용매수주문 예제:")
    try:
        # 실제 실행 시에는 아래 값들을 적절히 수정해주세요
        exchange_type = "KRX"  # 국내거래소구분 (KRX, NXT, SOR)
        stock_code = "005930"  # 삼성전자 종목코드
        order_quantity = "1"   # 주문수량
        order_price = "70000"  # 주문단가 (시장가일 경우 '0')
        
        # 실제 주문을 원하는 경우 주석 해제
        # result = api.credit_buy_order(exchange_type, stock_code, order_quantity, order_price)
        # pprint(result)
        
        print("# 주의: 실제 주문은 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용매수주문 예외 발생: {e}")
    
    # 신용매도주문 예제
    print("\n신용매도주문 예제:")
    try:
        # 실제 실행 시에는 아래 값들을 적절히 수정해주세요
        exchange_type = "KRX"       # 국내거래소구분 (KRX, NXT, SOR)
        stock_code = "005930"       # 삼성전자 종목코드
        order_quantity = "1"        # 주문수량
        order_price = "70000"       # 주문단가 (시장가일 경우 '0')
        credit_deal_type = "33"     # 신용거래구분 (33: 융자, 99: 융자합)
        credit_loan_date = "20231220"  # 대출일자 (YYYYMMDD, 융자일 경우 필수)
        
        # 실제 주문을 원하는 경우 주석 해제
        # result = api.credit_sell_order(exchange_type, stock_code, order_quantity, 
        #                              order_price, credit_deal_type, "0", credit_loan_date)
        # pprint(result)
        
        print("# 주의: 실제 주문은 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용매도주문 예외 발생: {e}")
    
    # 신용주문정정 예제
    print("\n신용주문정정 예제:")
    try:
        # 실제 실행 시에는 아래 값들을 적절히 수정해주세요
        exchange_type = "KRX"       # 국내거래소구분 (KRX, NXT, SOR)
        original_order_no = "00000000"  # 원주문번호 (실제 주문 번호로 변경 필요)
        stock_code = "005930"       # 삼성전자 종목코드
        modify_quantity = "1"       # 정정수량
        modify_price = "71000"      # 정정단가
        
        # 실제 주문을 원하는 경우 주석 해제
        # result = api.credit_modify_order(exchange_type, original_order_no, 
        #                               stock_code, modify_quantity, modify_price)
        # pprint(result)
        
        print("# 주의: 실제 주문은 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용주문정정 예외 발생: {e}")
    
    # 신용주문취소 예제
    print("\n신용주문취소 예제:")
    try:
        # 실제 실행 시에는 아래 값들을 적절히 수정해주세요
        exchange_type = "KRX"       # 국내거래소구분 (KRX, NXT, SOR)
        original_order_no = "00000000"  # 원주문번호 (실제 주문 번호로 변경 필요)
        stock_code = "005930"       # 삼성전자 종목코드
        cancel_quantity = "1"       # 취소수량 ('0' 입력시 잔량 전부 취소)
        
        # 실제 주문을 원하는 경우 주석 해제
        # result = api.credit_cancel_order(exchange_type, original_order_no, 
        #                               stock_code, cancel_quantity)
        # pprint(result)
        
        print("# 주의: 실제 주문은 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용주문취소 예외 발생: {e}")
    
    # 신용융자잔고조회 예제
    print("\n신용융자잔고조회 예제:")
    try:
        # 실제 조회를 원하는 경우 주석 해제
        # result = api.get_credit_loan_balance()
        # pprint(result)
        
        print("# 주의: 실제 조회는 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용융자잔고조회 예외 발생: {e}")
    
    # 신용대출상환 예제
    print("\n신용대출상환 예제:")
    try:
        # 실제 상환을 원하는 경우 주석 해제
        # result = api.credit_loan_repayment()
        # pprint(result)
        
        print("# 주의: 실제 상환은 코드 수정 후 실행해주세요.")
    except Exception as e:
        print(f"신용대출상환 예외 발생: {e}")

if __name__ == "__main__":
    main() 