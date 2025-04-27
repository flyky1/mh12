#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 API 실시간시세 예제
"""

import os
import json
import asyncio
from kiwoom_api import KiwoomClient

# 환경변수에서 API 키 가져오기
appkey = os.environ.get('kiwoom_appkey')
secretkey = os.environ.get('kiwoom_secretkey')

# 콜백 함수 정의
def on_current_price(data):
    """현재가 실시간 데이터 수신 콜백"""
    print(f"\n[실시간 현재가] {json.dumps(data, indent=2, ensure_ascii=False)}")

def on_askbid(data):
    """호가 실시간 데이터 수신 콜백"""
    print(f"\n[실시간 호가] {json.dumps(data, indent=2, ensure_ascii=False)}")

def on_transaction(data):
    """체결 실시간 데이터 수신 콜백"""
    print(f"\n[실시간 체결] {json.dumps(data, indent=2, ensure_ascii=False)}")

async def main():
    # 클라이언트 초기화
    client = KiwoomClient(appkey, secretkey, is_mock=True)
    
    # 실시간 클라이언트 생성
    realtime_client = client.get_realtime_client()
    
    # 콜백 함수 등록
    # 실시간 시세 항목은 '실시간시세.txt' 파일에서 확인
    realtime_client.add_callback('00', on_transaction)  # 주문체결
    realtime_client.add_callback('01', on_current_price)  # 현재가
    realtime_client.add_callback('02', on_askbid)  # 호가
    
    # 실시간 클라이언트 실행 (백그라운드에서 실행)
    background_task = asyncio.create_task(realtime_client.run())
    
    # 잠시 대기
    await asyncio.sleep(2)
    
    # 삼성전자 실시간 시세 등록
    stock_codes = ['005930']  # 삼성전자
    real_types = ['01', '02']  # 현재가, 호가
    
    print("실시간 데이터 등록 중...")
    await realtime_client.register_realtime(stock_codes, real_types)
    
    # 60초 동안 실시간 데이터 수신
    print("60초 동안 실시간 데이터 수신...")
    await asyncio.sleep(60)
    
    # 실시간 시세 해지
    print("실시간 데이터 해지 중...")
    await realtime_client.unregister_realtime(stock_codes, real_types)
    
    # 연결 종료
    print("연결 종료 중...")
    await realtime_client.disconnect()
    
    # 백그라운드 태스크 종료 대기
    await asyncio.wait([background_task])

if __name__ == '__main__':
    asyncio.run(main()) 