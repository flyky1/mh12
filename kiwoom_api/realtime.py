"""
키움증권 실시간시세 WebSocket 클라이언트
"""

import os
import json
import asyncio
import websockets
from typing import Dict, List, Callable, Any, Optional, Union

from .auth import KiwoomAuth, MOCK_HOST, REAL_HOST


class KiwoomRealtimeClient:
    """키움증권 실시간시세 WebSocket 클라이언트"""
    
    def __init__(self, 
                 token: str = None, 
                 appkey: str = None, 
                 secretkey: str = None, 
                 is_mock: bool = False,
                 auto_reconnect: bool = True,
                 ping_interval: int = 30):
        """
        실시간시세 WebSocket 클라이언트 초기화
        
        Args:
            token (str, optional): 접근 토큰. 기본값은 None (자동 발급)
            appkey (str, optional): API 앱키. 기본값은 환경변수 'kiwoom_appkey'에서 가져옴
            secretkey (str, optional): API 시크릿키. 기본값은 환경변수 'kiwoom_secretkey'에서 가져옴
            is_mock (bool, optional): 모의투자 여부. 기본값은 False
            auto_reconnect (bool, optional): 연결 끊김시 자동 재연결 여부. 기본값은 True
            ping_interval (int, optional): PING 메시지 전송 간격(초). 기본값은 30
        """
        self.auth = KiwoomAuth(appkey, secretkey, is_mock)
        host_domain = MOCK_HOST.replace('https://', '') if is_mock else REAL_HOST.replace('https://', '')
        self.websocket_url = f'wss://{host_domain}:10000/api/dostk/websocket'
        self.token = token
        self.websocket = None
        self.connected = False
        self.keep_running = True
        self.auto_reconnect = auto_reconnect
        self.ping_interval = ping_interval
        self.callbacks = {}
        
        # 토큰이 없으면 자동으로 발급
        if not self.token:
            self.token = self.auth.get_access_token()
    
    async def connect(self):
        """WebSocket 서버에 연결"""
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            self.connected = True
            print("서버와 연결을 시도 중입니다.")
            
            # 로그인 패킷
            login_message = {
                'trnm': 'LOGIN',
                'token': self.token
            }
            
            print('실시간 시세 서버로 로그인 패킷을 전송합니다.')
            await self.send_message(login_message)
            
            return True
        except Exception as e:
            print(f'Connection error: {e}')
            self.connected = False
            return False
    
    async def send_message(self, message):
        """
        서버에 메시지 전송
        
        Args:
            message: 전송할 메시지 (dict 또는 str)
        """
        if not self.connected:
            await self.connect()
            
        if self.connected:
            # message가 문자열이 아니면 JSON으로 직렬화
            if not isinstance(message, str):
                message = json.dumps(message)
                
            await self.websocket.send(message)
            print(f'Message sent: {message}')
    
    async def register_realtime(self, items: List[str], types: List[str], group_no: str = '1', refresh: str = '1'):
        """
        실시간시세 항목 등록
        
        Args:
            items (List[str]): 실시간 등록 요소 (종목코드 등)
            types (List[str]): 실시간 항목 (TR 코드)
            group_no (str, optional): 그룹번호. 기본값은 '1'
            refresh (str, optional): 기존등록유지여부. 기본값은 '1' (유지)
        """
        register_message = {
            'trnm': 'REG',
            'grp_no': group_no,
            'refresh': refresh,
            'data': [{
                'item': items,
                'type': types
            }]
        }
        
        await self.send_message(register_message)
    
    async def unregister_realtime(self, items: List[str], types: List[str], group_no: str = '1'):
        """
        실시간시세 항목 해지
        
        Args:
            items (List[str]): 실시간 등록 요소 (종목코드 등)
            types (List[str]): 실시간 항목 (TR 코드)
            group_no (str, optional): 그룹번호. 기본값은 '1'
        """
        unregister_message = {
            'trnm': 'REMOVE',
            'grp_no': group_no,
            'data': [{
                'item': items,
                'type': types
            }]
        }
        
        await self.send_message(unregister_message)
    
    def add_callback(self, realtime_type: str, callback: Callable[[Dict[str, Any]], None]):
        """
        실시간시세 수신 콜백 함수 추가
        
        Args:
            realtime_type (str): 실시간 항목 (TR 코드)
            callback (Callable): 콜백 함수 (인자로 실시간 데이터를 받음)
        """
        if realtime_type not in self.callbacks:
            self.callbacks[realtime_type] = []
            
        self.callbacks[realtime_type].append(callback)
    
    async def receive_messages(self):
        """서버로부터 메시지 수신 및 처리"""
        while self.keep_running:
            try:
                response = json.loads(await self.websocket.recv())
                
                # 로그인 응답 처리
                if response.get('trnm') == 'LOGIN':
                    if response.get('return_code') != 0:
                        print('로그인 실패하였습니다. : ', response.get('return_msg'))
                        await self.disconnect()
                    else:
                        print('로그인 성공하였습니다.')
                
                # PING 응답 처리
                elif response.get('trnm') == 'PING':
                    await self.send_message(response)
                
                # 실시간 데이터 처리
                elif response.get('trnm') == 'REAL':
                    self._process_realtime(response)
                
                # 디버깅용 로그 출력 (PING 제외)
                if response.get('trnm') != 'PING':
                    print(f'실시간 시세 서버 응답 수신: {response}')
                    
            except websockets.ConnectionClosed:
                print('Connection closed by the server')
                self.connected = False
                
                if self.auto_reconnect:
                    print('Attempting to reconnect...')
                    await asyncio.sleep(5)  # 재연결 시도 전 대기
                    await self.connect()
                else:
                    break
                    
            except Exception as e:
                print(f'Error in receive_messages: {e}')
                if self.auto_reconnect:
                    print('Attempting to reconnect...')
                    await asyncio.sleep(5)
                    await self.connect()
                else:
                    break
    
    def _process_realtime(self, data: Dict[str, Any]):
        """
        실시간 데이터 처리 및 콜백 호출
        
        Args:
            data (Dict[str, Any]): 수신된 실시간 데이터
        """
        try:
            for item_data in data.get('data', []):
                realtime_type = item_data.get('type')
                
                if realtime_type in self.callbacks:
                    for callback in self.callbacks[realtime_type]:
                        callback(item_data)
        except Exception as e:
            print(f'Error processing realtime data: {e}')
    
    async def disconnect(self):
        """WebSocket 연결 종료"""
        self.keep_running = False
        if self.connected and self.websocket:
            await self.websocket.close()
            self.connected = False
            print('Disconnected from WebSocket server')
    
    async def _ping_sender(self):
        """일정 간격으로 PING 메시지 전송"""
        while self.keep_running and self.connected:
            try:
                await asyncio.sleep(self.ping_interval)
                if self.connected:
                    await self.send_message({'trnm': 'PING'})
            except Exception as e:
                print(f'Error sending ping: {e}')
    
    async def run(self):
        """WebSocket 클라이언트 실행"""
        if await self.connect():
            # PING 전송 태스크 시작
            ping_task = asyncio.create_task(self._ping_sender())
            # 메시지 수신 태스크 시작
            receive_task = asyncio.create_task(self.receive_messages())
            
            # 모든 태스크가 완료될 때까지 대기
            await asyncio.gather(ping_task, receive_task)
        else:
            print("WebSocket 연결에 실패했습니다.") 