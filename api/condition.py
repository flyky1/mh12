#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 조건검색 API 모듈

이 모듈은 키움 OpenAPI의 조건검색 관련 API 기능을 제공합니다.
- 조건검색 목록 조회
- 조건검색 기본 조회
- 조건검색 실시간 조회
- 조건검색 실시간 해제
"""

import json
import logging
import asyncio
import websockets
from typing import Dict, Any, Optional, List, Union
import os
from datetime import datetime

from .base import APIBase, BaseAPI

logger = logging.getLogger(__name__)


class ConditionAPI(BaseAPI):
    """
    조건검색 API 클래스
    
    조건검색과 관련된 API 기능을 제공합니다.
    """
    
    def __init__(self, base_url: str, app_key: str, app_secret: str):
        """
        ConditionAPI 생성자
        
        Args:
            base_url (str): API 기본 URL
            app_key (str): 앱 키
            app_secret (str): 앱 시크릿
        """
        super().__init__(base_url, app_key, app_secret)
        self.websocket = None
        self.logger = logging.getLogger("ConditionAPI")
        self.ws_url = "wss://openapi.kiwoom.com/openapi/ws/condition"
        self.callbacks = {}
        self.condition_websocket_connected = False
        
    async def connect_websocket(self) -> bool:
        """
        조건검색 웹소켓 연결
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            if self.websocket and not self.websocket.closed:
                return True
                
            token = self._get_access_token()
            if not token:
                self.logger.error("Failed to get access token for websocket connection")
                return False
                
            headers = {
                "authorization": f"Bearer {token}"
            }
            
            self.websocket = await websockets.connect(
                self.ws_url,
                extra_headers=headers
            )
            
            self.condition_websocket_connected = True
            self.logger.info("Connected to condition websocket server")
            
            # 웹소켓 메시지 리스너 시작
            asyncio.create_task(self._listen_websocket_messages())
            
            return True
        except Exception as e:
            self.logger.error(f"Error connecting to websocket: {str(e)}")
            return False
            
    async def _listen_websocket_messages(self):
        """웹소켓 메시지 리스너"""
        try:
            while self.condition_websocket_connected and self.websocket:
                message = await self.websocket.recv()
                self.logger.debug(f"Received message: {message}")
                
                try:
                    data = json.loads(message)
                    tr_id = data.get("header", {}).get("tr_id", "")
                    
                    if tr_id in self.callbacks:
                        callback = self.callbacks.get(tr_id)
                        if callback:
                            callback(data)
                except json.JSONDecodeError:
                    self.logger.error(f"Failed to parse message: {message}")
                except Exception as e:
                    self.logger.error(f"Error processing message: {str(e)}")
        except websockets.exceptions.ConnectionClosed:
            self.logger.info("Websocket connection closed")
            self.condition_websocket_connected = False
        except Exception as e:
            self.logger.error(f"Error in websocket listener: {str(e)}")
            self.condition_websocket_connected = False
            
    async def disconnect_websocket(self):
        """웹소켓 연결 종료"""
        if self.websocket:
            await self.websocket.close()
            self.condition_websocket_connected = False
            self.logger.info("Disconnected from condition websocket server")
            
    def get_condition_list(self) -> Dict[str, Any]:
        """
        조건검색 목록 조회
        
        Returns:
            Dict[str, Any]: 조건검색 목록 정보
        """
        try:
            url = f"{self.base_url}/uapi/condition/v1/list"
            
            headers = self._get_headers()
            headers.update({
                "tr_id": "CTRP6548R"
            })
            
            response = self.session.get(url, headers=headers)
            
            if response.status_code != 200:
                self.logger.error(f"Error in get_condition_list: {response.text}")
                return {
                    "status": "error",
                    "message": f"API request failed with status code {response.status_code}",
                    "data": None
                }
                
            result = response.json()
            
            return {
                "status": "success",
                "message": "조건검색 목록을 성공적으로 조회하였습니다.",
                "data": result
            }
        except Exception as e:
            self.logger.error(f"Error in get_condition_list: {str(e)}")
            return {
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "data": None
            }
            
    def execute_condition(self, condition_name: str, condition_index: str, 
                         search_type: str = "0") -> Dict[str, Any]:
        """
        일반 조건검색 실행
        
        Args:
            condition_name (str): 조건검색 이름
            condition_index (str): 조건검색 인덱스
            search_type (str): 검색 유형 (0: 전체조회, 1: 실시간조회)
            
        Returns:
            Dict[str, Any]: 조건검색 결과
        """
        try:
            url = f"{self.base_url}/uapi/condition/v1/search"
            
            headers = self._get_headers()
            headers.update({
                "tr_id": "CTRP6549R"
            })
            
            params = {
                "con_name": condition_name,
                "con_index": condition_index,
                "search_tp": search_type
            }
            
            response = self.session.get(url, headers=headers, params=params)
            
            if response.status_code != 200:
                self.logger.error(f"Error in execute_condition: {response.text}")
                return {
                    "status": "error",
                    "message": f"API request failed with status code {response.status_code}",
                    "data": None
                }
                
            result = response.json()
            
            return {
                "status": "success",
                "message": "조건검색을 성공적으로 실행하였습니다.",
                "data": result
            }
        except Exception as e:
            self.logger.error(f"Error in execute_condition: {str(e)}")
            return {
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "data": None
            }
            
    async def start_realtime_condition(self, condition_name: str, condition_index: str, 
                                      callback) -> Dict[str, Any]:
        """
        실시간 조건검색 시작
        
        Args:
            condition_name (str): 조건검색 이름
            condition_index (str): 조건검색 인덱스
            callback (callable): 실시간 데이터 수신 콜백 함수
            
        Returns:
            Dict[str, Any]: 실시간 조건검색 요청 결과
        """
        try:
            # 웹소켓 연결 확인
            if not self.condition_websocket_connected:
                connected = await self.connect_websocket()
                if not connected:
                    return {
                        "status": "error",
                        "message": "Failed to connect to websocket server",
                        "data": None
                    }
                    
            # 트랜잭션 ID 생성
            tr_id = f"CTRP6549R_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
            
            # 콜백 등록
            self.callbacks[tr_id] = callback
            
            # 요청 메시지 생성
            request = {
                "header": {
                    "tr_id": tr_id,
                    "tr_type": "1"  # 실시간 등록
                },
                "body": {
                    "con_name": condition_name,
                    "con_index": condition_index
                }
            }
            
            # 요청 전송
            await self.websocket.send(json.dumps(request))
            
            return {
                "status": "success",
                "message": "실시간 조건검색을 시작했습니다.",
                "data": {"tr_id": tr_id}
            }
        except Exception as e:
            self.logger.error(f"Error in start_realtime_condition: {str(e)}")
            return {
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "data": None
            }
            
    async def stop_realtime_condition(self, tr_id: str) -> Dict[str, Any]:
        """
        실시간 조건검색 중지
        
        Args:
            tr_id (str): 실시간 조건검색 트랜잭션 ID
            
        Returns:
            Dict[str, Any]: 중지 요청 결과
        """
        try:
            if not self.condition_websocket_connected or not self.websocket:
                return {
                    "status": "error",
                    "message": "웹소켓이 연결되어 있지 않습니다.",
                    "data": None
                }
                
            # 요청 메시지 생성
            request = {
                "header": {
                    "tr_id": tr_id,
                    "tr_type": "2"  # 실시간 해제
                }
            }
            
            # 요청 전송
            await self.websocket.send(json.dumps(request))
            
            # 콜백 제거
            if tr_id in self.callbacks:
                del self.callbacks[tr_id]
                
            return {
                "status": "success",
                "message": "실시간 조건검색을 중지했습니다.",
                "data": None
            }
        except Exception as e:
            self.logger.error(f"Error in stop_realtime_condition: {str(e)}")
            return {
                "status": "error",
                "message": f"An error occurred: {str(e)}",
                "data": None
            }


class WebSocketClient:
    """
    WebSocket 클라이언트 클래스
    
    실시간 조건검색을 위한 WebSocket 연결을 관리합니다.
    """
    
    def __init__(self, uri: str, token: str):
        """
        WebSocketClient 클래스 초기화
        
        Args:
            uri (str): WebSocket URI
            token (str): 액세스 토큰
        """
        self.uri = uri
        self.token = token
        self.websocket = None
        self.connected = False
        self.keep_running = True
        self.callbacks = {}
    
    async def connect(self):
        """
        WebSocket 서버에 연결
        
        Returns:
            bool: 연결 성공 여부
        """
        try:
            self.websocket = await websockets.connect(self.uri)
            self.connected = True
            logger.info("WebSocket 서버에 연결을 시도합니다.")
            
            # 로그인 패킷
            login_data = {
                'trnm': 'LOGIN',
                'token': self.token
            }
            
            logger.info("실시간 시세 서버로 로그인 패킷을 전송합니다.")
            await self.send_message(login_data)
            
            # 메시지 수신 작업 시작
            asyncio.create_task(self._receive_messages())
            
            return True
        except Exception as e:
            logger.error(f"WebSocket 연결 오류: {str(e)}")
            self.connected = False
            return False
    
    async def send_message(self, message: Dict[str, Any]) -> bool:
        """
        서버에 메시지 전송
        
        Args:
            message (Dict[str, Any]): 전송할 메시지
            
        Returns:
            bool: 메시지 전송 성공 여부
        """
        if not self.connected:
            result = await self.connect()
            if not result:
                return False
        
        try:
            # 메시지 직렬화
            if not isinstance(message, str):
                message = json.dumps(message)
            
            await self.websocket.send(message)
            logger.debug(f"메시지 전송: {message}")
            return True
        except Exception as e:
            logger.error(f"메시지 전송 오류: {str(e)}")
            return False
    
    async def _receive_messages(self):
        """
        서버로부터 메시지 수신 및 처리
        """
        while self.keep_running:
            try:
                # 서버로부터 메시지 수신 및 JSON 파싱
                raw_message = await self.websocket.recv()
                message = json.loads(raw_message)
                
                # 메시지 유형에 따른 처리
                if message.get('trnm') == 'LOGIN':
                    if message.get('return_code') != 0:
                        logger.error(f"로그인 실패: {message.get('return_msg')}")
                        await self.disconnect()
                    else:
                        logger.info("로그인 성공")
                
                # PING 메시지 처리
                elif message.get('trnm') == 'PING':
                    await self.send_message(message)
                
                # 실시간 데이터 처리
                elif message.get('trnm') == 'REAL':
                    # 콜백 호출
                    for callback in self.callbacks.values():
                        if callable(callback):
                            callback(message)
                
                # 일반 메시지 처리
                elif message.get('trnm') != 'PING':
                    logger.debug(f"서버 응답 수신: {message}")
                    
                    # 콜백 호출
                    seq = message.get('seq')
                    if seq in self.callbacks and callable(self.callbacks[seq]):
                        self.callbacks[seq](message)
            
            except websockets.ConnectionClosed:
                logger.info("서버에 의해 연결이 닫혔습니다.")
                self.connected = False
                break
            except Exception as e:
                logger.error(f"메시지 수신 중 오류 발생: {str(e)}")
    
    async def disconnect(self):
        """
        WebSocket 연결 종료
        """
        self.keep_running = False
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            logger.info("WebSocket 서버와의 연결을 종료했습니다.")
    
    def register_callback(self, seq: str, callback):
        """
        콜백 함수 등록
        
        Args:
            seq (str): 조건검색식 일련번호
            callback (callable): 콜백 함수
        """
        self.callbacks[seq] = callback
    
    def unregister_callback(self, seq: str):
        """
        콜백 함수 등록 해제
        
        Args:
            seq (str): 조건검색식 일련번호
        """
        if seq in self.callbacks:
            del self.callbacks[seq] 