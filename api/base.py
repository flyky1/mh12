#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 기본 API 모듈

이 모듈은 키움 OpenAPI의 기본 API 클래스를 제공합니다.
모든 API 모듈의 기본 클래스로 사용됩니다.
"""

import json
import logging
import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class APIBase:
    """
    API 기본 클래스
    
    모든 API 클래스의 기본 클래스로 사용되며, 공통 기능을 제공합니다.
    - HTTP 요청 메서드 (GET, POST, PUT, DELETE)
    - 헤더 생성
    - 응답 처리
    """
    
    def __init__(self, base_url: str, headers: Dict[str, str]):
        """
        APIBase 클래스 초기화
        
        Args:
            base_url (str): API 기본 URL
            headers (Dict[str, str]): API 요청 헤더
        """
        self.base_url = base_url
        self.headers = headers
    
    def _get_url(self, endpoint: str) -> str:
        """
        URL 생성
        
        Args:
            endpoint (str): API 엔드포인트
            
        Returns:
            str: 완성된 URL
        """
        return urljoin(self.base_url, endpoint)
    
    def _process_response(self, response: requests.Response) -> Dict[str, Any]:
        """
        응답 처리
        
        Args:
            response (requests.Response): 요청 응답 객체
            
        Returns:
            Dict[str, Any]: 처리된 응답 데이터
        """
        try:
            response.raise_for_status()
            data = response.json()
            return {
                'status': 'success',
                'message': data.get('msg1', ''),
                'code': data.get('msg_cd', ''),
                'data': data
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP 오류: {str(e)}")
            return {
                'status': 'error',
                'message': f'HTTP 오류: {str(e)}',
                'code': str(response.status_code),
                'data': {}
            }
        except json.JSONDecodeError as e:
            logger.error(f"JSON 디코딩 오류: {str(e)}")
            return {
                'status': 'error',
                'message': f'응답을 JSON으로 변환할 수 없습니다: {str(e)}',
                'code': 'JSON_DECODE_ERROR',
                'data': {}
            }
        except Exception as e:
            logger.error(f"요청 처리 중 오류 발생: {str(e)}")
            return {
                'status': 'error',
                'message': f'요청 처리 중 오류 발생: {str(e)}',
                'code': 'UNKNOWN_ERROR',
                'data': {}
            }
    
    def request_get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        GET 요청
        
        Args:
            endpoint (str): API 엔드포인트
            params (Dict[str, Any], optional): 요청 파라미터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = self._get_url(endpoint)
        
        try:
            response = requests.get(url, headers=self.headers, params=params)
            return self._process_response(response)
        except Exception as e:
            logger.error(f"GET 요청 중 오류 발생: {str(e)}")
            return {
                'status': 'error',
                'message': f'GET 요청 중 오류 발생: {str(e)}',
                'code': 'REQUEST_ERROR',
                'data': {}
            }
    
    def request_post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        POST 요청
        
        Args:
            endpoint (str): API 엔드포인트
            data (Dict[str, Any], optional): 요청 데이터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = self._get_url(endpoint)
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            return self._process_response(response)
        except Exception as e:
            logger.error(f"POST 요청 중 오류 발생: {str(e)}")
            return {
                'status': 'error',
                'message': f'POST 요청 중 오류 발생: {str(e)}',
                'code': 'REQUEST_ERROR',
                'data': {}
            }
    
    def request_put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        PUT 요청
        
        Args:
            endpoint (str): API 엔드포인트
            data (Dict[str, Any], optional): 요청 데이터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = self._get_url(endpoint)
        
        try:
            response = requests.put(url, headers=self.headers, json=data)
            return self._process_response(response)
        except Exception as e:
            logger.error(f"PUT 요청 중 오류 발생: {str(e)}")
            return {
                'status': 'error',
                'message': f'PUT 요청 중 오류 발생: {str(e)}',
                'code': 'REQUEST_ERROR',
                'data': {}
            }
    
    def request_delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        DELETE 요청
        
        Args:
            endpoint (str): API 엔드포인트
            params (Dict[str, Any], optional): 요청 파라미터
            
        Returns:
            Dict[str, Any]: 응답 데이터
        """
        url = self._get_url(endpoint)
        
        try:
            response = requests.delete(url, headers=self.headers, params=params)
            return self._process_response(response)
        except Exception as e:
            logger.error(f"DELETE 요청 중 오류 발생: {str(e)}")
            return {
                'status': 'error',
                'message': f'DELETE 요청 중 오류 발생: {str(e)}',
                'code': 'REQUEST_ERROR',
                'data': {}
            }


class BaseAPI:
    """
    조건 검색 API를 위한 기본 클래스
    """
    
    def __init__(self, api_key: Optional[str] = None, secret_key: Optional[str] = None, access_token: Optional[str] = None):
        """
        BaseAPI 클래스 초기화
        
        Args:
            api_key (str, optional): API 키
            secret_key (str, optional): 시크릿 키
            access_token (str, optional): 액세스 토큰
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = access_token
        self.base_url = "https://openapi.kiwoom.com"
    
    def _get_headers(self, tr_id: str, tr_cd: str) -> Dict[str, str]:
        """
        API 요청 헤더 생성
        
        Args:
            tr_id (str): 거래 ID
            tr_cd (str): 거래 코드
            
        Returns:
            Dict[str, str]: 헤더 정보
        """
        if not self.access_token:
            self.access_token = self._get_access_token()
        
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
            "tr_id": tr_id,
            "tr_cd": tr_cd
        }
    
    def _get_access_token(self) -> str:
        """
        액세스 토큰 획득
        
        Returns:
            str: 액세스 토큰
        """
        # 여기에 액세스 토큰 획득 로직 구현
        # 임시 구현으로 빈 문자열 반환
        return "" 