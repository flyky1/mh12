#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 차트 데이터 조회 모듈

이 모듈은 키움 OpenAPI를 통해 국내 및 해외 주식 차트 데이터를 조회하는 기능을 제공합니다.
"""

import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional

from .base import APIBase


logger = logging.getLogger(__name__)


class ChartAPI(APIBase):
    """
    차트 데이터 조회 API 클래스
    
    이 클래스는 국내 및 해외 주식의 차트 데이터를 조회하는 메서드를 제공합니다.
    - 일봉 데이터 조회
    - 주봉 데이터 조회
    - 월봉 데이터 조회
    - 분봉 데이터 조회
    - 틱 데이터 조회 (국내주식)
    """
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        """
        ChartAPI 클래스 초기화
        
        Args:
            base_url (str): API 기본 URL
            headers (Dict[str, str]): 요청 헤더
        """
        super().__init__(base_url, headers)
    
    # 국내 주식 차트 API
    
    def get_domestic_daily(self, 
                           stock_code: str, 
                           start_date: str, 
                           end_date: str, 
                           period_division: str = "D") -> Dict[str, Any]:
        """
        국내 주식 일봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드 (예: '005930' for 삼성전자)
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            period_division (str): 기간분류코드 (D:일봉, W:주봉, M:월봉)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 주식
            "FID_INPUT_ISCD": stock_code,  # 종목코드
            "FID_INPUT_DATE_1": start_date,  # 조회시작일자
            "FID_INPUT_DATE_2": end_date,  # 조회종료일자
            "FID_PERIOD_DIV_CODE": period_division,  # 기간분류코드
            "FID_ORG_ADJ_PRC": "0"  # 수정주가 반영 여부
        }
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    def get_domestic_weekly(self, 
                            stock_code: str, 
                            start_date: str, 
                            end_date: str) -> Dict[str, Any]:
        """
        국내 주식 주봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.get_domestic_daily(stock_code, start_date, end_date, "W")
    
    def get_domestic_monthly(self, 
                             stock_code: str, 
                             start_date: str, 
                             end_date: str) -> Dict[str, Any]:
        """
        국내 주식 월봉 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_date (str): 조회 시작일 (YYYYMMDD)
            end_date (str): 조회 종료일 (YYYYMMDD)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        return self.get_domestic_daily(stock_code, start_date, end_date, "M")
    
    def get_domestic_minute(self, 
                            stock_code: str, 
                            start_time: str, 
                            end_time: str, 
                            time_interval: str = "1") -> Dict[str, Any]:
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
        path = "uapi/domestic-stock/v1/quotations/inquire-time-itemchartprice"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 주식
            "FID_INPUT_ISCD": stock_code,  # 종목코드
            "FID_INPUT_DATE_1": start_time[:8],  # 조회시작일자
            "FID_INPUT_DATE_2": end_time[:8],  # 조회종료일자
            "FID_INPUT_HOUR_1": start_time[8:12],  # 조회시작시간
            "FID_INPUT_HOUR_2": end_time[8:12],  # 조회종료시간
            "FID_PERIOD_DIV_CODE": time_interval,  # 시간간격
            "FID_ORG_ADJ_PRC": "0"  # 수정주가 반영 여부
        }
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    def get_domestic_tick(self, 
                          stock_code: str, 
                          start_time: str, 
                          end_time: str) -> Dict[str, Any]:
        """
        국내 주식 틱 차트 데이터 조회
        
        Args:
            stock_code (str): 종목 코드
            start_time (str): 조회 시작시간 (YYYYMMDDHHMMSS)
            end_time (str): 조회 종료시간 (YYYYMMDDHHMMSS)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/domestic-stock/v1/quotations/inquire-tick-itemchartprice"
        
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",  # 주식
            "FID_INPUT_ISCD": stock_code,  # 종목코드
            "FID_INPUT_DATE_1": start_time[:8],  # 조회시작일자
            "FID_INPUT_DATE_2": end_time[:8],  # 조회종료일자
            "FID_INPUT_HOUR_1": start_time[8:12],  # 조회시작시간
            "FID_INPUT_HOUR_2": end_time[8:12],  # 조회종료시간
            "FID_ORG_ADJ_PRC": "0"  # 수정주가 반영 여부
        }
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    # 해외 주식 차트 API
    
    def get_overseas_daily(self, 
                           bass_code: str, 
                           exch_cd: str, 
                           inq_strt_dd: str, 
                           inq_end_dd: str, 
                           adj_clos: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 일봉 차트 데이터 조회
        
        Args:
            bass_code (str): 기초코드 (예: 'AAPL' for 애플)
            exch_cd (str): 거래소코드 (NAS, NYSE, AMEX 등)
            inq_strt_dd (str): 조회 시작일 (YYYYMMDD)
            inq_end_dd (str): 조회 종료일 (YYYYMMDD)
            adj_clos (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/overseas-price/v1/quotations/dailyprice"
        
        params = {
            "AUTH": "",
            "BASS_ICS_EXCD": exch_cd,  # 거래소 코드
            "BASS_CODE": bass_code,  # 종목 코드
            "INQY_STRT_DT": inq_strt_dd,  # 조회 시작일
            "INQY_END_DT": inq_end_dd,  # 조회 종료일
        }
        
        if adj_clos:
            params["ADJ_CLOS"] = adj_clos
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    def get_overseas_weekly(self, 
                            bass_code: str, 
                            exch_cd: str, 
                            inq_strt_dd: str, 
                            inq_end_dd: str, 
                            adj_clos: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 주봉 차트 데이터 조회
        
        Args:
            bass_code (str): 기초코드
            exch_cd (str): 거래소코드
            inq_strt_dd (str): 조회 시작일 (YYYYMMDD)
            inq_end_dd (str): 조회 종료일 (YYYYMMDD)
            adj_clos (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/overseas-price/v1/quotations/weeklyprice"
        
        params = {
            "AUTH": "",
            "BASS_ICSN_EXCD": exch_cd,  # 거래소 코드
            "BASS_CODE": bass_code,  # 종목 코드
            "INQY_STRT_DT": inq_strt_dd,  # 조회 시작일
            "INQY_END_DT": inq_end_dd,  # 조회 종료일
        }
        
        if adj_clos:
            params["ADJ_CLOS"] = adj_clos
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    def get_overseas_monthly(self, 
                             bass_code: str, 
                             exch_cd: str, 
                             inq_strt_dd: str, 
                             inq_end_dd: str, 
                             adj_clos: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 월봉 차트 데이터 조회
        
        Args:
            bass_code (str): 기초코드
            exch_cd (str): 거래소코드
            inq_strt_dd (str): 조회 시작일 (YYYYMMDD)
            inq_end_dd (str): 조회 종료일 (YYYYMMDD)
            adj_clos (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/overseas-price/v1/quotations/monthlyprice"
        
        params = {
            "AUTH": "",
            "BASS_ICSN_EXCD": exch_cd,  # 거래소 코드
            "BASS_CODE": bass_code,  # 종목 코드
            "INQY_STRT_DT": inq_strt_dd,  # 조회 시작일
            "INQY_END_DT": inq_end_dd,  # 조회 종료일
        }
        
        if adj_clos:
            params["ADJ_CLOS"] = adj_clos
        
        url = urljoin(self.base_url, path)
        return self._get(url, params)
    
    def get_overseas_minute(self, 
                            bass_code: str, 
                            exch_cd: str, 
                            inq_strt_dtm: str, 
                            inq_end_dtm: str, 
                            time_interval_cd: str = "5",
                            adj_clos: Optional[str] = None) -> Dict[str, Any]:
        """
        해외 주식 분봉 차트 데이터 조회
        
        Args:
            bass_code (str): 기초코드
            exch_cd (str): 거래소코드
            inq_strt_dtm (str): 조회 시작일시 (YYYYMMDDHHmmss)
            inq_end_dtm (str): 조회 종료일시 (YYYYMMDDHHmmss)
            time_interval_cd (str): 시간간격 (1, 3, 5, 10, 15, 30, 60 분)
            adj_clos (str, optional): 수정주가 여부 (0: 원주가, 1: 수정주가)
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        path = "uapi/overseas-price/v1/quotations/minuteprice"
        
        params = {
            "AUTH": "",
            "BASS_ICSN_EXCD": exch_cd,  # 거래소 코드
            "BASS_CODE": bass_code,  # 종목 코드
            "INQY_STRT_DTM": inq_strt_dtm,  # 조회 시작일시
            "INQY_END_DTM": inq_end_dtm,  # 조회 종료일시
            "CSMN_INTF_CD": time_interval_cd  # 시간간격
        }
        
        if adj_clos:
            params["ADJ_CLOS"] = adj_clos
        
        url = urljoin(self.base_url, path)
        return self._get(url, params) 