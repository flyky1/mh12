"""
키움증권 계좌 관련 API 모듈
"""

from typing import Dict, Any, Optional, List

from ..client import KiwoomClient


class AccountAPI:
    """키움증권 계좌 정보 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        계좌 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def get_account_balance(self, 
                          cano: str, 
                          acnt_prdt_cd: str, 
                          inqr_dvsn_cd: str = '00', 
                          bal_dvsn_cd: str = '01', 
                          next_key: str = '') -> Dict[str, Any]:
        """
        계좌 잔고 조회 (domestic-stock-balance, etc_psbl_amt2)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            inqr_dvsn_cd (str, optional): 조회구분코드. 기본값은 '00'
                00: 전체, 01: 주식, 02: 채권 등
            bal_dvsn_cd (str, optional): 잔고구분코드. 기본값은 '01'
                01: 유가증권잔고, 02: 신용잔고 등
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'inqr_dvsn_cd': inqr_dvsn_cd,
            'bal_dvsn_cd': bal_dvsn_cd
        }
        return self.client.request_api('etc_psbl_amt2', data, next_key=next_key)
    
    def get_account_info(self, 
                       cano: str, 
                       acnt_prdt_cd: str, 
                       acnt_inqr_dvsn_cd: str = '0') -> Dict[str, Any]:
        """
        계좌 상세정보 조회 (account-info, etc_crdt_bal)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            acnt_inqr_dvsn_cd (str, optional): 계좌조회구분코드. 기본값은 '0'
                0: 전체, 1: 일반, 2: 신용 등
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'acnt_inqr_dvsn_cd': acnt_inqr_dvsn_cd
        }
        return self.client.request_api('etc_crdt_bal', data)
    
    def get_deposit(self, 
                  cano: str, 
                  acnt_prdt_cd: str, 
                  inqr_dvsn: str = '2', 
                  next_key: str = '') -> Dict[str, Any]:
        """
        계좌 예수금 조회 (deposit-detail, etc_cma_dt)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            inqr_dvsn (str, optional): 조회구분. 기본값은 '2'
                1: 예수금총합, 2: 예수금상세
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'inqr_dvsn': inqr_dvsn
        }
        return self.client.request_api('etc_cma_dt', data, next_key=next_key)
    
    def get_account_profit_loss(self, 
                              cano: str, 
                              acnt_prdt_cd: str, 
                              inqr_dvsn_cd: str = '00', 
                              next_key: str = '') -> Dict[str, Any]:
        """
        계좌 손익현황 조회 (domestic-stock-profit-loss, etc_psbl_amt4)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            inqr_dvsn_cd (str, optional): 조회구분코드. 기본값은 '00'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'inqr_dvsn_cd': inqr_dvsn_cd
        }
        return self.client.request_api('etc_psbl_amt4', data, next_key=next_key)
    
    def get_credit_info(self, 
                      cano: str, 
                      acnt_prdt_cd: str) -> Dict[str, Any]:
        """
        계좌 신용정보 조회 (credit-info, etc_crdt_ord)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd
        }
        return self.client.request_api('etc_crdt_ord', data)
    
    def get_overseas_account_balance(self, 
                                   cano: str, 
                                   acnt_prdt_cd: str, 
                                   ovrs_excg_cd: str, 
                                   curr_cd: str, 
                                   next_key: str = '') -> Dict[str, Any]:
        """
        해외주식 계좌 잔고 조회 (overseas-stock-balance, otc_bal1)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            curr_cd (str): 통화코드
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'curr_cd': curr_cd
        }
        return self.client.request_api('otc_bal1', data, next_key=next_key)
    
    def get_overseas_account_info(self, 
                                cano: str, 
                                acnt_prdt_cd: str, 
                                ovrs_excg_cd: str, 
                                curr_cd: str) -> Dict[str, Any]:
        """
        해외주식 계좌 상세정보 조회 (overseas-account-info, otc_bal2)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            curr_cd (str): 통화코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'curr_cd': curr_cd
        }
        return self.client.request_api('otc_bal2', data)
    
    def get_transaction_history(self, 
                              cano: str, 
                              acnt_prdt_cd: str, 
                              inqr_strt_dt: str, 
                              inqr_end_dt: str, 
                              stk_cd: str = '', 
                              sll_buy_dvsn_cd: str = '00', 
                              inqr_dvsn: str = '00', 
                              pdno: str = '', 
                              ccld_dvsn: str = '00', 
                              next_key: str = '') -> Dict[str, Any]:
        """
        계좌 거래내역 조회 (account-transaction-history, etc_ctrct_qty)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            inqr_strt_dt (str): 조회시작일자 (YYYYMMDD)
            inqr_end_dt (str): 조회종료일자 (YYYYMMDD)
            stk_cd (str, optional): 종목코드. 기본값은 빈 문자열
            sll_buy_dvsn_cd (str, optional): 매매구분코드. 기본값은 '00'
                00: 전체, 01: 매도, 02: 매수
            inqr_dvsn (str, optional): 조회구분. 기본값은 '00'
                00: 전체, 01: 체결, 02: 미체결
            pdno (str, optional): 상품번호. 기본값은 빈 문자열
            ccld_dvsn (str, optional): 체결구분. 기본값은 '00'
                00: 전체, 01: 매매, 02: 입출금 등
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'inqr_strt_dt': inqr_strt_dt,
            'inqr_end_dt': inqr_end_dt,
            'sll_buy_dvsn_cd': sll_buy_dvsn_cd,
            'inqr_dvsn': inqr_dvsn,
            'ccld_dvsn': ccld_dvsn
        }
        
        if stk_cd:
            data['stk_cd'] = stk_cd
            
        if pdno:
            data['pdno'] = pdno
            
        return self.client.request_api('etc_ctrct_qty', data, next_key=next_key)
    
    def get_overseas_transaction_history(self, 
                                       cano: str, 
                                       acnt_prdt_cd: str, 
                                       ovrs_excg_cd: str, 
                                       strt_dt: str, 
                                       end_dt: str, 
                                       stk_cd: str = '', 
                                       next_key: str = '') -> Dict[str, Any]:
        """
        해외주식 계좌 거래내역 조회 (overseas-account-transaction-history, otc_ctrct_eng)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            strt_dt (str): 시작일자 (YYYYMMDD)
            end_dt (str): 종료일자 (YYYYMMDD)
            stk_cd (str, optional): 종목코드. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'strt_dt': strt_dt,
            'end_dt': end_dt
        }
        
        if stk_cd:
            data['stk_cd'] = stk_cd
            
        return self.client.request_api('otc_ctrct_eng', data, next_key=next_key) 