"""
ELW 모듈 (ELW Module)

이 모듈은 키움증권 OpenAPI를 통해 ELW(주식워런트증권) 관련 정보를 조회하는 기능을 제공합니다.
주요 기능:
- ELW 기본 정보 조회
- ELW 시세 정보 조회
- ELW 민감도 지표 조회 (델타, 감마, 세타, 베가 등)
- ELW 잔존일수/배당락 조회
- ELW 발행회사별 정보 조회
"""

import logging
from urllib.parse import urljoin
from typing import Dict, Any, Optional, List

from .base import APIBase

class ELWAPI(APIBase):
    """
    ELW API 클래스

    이 클래스는 ELW(주식워런트증권) 관련 정보를 조회하는 API를 제공합니다.
    """

    def get_elw_info(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 기본 정보 조회 (kf10001)

        Args:
            symbol (str): ELW 종목 코드

        Returns:
            Dict[str, Any]: ELW 기본 정보
                - code (str): 종목코드
                - name (str): 종목명
                - base_asset (str): 기초자산
                - exercise_price (float): 행사가격
                - exercise_ratio (float): 전환비율
                - exercise_date (str): 만기일
                - remain_days (int): 잔존일수
                - issuer (str): 발행회사
                - right_type (str): 권리유형 (콜/풋)
                - issue_date (str): 발행일
                - issue_amount (int): 발행규모
                - market_price (float): 현재가
                - iv (float): 내재변동성
                - delta (float): 델타
                - gamma (float): 감마
                - theta (float): 세타
                - vega (float): 베가
        """
        url = "uapi/domestic-stock/v1/quotations/elw-info"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_elw_price(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 시세 정보 조회 (kf10002)

        Args:
            symbol (str): ELW 종목 코드

        Returns:
            Dict[str, Any]: ELW 시세 정보
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
                - ask_price (float): 매도호가
                - bid_price (float): 매수호가
                - ask_volume (int): 매도호가수량
                - bid_volume (int): 매수호가수량
                - base_asset_price (float): 기초자산가격
                - base_asset_change (float): 기초자산전일대비
                - premium (float): 프리미엄
                - intrinsic_value (float): 내재가치
                - time_value (float): 시간가치
        """
        url = "uapi/domestic-stock/v1/quotations/elw-price"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_elw_remain_days(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 잔존일수/배당락 조회 (kf10003)

        Args:
            symbol (str): ELW 종목 코드

        Returns:
            Dict[str, Any]: ELW 잔존일수 및 배당락 정보
                - code (str): 종목코드
                - name (str): 종목명
                - exercise_date (str): 만기일
                - remain_days (int): 잔존일수
                - dividend_ex_date (str): 배당락일
                - dividend_amount (float): 배당금액
                - dividend_impact (float): 배당영향
        """
        url = "uapi/domestic-stock/v1/quotations/elw-remain-days"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISCD": symbol,
        }
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_elw_by_issuer(self, issuer_code: str, base_asset_code: Optional[str] = None) -> Dict[str, Any]:
        """
        ELW 발행회사별 정보 조회 (kf10004)

        Args:
            issuer_code (str): 발행회사 코드
            base_asset_code (str, optional): 기초자산 코드. None이면 모든 기초자산

        Returns:
            Dict[str, Any]: 발행회사별 ELW 목록
                - issuer (str): 발행회사명
                - elw_list (List[Dict]): ELW 목록
                    - code (str): 종목코드
                    - name (str): 종목명
                    - base_asset (str): 기초자산
                    - right_type (str): 권리유형
                    - exercise_price (float): 행사가격
                    - remain_days (int): 잔존일수
                    - price (float): 현재가
                    - change_rate (float): 등락률
                    - volume (int): 거래량
        """
        url = "uapi/domestic-stock/v1/quotations/elw-by-issuer"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_ISSU_CD": issuer_code,
        }
        
        if base_asset_code:
            params["FID_INPUT_BASS_ASST_CD"] = base_asset_code
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json()
    
    def get_elw_sensitivity(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 민감도 지표 조회 (ka10050)

        Args:
            symbol (str): ELW 종목 코드

        Returns:
            Dict[str, Any]: ELW 민감도 지표 정보
                - code (str): 종목코드
                - name (str): 종목명
                - sensitivity_list (List[Dict]): 민감도 지표 목록
                    - time (str): 시간
                    - price (float): 현재가
                    - theoretical_price (float): 이론가
                    - iv (float): 내재변동성
                    - delta (float): 델타
                    - gamma (float): 감마
                    - theta (float): 세타
                    - vega (float): 베가
                    - rho (float): 로
                    - lp (float): LP
        """
        url = "api/dostk/elw"
        headers = self._get_headers()
        headers["api-id"] = "ka10050"
        
        data = {
            "stk_cd": symbol
        }
        
        res = self.request_post(url, headers=headers, json=data)
        return res.json()
    
    def get_elw_daily_sensitivity(self, symbol: str) -> Dict[str, Any]:
        """
        ELW 일별 민감도 지표 조회 (ka10048)

        Args:
            symbol (str): ELW 종목 코드

        Returns:
            Dict[str, Any]: ELW 일별 민감도 지표 정보
                - code (str): 종목코드
                - name (str): 종목명
                - daily_sensitivity_list (List[Dict]): 일별 민감도 지표 목록
                    - date (str): 일자
                    - iv (float): 내재변동성
                    - delta (float): 델타
                    - gamma (float): 감마
                    - theta (float): 세타
                    - vega (float): 베가
                    - rho (float): 로
                    - lp (float): LP
        """
        url = "api/dostk/elw"
        headers = self._get_headers()
        headers["api-id"] = "ka10048"
        
        data = {
            "stk_cd": symbol
        }
        
        res = self.request_post(url, headers=headers, json=data)
        return res.json()
    
    def get_elw_price_change(self, 
                            change_type: str = "1", 
                            time_type: str = "2",
                            time_value: str = "1",
                            volume_type: str = "0",
                            issuer_code: str = "000000000000",
                            base_asset_code: str = "000000000000") -> Dict[str, Any]:
        """
        ELW 가격 급등락 조회 (ka30001)

        Args:
            change_type (str): 등락구분 (1: 급등, 2: 급락)
            time_type (str): 시간구분 (1: 분전, 2: 일전)
            time_value (str): 시간 값 (분 또는 일, 예: 1, 3, 5)
            volume_type (str): 거래량구분 (0: 전체, 10: 만주이상, 50: 5만주이상, 100: 10만주이상 등)
            issuer_code (str): 발행사코드 (전체: 000000000000)
            base_asset_code (str): 기초자산코드 (전체: 000000000000)

        Returns:
            Dict[str, Any]: ELW 가격 급등락 목록
                - elw_list (List[Dict]): ELW 목록
                    - code (str): 종목코드
                    - name (str): 종목명
                    - price (float): 현재가
                    - change_rate (float): 등락률
                    - volume (int): 거래량
                    - base_asset (str): 기초자산
                    - issuer (str): 발행회사
        """
        url = "api/dostk/elw"
        headers = self._get_headers()
        headers["api-id"] = "ka30001"
        
        data = {
            "flu_tp": change_type,
            "tm_tp": time_type,
            "tm": time_value,
            "trde_qty_tp": volume_type,
            "isscomp_cd": issuer_code,
            "bsis_aset_cd": base_asset_code
        }
        
        res = self.request_post(url, headers=headers, json=data)
        return res.json()
    
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
                - elw_list (List[Dict]): ELW 목록
                    - code (str): 종목코드
                    - name (str): 종목명
                    - base_asset (str): 기초자산
                    - right_type (str): 권리유형
                    - exercise_price (float): 행사가격
                    - exercise_date (str): 만기일
                    - issuer (str): 발행회사
        """
        url = "uapi/domestic-stock/v1/quotations/elw-search"
        headers = self._get_headers()
        params = {
            "FID_COND_MRKT_DIV_CODE": "J",
            "FID_INPUT_SEARCH_WORD": query,
        }
        
        if right_type:
            params["FID_INPUT_RIGHT_TYPE"] = right_type
        
        if base_asset_code:
            params["FID_INPUT_BASS_ASST_CD"] = base_asset_code
            
        if issuer_code:
            params["FID_INPUT_ISSU_CD"] = issuer_code
        
        res = self.request_get(url, headers=headers, params=params)
        return res.json() 