#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 차트 데이터 관련 API 모듈
"""

from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta

from ..client import KiwoomClient


class ChartAPI:
    """차트 데이터 조회를 위한 API 클래스
    
    키움증권 REST API를 사용하여 차트 데이터를 조회합니다.
    일/주/월/분/틱 데이터를 지원합니다.
    """
    
    def __init__(self, client: KiwoomClient):
        """ChartAPI 클래스 초기화
        
        Args:
            client: API 클라이언트 인스턴스
        """
        self.client = client
    
    def get_domestic_stock_daily(
        self,
        stk_cd: str,
        inq_strt_dt: Optional[str] = None,
        inq_end_dt: Optional[str] = None,
        adj_cls_prc_yn: str = 'N',
    ) -> Dict[str, Any]:
        """국내주식 일봉 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_strt_dt: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_dt: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            adj_cls_prc_yn: 수정주가 여부 (Y/N)
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dt is None:
            inq_end_dt = datetime.now().strftime('%Y%m%d')
        if inq_strt_dt is None:
            inq_strt_dt = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
        params = {
            'stk_cd': stk_cd,
            'adj_cls_prc_yn': adj_cls_prc_yn,
            'inq_strt_dt': inq_strt_dt,
            'inq_end_dt': inq_end_dt,
        }
        
        return self.client.request('get', 'domestic_stock_daily', params=params)
    
    def get_domestic_stock_weekly(
        self,
        stk_cd: str,
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
        adj_cls_prc_yn: str = 'N',
    ) -> Dict[str, Any]:
        """국내주식 주봉 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 30주전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            adj_cls_prc_yn: 수정주가 여부 (Y/N)
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(weeks=30)).strftime('%Y%m%d')
            
        params = {
            'stk_cd': stk_cd,
            'adj_cls_prc_yn': adj_cls_prc_yn,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        return self.client.request('get', 'domestic_stock_weekly', params=params)
    
    def get_domestic_stock_monthly(
        self,
        stk_cd: str,
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
        adj_cls_prc_yn: str = 'N',
    ) -> Dict[str, Any]:
        """국내주식 월봉 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 12개월전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            adj_cls_prc_yn: 수정주가 여부 (Y/N)
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
            
        params = {
            'stk_cd': stk_cd,
            'adj_cls_prc_yn': adj_cls_prc_yn,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        return self.client.request('get', 'domestic_stock_monthly', params=params)
    
    def get_domestic_stock_minute(
        self,
        stk_cd: str,
        inq_dvsn_cd: str = '1',  # 1:분단위, 3:틱단위
        cts_date: Optional[str] = None,
        cts_time: Optional[str] = None,
        inq_data_ctnt: Optional[int] = None,
        adj_cls_prc_yn: str = 'N',
    ) -> Dict[str, Any]:
        """국내주식 분봉 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_dvsn_cd: 조회구분코드 (1:분단위, 3:틱단위)
            cts_date: 연속일자 (YYYYMMDD), 연속조회시 이전 응답의 cts_date
            cts_time: 연속시간 (HHMMSS), 연속조회시 이전 응답의 cts_time
            inq_data_ctnt: 조회갯수 (최대 30,000건)
            adj_cls_prc_yn: 수정주가 여부 (Y/N)
            
        Returns:
            API 응답 데이터
        """
        params = {
            'stk_cd': stk_cd,
            'inq_dvsn_cd': inq_dvsn_cd,
            'adj_cls_prc_yn': adj_cls_prc_yn,
        }
        
        if cts_date:
            params['cts_date'] = cts_date
        if cts_time:
            params['cts_time'] = cts_time
        if inq_data_ctnt:
            params['inq_data_ctnt'] = inq_data_ctnt
        
        return self.client.request('get', 'domestic_stock_tick', params=params)
    
    def get_domestic_stock_minute_by_period(
        self,
        stk_cd: str,
        mkt_cd: str = '1',  # 시장코드 (1:코스피, 2:코스닥)
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
        inq_time: Optional[str] = None,
        adj_cls_prc_yn: str = 'N',
    ) -> Dict[str, Any]:
        """국내주식 분봉 차트 데이터 기간별 조회
        
        Args:
            stk_cd: 종목코드
            mkt_cd: 시장코드 (1:코스피, 2:코스닥)
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            inq_time: 조회단위시간 (1, 3, 5, 10, 15, 30, 60분 단위)
            adj_cls_prc_yn: 수정주가 여부 (Y/N)
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        params = {
            'stk_cd': stk_cd,
            'mkt_cd': mkt_cd,
            'adj_cls_prc_yn': adj_cls_prc_yn,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        if inq_time:
            params['inq_time'] = inq_time
            
        return self.client.request('get', 'domestic_stock_minute_period', params=params)
    
    def get_overseas_stock_daily(
        self,
        excd: str,
        symb: str,
        gubn: str = '0',  # 조회구분 (0:일, 1:주, 2:월)
        inq_strt_ymd: Optional[str] = None,
        inq_end_ymd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """해외주식 일봉 차트 데이터 조회
        
        Args:
            excd: 거래소코드 (NYS:뉴욕, NAS:나스닥, AMS:아멕스 등)
            symb: 종목코드
            gubn: 조회구분 (0:일, 1:주, 2:월)
            inq_strt_ymd: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_ymd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_ymd is None:
            inq_end_ymd = datetime.now().strftime('%Y%m%d')
        if inq_strt_ymd is None:
            inq_strt_ymd = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
        params = {
            'excd': excd,
            'symb': symb,
            'gubn': gubn,
            'inq_strt_ymd': inq_strt_ymd,
            'inq_end_ymd': inq_end_ymd,
        }
        
        return self.client.request('get', 'overseas_stock_chart_daily', params=params)
    
    def get_domestic_stock_day_trend(
        self,
        stk_cd: str,
        inq_date: Optional[str] = None,
    ) -> Dict[str, Any]:
        """국내주식 일중 추이 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_date: 조회일자 (YYYYMMDD), 미입력시 당일
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_date is None:
            inq_date = datetime.now().strftime('%Y%m%d')
            
        params = {
            'stk_cd': stk_cd,
            'inq_date': inq_date,
        }
        
        return self.client.request('get', 'domestic_stock_day_trend', params=params)
    
    def get_domestic_index_daily(
        self,
        stk_id_cd: str,
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """국내지수 일봉 차트 데이터 조회
        
        Args:
            stk_id_cd: 종목지수코드 (ex: 코스피: U001, 코스닥: U201)
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
        params = {
            'stk_id_cd': stk_id_cd,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        return self.client.request('get', 'domestic_index_daily', params=params)
    
    def get_domestic_index_minute(
        self,
        stk_id_cd: str,
        inq_time: str = '5',  # 조회단위시간 (1, 3, 5, 10, 15, 30, 60분 단위)
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """국내지수 분봉 차트 데이터 조회
        
        Args:
            stk_id_cd: 종목지수코드 (ex: 코스피: U001, 코스닥: U201)
            inq_time: 조회단위시간 (1, 3, 5, 10, 15, 30, 60분 단위)
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
        params = {
            'stk_id_cd': stk_id_cd,
            'inq_time': inq_time,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        return self.client.request('get', 'domestic_index_minute', params=params)
    
    def get_domestic_elw_daily(
        self,
        stk_cd: str,
        inq_strt_dd: Optional[str] = None,
        inq_end_dd: Optional[str] = None,
    ) -> Dict[str, Any]:
        """국내 ELW 일봉 차트 데이터 조회
        
        Args:
            stk_cd: 종목코드
            inq_strt_dd: 조회 시작일자 (YYYYMMDD), 미입력시 30일전
            inq_end_dd: 조회 종료일자 (YYYYMMDD), 미입력시 당일
            
        Returns:
            API 응답 데이터
        """
        # 날짜 기본값 설정
        if inq_end_dd is None:
            inq_end_dd = datetime.now().strftime('%Y%m%d')
        if inq_strt_dd is None:
            inq_strt_dd = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
            
        params = {
            'stk_cd': stk_cd,
            'inq_strt_dd': inq_strt_dd,
            'inq_end_dd': inq_end_dd,
        }
        
        return self.client.request('get', 'domestic_elw_daily', params=params)

    def get_domestic_chart(self, 
                          stk_cd: str, 
                          base_dt: str, 
                          period_div_code: str, 
                          time_cls_code: str = '', 
                          range: str = '', 
                          next_key: str = '') -> Dict[str, Any]:
        """
        국내주식 기간별 시세 (국내주식기간별시세, etc_day4)
        
        Args:
            stk_cd (str): 종목코드
            base_dt (str): 기준일자 (YYYYMMDD)
            period_div_code (str): 기간분류코드
                D: 일봉, W: 주봉, M: 월봉, Y: 년봉
            time_cls_code (str, optional): 시간분류코드 (분봉 요청시 입력)
                1: 1분, 3: 3분, 5: 5분, 10: 10분, 15: 15분, 30: 30분, 60: 60분
            range (str, optional): 조회범위 (기본값 100건)
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'base_dt': base_dt,
            'period_div_code': period_div_code
        }
        
        if time_cls_code:
            data['time_cls_code'] = time_cls_code
            
        if range:
            data['range'] = range
        
        return self.client.request_api('etc_day4', data, next_key=next_key)
    
    def get_domestic_tick_chart(self, 
                               stk_cd: str, 
                               base_dt: str, 
                               base_tm: str, 
                               inqr_cnt: str = '1', 
                               next_key: str = '') -> Dict[str, Any]:
        """
        국내주식 틱 차트 (domestic-stock-price-tick-kr, etc_time0)
        
        Args:
            stk_cd (str): 종목코드
            base_dt (str): 기준일자 (YYYYMMDD)
            base_tm (str): 기준시간 (HHMMSSsss)
            inqr_cnt (str, optional): 조회건수. 기본값은 '1'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'base_dt': base_dt,
            'base_tm': base_tm,
            'inqr_cnt': inqr_cnt
        }
        return self.client.request_api('etc_time0', data, next_key=next_key)
    
    def get_overseas_chart(self, 
                         stk_cd: str, 
                         ovrs_excg_cd: str, 
                         base_dt: str, 
                         period_div_code: str, 
                         inqr_cnt: str = '100', 
                         next_key: str = '') -> Dict[str, Any]:
        """
        해외주식 기간별 시세 (overseas-stock-price-daily, otc_day3)
        
        Args:
            stk_cd (str): 종목코드
            ovrs_excg_cd (str): 해외거래소코드
            base_dt (str): 기준일자 (YYYYMMDD)
            period_div_code (str): 기간분류코드
                D: 일봉, W: 주봉, M: 월봉, Y: 년봉
            inqr_cnt (str, optional): 조회건수. 기본값은 '100'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'base_dt': base_dt,
            'period_div_code': period_div_code,
            'inqr_cnt': inqr_cnt
        }
        return self.client.request_api('otc_day3', data, next_key=next_key)
    
    def get_indices_chart(self, 
                        idx_cd: str, 
                        base_dt: str, 
                        period_div_code: str, 
                        inqr_cnt: str = '100', 
                        next_key: str = '') -> Dict[str, Any]:
        """
        주요지수 기간별 시세 (indices-price-daily, etc_day5)
        
        Args:
            idx_cd (str): 지수코드
            base_dt (str): 기준일자 (YYYYMMDD)
            period_div_code (str): 기간분류코드
                D: 일봉, W: 주봉, M: 월봉, Y: 년봉
            inqr_cnt (str, optional): 조회건수. 기본값은 '100'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'idx_cd': idx_cd,
            'base_dt': base_dt,
            'period_div_code': period_div_code,
            'inqr_cnt': inqr_cnt
        }
        return self.client.request_api('etc_day5', data, next_key=next_key)
    
    def get_real_time_stock_price(self, 
                                stk_cd: str) -> Dict[str, Any]:
        """
        실시간 주식 시세 (domestic-stock-price-real-time, etc_time5)
        
        Args:
            stk_cd (str): 종목코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('etc_time5', data)
    
    def get_today_price_trend(self, 
                            stk_cd: str, 
                            base_tm: str = '', 
                            inqr_dvsn_cd: str = '00', 
                            next_key: str = '') -> Dict[str, Any]:
        """
        당일 주식 시세 추이 (domestic-stock-price-daily-trend, etc_time1)
        
        Args:
            stk_cd (str): 종목코드
            base_tm (str, optional): 기준시간 (HHMMSSsss). 기본값은 빈 문자열
            inqr_dvsn_cd (str, optional): 조회구분코드. 기본값은 '00'
                00: 전체, 01: 최근 5개만
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inqr_dvsn_cd': inqr_dvsn_cd
        }
        
        if base_tm:
            data['base_tm'] = base_tm
            
        return self.client.request_api('etc_time1', data, next_key=next_key)
    
    def get_daily_price_trend(self, 
                            stk_cd: str, 
                            base_dt: str = '', 
                            strt_dt: str = '', 
                            end_dt: str = '', 
                            inqr_dvsn_cd: str = '00', 
                            next_key: str = '') -> Dict[str, Any]:
        """
        일자별 주식 시세 추이 (domestic-stock-price-daily-trend, etc_day1)
        
        Args:
            stk_cd (str): 종목코드
            base_dt (str, optional): 기준일자 (YYYYMMDD). 기본값은 빈 문자열
            strt_dt (str, optional): 시작일자 (YYYYMMDD). 기본값은 빈 문자열
            end_dt (str, optional): 종료일자 (YYYYMMDD). 기본값은 빈 문자열
            inqr_dvsn_cd (str, optional): 조회구분코드. 기본값은 '00'
                00: 전체, 01: 전체 중 일자별 최고/최저 시간만 조회, 02: 전체 중 일자별 시가/종가만 조회
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inqr_dvsn_cd': inqr_dvsn_cd
        }
        
        if base_dt:
            data['base_dt'] = base_dt
            
        if strt_dt:
            data['strt_dt'] = strt_dt
            
        if end_dt:
            data['end_dt'] = end_dt
            
        return self.client.request_api('etc_day1', data, next_key=next_key)
    
    def get_today_time_price(self, 
                           stk_cd: str, 
                           base_tm: str, 
                           time_cls_code: str) -> Dict[str, Any]:
        """
        당일 분봉 차트 (domestic-stock-price-time, etc_time8)
        
        Args:
            stk_cd (str): 종목코드
            base_tm (str): 기준시간 (HHMM)
            time_cls_code (str): 시간분류코드
                1: 1분, 3: 3분, 5: 5분, 10: 10분, 15: 15분, 30: 30분, 60: 60분
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'base_tm': base_tm,
            'time_cls_code': time_cls_code
        }
        return self.client.request_api('etc_time8', data)
    
    def get_stock_completion_chart(self, 
                                 stk_cd: str, 
                                 strt_dt: str, 
                                 end_dt: str, 
                                 base_dt: str = '', 
                                 period_div_code: str = 'D', 
                                 time_cls_code: str = '',
                                 next_key: str = '') -> Dict[str, Any]:
        """
        국내주식 종합차트 (domestic-stock-charts, etc_time2)
        
        Args:
            stk_cd (str): 종목코드
            strt_dt (str): 시작일자 (YYYYMMDD)
            end_dt (str): 종료일자 (YYYYMMDD)
            base_dt (str, optional): 기준일자 (YYYYMMDD). 기본값은 빈 문자열
            period_div_code (str, optional): 기간분류코드. 기본값은 'D'
                D: 일봉, W: 주봉, M: 월봉, Y: 년봉
            time_cls_code (str, optional): 시간분류코드 (분봉 요청시 입력). 기본값은 빈 문자열
                1: 1분, 3: 3분, 5: 5분, 10: 10분, 15: 15분, 30: 30분, 60: 60분
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'strt_dt': strt_dt,
            'end_dt': end_dt,
            'period_div_code': period_div_code
        }
        
        if base_dt:
            data['base_dt'] = base_dt
            
        if time_cls_code:
            data['time_cls_code'] = time_cls_code
            
        return self.client.request_api('etc_time2', data, next_key=next_key)

    def get_domestic_stock_daily_chart(self,
                                      stk_cd: str,
                                      adj_prce: str = '1',
                                      inq_qt_char_1: str = '',
                                      inq_qt_char_2: str = '',
                                      next_key: str = '') -> Dict[str, Any]:
        """
        국내주식 일봉 데이터 (domestic-stock-daily-chart, etc_psbl_caland)
        
        Args:
            stk_cd (str): 종목 코드
            adj_prce (str, optional): 수정주가 여부. 기본값은 '1'
                '0': 수정주가 미반영, '1': 수정주가 반영
            inq_qt_char_1 (str, optional): 수량시작일자 (YYYYMMDD). 
                기본값 공백시 최근 데이터부터 조회
            inq_qt_char_2 (str, optional): 수량종료일자 (YYYYMMDD).
                기본값 공백시 조회개수로 조회
            next_key (str, optional): 연속조회키
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'adj_prce': adj_prce,
        }
        
        if inq_qt_char_1:
            data['inq_qt_char_1'] = inq_qt_char_1
            
        if inq_qt_char_2:
            data['inq_qt_char_2'] = inq_qt_char_2
            
        return self.client.request_api('etc_psbl_caland', data, next_key=next_key)
    
    def get_domestic_stock_minute_chart(self,
                                       stk_cd: str,
                                       inq_qty_div_cd: str = '1',
                                       adj_prce: str = '1',
                                       inq_begin_dt: str = '',
                                       inq_end_dt: str = '',
                                       inq_end_tm: str = '',
                                       next_key: str = '') -> Dict[str, Any]:
        """
        국내주식 분봉 데이터 (domestic-stock-minute-chart, etc_bdmst)
        
        Args:
            stk_cd (str): 종목 코드
            inq_qty_div_cd (str, optional): 조회분단위코드. 기본값은 '1'
                1: 1분, 3: 3분, 5: 5분, 10: 10분, 15: 15분, 30: 30분, 60: 60분
            adj_prce (str, optional): 수정주가 여부. 기본값은 '1'
                '0': 수정주가 미반영, '1': 수정주가 반영
            inq_begin_dt (str, optional): 조회시작일자 (YYYYMMDD)
            inq_end_dt (str, optional): 조회종료일자 (YYYYMMDD)
            inq_end_tm (str, optional): 조회종료시간 (HHMM)
            next_key (str, optional): 연속조회키
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inq_qty_div_cd': inq_qty_div_cd,
            'adj_prce': adj_prce,
        }
        
        if inq_begin_dt:
            data['inq_begin_dt'] = inq_begin_dt
            
        if inq_end_dt:
            data['inq_end_dt'] = inq_end_dt
            
        if inq_end_tm:
            data['inq_end_tm'] = inq_end_tm
            
        return self.client.request_api('etc_bdmst', data, next_key=next_key)
    
    def get_stock_price_by_date(self,
                              stk_cd: str,
                              base_dt: str,
                              ofl_hld_cls_cd: str = '',
                              stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        일자별 주식 시세 (stock-price-by-date, etc_cdnl1)
        
        Args:
            stk_cd (str): 종목 코드
            base_dt (str): 기준일자 (YYYYMMDD)
            ofl_hld_cls_cd (str, optional): 영업휴일구분코드. 기본값은 빈 문자열
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'base_dt': base_dt
        }
        
        if ofl_hld_cls_cd:
            data['ofl_hld_cls_cd'] = ofl_hld_cls_cd
            
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_cdnl1', data)
    
    def get_stock_price_by_time(self,
                              stk_cd: str,
                              base_dt: str = '',
                              stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        시간별 주식 시세 (stock-price-by-time, etc_thdi2)
        
        Args:
            stk_cd (str): 종목 코드
            base_dt (str, optional): 기준일자 (YYYYMMDD). 기본값은 빈 문자열
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        if base_dt:
            data['base_dt'] = base_dt
            
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_thdi2', data)
    
    def get_domestic_ticker_real_time(self,
                                    stk_cd: str) -> Dict[str, Any]:
        """
        국내주식 실시간 시세 조회 (domestic-ticker, etc_rtntc)
        
        Args:
            stk_cd (str): 종목 코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        return self.client.request_api('etc_rtntc', data)
    
    def get_overseas_stock_daily_chart(self,
                                     excd: str,
                                     symb: str,
                                     gubn: str = '0',
                                     nmin: str = '',
                                     cnt: str = '100',
                                     bgdt: str = '',
                                     eddt: str = '',
                                     cts: str = '') -> Dict[str, Any]:
        """
        해외주식 일봉 데이터 (overseas-stock-daily-chart, ovc_ccchart)
        
        Args:
            excd (str): 거래소코드
            symb (str): 종목코드
            gubn (str, optional): 구분. 기본값은 '0'
                0: 일, 1: 주, 2: 월
            nmin (str, optional): N분. 기본값은 빈 문자열
            cnt (str, optional): 요청건수. 기본값은 '100'
            bgdt (str, optional): 시작일자 (YYYYMMDD). 기본값은 빈 문자열
            eddt (str, optional): 종료일자 (YYYYMMDD). 기본값은 빈 문자열
            cts (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'excd': excd,
            'symb': symb,
            'gubn': gubn,
            'cnt': cnt
        }
        
        if nmin:
            data['nmin'] = nmin
            
        if bgdt:
            data['bgdt'] = bgdt
            
        if eddt:
            data['eddt'] = eddt
            
        return self.client.request_api('ovc_ccchart', data, next_key=cts)
    
    def get_overseas_ticker_real_time(self,
                                    excd: str,
                                    symb: str) -> Dict[str, Any]:
        """
        해외주식 실시간 시세 조회 (overseas-ticker, ovc_ccreal)
        
        Args:
            excd (str): 거래소코드
            symb (str): 종목코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'excd': excd,
            'symb': symb
        }
        
        return self.client.request_api('ovc_ccreal', data)
    
    def get_stock_depth(self,
                      stk_cd: str) -> Dict[str, Any]:
        """
        주식 호가 조회 (stock-depth, etc_askp)
        
        Args:
            stk_cd (str): 종목 코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        return self.client.request_api('etc_askp', data)
    
    def get_index_daily_chart(self,
                            stk_cd: str,
                            inq_qt_char_1: str = '',
                            inq_qt_char_2: str = '',
                            next_key: str = '') -> Dict[str, Any]:
        """
        지수 일봉 데이터 (index-daily-chart, etc_isu_cdnl)
        
        Args:
            stk_cd (str): 종목 코드
            inq_qt_char_1 (str, optional): 수량시작일자 (YYYYMMDD). 
                기본값 공백시 최근 데이터부터 조회
            inq_qt_char_2 (str, optional): 수량종료일자 (YYYYMMDD).
                기본값 공백시 조회개수로 조회
            next_key (str, optional): 연속조회키
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        if inq_qt_char_1:
            data['inq_qt_char_1'] = inq_qt_char_1
            
        if inq_qt_char_2:
            data['inq_qt_char_2'] = inq_qt_char_2
            
        return self.client.request_api('etc_isu_cdnl', data, next_key=next_key)
    
    def get_stock_current_price(self,
                              stk_cd: str) -> Dict[str, Any]:
        """
        주식 현재가 조회 (stock-current-price, etc_csstoc)
        
        Args:
            stk_cd (str): 종목 코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        return self.client.request_api('etc_csstoc', data) 