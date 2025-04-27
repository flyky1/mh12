"""
키움증권 종목정보 관련 API 모듈
"""

from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from ..client import KiwoomClient


class StockAPI:
    """키움증권 종목정보 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        종목정보 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def get_stock_basic_info(self,
                           stk_cd: str) -> Dict[str, Any]:
        """
        종목 기본정보 조회 (stock-basic-info, etc_issue)
        
        Args:
            stk_cd (str): 종목 코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        return self.client.request_api('etc_issue', data)
    
    def get_stock_meta_info(self,
                          stk_cd: str,
                          stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        종목 메타정보 조회 (stock-meta-info, etc_misi)
        
        Args:
            stk_cd (str): 종목 코드
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd
        }
        
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_misi', data)
    
    def get_stock_list(self,
                     inq_cnd_dvsn_cd: str = '1',
                     inq_cnd_dvsn_val: str = '') -> Dict[str, Any]:
        """
        종목 목록 조회 (stock-list, etc_sangsi)
        
        Args:
            inq_cnd_dvsn_cd (str, optional): 조회조건구분코드. 기본값은 '1'
                '1': 시장구분, '2': 업종구분, '6': 상장주식수 '7': 자본금 '8': 시가총액 등
            inq_cnd_dvsn_val (str, optional): 조회조건구분값. 기본값은 빈 문자열
                inq_cnd_dvsn_cd가 '1'인 경우: '0': 전체, '1': 코스피, '2': 코스닥 등
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'inq_cnd_dvsn_cd': inq_cnd_dvsn_cd
        }
        
        if inq_cnd_dvsn_val:
            data['inq_cnd_dvsn_val'] = inq_cnd_dvsn_val
            
        return self.client.request_api('etc_sangsi', data)
    
    def get_delisted_stocks(self,
                          inq_dt_strt: str = '',
                          inq_dt_end: str = '',
                          stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        상장폐지 종목 조회 (delisted-stocks, etc_sanof)
        
        Args:
            inq_dt_strt (str, optional): 조회시작일자 (YYYYMMDD). 기본값은 빈 문자열
            inq_dt_end (str, optional): 조회종료일자 (YYYYMMDD). 기본값은 빈 문자열
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        
        if inq_dt_strt:
            data['inq_dt_strt'] = inq_dt_strt
            
        if inq_dt_end:
            data['inq_dt_end'] = inq_dt_end
            
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_sanof', data)
    
    def get_suspended_stocks(self,
                           inq_tp_cd: str = '00',
                           stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        거래정지 종목 조회 (suspended-stocks, etc_sangf)
        
        Args:
            inq_tp_cd (str, optional): 조회구분코드. 기본값은 '00'
                '00': 전체, '01': 거래정지, '02': 단기과열, '03': 투자유의 등
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'inq_tp_cd': inq_tp_cd
        }
        
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_sangf', data)
    
    def get_watch_stocks(self,
                       stk_mkt_cd: str = '') -> Dict[str, Any]:
        """
        관리종목 조회 (watch-stocks, etc_sangg)
        
        Args:
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_sangg', data)
    
    def get_stock_disclosure(self,
                           inq_strt_dt: str = '',
                           inq_end_dt: str = '',
                           stk_cd: str = '',
                           stk_nm: str = '',
                           opn_tp_cd: str = '',
                           dsc_cd: str = '',
                           next_key: str = '') -> Dict[str, Any]:
        """
        종목 공시정보 조회 (stock-disclosure, etc_sangi)
        
        Args:
            inq_strt_dt (str, optional): 조회시작일자 (YYYYMMDD). 기본값은 빈 문자열
            inq_end_dt (str, optional): 조회종료일자 (YYYYMMDD). 기본값은 빈 문자열
            stk_cd (str, optional): 종목 코드. 기본값은 빈 문자열
            stk_nm (str, optional): 종목명. 기본값은 빈 문자열
            opn_tp_cd (str, optional): 공시구분코드. 기본값은 빈 문자열
            dsc_cd (str, optional): 공시코드. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        
        if inq_strt_dt:
            data['inq_strt_dt'] = inq_strt_dt
            
        if inq_end_dt:
            data['inq_end_dt'] = inq_end_dt
            
        if stk_cd:
            data['stk_cd'] = stk_cd
            
        if stk_nm:
            data['stk_nm'] = stk_nm
            
        if opn_tp_cd:
            data['opn_tp_cd'] = opn_tp_cd
            
        if dsc_cd:
            data['dsc_cd'] = dsc_cd
            
        return self.client.request_api('etc_sangi', data, next_key=next_key)
    
    def get_stock_symbol_search(self,
                              stk_ctr_no: str = '',
                              stk_nm: str = '',
                              stk_tp_cd_1: str = 'Y',
                              stk_tp_cd_2: str = 'Y',
                              stk_tp_cd_3: str = 'Y',
                              stk_tp_cd_4: str = 'Y',
                              next_key: str = '') -> Dict[str, Any]:
        """
        종목 코드/명 조회 (stock-symbol-search, etc_sangj)
        
        Args:
            stk_ctr_no (str, optional): 종목 코드. 기본값은 빈 문자열
            stk_nm (str, optional): 종목명. 기본값은 빈 문자열
            stk_tp_cd_1 (str, optional): 주식구분코드1(코스피). 기본값은 'Y'
            stk_tp_cd_2 (str, optional): 주식구분코드2(코스닥). 기본값은 'Y'
            stk_tp_cd_3 (str, optional): 주식구분코드3(ETF). 기본값은 'Y'
            stk_tp_cd_4 (str, optional): 주식구분코드4(ELW). 기본값은 'Y'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_tp_cd_1': stk_tp_cd_1,
            'stk_tp_cd_2': stk_tp_cd_2,
            'stk_tp_cd_3': stk_tp_cd_3,
            'stk_tp_cd_4': stk_tp_cd_4
        }
        
        if stk_ctr_no:
            data['stk_ctr_no'] = stk_ctr_no
            
        if stk_nm:
            data['stk_nm'] = stk_nm
            
        return self.client.request_api('etc_sangj', data, next_key=next_key)
    
    def get_overseas_stock_symbol_search(self,
                                       excd: str = '',
                                       symb: str = '',
                                       name: str = '',
                                       next_key: str = '') -> Dict[str, Any]:
        """
        해외종목 코드/명 조회 (overseas-stock-symbol-search, ovc_ccsymbolic)
        
        Args:
            excd (str, optional): 거래소코드. 기본값은 빈 문자열
            symb (str, optional): 종목코드. 기본값은 빈 문자열
            name (str, optional): 종목명. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {}
        
        if excd:
            data['excd'] = excd
            
        if symb:
            data['symb'] = symb
            
        if name:
            data['name'] = name
            
        return self.client.request_api('ovc_ccsymbolic', data, next_key=next_key)
    
    def get_stock_financial_info(self,
                               stk_cd: str,
                               fin_gubun: str = '0',
                               next_key: str = '') -> Dict[str, Any]:
        """
        종목 재무정보 조회 (stock-financial-info, etc_sangk)
        
        Args:
            stk_cd (str): 종목 코드
            fin_gubun (str, optional): 재무구분. 기본값은 '0'
                '0': 전체, '1': 포괄손익계산서, '2': 재무상태표, '3': 현금흐름표
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'fin_gubun': fin_gubun
        }
        
        return self.client.request_api('etc_sangk', data, next_key=next_key)
    
    def get_stock_investor_trend(self,
                               stk_cd: str,
                               inq_strt_dt: str,
                               inq_end_dt: str,
                               stk_mkt_cd: str = '',
                               next_key: str = '') -> Dict[str, Any]:
        """
        투자자별 동향 조회 (stock-investor-trend, etc_sangm)
        
        Args:
            stk_cd (str): 종목 코드
            inq_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inq_end_dt (str): 조회종료일자 (YYYYMMDD)
            stk_mkt_cd (str, optional): 주식시장코드. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'stk_cd': stk_cd,
            'inq_strt_dt': inq_strt_dt,
            'inq_end_dt': inq_end_dt
        }
        
        if stk_mkt_cd:
            data['stk_mkt_cd'] = stk_mkt_cd
            
        return self.client.request_api('etc_sangm', data, next_key=next_key)
    
    def get_overseas_stock_info(self,
                              excd: str,
                              symb: str) -> Dict[str, Any]:
        """
        해외종목 기본정보 조회 (overseas-stock-info, ovc_ccbasic)
        
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
        
        return self.client.request_api('ovc_ccbasic', data) 