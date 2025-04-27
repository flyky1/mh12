"""
키움증권 순위정보 API 모듈
"""

from typing import Dict, Any, Optional

from ..client import KiwoomClient


class RankingAPI:
    """키움증권 순위정보 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        순위정보 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def get_trade_amount_rank(self, 
                            mrkt_tp: str = '000', 
                            mang_stk_incls: str = '1',
                            stex_tp: str = '3',
                            cont_yn: str = 'N', 
                            next_key: str = '') -> Dict[str, Any]:
        """
        거래대금상위요청 (ki10001)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10001', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_trade_volume_rank(self, 
                            mrkt_tp: str = '000', 
                            mang_stk_incls: str = '1',
                            stex_tp: str = '3',
                            cont_yn: str = 'N', 
                            next_key: str = '') -> Dict[str, Any]:
        """
        거래량상위요청 (ki10002)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10002', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_market_cap_rank(self, 
                          mrkt_tp: str = '000', 
                          mang_stk_incls: str = '1',
                          stex_tp: str = '3',
                          cont_yn: str = 'N', 
                          next_key: str = '') -> Dict[str, Any]:
        """
        시가총액상위요청 (ki10003)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10003', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_ask_volume_rank(self, 
                          mrkt_tp: str = '000', 
                          mang_stk_incls: str = '1',
                          stex_tp: str = '3',
                          cont_yn: str = 'N', 
                          next_key: str = '') -> Dict[str, Any]:
        """
        호가잔량상위요청 (ki10004)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10004', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_increase_rank(self, 
                        mrkt_tp: str = '000', 
                        mang_stk_incls: str = '1',
                        stex_tp: str = '3',
                        cont_yn: str = 'N', 
                        next_key: str = '') -> Dict[str, Any]:
        """
        상승률상위요청 (ki10005)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10005', data, cont_yn=cont_yn, next_key=next_key)
    
    def get_decrease_rank(self, 
                        mrkt_tp: str = '000', 
                        mang_stk_incls: str = '1',
                        stex_tp: str = '3',
                        cont_yn: str = 'N', 
                        next_key: str = '') -> Dict[str, Any]:
        """
        하락률상위요청 (ki10006)
        
        Args:
            mrkt_tp (str, optional): 시장구분. 기본값은 '000'
                000: 전체, 001: 코스피, 101: 코스닥
            mang_stk_incls (str, optional): 관리종목포함. 기본값은 '1'
                0: 관리종목 미포함, 1: 관리종목 포함
            stex_tp (str, optional): 거래소구분. 기본값은 '3'
                1: KRX, 2: NXT, 3: 통합
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'mrkt_tp': mrkt_tp,
            'mang_stk_incls': mang_stk_incls,
            'stex_tp': stex_tp
        }
        return self.client.request_api('ki10006', data, cont_yn=cont_yn, next_key=next_key) 