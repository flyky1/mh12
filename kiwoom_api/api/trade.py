"""
키움증권 매매 API 모듈
"""

from typing import Dict, Any, Optional, List

from ..client import KiwoomClient


class TradeAPI:
    """키움증권 매매 API 클래스"""
    
    def __init__(self, client: KiwoomClient):
        """
        매매 API 초기화
        
        Args:
            client (KiwoomClient): 키움증권 API 클라이언트 객체
        """
        self.client = client
    
    def order_cash(self, 
                  cano: str, 
                  acnt_prdt_cd: str, 
                  stk_cd: str, 
                  ord_dvsn_cd: str, 
                  ord_qty: str, 
                  ord_unpr: str) -> Dict[str, Any]:
        """
        주식 현금 주문 (ord01)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            stk_cd (str): 종목코드
            ord_dvsn_cd (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 조건부지정가, 03: 최유리지정가, 04: 최우선지정가
                05: 장전시간외, 06: 장후시간외, 07: 시간외단일가, 08: 자기주식, 09: 자기주식S-Option
                10: 자기주식금전신탁, 11: IOC지정가, 12: FOK지정가, 13: IOC시장가, 14: FOK시장가
                15: IOC최유리, 16: FOK최유리
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가 (시장가의 경우 '0')
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr
        }
        return self.client.request_api('ord01', data)
    
    def order_credit(self, 
                   cano: str, 
                   acnt_prdt_cd: str, 
                   stk_cd: str, 
                   ord_dvsn_cd: str, 
                   ord_qty: str, 
                   ord_unpr: str, 
                   loan_dvsn_cd: str, 
                   ord_dvsn: str = '00') -> Dict[str, Any]:
        """
        주식 신용 주문 (ord02)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            stk_cd (str): 종목코드
            ord_dvsn_cd (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 조건부지정가, 03: 최유리지정가, 04: 최우선지정가
                05: 장전시간외, 06: 장후시간외, 07: 시간외단일가, 08: 자기주식, 09: 자기주식S-Option
                10: 자기주식금전신탁, 11: IOC지정가, 12: FOK지정가, 13: IOC시장가, 14: FOK시장가
                15: IOC최유리, 16: FOK최유리
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가 (시장가의 경우 '0')
            loan_dvsn_cd (str): 신용대출구분코드
                01: 유통융자, 02: 자기융자, 03: 유통대주, 04: 자기대주
            ord_dvsn (str, optional): 매매구분. 기본값은 '00'
                00: 고객 지정가, 01: 시스템 자동주문
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr,
            'loan_dvsn_cd': loan_dvsn_cd,
            'ord_dvsn': ord_dvsn
        }
        return self.client.request_api('ord02', data)
    
    def order_cancel_or_modify(self, 
                            cano: str, 
                            acnt_prdt_cd: str, 
                            org_odno: str, 
                            stk_cd: str, 
                            ord_dvsn_cd: str, 
                            ord_qty: str, 
                            ord_unpr: str, 
                            cncl_dvsn_cd: str = '01', 
                            loan_dvsn_cd: str = '') -> Dict[str, Any]:
        """
        주식 주문 취소/정정 (ord03)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            org_odno (str): 원주문번호
            stk_cd (str): 종목코드
            ord_dvsn_cd (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 조건부지정가, 03: 최유리지정가, 04: 최우선지정가
                05: 장전시간외, 06: 장후시간외, 07: 시간외단일가, 08: 자기주식, 09: 자기주식S-Option
                10: 자기주식금전신탁, 11: IOC지정가, 12: FOK지정가, 13: IOC시장가, 14: FOK시장가
                15: IOC최유리, 16: FOK최유리
            ord_qty (str): 주문수량
            ord_unpr (str): 주문단가 (시장가의 경우 '0')
            cncl_dvsn_cd (str, optional): 취소구분코드. 기본값은 '01'
                01: 취소, 02: 정정
            loan_dvsn_cd (str, optional): 신용대출구분코드. 기본값은 빈 문자열
                '': 해당없음, 01: 유통융자, 02: 자기융자, 03: 유통대주, 04: 자기대주
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'org_odno': org_odno,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'ord_qty': ord_qty,
            'ord_unpr': ord_unpr,
            'cncl_dvsn_cd': cncl_dvsn_cd
        }
        
        if loan_dvsn_cd:
            data['loan_dvsn_cd'] = loan_dvsn_cd
            
        return self.client.request_api('ord03', data)
    
    def get_order_list(self, 
                    cano: str, 
                    acnt_prdt_cd: str, 
                    ord_strt_dt: str, 
                    ord_end_dt: str, 
                    stk_cd: str = '', 
                    ord_dvsn_cd: str = '00', 
                    sll_buy_dvsn_cd: str = '00', 
                    ord_stus_dvsn_cd: str = '00', 
                    cont_yn: str = 'N', 
                    next_key: str = '') -> Dict[str, Any]:
        """
        주식 주문 조회 (ord01prct)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ord_strt_dt (str): 주문시작일자 (YYYYMMDD)
            ord_end_dt (str): 주문종료일자 (YYYYMMDD)
            stk_cd (str, optional): 종목코드. 기본값은 빈 문자열(전체)
            ord_dvsn_cd (str, optional): 주문구분코드. 기본값은 '00'(전체)
            sll_buy_dvsn_cd (str, optional): 매도매수구분코드. 기본값은 '00'
                00: 전체, 01: 매도, 02: 매수
            ord_stus_dvsn_cd (str, optional): 주문상태구분코드. 기본값은 '00'
                00: 전체, 01: 접수, 02: 확인, 03: 취소, 04: 거부
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ord_strt_dt': ord_strt_dt,
            'ord_end_dt': ord_end_dt,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'sll_buy_dvsn_cd': sll_buy_dvsn_cd,
            'ord_stus_dvsn_cd': ord_stus_dvsn_cd
        }
        return self.client.request_api('ord01prct', data, cont_yn=cont_yn, next_key=next_key)
    
    def order_overseas_stock(self, 
                          cano: str, 
                          acnt_prdt_cd: str, 
                          ovrs_excg_cd: str, 
                          frcr_cd: str, 
                          stk_cd: str, 
                          ord_dvsn_cd: str, 
                          ord_qty: str, 
                          ovrs_ord_unpr: str, 
                          ord_gnd_dvsn_cd: str) -> Dict[str, Any]:
        """
        해외주식 주문 (oos01)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            frcr_cd (str): 외화코드
            stk_cd (str): 종목코드
            ord_dvsn_cd (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 지정가(IOC), 03: 지정가(FOK), 04: 시장가(IOC), 05: 시장가(FOK)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가
            ord_gnd_dvsn_cd (str): 주문근거구분코드
                01: 매수, 02: 매도
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'frcr_cd': frcr_cd,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'ord_qty': ord_qty,
            'ovrs_ord_unpr': ovrs_ord_unpr,
            'ord_gnd_dvsn_cd': ord_gnd_dvsn_cd
        }
        return self.client.request_api('oos01', data)
    
    def cancel_or_modify_overseas_order(self, 
                                     cano: str, 
                                     acnt_prdt_cd: str, 
                                     ovrs_excg_cd: str, 
                                     frcr_cd: str, 
                                     orgn_odno: str, 
                                     stk_cd: str, 
                                     ord_dvsn_cd: str, 
                                     ord_qty: str, 
                                     ovrs_ord_unpr: str, 
                                     ord_gnd_dvsn_cd: str, 
                                     cncl_cfrm_dvsn_cd: str) -> Dict[str, Any]:
        """
        해외주식 취소/정정 주문 (oos02)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            frcr_cd (str): 외화코드
            orgn_odno (str): 원주문번호
            stk_cd (str): 종목코드
            ord_dvsn_cd (str): 주문구분코드
                00: 지정가, 01: 시장가, 02: 지정가(IOC), 03: 지정가(FOK), 04: 시장가(IOC), 05: 시장가(FOK)
            ord_qty (str): 주문수량
            ovrs_ord_unpr (str): 해외주문단가
            ord_gnd_dvsn_cd (str): 주문근거구분코드
                01: 매수, 02: 매도
            cncl_cfrm_dvsn_cd (str): 취소확인구분코드
                01: 취소, 02: 정정
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'frcr_cd': frcr_cd,
            'orgn_odno': orgn_odno,
            'stk_cd': stk_cd,
            'ord_dvsn_cd': ord_dvsn_cd,
            'ord_qty': ord_qty,
            'ovrs_ord_unpr': ovrs_ord_unpr,
            'ord_gnd_dvsn_cd': ord_gnd_dvsn_cd,
            'cncl_cfrm_dvsn_cd': cncl_cfrm_dvsn_cd
        }
        return self.client.request_api('oos02', data)
    
    def get_overseas_order_list(self, 
                             cano: str, 
                             acnt_prdt_cd: str, 
                             ovrs_excg_cd: str, 
                             ord_strt_dt: str, 
                             ord_end_dt: str, 
                             cont_yn: str = 'N', 
                             next_key: str = '') -> Dict[str, Any]:
        """
        해외주식 주문 내역 조회 (ood01)
        
        Args:
            cano (str): 계좌번호
            acnt_prdt_cd (str): 계좌상품코드
            ovrs_excg_cd (str): 해외거래소코드
            ord_strt_dt (str): 주문시작일자 (YYYYMMDD)
            ord_end_dt (str): 주문종료일자 (YYYYMMDD)
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        data = {
            'cano': cano,
            'acnt_prdt_cd': acnt_prdt_cd,
            'ovrs_excg_cd': ovrs_excg_cd,
            'ord_strt_dt': ord_strt_dt,
            'ord_end_dt': ord_end_dt
        }
        return self.client.request_api('ood01', data, cont_yn=cont_yn, next_key=next_key) 