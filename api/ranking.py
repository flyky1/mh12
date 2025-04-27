"""
키움증권 REST API를 위한 순위정보 모듈

이 모듈은 상위 종목 조회와 관련된 API를 제공합니다:
- 거래대금 상위
- 거래량 상위
- 시가총액 상위
- 호가잔량 상위
- 상승률 상위
- 하락률 상위
- 투자자별 순매수 상위
- 신고가/신저가
"""

import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional, List

from .base import APIBase

logger = logging.getLogger(__name__)


class RankingAPI(APIBase):
    """
    순위정보 관련 API 클래스
    
    상위 종목 조회와 관련된 다양한 API 메서드를 제공합니다.
    """
    
    def get_trading_value_top(self, market_code: str, industry_code: Optional[str] = None, 
                              sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        거래대금 상위 종목 조회 (ki10001)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 거래대금 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/trading-value-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        if industry_code:
            params["INDUSTRY_CODE"] = industry_code
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_trading_volume_top(self, market_code: str, industry_code: Optional[str] = None,
                               sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        거래량 상위 종목 조회 (ki10002)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 거래량 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/trading-volume-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        if industry_code:
            params["INDUSTRY_CODE"] = industry_code
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_market_cap_top(self, market_code: str, industry_code: Optional[str] = None,
                           sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        시가총액 상위 종목 조회 (ki10003)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 시가총액 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/market-cap-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        if industry_code:
            params["INDUSTRY_CODE"] = industry_code
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_order_residual_top(self, market_code: str, residual_type: str = "BUY",
                               sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        호가잔량 상위 종목 조회 (ki10004)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            residual_type (str): 잔량 구분 ('BUY': 매수잔량, 'SELL': 매도잔량, 'RATIO': 매수/매도 잔량비율)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 호가잔량 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/order-residual-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "RESIDUAL_TYPE": residual_type,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_rising_top(self, market_code: str, time_period: str = "DAY",
                       sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        상승률 상위 종목 조회 (ki10005)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 상승률 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/rising-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "TIME_PERIOD": time_period,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_falling_top(self, market_code: str, time_period: str = "DAY",
                        sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        하락률 상위 종목 조회 (ki10006)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 하락률 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/falling-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "TIME_PERIOD": time_period,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_investor_net_buying_top(self, market_code: str, investor_type: str = "FOREIGN",
                                    time_period: str = "DAY", sort_type: str = "DESC", 
                                    top_n: int = 30) -> Dict[str, Any]:
        """
        투자자별 순매수 상위 종목 조회 (ki10007)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            investor_type (str): 투자자 구분 ('FOREIGN': 외국인, 'INSTITUTION': 기관, 'INDIVIDUAL': 개인)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 투자자별 순매수 상위 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/investor-net-buying-top"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "INVESTOR_TYPE": investor_type,
            "TIME_PERIOD": time_period,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "SORTBY": sort_type,
            "RANKINGS": top_n,
        }
        
        response = self.request_get(path, params=params)
        return response.json()
    
    def get_new_high_low(self, market_code: str, high_low_type: str = "HIGH",
                         time_period: str = "YEAR", top_n: int = 30) -> Dict[str, Any]:
        """
        신고가/신저가 종목 조회 (ki10008)
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            high_low_type (str): 고가/저가 구분 ('HIGH': 신고가, 'LOW': 신저가)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 신고가/신저가 종목 목록
        """
        path = "/uapi/domestic-stock/v1/ranking/new-high-low"
        
        params = {
            "MKSC_SHRN_ISCD": market_code,
            "HIGH_LOW_TYPE": high_low_type,
            "TIME_PERIOD": time_period,
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "RANKINGS": top_n,
        }
        
        response = self.request_get(path, params=params)
        return response.json() 