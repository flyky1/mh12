#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 테마 정보 모듈

이 모듈은 키움 OpenAPI를 통해 테마 정보를 조회하는 기능을 제공합니다.
- 테마 목록 조회
- 테마별 구성 종목 조회
- 종목별 테마 조회
"""

import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from .base import APIBase


logger = logging.getLogger(__name__)


class ThemeAPI(APIBase):
    """
    테마 정보 API 클래스
    
    이 클래스는 테마 정보를 조회하는 메서드를 제공합니다.
    - 테마 목록 조회
    - 테마별 구성 종목 조회
    - 종목별 테마 조회
    """
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        """
        ThemeAPI 클래스 초기화
        
        Args:
            base_url (str): API 기본 URL
            headers (Dict[str, str]): API 요청 헤더
        """
        super().__init__(base_url, headers)
    
    def get_theme_list(self, 
                      query_type: str = '0', 
                      date_type: str = '10', 
                      theme_name: Optional[str] = None,
                      flu_pl_amt_type: str = '1',
                      exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마 목록 조회 (ka90001)
        
        Args:
            query_type (str): 검색구분 (0: 전체검색, 1: 테마검색, 2: 종목검색)
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            theme_name (str, optional): 테마명 검색어
            flu_pl_amt_type (str): 등락수익구분 (1: 상위기간수익률, 2: 하위기간수익률, 3: 상위등락률, 4: 하위등락률)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 테마 목록 정보
        """
        endpoint = "/api/dostk/thme"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka90001',
        })
        
        params = {
            'qry_tp': query_type,
            'date_tp': date_type,
            'flu_pl_amt_tp': flu_pl_amt_type,
            'stex_tp': exchange_type,
        }
        
        if theme_name:
            params['thema_nm'] = theme_name
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_theme_stocks(self, 
                        theme_group_code: str, 
                        date_type: str = '2', 
                        exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마별 구성 종목 조회 (ka90002)
        
        Args:
            theme_group_code (str): 테마그룹코드
            date_type (str): 날짜구분 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 테마별 구성 종목 목록
        """
        endpoint = "/api/dostk/thme"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka90002',
        })
        
        params = {
            'thema_grp_cd': theme_group_code,
            'date_tp': date_type,
            'stex_tp': exchange_type,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def get_stock_themes(self, 
                        stock_code: str, 
                        date_type: str = '10', 
                        exchange_type: str = '3') -> Dict[str, Any]:
        """
        종목별 테마 조회 (ka90001 - 종목검색)
        
        Args:
            stock_code (str): 종목코드
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 종목이 속한 테마 목록
        """
        endpoint = "/api/dostk/thme"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka90001',
        })
        
        params = {
            'qry_tp': '2',  # 종목검색
            'stk_cd': stock_code,
            'date_tp': date_type,
            'flu_pl_amt_tp': '1',  # 상위기간수익률
            'stex_tp': exchange_type,
        }
        
        return self.request_post(endpoint, headers=headers, json=params)
    
    def search_themes(self, 
                     theme_name: str, 
                     date_type: str = '10', 
                     exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마 이름으로 검색 (ka90001 - 테마검색)
        
        Args:
            theme_name (str): 테마명 검색어
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 검색된 테마 목록
        """
        endpoint = "/api/dostk/thme"
        
        headers = self._get_headers()
        headers.update({
            'api-id': 'ka90001',
        })
        
        params = {
            'qry_tp': '1',  # 테마검색
            'thema_nm': theme_name,
            'date_tp': date_type,
            'flu_pl_amt_tp': '1',  # 상위기간수익률
            'stex_tp': exchange_type,
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