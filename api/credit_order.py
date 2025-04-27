#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 신용주문 모듈

이 모듈은 키움 OpenAPI의 신용주문 관련 API 기능을 제공합니다.
- 신용매수주문
- 신용매도주문
- 신용주문정정
- 신용주문취소
- 신용융자잔고조회
- 신용대출상환
"""

import logging
import json
from typing import Dict, Any, Optional
import os

from .base import BaseAPI

logger = logging.getLogger(__name__)


class CreditOrderAPI(BaseAPI):
    """
    신용주문 API 클래스
    
    신용주문 관련 기능을 제공하는 API 클래스입니다.
    """
    
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, access_token: Optional[str] = None):
        """
        신용주문 API 초기화
        
        Args:
            api_key (str, optional): API 키
            secret_key (str, optional): 시크릿 키
            access_token (str, optional): 액세스 토큰
        """
        super().__init__(api_key, secret_key, access_token)
        self.endpoint = '/api/dostk/crdordr'
    
    def _get_headers(self, api_id, cont_yn='N', next_key=''):
        """
        HTTP 요청에 필요한 헤더를 생성합니다.
        
        Args:
            api_id (str): API ID
            cont_yn (str, optional): 연속조회여부. Defaults to 'N'.
            next_key (str, optional): 연속조회키. Defaults to ''.
            
        Returns:
            dict: 요청 헤더
        """
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.get_access_token()}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': api_id,
        }
        return headers
    
    def place_credit_buy_order(self, exchange_type, stock_code, order_quantity, 
                               order_price="", trade_type="0", credit_deal_type="99", 
                               credit_loan_date="", condition_price=""):
        """
        신용 매수 주문을 실행합니다.
        
        Args:
            exchange_type (str): 국내거래소구분 (KRX, NXT, SOR)
            stock_code (str): 종목코드
            order_quantity (str): 주문수량
            order_price (str, optional): 주문단가. Defaults to "".
            trade_type (str, optional): 매매구분. Defaults to "0".
                0: 보통, 3: 시장가, 5: 조건부지정가, 81: 장마감후시간외,
                61: 장시작전시간외, 62: 시간외단일가, 6: 최유리지정가,
                7: 최우선지정가, 10: 보통(IOC), 13: 시장가(IOC),
                16: 최유리(IOC), 20: 보통(FOK), 23: 시장가(FOK), 26: 최유리(FOK)
            credit_deal_type (str, optional): 신용거래구분. Defaults to "99".
                33: 융자, 99: 융자합
            credit_loan_date (str, optional): 대출일 (YYYYMMDD) - 융자일 경우 필수. Defaults to "".
            condition_price (str, optional): 조건단가. Defaults to "".
            
        Returns:
            dict: 주문 결과 응답
        """
        api_id = "kt10006"
        endpoint = "/api/dostk/crdordr"
        
        params = {
            'dmst_stex_tp': exchange_type,
            'stk_cd': stock_code,
            'ord_qty': order_quantity,
            'ord_uv': order_price,
            'trde_tp': trade_type,
            'crd_deal_tp': credit_deal_type,
            'crd_loan_dt': credit_loan_date,
            'cond_uv': condition_price,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용 매수 주문 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def place_credit_sell_order(self, exchange_type, stock_code, order_quantity, 
                               order_price="", trade_type="0", credit_deal_type="99", 
                               credit_loan_date="", condition_price=""):
        """
        신용 매도 주문을 실행합니다.
        
        Args:
            exchange_type (str): 국내거래소구분 (KRX, NXT, SOR)
            stock_code (str): 종목코드
            order_quantity (str): 주문수량
            order_price (str, optional): 주문단가. Defaults to "".
            trade_type (str, optional): 매매구분. Defaults to "0".
                0: 보통, 3: 시장가, 5: 조건부지정가, 81: 장마감후시간외,
                61: 장시작전시간외, 62: 시간외단일가, 6: 최유리지정가,
                7: 최우선지정가, 10: 보통(IOC), 13: 시장가(IOC),
                16: 최유리(IOC), 20: 보통(FOK), 23: 시장가(FOK), 26: 최유리(FOK)
            credit_deal_type (str, optional): 신용거래구분. Defaults to "99".
                33: 융자, 99: 융자합
            credit_loan_date (str, optional): 대출일 (YYYYMMDD) - 융자일 경우 필수. Defaults to "".
            condition_price (str, optional): 조건단가. Defaults to "".
            
        Returns:
            dict: 주문 결과 응답
        """
        api_id = "kt10007"
        endpoint = "/api/dostk/crdordr"
        
        params = {
            'dmst_stex_tp': exchange_type,
            'stk_cd': stock_code,
            'ord_qty': order_quantity,
            'ord_uv': order_price,
            'trde_tp': trade_type,
            'crd_deal_tp': credit_deal_type,
            'crd_loan_dt': credit_loan_date,
            'cond_uv': condition_price,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용 매도 주문 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def modify_credit_order(self, exchange_type, original_order_number, stock_code, 
                          modify_quantity, modify_price, modify_condition_price=""):
        """
        신용 주문을 정정합니다.
        
        Args:
            exchange_type (str): 국내거래소구분 (KRX, NXT, SOR)
            original_order_number (str): 원주문번호
            stock_code (str): 종목코드
            modify_quantity (str): 정정수량
            modify_price (str): 정정단가
            modify_condition_price (str, optional): 정정조건단가. Defaults to "".
            
        Returns:
            dict: 주문 정정 결과 응답
        """
        api_id = "kt10008"
        endpoint = "/api/dostk/crdordr"
        
        params = {
            'dmst_stex_tp': exchange_type,
            'orig_ord_no': original_order_number,
            'stk_cd': stock_code,
            'mdfy_qty': modify_quantity,
            'mdfy_uv': modify_price,
            'mdfy_cond_uv': modify_condition_price,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용 주문 정정 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def cancel_credit_order(self, exchange_type, original_order_number, stock_code, cancel_quantity):
        """
        신용 주문을 취소합니다.
        
        Args:
            exchange_type (str): 국내거래소구분 (KRX, NXT, SOR)
            original_order_number (str): 원주문번호
            stock_code (str): 종목코드
            cancel_quantity (str): 취소수량 ('0' 입력시 잔량 전부 취소)
            
        Returns:
            dict: 주문 취소 결과 응답
        """
        api_id = "kt10009"
        endpoint = "/api/dostk/crdordr"
        
        params = {
            'dmst_stex_tp': exchange_type,
            'orig_ord_no': original_order_number,
            'stk_cd': stock_code,
            'cncl_qty': cancel_quantity,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용 주문 취소 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_credit_balance(self, account_number, exchange_type="KRX", credit_type="33"):
        """
        신용융자잔고를 조회합니다.
        
        Args:
            account_number (str): 계좌번호
            exchange_type (str, optional): 국내거래소구분 (KRX, NXT, SOR). Defaults to "KRX".
            credit_type (str, optional): 신용거래구분 (33: 융자, 99: 융자합). Defaults to "33".
            
        Returns:
            dict: 신용융자잔고 정보
        """
        api_id = "kr10005"
        endpoint = "/api/dostk/crdbal"
        
        params = {
            'cano': account_number,
            'dmst_stex_tp': exchange_type,
            'crd_deal_tp': credit_type,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용융자잔고 조회 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def repay_credit_loan(self, account_number, exchange_type, stock_code, 
                         repay_quantity, repay_type="00", loan_date=""):
        """
        신용대출을 상환합니다.
        
        Args:
            account_number (str): 계좌번호
            exchange_type (str): 국내거래소구분 (KRX, NXT, SOR)
            stock_code (str): 종목코드
            repay_quantity (str): 상환수량
            repay_type (str, optional): 상환구분 (00: 상환출고, 01: 상환매수). Defaults to "00".
            loan_date (str, optional): 대출일자 (YYYYMMDD). Defaults to "".
            
        Returns:
            dict: 상환 결과 응답
        """
        api_id = "kr10006"
        endpoint = "/api/dostk/crdrepaymnt"
        
        params = {
            'cano': account_number,
            'dmst_stex_tp': exchange_type,
            'stk_cd': stock_code,
            'qty': repay_quantity,
            'repaymnt_tp': repay_type,
            'loan_dt': loan_date,
        }
        
        try:
            response = self.request_post(endpoint, params, api_id=api_id)
            return response
        except Exception as e:
            logger.error(f"신용대출 상환 요청 실패: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def request_post(self, url, data, headers):
        """
        POST 요청 처리
        
        Args:
            url (str): 요청 URL
            data (dict): 요청 데이터
            headers (dict): 요청 헤더
            
        Returns:
            dict: 응답 데이터
        """
        return super().request_post(url, data) 