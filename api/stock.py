#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 종목정보 모듈

이 모듈은 키움 OpenAPI를 통해 국내 및 해외 주식 종목 정보를 조회하는 기능을 제공합니다.
- 종목 기본정보 조회
- 거래정지종목 조회
- 관리종목 조회
- 종목별 공시정보 조회
- 종목코드/명 검색
"""

import logging
from typing import Dict, Any, Optional, List
from urllib.parse import urljoin

from .base import APIBase


logger = logging.getLogger(__name__)


class StockAPI(APIBase):
    """
    종목정보 API 클래스
    
    이 클래스는 국내 및 해외 주식의 종목 정보를 조회하는 메서드를 제공합니다.
    """
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        """
        StockAPI 클래스 초기화
        
        Args:
            base_url (str): API 기본 URL
            headers (Dict[str, str]): API 요청 헤더
        """
        super().__init__(base_url, headers)
    
    def get_domestic_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        국내 주식 종목 기본정보 조회 (ke10001)
        
        Args:
            stock_code (str): 종목 코드 (예: '005930' for 삼성전자)
            
        Returns:
            Dict[str, Any]: 종목 기본정보
        """
        endpoint = "stock/basic-info"
        params = {
            "stock_code": stock_code
        }
        
        return self.request_get(endpoint, params)
    
    def get_overseas_stock_info(self, stock_code: str, exchange: str) -> Dict[str, Any]:
        """
        해외 주식 종목 기본정보 조회 (ke20001)
        
        Args:
            stock_code (str): 종목 코드 (예: 'AAPL' for 애플)
            exchange (str): 거래소 코드 (예: 'NAS', 'NYSE')
            
        Returns:
            Dict[str, Any]: 종목 기본정보
        """
        endpoint = "overseas/stock/basic-info"
        params = {
            "stock_code": stock_code,
            "exchange": exchange
        }
        
        return self.request_get(endpoint, params)
    
    def get_suspended_stocks(self, market_code: Optional[str] = None) -> Dict[str, Any]:
        """
        거래정지종목 조회 (ke10002)
        
        Args:
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            
        Returns:
            Dict[str, Any]: 거래정지종목 목록
        """
        endpoint = "stock/suspended"
        params = {}
        
        if market_code:
            params["market_code"] = market_code
        
        return self.request_get(endpoint, params)
    
    def get_managed_stocks(self, market_code: Optional[str] = None) -> Dict[str, Any]:
        """
        관리종목 조회 (ke10003)
        
        Args:
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            
        Returns:
            Dict[str, Any]: 관리종목 목록
        """
        endpoint = "stock/managed"
        params = {}
        
        if market_code:
            params["market_code"] = market_code
        
        return self.request_get(endpoint, params)
    
    def get_stock_disclosure(self, 
                           stock_code: Optional[str] = None, 
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None, 
                           disclosure_type: Optional[str] = None) -> Dict[str, Any]:
        """
        종목별 공시정보 조회 (ke10004)
        
        Args:
            stock_code (str, optional): 종목 코드. 기본값은 None으로 모든 종목 조회
            start_date (str, optional): 조회 시작일 (YYYYMMDD). 기본값은 None으로 최근 1주일
            end_date (str, optional): 조회 종료일 (YYYYMMDD). 기본값은 None으로 오늘
            disclosure_type (str, optional): 공시 유형 코드. 기본값은 None으로 모든 유형
            
        Returns:
            Dict[str, Any]: 공시정보 목록
        """
        endpoint = "stock/disclosure"
        params = {}
        
        if stock_code:
            params["stock_code"] = stock_code
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        if disclosure_type:
            params["disclosure_type"] = disclosure_type
        
        return self.request_get(endpoint, params)
    
    def search_stock(self, 
                    query: str, 
                    market_code: Optional[str] = None, 
                    is_etf: Optional[bool] = None, 
                    is_elw: Optional[bool] = None) -> Dict[str, Any]:
        """
        종목코드/명 검색 (ke10005)
        
        Args:
            query (str): 검색어 (종목명 또는 종목코드의 일부)
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            is_etf (bool, optional): ETF 종목만 검색 여부. 기본값은 None으로 모든 종목 조회
            is_elw (bool, optional): ELW 종목만 검색 여부. 기본값은 None으로 모든 종목 조회
            
        Returns:
            Dict[str, Any]: 검색 결과 종목 목록
        """
        endpoint = "stock/search"
        params = {
            "query": query
        }
        
        if market_code:
            params["market_code"] = market_code
        if is_etf is not None:
            params["is_etf"] = "Y" if is_etf else "N"
        if is_elw is not None:
            params["is_elw"] = "Y" if is_elw else "N"
        
        return self.request_get(endpoint, params)
    
    def search_overseas_stock(self, 
                            query: str, 
                            exchange: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 종목코드/명 검색 (ke20002)
        
        Args:
            query (str): 검색어 (종목명 또는 종목코드의 일부)
            exchange (str, optional): 거래소 코드 (예: 'NAS', 'NYSE'). 기본값은 None으로 모든 거래소 조회
            
        Returns:
            Dict[str, Any]: 검색 결과 종목 목록
        """
        endpoint = "overseas/stock/search"
        params = {
            "query": query
        }
        
        if exchange:
            params["exchange"] = exchange
        
        return self.request_get(endpoint, params)
    
    def get_stock_financial_info(self, 
                               stock_code: str, 
                               info_type: Optional[str] = None) -> Dict[str, Any]:
        """
        종목 재무정보 조회 (ke10006)
        
        Args:
            stock_code (str): 종목 코드
            info_type (str, optional): 재무정보 유형 (예: 'QUARTER', 'ANNUAL'). 기본값은 None으로 모든 유형 조회
            
        Returns:
            Dict[str, Any]: 종목 재무정보
        """
        endpoint = "stock/financial"
        params = {
            "stock_code": stock_code
        }
        
        if info_type:
            params["info_type"] = info_type
        
        return self.request_get(endpoint, params)
    
    def get_stock_investor_trend(self, 
                               stock_code: str, 
                               start_date: str, 
                               end_date: str) -> Dict[str, Any]:
        """
        종목별 투자자 동향 조회 (ke10007)
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 투자자별 매매동향 정보
        """
        endpoint = "stock/investor-trend"
        params = {
            "stock_code": stock_code,
            "start_date": start_date,
            "end_date": end_date
        }
        
        return self.request_get(endpoint, params)
    
    def get_market_stock_list(self, market_code: str) -> Dict[str, Any]:
        """
        시장별 종목 목록 조회 (ke10008)
        
        Args:
            market_code (str): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ')
            
        Returns:
            Dict[str, Any]: 종목 목록
        """
        endpoint = "stock/market-list"
        params = {
            "market_code": market_code
        }
        
        return self.request_get(endpoint, params)
    
    def get_industry_stock_list(self, industry_code: str) -> Dict[str, Any]:
        """
        업종별 종목 목록 조회 (ke10009)
        
        Args:
            industry_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 종목 목록
        """
        endpoint = "stock/industry-list"
        params = {
            "industry_code": industry_code
        }
        
        return self.request_get(endpoint, params)
    
    def get_stock_price_info(self, 
                          stock_code: str, 
                          date: Optional[str] = None) -> Dict[str, Any]:
        """
        종목 시세정보 상세 조회 (ke10010)
        
        Args:
            stock_code (str): 종목 코드
            date (str, optional): 조회 일자 (YYYYMMDD). 기본값은 None으로 오늘
            
        Returns:
            Dict[str, Any]: 종목 시세 상세정보
        """
        endpoint = "stock/price-info"
        params = {
            "stock_code": stock_code
        }
        
        if date:
            params["date"] = date
        
        return self.request_get(endpoint, params) 