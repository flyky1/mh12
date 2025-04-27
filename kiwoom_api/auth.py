"""
키움증권 OAuth2 인증 모듈
"""
import os
import requests
import json
from typing import Dict, Optional, Any, Tuple

# API 호스트 정보
MOCK_HOST = "https://mockapi.kiwoom.com"
REAL_HOST = "https://api.kiwoom.com"


class KiwoomAuth:
    """키움증권 인증 클래스"""
    
    def __init__(self, appkey: str = None, secretkey: str = None, is_mock: bool = False):
        """
        키움증권 인증 객체 초기화
        
        Args:
            appkey (str, optional): API 앱키. 기본값은 환경변수 'kiwoom_appkey'에서 가져옴
            secretkey (str, optional): API 시크릿키. 기본값은 환경변수 'kiwoom_secretkey'에서 가져옴
            is_mock (bool, optional): 모의투자 여부. 기본값은 False
        """
        self.appkey = appkey or os.environ.get('kiwoom_appkey')
        self.secretkey = secretkey or os.environ.get('kiwoom_secretkey')
        self.host = MOCK_HOST if is_mock else REAL_HOST
        self.token = None
        self.token_type = None
        self.expires_dt = None
        
        if not self.appkey or not self.secretkey:
            raise ValueError("appkey와 secretkey가 필요합니다. 환경변수 'kiwoom_appkey'와 'kiwoom_secretkey'를 설정하거나 직접 인자로 전달하세요.")
    
    def get_access_token(self) -> str:
        """
        접근 토큰 발급 (au10001)
        
        Returns:
            str: 발급된 접근 토큰
        """
        endpoint = '/oauth2/token'
        url = self.host + endpoint
        
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        
        data = {
            'grant_type': 'client_credentials',
            'appkey': self.appkey,
            'secretkey': self.secretkey,
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        self.token = result.get('token')
        self.token_type = result.get('token_type')
        self.expires_dt = result.get('expires_dt')
        
        return self.token
    
    def revoke_token(self, token: str = None) -> bool:
        """
        접근 토큰 폐기 (au10002)
        
        Args:
            token (str, optional): 폐기할 토큰. 기본값은 현재 객체에 저장된 토큰
            
        Returns:
            bool: 폐기 성공 여부
        """
        endpoint = '/oauth2/revoke'
        url = self.host + endpoint
        
        token_to_revoke = token or self.token
        if not token_to_revoke:
            raise ValueError("폐기할 토큰이 없습니다. 먼저 토큰을 발급받으세요.")
        
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
        }
        
        data = {
            'appkey': self.appkey,
            'secretkey': self.secretkey,
            'token': token_to_revoke,
        }
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            if token_to_revoke == self.token:
                self.token = None
                self.token_type = None
                self.expires_dt = None
            return True
        return False


def get_access_token(appkey: str = None, secretkey: str = None, is_mock: bool = False) -> str:
    """
    접근 토큰 빠르게 발급받기
    
    Args:
        appkey (str, optional): API 앱키. 기본값은 환경변수 'kiwoom_appkey'에서 가져옴
        secretkey (str, optional): API 시크릿키. 기본값은 환경변수 'kiwoom_secretkey'에서 가져옴
        is_mock (bool, optional): 모의투자 여부. 기본값은 False
        
    Returns:
        str: 발급된 접근 토큰
    """
    auth = KiwoomAuth(appkey, secretkey, is_mock)
    return auth.get_access_token() 