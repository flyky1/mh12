#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 업종정보 모듈

이 모듈은 키움 OpenAPI를 통해 업종 정보를 조회하는 기능을 제공합니다.
- 업종 기본정보 조회
- 업종 시세정보 조회
- 업종별 종목 조회
- 섹터 지수 조회
- 업종별 투자자 순매수 조회
- 업종 프로그램 매매 정보 조회
"""

import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from .base import APIBase


logger = logging.getLogger(__name__)


class SectorAPI(APIBase):
    """
    업종정보 API 클래스
    
    이 클래스는 업종 정보를 조회하는 메서드를 제공합니다.
    - 업종 현재가 조회
    - 업종 구성 종목 조회
    - 업종별 투자자 순매수 조회
    - 업종 프로그램 매매 조회
    - 섹터 지수 조회
    """
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        """
        SectorAPI 클래스 초기화
        
        Args:
            base_url (str): API 기본 URL
            headers (Dict[str, str]): API 요청 헤더
        """
        super().__init__(base_url, headers)
    
    def get_sector_price(self, market_type: str, sector_code: str) -> Dict[str, Any]:
        """
        업종 현재가 정보 조회 (ka20001)
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥, 2: 코스피200)
            sector_code (str): 업종 코드
                - 001: 종합(KOSPI)
                - 002: 대형주
                - 003: 중형주
                - 004: 소형주
                - 101: 종합(KOSDAQ)
                - 201: KOSPI200
                - 302: KOSTAR
                - 701: KRX100
            
        Returns:
            Dict[str, Any]: 업종 현재가 정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka20001',
        })
        
        params = {
            'mrkt_tp': market_type,
            'inds_cd': sector_code,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_components(self, market_type: str, sector_code: str) -> Dict[str, Any]:
        """
        업종별 종목 정보 조회 (kb10003)
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            sector_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 업종별 종목 목록
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'kb10003',
        })
        
        params = {
            'mrkt_tp': market_type,
            'inds_cd': sector_code,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_basic_info(self, sector_code: str) -> Dict[str, Any]:
        """
        업종 기본정보 조회 (kb10001)
        
        Args:
            sector_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 업종 기본정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'kb10001',
        })
        
        params = {
            'inds_cd': sector_code,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_price_info(self, sector_code: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        업종 시세정보 조회 (kb10002)
        
        Args:
            sector_code (str): 업종 코드
            date (str, optional): 조회 일자 (YYYYMMDD). 기본값은 None으로 오늘
            
        Returns:
            Dict[str, Any]: 업종 시세정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'kb10002',
        })
        
        params = {
            'inds_cd': sector_code,
        }
        
        if date:
            params['base_dt'] = date
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_investor_trend(self, 
                                  market_type: str,
                                  amount_qty_type: str = '0',
                                  base_date: Optional[str] = None,
                                  exchange_type: str = '3') -> Dict[str, Any]:
        """
        업종별 투자자 순매수 정보 조회 (ka10051)
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            amount_qty_type (str): 금액/수량 구분 (0: 금액, 1: 수량)
            base_date (str, optional): 기준일자 (YYYYMMDD). 기본값은 None으로 오늘
            exchange_type (str): 거래소 구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 업종별 투자자 순매수 정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka10051',
        })
        
        params = {
            'mrkt_tp': market_type,
            'amt_qty_tp': amount_qty_type,
            'stex_tp': exchange_type,
        }
        
        if base_date:
            params['base_dt'] = base_date
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_program_trading(self, stock_code: str) -> Dict[str, Any]:
        """
        업종 프로그램 매매 정보 조회 (ka10010)
        
        Args:
            stock_code (str): 종목 코드
            
        Returns:
            Dict[str, Any]: 업종 프로그램 매매 정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka10010',
        })
        
        params = {
            'stk_cd': stock_code,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_sector_index(self, market_type: str) -> Dict[str, Any]:
        """
        섹터 지수 정보 조회 (kb10004)
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            
        Returns:
            Dict[str, Any]: 섹터 지수 정보
        """
        endpoint = "/api/dostk/sect"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'kb10004',
        })
        
        params = {
            'mrkt_tp': market_type,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def _get_headers(self) -> Dict[str, str]:
        """
        API 요청용 헤더 생성
        
        Returns:
            Dict[str, str]: API 요청 헤더
        """
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self._get_access_token()}',
            'cont-yn': 'N',
            'next-key': '',
        }
        return headers
        
    def _get_access_token(self) -> str:
        """
        액세스 토큰 가져오기
        
        Returns:
            str: 액세스 토큰
        """
        # 실제 구현에서는 토큰 관리 로직 추가
        # 예시 목적으로 임시 문자열 반환
        return "ACCESS_TOKEN" 