"""
키움증권 국내시장 지수 API 모듈
"""

from typing import Dict, Any, Optional

from ..client import KiwoomClient


class IndexAPI:
    """키움증권 국내시장 지수 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        국내시장 지수 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def get_kospi_index(self, 
                       idx_cd: str = '0001', 
                       inq_tp: str = '1', 
                       cont_yn: str = 'N', 
                       next_key: str = '') -> Dict[str, Any]:
        """
        코스피 지수요청 (kr10001)
        
        Args:
            idx_cd (str, optional): 지수코드. 기본값은 '0001'
            inq_tp (str, optional): 조회구분. 기본값은 '1'
                1: 기간별, 2: 일별
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'idx_cd': idx_cd,
            'inq_tp': inq_tp
        }
        return self.client.request_api('kr10001', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_kosdaq_index(self, 
                        idx_cd: str = '1001', 
                        inq_tp: str = '1', 
                        cont_yn: str = 'N', 
                        next_key: str = '') -> Dict[str, Any]:
        """
        코스닥 지수요청 (kr10002)
        
        Args:
            idx_cd (str, optional): 지수코드. 기본값은 '1001'
            inq_tp (str, optional): 조회구분. 기본값은 '1'
                1: 기간별, 2: 일별
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'idx_cd': idx_cd,
            'inq_tp': inq_tp
        }
        return self.client.request_api('kr10002', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_kospi_market_info(self, 
                            cont_yn: str = 'N', 
                            next_key: str = '') -> Dict[str, Any]:
        """
        코스피 거래정보 요청 (kr10003)
        
        Args:
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        return self.client.request_api('kr10003', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_kosdaq_market_info(self, 
                             cont_yn: str = 'N', 
                             next_key: str = '') -> Dict[str, Any]:
        """
        코스닥 거래정보 요청 (kr10004)
        
        Args:
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        return self.client.request_api('kr10004', data, cont_yn=cont_yn, next_key=next_key) 