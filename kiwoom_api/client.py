"""
키움증권 REST API 클라이언트
"""

import os
import requests
import json
from typing import Dict, List, Optional, Any, Union, Tuple

from .auth import KiwoomAuth, MOCK_HOST, REAL_HOST


class KiwoomClient:
    """키움증권 API 클라이언트 클래스"""
    
    def __init__(self, appkey: str = None, secretkey: str = None, is_mock: bool = False, auto_auth: bool = True):
        """
        키움증권 API 클라이언트 초기화
        
        Args:
            appkey (str, optional): API 앱키. 기본값은 환경변수 'kiwoom_appkey'에서 가져옴
            secretkey (str, optional): API 시크릿키. 기본값은 환경변수 'kiwoom_secretkey'에서 가져옴
            is_mock (bool, optional): 모의투자 여부. 기본값은 False
            auto_auth (bool, optional): 초기화시 자동으로 인증 수행 여부. 기본값은 True
        """
        self.auth = KiwoomAuth(appkey, secretkey, is_mock)
        self.host = MOCK_HOST if is_mock else REAL_HOST
        self.is_mock = is_mock
        
        # API 모듈 초기화
        self._init_api_modules()
        
        # 자동 인증 수행
        if auto_auth:
            self.auth.get_access_token()
    
    def _init_api_modules(self):
        """API 모듈 초기화"""
        # lazy import to avoid circular imports
        from .api.account import AccountAPI
        from .api.order import OrderAPI
        from .api.price import PriceAPI
        
        # API 모듈 인스턴스 생성
        self.account = AccountAPI(self)
        self.order = OrderAPI(self)
        self.price = PriceAPI(self)
    
    def _request(self, 
                method: str, 
                endpoint: str, 
                api_id: str, 
                data: Dict[str, Any] = None, 
                cont_yn: str = 'N', 
                next_key: str = '') -> Dict[str, Any]:
        """
        API 요청 공통 메서드
        
        Args:
            method (str): HTTP 메서드 (GET, POST 등)
            endpoint (str): API 엔드포인트 경로
            api_id (str): API ID (TR 코드)
            data (Dict[str, Any], optional): 요청 데이터
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        if not self.auth.token:
            self.auth.get_access_token()
            
        url = self.host + endpoint
        
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.auth.token}',
            'cont-yn': cont_yn,
            'next-key': next_key,
            'api-id': api_id,
        }
        
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, params=data)
        else:  # POST
            response = requests.post(url, headers=headers, json=data)
        
        # HTTP 에러 처리
        response.raise_for_status()
        
        # 응답 헤더 정보 저장
        response_headers = {
            'cont-yn': response.headers.get('cont-yn'),
            'next-key': response.headers.get('next-key'),
            'api-id': response.headers.get('api-id')
        }
        
        # 응답 데이터와 헤더 정보 함께 반환
        result = {
            'status_code': response.status_code,
            'headers': response_headers,
            'data': response.json()
        }
        
        return result
    
    def request_api(self, 
                   api_id: str, 
                   data: Dict[str, Any] = None, 
                   method: str = 'POST', 
                   endpoint: str = None,
                   cont_yn: str = 'N', 
                   next_key: str = '') -> Dict[str, Any]:
        """
        API 요청 메서드
        
        Args:
            api_id (str): API ID (TR 코드)
            data (Dict[str, Any], optional): 요청 데이터
            method (str, optional): HTTP 메서드. 기본값은 'POST'
            endpoint (str, optional): API 엔드포인트 경로. 기본값은 None (자동 결정)
            cont_yn (str, optional): 연속조회여부. 기본값은 'N'
            next_key (str, optional): 연속조회키. 기본값은 빈 문자열
            
        Returns:
            Dict[str, Any]: API 응답 데이터
        """
        # API ID 앞 두 글자로 API 타입 판별하여, 엔드포인트 자동 결정
        if not endpoint:
            # 앞 두 글자에 따라 다른 엔드포인트 지정
            api_type = api_id[:2].lower()
            
            if api_type == 'au':  # 인증
                endpoint = '/oauth2/token'
            elif api_type == 'ka':  # 계좌
                endpoint = '/api/dostk/acnt'
            elif api_type == 'kt':  # 주문
                endpoint = '/api/dostk/ordr'
            elif api_type == 'kr':  # 신용주문
                endpoint = '/api/dostk/ordr'
            elif api_type == 'kc':  # 차트
                endpoint = '/api/dostk/chart'
            elif api_type == 'ks':  # 시세
                endpoint = '/api/dostk/price'
            elif api_type == 'ke':  # 종목정보
                endpoint = '/api/dostk/stock'
            elif api_type == 'ki':  # 순위정보
                endpoint = '/api/dostk/rkinfo'
            elif api_type == 'kb':  # 업종
                endpoint = '/api/dostk/sector'
            elif api_type == 'kl':  # ETF
                endpoint = '/api/dostk/etf'
            elif api_type == 'kf':  # ELW
                endpoint = '/api/dostk/elw'
            elif api_type == 'kh':  # 테마
                endpoint = '/api/dostk/theme'
            elif api_type == 'ko':  # 조건검색
                endpoint = '/api/dostk/condition'
            elif api_type == 'kg':  # 기관외국인
                endpoint = '/api/dostk/forgnr'
            else:
                raise ValueError(f"알 수 없는 API 유형: {api_id}")
        
        return self._request(method, endpoint, api_id, data, cont_yn, next_key)
        
    def get_realtime_client(self):
        """
        실시간시세 클라이언트 생성
        
        Returns:
            KiwoomRealtimeClient: 실시간시세 클라이언트 객체
        """
        from .realtime import KiwoomRealtimeClient
        return KiwoomRealtimeClient(
            token=self.auth.token,
            appkey=self.auth.appkey,
            secretkey=self.auth.secretkey,
            is_mock=self.is_mock
        ) 