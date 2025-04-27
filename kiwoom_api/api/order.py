"""
키움증권 주문 관련 API 모듈
"""

from typing import Dict, Any, Optional, List

from ..client import KiwoomClient


class OrderAPI:
    """키움증권 주문 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        주문 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def place_domestic_order(self,
                           cano: str,
                           acnt_prdt_cd: str,
                           stk_cd: str,
                           ord_dvsn: str,
                           ord_qty: str,
                           ord_unpr: str,
                           loan_dvsn: str = None,
                           loan_dt: str = None,
                           ord_mkis_mkt_name: str = None) -> Dict[str, Any]:
        """
        국내주식 주문 (domestic-stock-order, etc_ord)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            stk_cd (str): 종목코드
            ord_dvsn (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 조건부지정가, ...
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가
            loan_dvsn (str, optional): 신용구분
                00: 현금, 01: 융자, 02: 대주, ...
            loan_dt (str, optional): 대출일자 (YYYYMMDD)
            ord_mkis_mkt_name (str, optional): 주문시장조건구분코드명
                (장, 시간외단일가, 시간외종가, ...)
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'stk_cd': stk_cd,
            'ord_dvsn': ord_dvsn,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr
        }
        
        if loan_dvsn:
            data['loan_dvsn'] = loan_dvsn
        
        if loan_dt:
            data['loan_dt'] = loan_dt
            
        if ord_mkis_mkt_name:
            data['ord_mkis_mkt_name'] = ord_mkis_mkt_name
            
        return self.client.request_api('etc_ord', data)
    
    def place_overseas_order(self,
                           cano: str,
                           acnt_prdt_cd: str,
                           ovrs_excg_cd: str,
                           stk_cd: str,
                           ord_dvsn: str,
                           ord_qty: str,
                           ord_unpr: str,
                           curr_cd: str,
                           ord_gnd_cndt_cd: str = None,
                           prd_prc_rule_cd: str = None) -> Dict[str, Any]:
        """
        해외주식 주문 (overseas-stock-order, otc_ord)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            stk_cd (str): 종목코드
            ord_dvsn (str): 주문구분코드
                00: 지정가, 01: 시장가, ...
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가
            curr_cd (str): 통화코드
            ord_gnd_cndt_cd (str, optional): 주문체결조건코드
            prd_prc_rule_cd (str, optional): 상품가격규칙코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'stk_cd': stk_cd,
            'ord_dvsn': ord_dvsn,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr,
            'curr_cd': curr_cd
        }
        
        if ord_gnd_cndt_cd:
            data['ord_gnd_cndt_cd'] = ord_gnd_cndt_cd
            
        if prd_prc_rule_cd:
            data['prd_prc_rule_cd'] = prd_prc_rule_cd
            
        return self.client.request_api('otc_ord', data)
    
    def cancel_domestic_order(self,
                            cano: str,
                            acnt_prdt_cd: str,
                            stk_cd: str,
                            orgn_odno: str,
                            ord_qty: str,
                            ord_mkis_mkt_name: str = None) -> Dict[str, Any]:
        """
        국내주식 주문 취소 (domestic-stock-order-cancel, etc_cncl)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            stk_cd (str): 종목코드
            orgn_odno (str): 원주문번호
            ord_qty (str): 주문수량
            ord_mkis_mkt_name (str, optional): 주문시장조건구분코드명
                (장, 시간외단일가, 시간외종가, ...)
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'stk_cd': stk_cd,
            'orgn_odno': orgn_odno,
            'ord_qty': ord_qty
        }
        
        if ord_mkis_mkt_name:
            data['ord_mkis_mkt_name'] = ord_mkis_mkt_name
            
        return self.client.request_api('etc_cncl', data)
    
    def modify_domestic_order(self,
                            cano: str,
                            acnt_prdt_cd: str,
                            stk_cd: str,
                            orgn_odno: str,
                            ord_qty: str,
                            ord_unpr: str,
                            ord_dvsn: str,
                            ord_mkis_mkt_name: str = None) -> Dict[str, Any]:
        """
        국내주식 주문 정정 (domestic-stock-order-revision, etc_mdfy)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            stk_cd (str): 종목코드
            orgn_odno (str): 원주문번호
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가
            ord_dvsn (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 조건부지정가, ...
            ord_mkis_mkt_name (str, optional): 주문시장조건구분코드명
                (장, 시간외단일가, 시간외종가, ...)
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'stk_cd': stk_cd,
            'orgn_odno': orgn_odno,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr,
            'ord_dvsn': ord_dvsn
        }
        
        if ord_mkis_mkt_name:
            data['ord_mkis_mkt_name'] = ord_mkis_mkt_name
            
        return self.client.request_api('etc_mdfy', data)
    
    def cancel_overseas_order(self,
                            cano: str,
                            acnt_prdt_cd: str,
                            ovrs_excg_cd: str,
                            stk_cd: str,
                            orgn_odno: str,
                            ord_qty: str,
                            curr_cd: str,
                            ord_dvsn: str = None) -> Dict[str, Any]:
        """
        해외주식 주문 취소 (overseas-stock-order-cancel, otc_cncl)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            stk_cd (str): 종목코드
            orgn_odno (str): 원주문번호
            ord_qty (str): 주문수량
            curr_cd (str): 통화코드
            ord_dvsn (str, optional): 주문구분코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'stk_cd': stk_cd,
            'orgn_odno': orgn_odno,
            'ord_qty': ord_qty,
            'curr_cd': curr_cd
        }
        
        if ord_dvsn:
            data['ord_dvsn'] = ord_dvsn
            
        return self.client.request_api('otc_cncl', data)
    
    def modify_overseas_order(self,
                            cano: str,
                            acnt_prdt_cd: str,
                            ovrs_excg_cd: str,
                            stk_cd: str,
                            orgn_odno: str,
                            ord_qty: str,
                            ord_unpr: str,
                            curr_cd: str,
                            ord_dvsn: str = None) -> Dict[str, Any]:
        """
        해외주식 주문 정정 (overseas-stock-order-revision, otc_mdfy)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            stk_cd (str): 종목코드
            orgn_odno (str): 원주문번호
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가
            curr_cd (str): 통화코드
            ord_dvsn (str, optional): 주문구분코드
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'stk_cd': stk_cd,
            'orgn_odno': orgn_odno,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr,
            'curr_cd': curr_cd
        }
        
        if ord_dvsn:
            data['ord_dvsn'] = ord_dvsn
            
        return self.client.request_api('otc_mdfy', data)
    
    def get_order_status(self,
                       cano: str,
                       acnt_prdt_cd: str,
                       inqr_dvsn: str = '00',
                       stk_cd: str = '',
                       next_key: str = '') -> Dict[str, Any]:
        """
        주문내역 조회 (domestic-stock-order-status, etc_psbl_amt3)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            inqr_dvsn (str, optional): 조회구분코드. 기본값은 '00'
                00: 전체, 01: 매도, 02: 매수
            stk_cd (str, optional): 종목코드. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'inqr_dvsn': inqr_dvsn
        }
        
        if stk_cd:
            data['stk_cd'] = stk_cd
            
        return self.client.request_api('etc_psbl_amt3', data, next_key=next_key)
    
    def get_overseas_order_status(self,
                                cano: str,
                                acnt_prdt_cd: str,
                                ovrs_excg_cd: str,
                                curr_cd: str = '',
                                stk_cd: str = '',
                                ord_brnc_cd: str = '',
                                next_key: str = '') -> Dict[str, Any]:
        """
        해외주식 주문내역 조회 (overseas-stock-order-status, otc_crct)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            curr_cd (str, optional): 통화코드. 기본값은 빈 문자열
            stk_cd (str, optional): 종목코드. 기본값은 빈 문자열
            ord_brnc_cd (str, optional): 주문지점코드. 기본값은 빈 문자열
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd
        }
        
        if curr_cd:
            data['curr_cd'] = curr_cd
            
        if stk_cd:
            data['stk_cd'] = stk_cd
            
        if ord_brnc_cd:
            data['ord_brnc_cd'] = ord_brnc_cd
            
        return self.client.request_api('otc_crct', data, next_key=next_key) 