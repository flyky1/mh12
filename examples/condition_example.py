#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 조건검색 예제

이 예제는 키움 OpenAPI를 통해 조건검색을 실행하고 결과를 조회하는 방법을 보여줍니다.
사용자가 저장한 조건검색식 목록을 조회하고, 특정 조건검색식을 실행하여 결과를 확인합니다.
"""

import os
import sys
import asyncio
import websockets
import json
import pandas as pd
from pprint import pprint

# 상위 디렉토리 추가 (프로젝트 루트 디렉토리)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom import KiwoomOpenAPI


def example_get_condition_list():
    """저장된 조건검색식 목록 조회 예제"""
    
    print("\n===== 조건검색식 목록 조회 =====")
    
    # 키움 OpenAPI 인스턴스 생성
    kiwoom = KiwoomOpenAPI()
    
    # 로그인
    result = kiwoom.auth_login()
    if result['status'] != 'success':
        print("로그인에 실패했습니다:", result['message'])
        return
    
    print("로그인에 성공했습니다.")
    
    # 조건검색식 목록 조회
    condition_list = kiwoom.condition.get_condition_list()
    
    if 'data' in condition_list and condition_list['data']:
        conditions = condition_list['data']
        print(f"총 {len(conditions)}개의 조건검색식이 있습니다.")
        
        # 조건검색식 목록 출력
        for i, condition in enumerate(conditions, 1):
            print(f"{i}. 일련번호: {condition.get('seq', '정보 없음')}")
            print(f"   조건명: {condition.get('name', '정보 없음')}")
            print("")
    else:
        print("조건검색식 목록을 조회할 수 없거나 저장된 조건검색식이 없습니다.")


def example_search_condition():
    """조건검색 실행 예제"""
    
    print("\n===== 조건검색 실행 =====")
    
    # 키움 OpenAPI 인스턴스 생성
    kiwoom = KiwoomOpenAPI()
    
    # 로그인
    result = kiwoom.auth_login()
    if result['status'] != 'success':
        print("로그인에 실패했습니다:", result['message'])
        return
    
    print("로그인에 성공했습니다.")
    
    # 조건검색식 목록 조회
    condition_list = kiwoom.condition.get_condition_list()
    
    if 'data' not in condition_list or not condition_list['data']:
        print("조건검색식 목록을 조회할 수 없거나 저장된 조건검색식이 없습니다.")
        return
    
    # 첫 번째 조건식 선택 (실제 사용 시에는 사용자가 선택하도록 변경 필요)
    condition_seq = condition_list['data'][0]['seq']
    condition_name = condition_list['data'][0]['name']
    
    print(f"조건검색식 '{condition_name}' (일련번호: {condition_seq})를 실행합니다.")
    
    # 조건검색 실행
    search_result = kiwoom.condition.search_condition(
        condition_seq=condition_seq,
        search_type='0',  # 일반 조건검색
        market_type='K',  # KRX 시장
        continue_search='N',
        next_key=''
    )
    
    if 'data' in search_result and search_result['data']:
        stocks = search_result['data']
        print(f"조건검색 결과: 총 {len(stocks)}개 종목 발견")
        
        # 상위 10개 종목만 출력
        for i, stock in enumerate(stocks[:10], 1):
            print(f"{i}. 종목코드: {stock.get('9001', '정보 없음')}")
            print(f"   종목명: {stock.get('302', '정보 없음')}")
            print(f"   현재가: {stock.get('10', '정보 없음')}")
            print(f"   전일대비: {stock.get('11', '정보 없음')} ({stock.get('12', '정보 없음')}%)")
            print(f"   거래량: {stock.get('13', '정보 없음')}")
            print("")
        
        # 데이터프레임으로 변환하여 분석
        if len(stocks) > 0:
            df = pd.DataFrame(stocks)
            
            # 컬럼명을 보기 좋게 변환
            columns_mapping = {
                '9001': '종목코드',
                '302': '종목명',
                '10': '현재가',
                '11': '전일대비',
                '12': '등락률',
                '13': '거래량',
                '16': '시가',
                '17': '고가',
                '18': '저가'
            }
            
            # 컬럼이 존재하는 경우에만 이름 변경
            rename_cols = {k: v for k, v in columns_mapping.items() if k in df.columns}
            if rename_cols:
                df = df.rename(columns=rename_cols)
            
            # 숫자형 컬럼 변환
            for col in ['현재가', '전일대비', '등락률', '거래량', '시가', '고가', '저가']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 등락률 기준 상위 5개 종목
            if '등락률' in df.columns:
                print("\n등락률 상위 5개 종목:")
                top_rise = df.sort_values(by='등락률', ascending=False).head(5)
                
                # 출력할 컬럼 선택
                display_cols = [col for col in ['종목명', '종목코드', '현재가', '등락률', '거래량'] if col in top_rise.columns]
                print(top_rise[display_cols])
    else:
        print("조건검색 결과가 없습니다.")


async def example_real_time_condition():
    """실시간 조건검색 예제"""
    
    print("\n===== 실시간 조건검색 =====")
    print("* 참고: 실시간 조건검색은 WebSocket 연결이 필요합니다.")
    print("* 이 예제는 실제 WebSocket 연결 없이 동작 방식만 설명합니다.")
    
    # 키움 OpenAPI 인스턴스 생성
    kiwoom = KiwoomOpenAPI()
    
    # 로그인
    result = kiwoom.auth_login()
    if result['status'] != 'success':
        print("로그인에 실패했습니다:", result['message'])
        return
    
    print("로그인에 성공했습니다.")
    
    # 조건검색식 목록 조회
    condition_list = kiwoom.condition.get_condition_list()
    
    if 'data' not in condition_list or not condition_list['data']:
        print("조건검색식 목록을 조회할 수 없거나 저장된 조건검색식이 없습니다.")
        return
    
    # 첫 번째 조건식 선택 (실제 사용 시에는 사용자가 선택하도록 변경 필요)
    condition_seq = condition_list['data'][0]['seq']
    condition_name = condition_list['data'][0]['name']
    
    print(f"조건검색식 '{condition_name}' (일련번호: {condition_seq})를 실시간으로 등록합니다.")
    
    # 실제 구현 시에는 WebSocket 연결 객체 생성 필요
    # ws = await websockets.connect("wss://api.kiwoom.com:10000/api/dostk/websocket")
    
    # 원래는 실시간 조건검색 등록을 호출해야 함
    # kiwoom.condition.register_real_condition(ws, condition_seq, condition_name, search_type='1')
    
    print("실시간 조건검색이 등록되었습니다. (가상 데모)")
    print("실시간 조건검색 시 다음과 같은 형태로 데이터가 수신됩니다:")
    
    # 샘플 데이터
    sample_data = {
        'trnm': 'REAL',
        'type': '0A',
        'name': '종목코드',
        'values': {
            '841': '1',  # 신호종류 (1: 진입, 2: 이탈)
            '9001': '005930',  # 종목코드
            '843': '1',  # 삽입삭제 구분
            '20': '153045',  # 체결시간
            '907': '2'  # 매도/매수 구분
        }
    }
    
    print(json.dumps(sample_data, indent=2, ensure_ascii=False))
    
    print("\n실시간 조건검색은 위와 같은 형태로 종목의 진입/이탈 정보를 수신합니다.")
    print("values.841 값이 1이면 종목 진입, 2이면 종목 이탈을 의미합니다.")
    
    # 실제 구현 시에는 일정 시간 후 해제
    await asyncio.sleep(3)
    
    print("\n실시간 조건검색을 해제합니다. (가상 데모)")
    # kiwoom.condition.unregister_real_condition(ws, condition_seq, condition_name)
    
    # 실제 구현 시에는 WebSocket 연결 종료 처리
    # await ws.close()


def main():
    """조건검색 예제 메인 함수"""
    
    print("키움 OpenAPI 조건검색 예제를 시작합니다.")
    
    # 조건검색식 목록 조회
    example_get_condition_list()
    
    # 조건검색 실행
    example_search_condition()
    
    # 실시간 조건검색 (비동기 함수 실행)
    try:
        asyncio.run(example_real_time_condition())
    except Exception as e:
        print(f"실시간 조건검색 예제 실행 중 오류 발생: {str(e)}")
    
    print("\n조건검색 예제가 완료되었습니다.")


if __name__ == "__main__":
    main() 