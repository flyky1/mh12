#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ETF API 사용 예제

이 예제는 키움 OpenAPI의 ETF 관련 기능 사용법을 보여줍니다.
주요 기능:
- ETF 기본 정보 조회
- ETF 구성종목 조회
- ETF NAV 조회
- ETF 시세 정보 조회
- ETF 목록 조회
- ETF 일별 시세 조회
"""

import os
import sys
import json
import logging
import pandas as pd
from pprint import pprint
from datetime import datetime, timedelta

# 상위 디렉토리 추가 (kiwoom 패키지 import를 위해)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom import KiwoomOpenAPI

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 날짜 설정
today = datetime.now()
start_date = (today - timedelta(days=30)).strftime('%Y%m%d')
end_date = today.strftime('%Y%m%d')

def print_separator(title):
    """구분선 출력 함수"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def example_get_etf_info():
    """ETF 기본 정보 조회 예제"""
    print_separator("ETF 기본 정보 조회")
    
    # KODEX 200 ETF (069500)
    symbol = "069500"
    
    try:
        # ETF 기본 정보 조회
        result = api.get_etf_info(symbol)
        
        if result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('stk_nm', '')}")
            print(f"기초지수: {result.get('etfobjt_idex_nm', '')}")
            print(f"과세유형: {result.get('etftxon_type', '')}")
            print(f"원주가격: {result.get('wonju_pric', '')}")
            
            # 추가 정보가 있다면 출력
            print("\n추가 정보:")
            for key, value in result.items():
                if key not in ['stk_nm', 'etfobjt_idex_nm', 'etftxon_type', 'wonju_pric']:
                    print(f"{key}: {value}")
        else:
            print("ETF 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF 정보 조회 실패: {e}")

def example_get_etf_components():
    """ETF 구성종목 조회 예제"""
    print_separator("ETF 구성종목 조회")
    
    # KODEX 200 ETF (069500)
    symbol = "069500"
    
    try:
        # ETF 구성종목 조회
        result = api.get_etf_components(symbol)
        
        if result and 'component_list' in result:
            print(f"ETF 종목코드: {symbol}")
            print(f"ETF 종목명: {result.get('etf_name', '')}")
            print(f"\n구성종목 목록 (상위 10개):")
            
            components = result['component_list']
            for i, component in enumerate(components[:10], 1):
                print(f"{i}. 코드: {component.get('code', '')}, "
                     f"종목명: {component.get('name', '')}, "
                     f"비중: {component.get('weight', '')}%, "
                     f"수량: {component.get('quantity', '')}")
            
            print(f"\n총 {len(components)}개 종목")
        else:
            print("ETF 구성종목을 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF 구성종목 조회 실패: {e}")

def example_get_etf_nav():
    """ETF NAV 조회 예제"""
    print_separator("ETF NAV 조회")
    
    # KODEX 200 ETF (069500)
    symbol = "069500"
    
    try:
        # ETF NAV 조회
        result = api.get_etf_nav(symbol)
        
        if result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            print(f"NAV: {result.get('nav', '')}")
            print(f"NAV 산출일자: {result.get('nav_date', '')}")
            print(f"NAV 산출시간: {result.get('nav_time', '')}")
            print(f"현재가: {result.get('price', '')}")
            print(f"괴리율: {result.get('premium', '')}%")
            print(f"추적오차: {result.get('tracking_error', '')}%")
            
            if 'hist_nav' in result and result['hist_nav']:
                print("\n과거 NAV 기록 (최근 5일):")
                for i, nav_data in enumerate(result['hist_nav'][:5], 1):
                    print(f"{i}. 날짜: {nav_data.get('date', '')}, "
                         f"NAV: {nav_data.get('nav', '')}, "
                         f"종가: {nav_data.get('price', '')}, "
                         f"괴리율: {nav_data.get('premium', '')}%")
        else:
            print("ETF NAV 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF NAV 조회 실패: {e}")

def example_get_etf_price():
    """ETF 시세 정보 조회 예제"""
    print_separator("ETF 시세 정보 조회")
    
    # KODEX 200 ETF (069500)
    symbol = "069500"
    
    try:
        # ETF 시세 정보 조회
        result = api.get_etf_price(symbol)
        
        if result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            print(f"현재가: {result.get('price', '')}")
            print(f"전일대비: {result.get('change', '')}")
            print(f"등락률: {result.get('change_rate', '')}%")
            print(f"시가: {result.get('open', '')}")
            print(f"고가: {result.get('high', '')}")
            print(f"저가: {result.get('low', '')}")
            print(f"거래량: {result.get('volume', '')}")
            print(f"거래대금: {result.get('value', '')}")
            print(f"시가총액: {result.get('market_cap', '')}")
            print(f"순자산가치: {result.get('nav', '')}")
            print(f"괴리율: {result.get('premium', '')}%")
        else:
            print("ETF 시세 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF 시세 정보 조회 실패: {e}")

def example_get_etf_list():
    """ETF 목록 조회 예제"""
    print_separator("ETF 목록 조회")
    
    try:
        # 전체 ETF 목록 조회
        result = api.get_etf_list()
        
        if result and 'etf_list' in result:
            etf_list = result['etf_list']
            print(f"전체 ETF 수: {len(etf_list)}")
            print("\n상위 10개 ETF:")
            
            for i, etf in enumerate(etf_list[:10], 1):
                print(f"{i}. 코드: {etf.get('code', '')}, "
                     f"종목명: {etf.get('name', '')}, "
                     f"ETF 유형: {etf.get('etf_type', '')}, "
                     f"기초지수: {etf.get('base_index', '')}, "
                     f"운용사: {etf.get('company', '')}")
            
            # 유형별 분류
            etf_types = {}
            for etf in etf_list:
                etf_type = etf.get('etf_type', '기타')
                if etf_type not in etf_types:
                    etf_types[etf_type] = 0
                etf_types[etf_type] += 1
            
            print("\nETF 유형별 분류:")
            for etf_type, count in etf_types.items():
                print(f"{etf_type}: {count}개")
        else:
            print("ETF 목록을 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF 목록 조회 실패: {e}")

def example_get_etf_price_by_date():
    """ETF 일별 시세 조회 예제"""
    print_separator("ETF 일별 시세 조회")
    
    # KODEX 200 ETF (069500)
    symbol = "069500"
    
    try:
        # ETF 일별 시세 조회
        result = api.get_etf_price_by_date(symbol, start_date, end_date)
        
        if result and 'price_list' in result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            print(f"조회기간: {start_date} ~ {end_date}")
            print(f"\n일별 시세 데이터 (최근 5일):")
            
            price_list = result['price_list']
            for i, price_data in enumerate(price_list[:5], 1):
                print(f"{i}. 날짜: {price_data.get('date', '')}, "
                     f"시가: {price_data.get('open', '')}, "
                     f"고가: {price_data.get('high', '')}, "
                     f"저가: {price_data.get('low', '')}, "
                     f"종가: {price_data.get('close', '')}, "
                     f"거래량: {price_data.get('volume', '')}")
            
            # 데이터프레임으로 변환 예시
            print("\n데이터프레임 변환 예시:")
            df = pd.DataFrame(price_list)
            print(df.head())
        else:
            print("ETF 일별 시세를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ETF 일별 시세 조회 실패: {e}")

if __name__ == "__main__":
    try:
        # KiwoomOpenAPI 인스턴스 생성
        api = KiwoomOpenAPI()
        
        # 로그인
        login_result = api.auth_login()
        if login_result['status'] != 'success':
            logger.error("로그인 실패")
            sys.exit(1)
        
        # 예제 실행
        example_get_etf_info()
        example_get_etf_components()
        example_get_etf_nav()
        example_get_etf_price()
        example_get_etf_list()
        example_get_etf_price_by_date()
        
    except Exception as e:
        logger.exception(f"예제 실행 중 오류 발생: {e}") 