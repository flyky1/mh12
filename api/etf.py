"""
ETF 모듈 (ETF Module)

이 모듈은 키움증권 OpenAPI를 통해 ETF(상장지수펀드) 관련 정보를 조회하는 기능을 제공합니다.
주요 기능:
- ETF 기본 정보 조회
- ETF 구성종목 조회
- ETF NAV(순자산가치) 조회
- ETF 시세 정보 조회
"""

import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional, List

from .base import APIBase

class ETFAPI(APIBase):
    """
    ETF API 클래스

    이 클래스는 ETF(상장지수펀드) 관련 정보를 조회하는 API를 제공합니다.
    """

    def get_etf_info(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 기본 정보 조회 (kl10001)

        Args:
            symbol (str): ETF 종목 코드

        Returns:
            Dict[str, Any]: ETF 기본 정보
                - code (str): 종목코드
                - name (str): 종목명
                - etf_type (str): ETF 유형
                - base_index (str): 기초지수
                - company (str): 운용사
                - base_date (str): 상장일
                - tax_type (str): 과세유형
                - manage_fee (float): 운용보수
                - trust_fee (float): 수탁보수
                - total_fee (float): 총보수
                - tr_volume (int): 거래량
                - tr_value (int): 거래대금
                - market_cap (int): 시가총액
                - nav (float): 순자산가치
                - te (float): 추적오차
                - basket_price (int): 장중 CU 가격
                - basket_count (int): CU당 주식수
                - distribution (str): 배당현황
                - yield_rate (float): 분배금수익률
        """
        url = "uapi/domestic-stock/v1/quotations/etf-info"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_etf_components(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 구성종목 조회 (kl10002)

        Args:
            symbol (str): ETF 종목 코드

        Returns:
            Dict[str, Any]: ETF 구성종목 정보
                - etf_code (str): ETF 종목코드
                - etf_name (str): ETF 종목명
                - component_list (List[Dict]): 구성종목 목록
                    - code (str): 구성종목 코드
                    - name (str): 구성종목 명
                    - quantity (int): 수량
                    - weight (float): 비중
                    - market_cap (int): 시가총액
                    - sector (str): 섹터
        """
        url = "uapi/domestic-stock/v1/quotations/etf-components"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_etf_nav(self, symbol: str) -> Dict[str, Any]:
        """
        ETF NAV 조회 (kl10003)

        Args:
            symbol (str): ETF 종목 코드

        Returns:
            Dict[str, Any]: ETF NAV 정보
                - code (str): 종목코드
                - name (str): 종목명
                - nav (float): 순자산가치(NAV)
                - nav_date (str): NAV 산출일자
                - nav_time (str): NAV 산출시간
                - price (float): 현재가
                - premium (float): 괴리율
                - tracking_error (float): 추적오차
                - hist_nav (List[Dict]): 과거 NAV 기록
                    - date (str): 날짜
                    - nav (float): NAV
                    - price (float): 종가
                    - premium (float): 괴리율
        """
        url = "uapi/domestic-stock/v1/quotations/etf-nav"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_etf_price(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 시세 정보 조회 (kl10004)

        Args:
            symbol (str): ETF 종목 코드

        Returns:
            Dict[str, Any]: ETF 시세 정보
                - code (str): 종목코드
                - name (str): 종목명
                - price (float): 현재가
                - change (float): 전일대비
                - change_rate (float): 등락률
                - open (float): 시가
                - high (float): 고가
                - low (float): 저가
                - volume (int): 거래량
                - value (int): 거래대금
                - market_cap (int): 시가총액
                - nav (float): 순자산가치
                - premium (float): 괴리율
                - ask_price (float): 매도호가
                - bid_price (float): 매수호가
                - ask_volume (int): 매도호가수량
                - bid_volume (int): 매수호가수량
        """
        url = "uapi/domestic-stock/v1/quotations/etf-price"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_etf_list(self, etf_type: Optional[str] = None, market_code: str = 'J') -> Dict[str, Any]:
        """
        ETF 목록 조회

        Args:
            etf_type (str, optional): ETF 유형 (None: 전체, "1": 시장지수, "2": 섹터지수, "3": 테마지수, "4": 해외지수, "5": 채권, "6": 상품, "7": 기타)
            market_code (str, optional): 시장구분코드 (J: 전체, 0: 코스피, 1: 코스닥)

        Returns:
            Dict[str, Any]: ETF 목록
                - etf_list (List[Dict]): ETF 목록
                    - code (str): 종목코드
                    - name (str): 종목명
                    - etf_type (str): ETF 유형
                    - base_index (str): 기초지수
                    - company (str): 운용사
                    - market (str): 시장구분
        """
        url = "uapi/domestic-stock/v1/quotations/etf-list"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": market_code,
        }
        
        if etf_type:
            params["FID_INPUT_ETF_TYPE"] = etf_type
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_etf_price_by_date(self, symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        ETF 일별 시세 조회

        Args:
            symbol (str): ETF 종목 코드
            start_date (str): 조회 시작일자 (YYYYMMDD 형식)
            end_date (str): 조회 종료일자 (YYYYMMDD 형식)

        Returns:
            Dict[str, Any]: ETF 일별 시세 정보
                - code (str): 종목코드
                - name (str): 종목명
                - price_list (List[Dict]): 일별 시세 목록
                    - date (str): 날짜
                    - open (float): 시가
                    - high (float): 고가
                    - low (float): 저가
                    - close (float): 종가
                    - volume (int): 거래량
                    - value (int): 거래대금
                    - nav (float): 순자산가치
                    - premium (float): 괴리율
        """
        url = "uapi/domestic-stock/v1/quotations/etf-price-by-date"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
            "FID_INPUT_DATE_1": start_date,
            "FID_INPUT_DATE_2": end_date,
            "FID_PERIOD_DIV_CODE": "D"  # 일별 데이터
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json() 