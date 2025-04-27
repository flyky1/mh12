#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 기관/외국인 모듈

이 모듈은 키움 OpenAPI의 기관 및 외국인 투자자 관련 API 기능을 제공합니다.
- 외국인 보유량 정보 조회
- 외국인 순매수 정보 조회
- 기관 순매수 정보 조회
- 외국인 기관 순매수 동향 조회
"""

import logging
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

from .base import BaseAPI

logger = logging.getLogger(__name__)


class ForeignerAPI(BaseAPI):
    """
    기관/외국인 API 클래스
    
    기관 투자자 및 외국인 투자자 관련 정보를 조회하는 API를 제공합니다.
    """
    
    def get_foreigner_holdings(self, stock_code: str, start_date: Optional[str] = None, 
                              end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        외국인 보유량 정보를 조회합니다.
        
        Args:
            stock_code: 종목코드
            start_date: 조회 시작일자 (YYYYMMDD 형식, 기본값: 1개월 전)
            end_date: 조회 종료일자 (YYYYMMDD 형식, 기본값: 오늘)
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 외국인 보유량 데이터
            }
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
                
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20001',
                'tr-id': 'FHKST03010100',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',  # 주식 시장 구분 코드 (J: 전체)
                'FID_INPUT_ISCD': stock_code,    # 종목코드
                'FID_INPUT_DATE_1': start_date,  # 조회 시작일자
                'FID_INPUT_DATE_2': end_date,    # 조회 종료일자
                'FID_PERIOD_DIV_CODE': 'D'       # 기간 분류 코드 (D: 일별)
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/foreign-investor-time-tick-of-item', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"외국인 보유량 정보 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'외국인 보유량 정보 조회 중 오류 발생: {str(e)}',
                'data': None
            }
    
    def get_foreigner_net_purchase(self, stock_code: str, start_date: Optional[str] = None, 
                                 end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        외국인 순매수 정보를 조회합니다.
        
        Args:
            stock_code: 종목코드
            start_date: 조회 시작일자 (YYYYMMDD 형식, 기본값: 1개월 전)
            end_date: 조회 종료일자 (YYYYMMDD 형식, 기본값: 오늘)
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 외국인 순매수 데이터
            }
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
                
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20002',
                'tr-id': 'FHKST03010200',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',  # 주식 시장 구분 코드 (J: 전체)
                'FID_INPUT_ISCD': stock_code,    # 종목코드
                'FID_INPUT_DATE_1': start_date,  # 조회 시작일자
                'FID_INPUT_DATE_2': end_date,    # 조회 종료일자
                'FID_PERIOD_DIV_CODE': 'D'       # 기간 분류 코드 (D: 일별)
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/foreign-investor-net-purchase-of-item', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"외국인 순매수 정보 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'외국인 순매수 정보 조회 중 오류 발생: {str(e)}',
                'data': None
            }
    
    def get_institutional_net_purchase(self, stock_code: str, start_date: Optional[str] = None, 
                                    end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        기관 순매수 정보를 조회합니다.
        
        Args:
            stock_code: 종목코드
            start_date: 조회 시작일자 (YYYYMMDD 형식, 기본값: 1개월 전)
            end_date: 조회 종료일자 (YYYYMMDD 형식, 기본값: 오늘)
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 기관 순매수 데이터
            }
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
                
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20003',
                'tr-id': 'FHKST03010300',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',  # 주식 시장 구분 코드 (J: 전체)
                'FID_INPUT_ISCD': stock_code,    # 종목코드
                'FID_INPUT_DATE_1': start_date,  # 조회 시작일자
                'FID_INPUT_DATE_2': end_date,    # 조회 종료일자
                'FID_PERIOD_DIV_CODE': 'D'       # 기간 분류 코드 (D: 일별)
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/institutional-investor-net-purchase-of-item', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"기관 순매수 정보 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'기관 순매수 정보 조회 중 오류 발생: {str(e)}',
                'data': None
            }
    
    def get_investor_trend(self, market_code: str = '0', start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        투자자별 매매동향을 조회합니다.
        
        Args:
            market_code: 시장코드 (0: 전체, 1: 코스피, 2: 코스닥)
            start_date: 조회 시작일자 (YYYYMMDD 형식, 기본값: 1개월 전)
            end_date: 조회 종료일자 (YYYYMMDD 형식, 기본값: 오늘)
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 투자자별 매매동향 데이터
            }
        """
        try:
            if start_date is None:
                start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            if end_date is None:
                end_date = datetime.now().strftime('%Y%m%d')
                
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20004', 
                'tr-id': 'FHKST03010400',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': market_code,  # 시장코드
                'FID_INPUT_DATE_1': start_date,         # 조회 시작일자
                'FID_INPUT_DATE_2': end_date,           # 조회 종료일자
                'FID_PERIOD_DIV_CODE': 'D'              # 기간 분류 코드 (D: 일별)
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/investor-trend', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"투자자별 매매동향 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'투자자별 매매동향 조회 중 오류 발생: {str(e)}',
                'data': None
            }
    
    def get_foreign_institution_day_trading(self, stock_code: str) -> Dict[str, Any]:
        """
        종목별 외국인/기관 매매 현황을 조회합니다.
        
        Args:
            stock_code: 종목코드
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 외국인/기관 매매 현황 데이터
            }
        """
        try:
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20005',
                'tr-id': 'FHKST03010500',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',  # 주식 시장 구분 코드 (J: 전체)
                'FID_INPUT_ISCD': stock_code     # 종목코드
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/foreign-institution-day-trading', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"종목별 외국인/기관 매매 현황 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'종목별 외국인/기관 매매 현황 조회 중 오류 발생: {str(e)}',
                'data': None
            }
    
    def get_foreign_ownership_limit(self, stock_code: str) -> Dict[str, Any]:
        """
        외국인 보유제한 정보를 조회합니다.
        
        Args:
            stock_code: 종목코드
            
        Returns:
            응답 객체: {
                'status': 응답 상태 코드,
                'message': 응답 메시지,
                'data': 외국인 보유제한 데이터
            }
        """
        try:
            headers = {
                'authorization': self.get_access_token(),
                'content-type': 'application/json; charset=utf-8',
                'api-id': 'ka20006',
                'tr-id': 'FHKST03010600',
                'appkey': self.api_key,
                'appsecret': self.api_secret
            }
            
            params = {
                'FID_COND_MRKT_DIV_CODE': 'J',  # 주식 시장 구분 코드 (J: 전체)
                'FID_INPUT_ISCD': stock_code     # 종목코드
            }
            
            res = requests.post(self.base_url + '/uapi/domestic-stock/v1/trading/foreign-ownership-limit', 
                              headers=headers, json=params)
            return res.json()
        
        except Exception as e:
            logger.error(f"외국인 보유제한 정보 조회 중 오류 발생: {str(e)}")
            return {
                'status': '400',
                'message': f'외국인 보유제한 정보 조회 중 오류 발생: {str(e)}',
                'data': None
            } 