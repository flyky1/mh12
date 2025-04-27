#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ELW API 사용 예제

이 예제는 키움 OpenAPI의 ELW(주식워런트증권) 관련 기능 사용법을 보여줍니다.
주요 기능:
- ELW 기본 정보 조회
- ELW 시세 정보 조회
- ELW 민감도 지표 조회
- ELW 잔존일수/배당락 조회
- ELW 발행회사별 정보 조회
- ELW 가격 급등락 조회
- ELW 종목 검색
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

def print_separator(title):
    """구분선 출력 함수"""
    print("\n" + "=" * 50)
    print(f" {title} ".center(50, "="))
    print("=" * 50 + "\n")

def example_get_elw_info():
    """ELW 기본 정보 조회 예제"""
    print_separator("ELW 기본 정보 조회")
    
    # 삼성전자 콜 ELW (예시 종목코드)
    symbol = "57JBHH"  # 실제 환경에서는 유효한 ELW 종목코드로 변경 필요
    
    try:
        # ELW 기본 정보 조회
        result = api.get_elw_info(symbol)
        
        if result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            print(f"기초자산: {result.get('base_asset', '')}")
            print(f"권리유형: {result.get('right_type', '')}")
            print(f"행사가격: {result.get('exercise_price', '')}")
            print(f"만기일: {result.get('exercise_date', '')}")
            print(f"잔존일수: {result.get('remain_days', '')}")
            print(f"발행회사: {result.get('issuer', '')}")
            
            # 민감도 지표
            print("\n민감도 지표:")
            print(f"내재변동성(IV): {result.get('iv', '')}")
            print(f"델타: {result.get('delta', '')}")
            print(f"감마: {result.get('gamma', '')}")
            print(f"세타: {result.get('theta', '')}")
            print(f"베가: {result.get('vega', '')}")
            
            # 추가 정보가 있다면 출력
            print("\n추가 정보:")
            for key, value in result.items():
                if key not in ['name', 'base_asset', 'right_type', 'exercise_price', 
                              'exercise_date', 'remain_days', 'issuer', 'iv', 'delta', 
                              'gamma', 'theta', 'vega']:
                    print(f"{key}: {value}")
        else:
            print("ELW 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 정보 조회 실패: {e}")

def example_get_elw_price():
    """ELW 시세 정보 조회 예제"""
    print_separator("ELW 시세 정보 조회")
    
    # 삼성전자 콜 ELW (예시 종목코드)
    symbol = "57JBHH"  # 실제 환경에서는 유효한 ELW 종목코드로 변경 필요
    
    try:
        # ELW 시세 정보 조회
        result = api.get_elw_price(symbol)
        
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
            
            print("\n기초자산 정보:")
            print(f"기초자산 가격: {result.get('base_asset_price', '')}")
            print(f"기초자산 전일대비: {result.get('base_asset_change', '')}")
            
            print("\n가치 정보:")
            print(f"프리미엄: {result.get('premium', '')}")
            print(f"내재가치: {result.get('intrinsic_value', '')}")
            print(f"시간가치: {result.get('time_value', '')}")
        else:
            print("ELW 시세 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 시세 정보 조회 실패: {e}")

def example_get_elw_remain_days():
    """ELW 잔존일수/배당락 조회 예제"""
    print_separator("ELW 잔존일수/배당락 조회")
    
    # 삼성전자 콜 ELW (예시 종목코드)
    symbol = "57JBHH"  # 실제 환경에서는 유효한 ELW 종목코드로 변경 필요
    
    try:
        # ELW 잔존일수/배당락 조회
        result = api.get_elw_remain_days(symbol)
        
        if result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            print(f"만기일: {result.get('exercise_date', '')}")
            print(f"잔존일수: {result.get('remain_days', '')}")
            
            print("\n배당락 정보:")
            print(f"배당락일: {result.get('dividend_ex_date', '')}")
            print(f"배당금액: {result.get('dividend_amount', '')}")
            print(f"배당영향: {result.get('dividend_impact', '')}")
        else:
            print("ELW 잔존일수/배당락 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 잔존일수/배당락 조회 실패: {e}")

def example_get_elw_by_issuer():
    """ELW 발행회사별 정보 조회 예제"""
    print_separator("ELW 발행회사별 정보 조회")
    
    # 발행회사 코드 (예: 한국투자증권)
    issuer_code = "3"
    
    try:
        # ELW 발행회사별 정보 조회
        result = api.get_elw_by_issuer(issuer_code)
        
        if result and 'elw_list' in result:
            print(f"발행회사: {result.get('issuer', '')}")
            elw_list = result['elw_list']
            print(f"발행 ELW 수: {len(elw_list)}")
            
            print("\n발행 ELW 목록 (상위 10개):")
            for i, elw in enumerate(elw_list[:10], 1):
                print(f"{i}. 코드: {elw.get('code', '')}, "
                     f"종목명: {elw.get('name', '')}, "
                     f"기초자산: {elw.get('base_asset', '')}, "
                     f"권리유형: {elw.get('right_type', '')}, "
                     f"행사가격: {elw.get('exercise_price', '')}")
            
            # 권리유형별 분류
            right_types = {}
            for elw in elw_list:
                right_type = elw.get('right_type', '기타')
                if right_type not in right_types:
                    right_types[right_type] = 0
                right_types[right_type] += 1
            
            print("\n권리유형별 분류:")
            for right_type, count in right_types.items():
                print(f"{right_type}: {count}개")
        else:
            print("ELW 발행회사별 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 발행회사별 정보 조회 실패: {e}")

def example_get_elw_sensitivity():
    """ELW 민감도 지표 조회 예제"""
    print_separator("ELW 민감도 지표 조회")
    
    # 삼성전자 콜 ELW (예시 종목코드)
    symbol = "57JBHH"  # 실제 환경에서는 유효한 ELW 종목코드로 변경 필요
    
    try:
        # ELW 민감도 지표 조회
        result = api.get_elw_sensitivity(symbol)
        
        if result and 'sensitivity_list' in result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            
            sensitivity_list = result['sensitivity_list']
            print("\n민감도 지표 (최근 5개):")
            for i, sens in enumerate(sensitivity_list[:5], 1):
                print(f"{i}. 시간: {sens.get('time', '')}")
                print(f"   현재가: {sens.get('price', '')}")
                print(f"   이론가: {sens.get('theoretical_price', '')}")
                print(f"   IV: {sens.get('iv', '')}")
                print(f"   델타: {sens.get('delta', '')}")
                print(f"   감마: {sens.get('gamma', '')}")
                print(f"   세타: {sens.get('theta', '')}")
                print(f"   베가: {sens.get('vega', '')}")
                print(f"   로: {sens.get('rho', '')}")
                print(f"   LP: {sens.get('lp', '')}")
                print("")
            
            # 데이터프레임으로 변환 예시
            if len(sensitivity_list) > 0:
                print("\n데이터프레임 변환 예시:")
                df = pd.DataFrame(sensitivity_list)
                print(df.head())
        else:
            print("ELW 민감도 지표를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 민감도 지표 조회 실패: {e}")

def example_get_elw_daily_sensitivity():
    """ELW 일별 민감도 지표 조회 예제"""
    print_separator("ELW 일별 민감도 지표 조회")
    
    # 삼성전자 콜 ELW (예시 종목코드)
    symbol = "57JBHH"  # 실제 환경에서는 유효한 ELW 종목코드로 변경 필요
    
    try:
        # ELW 일별 민감도 지표 조회
        result = api.get_elw_daily_sensitivity(symbol)
        
        if result and 'daily_sensitivity_list' in result:
            print(f"종목코드: {symbol}")
            print(f"종목명: {result.get('name', '')}")
            
            daily_sensitivity_list = result['daily_sensitivity_list']
            print("\n일별 민감도 지표 (최근 5일):")
            for i, sens in enumerate(daily_sensitivity_list[:5], 1):
                print(f"{i}. 날짜: {sens.get('date', '')}")
                print(f"   IV: {sens.get('iv', '')}")
                print(f"   델타: {sens.get('delta', '')}")
                print(f"   감마: {sens.get('gamma', '')}")
                print(f"   세타: {sens.get('theta', '')}")
                print(f"   베가: {sens.get('vega', '')}")
                print(f"   로: {sens.get('rho', '')}")
                print(f"   LP: {sens.get('lp', '')}")
                print("")
            
            # 데이터프레임으로 변환 예시
            if len(daily_sensitivity_list) > 0:
                print("\n데이터프레임 변환 예시:")
                df = pd.DataFrame(daily_sensitivity_list)
                print(df.head())
        else:
            print("ELW 일별 민감도 지표를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 일별 민감도 지표 조회 실패: {e}")

def example_get_elw_price_change():
    """ELW 가격 급등락 조회 예제"""
    print_separator("ELW 가격 급등락 조회")
    
    try:
        # ELW 가격 급등 조회 (1일전 기준, 5% 이상 급등, 전체 발행사/기초자산)
        result = api.get_elw_price_change(
            change_type="1",  # 급등
            time_type="2",    # 일전
            time_value="1",   # 1일
            volume_type="0",  # 전체 거래량
            issuer_code="000000000000",  # 전체 발행회사
            base_asset_code="000000000000"  # 전체 기초자산
        )
        
        if result and 'elw_list' in result:
            elw_list = result['elw_list']
            print(f"급등 ELW 수: {len(elw_list)}")
            
            print("\n급등 ELW 목록 (상위 10개):")
            for i, elw in enumerate(elw_list[:10], 1):
                print(f"{i}. 코드: {elw.get('code', '')}, "
                     f"종목명: {elw.get('name', '')}, "
                     f"현재가: {elw.get('price', '')}, "
                     f"등락률: {elw.get('change_rate', '')}%, "
                     f"거래량: {elw.get('volume', '')}")
            
            # 발행회사별 분류
            issuers = {}
            for elw in elw_list:
                issuer = elw.get('issuer', '기타')
                if issuer not in issuers:
                    issuers[issuer] = 0
                issuers[issuer] += 1
            
            print("\n발행회사별 분류:")
            for issuer, count in issuers.items():
                print(f"{issuer}: {count}개")
            
            # 데이터프레임으로 변환 예시
            if len(elw_list) > 0:
                print("\n데이터프레임 변환 예시:")
                df = pd.DataFrame(elw_list)
                print(df.head())
        else:
            print("ELW 가격 급등락 정보를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 가격 급등락 조회 실패: {e}")

def example_search_elw():
    """ELW 종목 검색 예제"""
    print_separator("ELW 종목 검색")
    
    # 삼성전자 콜 ELW 검색
    query = "삼성전자"
    right_type = "C"  # 콜 옵션
    
    try:
        # ELW 종목 검색
        result = api.search_elw(query, right_type)
        
        if result and 'elw_list' in result:
            elw_list = result['elw_list']
            print(f"검색 결과 수: {len(elw_list)}")
            
            print("\n검색 결과 (상위 10개):")
            for i, elw in enumerate(elw_list[:10], 1):
                print(f"{i}. 코드: {elw.get('code', '')}, "
                     f"종목명: {elw.get('name', '')}, "
                     f"기초자산: {elw.get('base_asset', '')}, "
                     f"권리유형: {elw.get('right_type', '')}, "
                     f"행사가격: {elw.get('exercise_price', '')}, "
                     f"만기일: {elw.get('exercise_date', '')}")
            
            # 행사가격별 분류
            exercise_prices = {}
            for elw in elw_list:
                exercise_price = elw.get('exercise_price', '기타')
                if exercise_price not in exercise_prices:
                    exercise_prices[exercise_price] = 0
                exercise_prices[exercise_price] += 1
            
            print("\n행사가격별 분류:")
            for exercise_price, count in exercise_prices.items():
                print(f"{exercise_price}: {count}개")
        else:
            print("ELW 종목 검색 결과를 조회할 수 없습니다.")
    
    except Exception as e:
        logger.error(f"ELW 종목 검색 실패: {e}")

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
        example_get_elw_info()
        example_get_elw_price()
        example_get_elw_remain_days()
        example_get_elw_by_issuer()
        example_get_elw_sensitivity()
        example_get_elw_daily_sensitivity()
        example_get_elw_price_change()
        example_search_elw()
        
    except Exception as e:
        logger.exception(f"예제 실행 중 오류 발생: {e}") 