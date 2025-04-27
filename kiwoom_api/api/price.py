"""
키움증권 시세 API 모듈
"""

from typing import Dict, Any, Optional

from ..client import KiwoomClient


class PriceAPI:
    """키움증권 시세 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        시세 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def get_current_price(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        현재가 조회 (ks10001)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10001', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_askbid_price(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        호가 조회 (ks10002)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10002', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_investor_breakdown(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        투자자별 매매동향 (ks10003)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10003', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_daily_price(self, 
                      stk_cd: str, 
                      inquiry_type: str = 'D', 
                      cont_yn: str = 'N', 
                      next_key: str = '') -> Dict[str, Any]:
        """
        일별 시세 (ks10004)
        
        Args:
            stk_cd (str): 종목코드
            inquiry_type (str, optional): 조회구분. 기본값은 'D' (일봉)
                D: 일봉, W: 주봉, M: 월봉
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inquiry_tp': inquiry_type
        }
        return self.client.request_api('ks10004', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_minute_price(self, 
                       stk_cd: str, 
                       inquiry_type: str = '1', 
                       cont_yn: str = 'N', 
                       next_key: str = '') -> Dict[str, Any]:
        """
        분봉 시세 (ks10005)
        
        Args:
            stk_cd (str): 종목코드
            inquiry_type (str, optional): 조회구분. 기본값은 '1' (1분봉)
                1: 1분봉, 3: 3분봉, 5: 5분봉, 10: 10분봉, 15: 15분봉, 30: 30분봉, 60: 60분봉
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inquiry_tp': inquiry_type
        }
        return self.client.request_api('ks10005', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_tick_price(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        틱 시세 (ks10006)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10006', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_time_price(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        시간대별시세 (ks10007)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10007', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_trade_history(self, stk_cd: str, cont_yn: str = 'N', next_key: str = '') -> Dict[str, Any]:
        """
        거래내역 (ks10015)
        
        Args:
            stk_cd (str): 종목코드
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        return self.client.request_api('ks10015', data, cont_yn=cont_yn, next_key=next_key) 