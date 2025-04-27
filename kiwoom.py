#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 메인 모듈

이 모듈은 키움 OpenAPI를 통해 국내 및 해외 주식 시장에 접근하는 기능을 제공합니다.
"""

import os
import logging
from typing import Dict, Any, Optional

from .api.base import APIBase
from .api.chart import ChartAPI
from .api.stock import StockAPI
from .api.ranking import RankingAPI
from .api.etf import ETFAPI
from .api.elw import ELWAPI
from .api.sector import SectorAPI
from .api.theme import ThemeAPI
from .auth import KiwoomAuth
from .api.condition import ConditionAPI
from .api.foreigner import ForeignerAPI
from .api.credit_order import CreditOrderAPI


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)


class KiwoomOpenAPI:
    """
    키움 OpenAPI 클래스
    
    이 클래스는 키움 OpenAPI를 통해 국내 및 해외 주식 시장에 접근하는 메서드를 제공합니다.
    - 사용자 인증
    - 차트 데이터 조회
    - 주문 처리
    - 계좌 정보 조회
    - 종목 정보 조회
    """
    
    # API 기본 URL
    BASE_URL = "https://openapi.kiwoom.com"
    
    def __init__(self, app_key: Optional[str] = None, app_secret: Optional[str] = None, base_url: Optional[str] = None):
        """
        KiwoomOpenAPI 클래스 초기화
        
        Args:
            app_key (str, optional): 애플리케이션 키. 기본값은 환경 변수에서 가져옵니다.
            app_secret (str, optional): 애플리케이션 시크릿. 기본값은 환경 변수에서 가져옵니다.
            base_url (str, optional): API 기본 URL. 기본값은 BASE_URL입니다.
        """
        self.app_key = app_key or os.environ.get('kiwoom_appkey')
        self.app_secret = app_secret or os.environ.get('kiwoom_secretkey')
        
        if not self.app_key or not self.app_secret:
            raise ValueError("키움 API 키가 설정되지 않았습니다. 환경 변수 또는 생성자를 통해 키를 제공하세요.")
        
        # 인증 모듈 초기화
        self.auth = KiwoomAuth(self.app_key, self.app_secret)
        
        # 헤더 초기화
        self.headers = {
            "content-type": "application/json",
            "authorization": "",  # 토큰 인증 후 설정
        }
        
        # API 모듈 초기화
        self._init_api_modules()
        
        self.condition = None
        
        if base_url:
            self.BASE_URL = base_url
    
    def _init_api_modules(self):
        """
        API 모듈들을 초기화합니다.
        """
        # 필요한 API 모듈 초기화
        self.stock = StockAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.ranking = RankingAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.etf = ETFAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.elw = ELWAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.sector = SectorAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.theme = ThemeAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.condition = ConditionAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.foreigner = ForeignerAPI(self.BASE_URL, self.app_key, self.app_secret)
        self.credit_order = CreditOrderAPI(self.BASE_URL, self.app_key, self.app_secret)
    
    def auth_login(self) -> Dict[str, Any]:
        """
        키움 API 로그인 인증
        
        Returns:
            Dict[str, Any]: 인증 결과
        """
        try:
            auth_result = self.auth.get_access_token()
            if auth_result and auth_result.get('access_token'):
                self.headers["authorization"] = f"Bearer {auth_result['access_token']}"
                logger.info("인증에 성공했습니다.")
                return {"status": "success", "message": "인증에 성공했습니다.", "data": auth_result}
            else:
                logger.error("인증에 실패했습니다.")
                return {"status": "error", "message": "인증에 실패했습니다.", "data": auth_result}
        except Exception as e:
            logger.exception("인증 중 오류가 발생했습니다.", exc_info=e)
            return {"status": "error", "message": f"인증 중 오류가 발생했습니다: {str(e)}", "data": None}
    
    # 국내 주식 차트 데이터 조회 메서드
    def get_domestic_daily_chart(self, stock_code: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        국내 주식 일봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드 (예: '005930' for 삼성전자)
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_domestic_daily(stock_code, start_date, end_date)
    
    def get_domestic_weekly_chart(self, stock_code: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        국내 주식 주봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_domestic_weekly(stock_code, start_date, end_date)
    
    def get_domestic_monthly_chart(self, stock_code: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        국내 주식 월봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_domestic_monthly(stock_code, start_date, end_date)
    
    def get_domestic_minute_chart(self, stock_code: str, start_time: str, end_time: str, time_interval: str = "1") -> Dict[str, Any]:
        """
        국내 주식 분봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_time (str): 조회 시작시간 (YYYYMMDDHHMMSS)
            end_time (str): 조회 종료시간 (YYYYMMDDHHMMSS)
            time_interval (str): 시간간격 (1, 3, 5, 10, 15, 30, 60 분)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_domestic_minute(stock_code, start_time, end_time, time_interval)
    
    def get_domestic_tick_chart(self, stock_code: str, start_time: str, end_time: str) -> Dict[str, Any]:
        """
        국내 주식 틱 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_time (str): 조회 시작시간 (YYYYMMDDHHMMSS)
            end_time (str): 조회 종료시간 (YYYYMMDDHHMMSS)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_domestic_tick(stock_code, start_time, end_time)
    
    # 해외 주식 차트 데이터 조회 메서드
    def get_overseas_daily_chart(self, 
                                stock_code: str, 
                                exchange: str, 
                                start_date: str, 
                                end_date: str, 
                                adj_price: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 일봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드 (예: 'AAPL' for 애플)
            exchange (str): 거래소 코드 (NAS, NYSE, AMEX 등)
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            adj_price (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_overseas_daily(stock_code, exchange, start_date, end_date, adj_price)
    
    def get_overseas_weekly_chart(self, 
                                 stock_code: str, 
                                 exchange: str, 
                                 start_date: str, 
                                 end_date: str, 
                                 adj_price: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 주봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            exchange (str): 거래소 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            adj_price (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_overseas_weekly(stock_code, exchange, start_date, end_date, adj_price)
    
    def get_overseas_monthly_chart(self, 
                                  stock_code: str, 
                                  exchange: str, 
                                  start_date: str, 
                                  end_date: str, 
                                  adj_price: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 월봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            exchange (str): 거래소 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            adj_price (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_overseas_monthly(stock_code, exchange, start_date, end_date, adj_price)
    
    def get_overseas_minute_chart(self, 
                                 stock_code: str, 
                                 exchange: str, 
                                 start_time: str, 
                                 end_time: str, 
                                 time_interval: str = "5",
                                 adj_price: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 분봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            exchange (str): 거래소 코드
            start_time (str): 조회 시작시간 (YYYYMMDDHHmmss)
            end_time (str): 조회 종료시간 (YYYYMMDDHHmmss)
            time_interval (str): 시간간격 (1, 3, 5, 10, 15, 30, 60 분)
            adj_price (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.chart.get_overseas_minute(stock_code, exchange, start_time, end_time, time_interval, adj_price)
    
    # 국내 주식 종목정보 조회 메서드
    def get_stock_info(self, stock_code: str) -> Dict[str, Any]:
        """
        국내 주식 종목 기본정보 조회
        
        Args:
            stock_code (str): 종목 코드 (예: '005930' for 삼성전자)
            
        Returns:
            Dict[str, Any]: 종목 기본정보
        """
        return self.stock.get_domestic_stock_info(stock_code)
    
    def get_overseas_stock_info(self, stock_code: str, exchange: str) -> Dict[str, Any]:
        """
        해외 주식 종목 기본정보 조회
        
        Args:
            stock_code (str): 종목 코드 (예: 'AAPL' for 애플)
            exchange (str): 거래소 코드 (예: 'NAS', 'NYSE')
            
        Returns:
            Dict[str, Any]: 종목 기본정보
        """
        return self.stock.get_overseas_stock_info(stock_code, exchange)
    
    def get_suspended_stocks(self, market_code: Optional[str] = None) -> Dict[str, Any]:
        """
        거래정지종목 조회
        
        Args:
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            
        Returns:
            Dict[str, Any]: 거래정지종목 목록
        """
        return self.stock.get_suspended_stocks(market_code)
    
    def get_managed_stocks(self, market_code: Optional[str] = None) -> Dict[str, Any]:
        """
        관리종목 조회
        
        Args:
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            
        Returns:
            Dict[str, Any]: 관리종목 목록
        """
        return self.stock.get_managed_stocks(market_code)
    
    def get_stock_disclosure(self, 
                           stock_code: Optional[str] = None, 
                           start_date: Optional[str] = None, 
                           end_date: Optional[str] = None, 
                           disclosure_type: Optional[str] = None) -> Dict[str, Any]:
        """
        종목별 공시정보 조회
        
        Args:
            stock_code (str, optional): 종목 코드. 기본값은 None으로 모든 종목 조회
            start_date (str, optional): 조회 시작일 (YYYYMMDD). 기본값은 None으로 최근 1주일
            end_date (str, optional): 조회 종료일 (YYYYMMDD). 기본값은 None으로 오늘
            disclosure_type (str, optional): 공시 유형 코드. 기본값은 None으로 모든 유형
            
        Returns:
            Dict[str, Any]: 공시정보 목록
        """
        return self.stock.get_stock_disclosure(stock_code, start_date, end_date, disclosure_type)
    
    def search_stock(self, 
                    query: str, 
                    market_code: Optional[str] = None, 
                    is_etf: Optional[bool] = None, 
                    is_elw: Optional[bool] = None) -> Dict[str, Any]:
        """
        종목코드/명 검색
        
        Args:
            query (str): 검색어 (종목명 또는 종목코드의 일부)
            market_code (str, optional): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ'). 기본값은 None으로 모든 시장 조회
            is_etf (bool, optional): ETF 종목만 검색 여부. 기본값은 None으로 모든 종목 조회
            is_elw (bool, optional): ELW 종목만 검색 여부. 기본값은 None으로 모든 종목 조회
            
        Returns:
            Dict[str, Any]: 검색 결과 종목 목록
        """
        return self.stock.search_stock(query, market_code, is_etf, is_elw)
    
    def search_overseas_stock(self, 
                            query: str, 
                            exchange: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 종목코드/명 검색
        
        Args:
            query (str): 검색어 (종목명 또는 종목코드의 일부)
            exchange (str, optional): 거래소 코드 (예: 'NAS', 'NYSE'). 기본값은 None으로 모든 거래소 조회
            
        Returns:
            Dict[str, Any]: 검색 결과 종목 목록
        """
        return self.stock.search_overseas_stock(query, exchange)
    
    def get_stock_financial_info(self, 
                               stock_code: str, 
                               info_type: Optional[str] = None) -> Dict[str, Any]:
        """
        종목 재무정보 조회
        
        Args:
            stock_code (str): 종목 코드
            info_type (str, optional): 재무정보 유형 (예: 'QUARTER', 'ANNUAL'). 기본값은 None으로 모든 유형 조회
            
        Returns:
            Dict[str, Any]: 종목 재무정보
        """
        return self.stock.get_stock_financial_info(stock_code, info_type)
    
    def get_stock_investor_trend(self, 
                               stock_code: str, 
                               start_date: str, 
                               end_date: str) -> Dict[str, Any]:
        """
        종목별 투자자 동향 조회
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 투자자별 매매동향 정보
        """
        return self.stock.get_stock_investor_trend(stock_code, start_date, end_date)
    
    def get_market_stock_list(self, market_code: str) -> Dict[str, Any]:
        """
        시장별 종목 목록 조회
        
        Args:
            market_code (str): 시장 구분 코드 (예: 'KOSPI', 'KOSDAQ')
            
        Returns:
            Dict[str, Any]: 종목 목록
        """
        return self.stock.get_market_stock_list(market_code)
    
    def get_industry_stock_list(self, industry_code: str) -> Dict[str, Any]:
        """
        업종별 종목 목록 조회
        
        Args:
            industry_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 종목 목록
        """
        return self.stock.get_industry_stock_list(industry_code)
    
    def get_stock_price_info(self, 
                          stock_code: str, 
                          date: Optional[str] = None) -> Dict[str, Any]:
        """
        종목 시세정보 상세 조회
        
        Args:
            stock_code (str): 종목 코드
            date (str, optional): 조회 일자 (YYYYMMDD). 기본값은 None으로 오늘
            
        Returns:
            Dict[str, Any]: 종목 시세 상세정보
        """
        return self.stock.get_stock_price_info(stock_code, date)
    
    # 순위정보 관련 메서드
    def get_trading_value_top(self, market_code: str, industry_code: Optional[str] = None, 
                             sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        거래대금 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 거래대금 상위 종목 목록
        """
        return self.ranking.get_trading_value_top(market_code, industry_code, sort_type, top_n)

    def get_trading_volume_top(self, market_code: str, industry_code: Optional[str] = None,
                              sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        거래량 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 거래량 상위 종목 목록
        """
        return self.ranking.get_trading_volume_top(market_code, industry_code, sort_type, top_n)

    def get_market_cap_top(self, market_code: str, industry_code: Optional[str] = None,
                            sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        시가총액 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            industry_code (Optional[str]): 업종 코드 (None: 전체 업종)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 시가총액 상위 종목 목록
        """
        return self.ranking.get_market_cap_top(market_code, industry_code, sort_type, top_n)

    def get_order_residual_top(self, market_code: str, residual_type: str = "BUY",
                              sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        호가잔량 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            residual_type (str): 잔량 구분 ('BUY': 매수잔량, 'SELL': 매도잔량, 'RATIO': 매수/매도 잔량비율)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 호가잔량 상위 종목 목록
        """
        return self.ranking.get_order_residual_top(market_code, residual_type, sort_type, top_n)

    def get_rising_top(self, market_code: str, time_period: str = "DAY",
                      sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        상승률 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 상승률 상위 종목 목록
        """
        return self.ranking.get_rising_top(market_code, time_period, sort_type, top_n)

    def get_falling_top(self, market_code: str, time_period: str = "DAY",
                       sort_type: str = "DESC", top_n: int = 30) -> Dict[str, Any]:
        """
        하락률 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 하락률 상위 종목 목록
        """
        return self.ranking.get_falling_top(market_code, time_period, sort_type, top_n)

    def get_investor_net_buying_top(self, market_code: str, investor_type: str = "FOREIGN",
                                   time_period: str = "DAY", sort_type: str = "DESC", 
                                   top_n: int = 30) -> Dict[str, Any]:
        """
        투자자별 순매수 상위 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            investor_type (str): 투자자 구분 ('FOREIGN': 외국인, 'INSTITUTION': 기관, 'INDIVIDUAL': 개인)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간)
            sort_type (str): 정렬 방식 ('DESC': 내림차순, 'ASC': 오름차순)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 투자자별 순매수 상위 종목 목록
        """
        return self.ranking.get_investor_net_buying_top(market_code, investor_type, time_period, sort_type, top_n)

    def get_new_high_low(self, market_code: str, high_low_type: str = "HIGH",
                        time_period: str = "YEAR", top_n: int = 30) -> Dict[str, Any]:
        """
        신고가/신저가 종목 조회
        
        Args:
            market_code (str): 시장 코드 ('ALL': 전체, 'KOSPI': 코스피, 'KOSDAQ': 코스닥)
            high_low_type (str): 고가/저가 구분 ('HIGH': 신고가, 'LOW': 신저가)
            time_period (str): 기간 ('DAY': 일간, 'WEEK': 주간, 'MONTH': 월간, 'YEAR': 연간)
            top_n (int): 조회할 종목 수 (최대 100)
            
        Returns:
            Dict[str, Any]: 신고가/신저가 종목 목록
        """
        return self.ranking.get_new_high_low(market_code, high_low_type, time_period, top_n)

    # ETF 관련 메서드
    def get_etf_info(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 기본 정보 조회
        
        Args:
            symbol (str): ETF 종목 코드
            
        Returns:
            Dict[str, Any]: ETF 기본 정보
        """
        return self.etf.get_etf_info(symbol)
    
    def get_etf_components(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 구성종목 조회
        
        Args:
            symbol (str): ETF 종목 코드
            
        Returns:
            Dict[str, Any]: ETF 구성종목 정보
        """
        return self.etf.get_etf_components(symbol)
    
    def get_etf_nav(self, symbol: str) -> Dict[str, Any]:
        """
        ETF NAV 조회
        
        Args:
            symbol (str): ETF 종목 코드
            
        Returns:
            Dict[str, Any]: ETF NAV 정보
        """
        return self.etf.get_etf_nav(symbol)
    
    def get_etf_price(self, symbol: str) -> Dict[str, Any]:
        """
        ETF 시세 정보 조회
        
        Args:
            symbol (str): ETF 종목 코드
            
        Returns:
            Dict[str, Any]: ETF 시세 정보
        """
        return self.etf.get_etf_price(symbol)
    
    def get_etf_list(self, etf_type: Optional[str] = None, market_code: str = 'J') -> Dict[str, Any]:
        """
        ETF 목록 조회
        
        Args:
            etf_type (str, optional): ETF 유형 (None: 전체, "1": 시장지수, "2": 섹터지수, "3": 테마지수, "4": 해외지수, "5": 채권, "6": 상품, "7": 기타)
            market_code (str, optional): 시장구분코드 (J: 전체, 0: 코스피, 1: 코스닥)
            
        Returns:
            Dict[str, Any]: ETF 목록
        """
        return self.etf.get_etf_list(etf_type, market_code)
    
    def get_etf_price_by_date(self, symbol: str, start_date: str, end_date: str) -> Dict[str, Any]:
        """
        ETF 일별 시세 조회
        
        Args:
            symbol (str): ETF 종목 코드
            start_date (str): 조회 시작일자 (YYYYMMDD 형식)
            end_date (str): 조회 종료일자 (YYYYMMDD 형식)
            
        Returns:
            Dict[str, Any]: ETF 일별 시세 정보
        """
        return self.etf.get_etf_price_by_date(symbol, start_date, end_date)
    
    # ELW 관련 메서드
    def get_elw_info(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 기본 정보 조회
        
        Args:
            symbol (str): ELW 종목 코드
            
        Returns:
            Dict[str, Any]: ELW 기본 정보
        """
        return self.elw.get_elw_info(symbol)
    
    def get_elw_price(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 시세 정보 조회
        
        Args:
            symbol (str): ELW 종목 코드
            
        Returns:
            Dict[str, Any]: ELW 시세 정보
        """
        return self.elw.get_elw_price(symbol)
    
    def get_elw_remain_days(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 잔존일수/배당락 조회
        
        Args:
            symbol (str): ELW 종목 코드
            
        Returns:
            Dict[str, Any]: ELW 잔존일수 및 배당락 정보
        """
        return self.elw.get_elw_remain_days(symbol)
    
    def get_elw_by_issuer(self, issuer_code: str, base_asset_code: Optional[str] = None) -> Dict[str, Any]:
        """
        ELW 발행회사별 정보 조회
        
        Args:
            issuer_code (str): 발행회사 코드
            base_asset_code (str, optional): 기초자산 코드. None이면 모든 기초자산
            
        Returns:
            Dict[str, Any]: 발행회사별 ELW 목록
        """
        return self.elw.get_elw_by_issuer(issuer_code, base_asset_code)
    
    def get_elw_sensitivity(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 민감도 지표 조회
        
        Args:
            symbol (str): ELW 종목 코드
            
        Returns:
            Dict[str, Any]: ELW 민감도 지표 정보
        """
        return self.elw.get_elw_sensitivity(symbol)
    
    def get_elw_daily_sensitivity(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 일별 민감도 지표 조회
        
        Args:
            symbol (str): ELW 종목 코드
            
        Returns:
            Dict[str, Any]: ELW 일별 민감도 지표 정보
        """
        return self.elw.get_elw_daily_sensitivity(symbol)
    
    def get_elw_price_change(self, 
                           change_type: str = "1", 
                           time_type: str = "2",
                           time_value: str = "1",
                           volume_type: str = "0",
                           issuer_code: str = "000000000000",
                           base_asset_code: str = "000000000000") -> Dict[str, Any]:
        """
        ELW 가격 급등락 조회
        
        Args:
            change_type (str): 등락구분 (1: 급등, 2: 급락)
            time_type (str): 시간구분 (1: 분전, 2: 일전)
            time_value (str): 시간 값 (분 또는 일, 예: 1, 3, 5)
            volume_type (str): 거래량구분 (0: 전체, 10: 만주이상 등)
            issuer_code (str): 발행사코드 (전체: 000000000000)
            base_asset_code (str): 기초자산코드 (전체: 000000000000)
            
        Returns:
            Dict[str, Any]: ELW 가격 급등락 목록
        """
        return self.elw.get_elw_price_change(
            change_type, time_type, time_value, volume_type, issuer_code, base_asset_code
        )
    
    def search_elw(self, 
                  query: str,
                  right_type: Optional[str] = None,
                  base_asset_code: Optional[str] = None,
                  issuer_code: Optional[str] = None) -> Dict[str, Any]:
        """
        ELW 종목 검색
        
        Args:
            query (str): 검색어 (종목명 또는 코드)
            right_type (str, optional): 권리유형 (C: 콜, P: 풋)
            base_asset_code (str, optional): 기초자산 코드
            issuer_code (str, optional): 발행회사 코드
            
        Returns:
            Dict[str, Any]: 검색 결과 ELW 목록
        """
        return self.elw.search_elw(query, right_type, base_asset_code, issuer_code)
    
    # 업종 정보 조회 메서드
    def get_sector_price(self, market_type: str, sector_code: str) -> Dict[str, Any]:
        """
        업종 현재가 정보 조회
        
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
        return self.sector.get_sector_price(market_type, sector_code)
    
    def get_sector_components(self, market_type: str, sector_code: str) -> Dict[str, Any]:
        """
        업종별 종목 정보 조회
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            sector_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 업종별 종목 목록
        """
        return self.sector.get_sector_components(market_type, sector_code)
    
    def get_sector_basic_info(self, sector_code: str) -> Dict[str, Any]:
        """
        업종 기본정보 조회
        
        Args:
            sector_code (str): 업종 코드
            
        Returns:
            Dict[str, Any]: 업종 기본정보
        """
        return self.sector.get_sector_basic_info(sector_code)
    
    def get_sector_price_info(self, sector_code: str, date: Optional[str] = None) -> Dict[str, Any]:
        """
        업종 시세정보 조회
        
        Args:
            sector_code (str): 업종 코드
            date (str, optional): 조회 일자 (YYYYMMDD). 기본값은 None으로 오늘
            
        Returns:
            Dict[str, Any]: 업종 시세정보
        """
        return self.sector.get_sector_price_info(sector_code, date)
    
    def get_sector_investor_trend(self, 
                                market_type: str,
                                amount_qty_type: str = '0',
                                base_date: Optional[str] = None,
                                exchange_type: str = '3') -> Dict[str, Any]:
        """
        업종별 투자자 순매수 정보 조회
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            amount_qty_type (str): 금액/수량 구분 (0: 금액, 1: 수량)
            base_date (str, optional): 기준일자 (YYYYMMDD). 기본값은 None으로 오늘
            exchange_type (str): 거래소 구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 업종별 투자자 순매수 정보
        """
        return self.sector.get_sector_investor_trend(market_type, amount_qty_type, base_date, exchange_type)
    
    def get_sector_program_trading(self, stock_code: str) -> Dict[str, Any]:
        """
        업종 프로그램 매매 정보 조회
        
        Args:
            stock_code (str): 종목 코드
            
        Returns:
            Dict[str, Any]: 업종 프로그램 매매 정보
        """
        return self.sector.get_sector_program_trading(stock_code)
    
    def get_sector_index(self, market_type: str) -> Dict[str, Any]:
        """
        섹터 지수 정보 조회
        
        Args:
            market_type (str): 시장 구분 (0: 코스피, 1: 코스닥)
            
        Returns:
            Dict[str, Any]: 섹터 지수 정보
        """
        return self.sector.get_sector_index(market_type)
    
    # 테마 정보 조회 메서드
    def get_theme_list(self, 
                      query_type: str = '0', 
                      date_type: str = '10', 
                      theme_name: Optional[str] = None,
                      flu_pl_amt_type: str = '1',
                      exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마 목록 조회
        
        Args:
            query_type (str): 검색구분 (0: 전체검색, 1: 테마검색, 2: 종목검색)
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            theme_name (str, optional): 테마명 검색어
            flu_pl_amt_type (str): 등락수익구분 (1: 상위기간수익률, 2: 하위기간수익률, 3: 상위등락률, 4: 하위등락률)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 테마 목록 정보
        """
        return self.theme.get_theme_list(query_type, date_type, theme_name, flu_pl_amt_type, exchange_type)
    
    def get_theme_stocks(self, 
                        theme_group_code: str, 
                        date_type: str = '2', 
                        exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마별 구성 종목 조회
        
        Args:
            theme_group_code (str): 테마그룹코드
            date_type (str): 날짜구분 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 테마별 구성 종목 목록
        """
        return self.theme.get_theme_stocks(theme_group_code, date_type, exchange_type)
    
    def get_stock_themes(self, 
                        stock_code: str, 
                        date_type: str = '10', 
                        exchange_type: str = '3') -> Dict[str, Any]:
        """
        종목별 테마 조회
        
        Args:
            stock_code (str): 종목코드
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 종목이 속한 테마 목록
        """
        return self.theme.get_stock_themes(stock_code, date_type, exchange_type)
    
    def search_themes(self, 
                     theme_name: str, 
                     date_type: str = '10', 
                     exchange_type: str = '3') -> Dict[str, Any]:
        """
        테마 이름으로 검색
        
        Args:
            theme_name (str): 테마명 검색어
            date_type (str): 날짜구분 n일전 (1일 ~ 99일 날짜입력)
            exchange_type (str): 거래소구분 (1: KRX, 2: NXT, 3: 통합)
            
        Returns:
            Dict[str, Any]: 검색된 테마 목록
        """
        return self.theme.search_themes(theme_name, date_type, exchange_type)
    
    # 조건검색 관련 메서드
    def get_condition_list(self):
        """
        조건검색 목록 조회
        
        Returns:
            Dict[str, Any]: 조건검색 목록 정보
        """
        return self.condition.get_condition_list()
    
    def execute_condition(self, condition_name, condition_index, search_type="0"):
        """
        일반 조건검색 실행
        
        Args:
            condition_name (str): 조건검색 이름
            condition_index (str): 조건검색 인덱스
            search_type (str): 검색 유형 (0: 전체조회, 1: 실시간조회)
            
        Returns:
            Dict[str, Any]: 조건검색 결과
        """
        return self.condition.execute_condition(condition_name, condition_index, search_type)
    
    async def start_realtime_condition(self, condition_name, condition_index, callback):
        """
        실시간 조건검색 시작
        
        Args:
            condition_name (str): 조건검색 이름
            condition_index (str): 조건검색 인덱스
            callback (callable): 실시간 데이터 수신 콜백 함수
            
        Returns:
            Dict[str, Any]: 실시간 조건검색 요청 결과
        """
        return await self.condition.start_realtime_condition(condition_name, condition_index, callback)
    
    async def stop_realtime_condition(self, tr_id):
        """
        실시간 조건검색 중지
        
        Args:
            tr_id (str): 실시간 조건검색 트랜잭션 ID
            
        Returns:
            Dict[str, Any]: 중지 요청 결과
        """
        return await self.condition.stop_realtime_condition(tr_id)
    
    async def disconnect_condition_websocket(self):
        """
        조건검색 웹소켓 연결 종료
        """
        await self.condition.disconnect_websocket()

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
        return self.foreigner.get_foreigner_holdings(stock_code, start_date, end_date)

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
        return self.foreigner.get_foreigner_net_purchase(stock_code, start_date, end_date)

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
        return self.foreigner.get_institutional_net_purchase(stock_code, start_date, end_date)

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
        return self.foreigner.get_investor_trend(market_code, start_date, end_date)

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
        return self.foreigner.get_foreign_institution_day_trading(stock_code)

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
        return self.foreigner.get_foreign_ownership_limit(stock_code)

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
        return self.credit_order.place_credit_buy_order(
            exchange_type, stock_code, order_quantity, order_price, 
            trade_type, credit_deal_type, credit_loan_date, condition_price
        )

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
        return self.credit_order.place_credit_sell_order(
            exchange_type, stock_code, order_quantity, order_price, 
            trade_type, credit_deal_type, credit_loan_date, condition_price
        )

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
        return self.credit_order.modify_credit_order(
            exchange_type, original_order_number, stock_code, 
            modify_quantity, modify_price, modify_condition_price
        )

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
        return self.credit_order.cancel_credit_order(
            exchange_type, original_order_number, stock_code, cancel_quantity
        )

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
        return self.credit_order.get_credit_balance(
            account_number, exchange_type, credit_type
        )

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
        return self.credit_order.repay_credit_loan(
            account_number, exchange_type, stock_code, 
            repay_quantity, repay_type, loan_date
        ) 