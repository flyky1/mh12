#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
종목정보 조회 예제

이 예제는 키움 OpenAPI를 사용하여 국내 및 해외 주식의 종목 정보를 조회하는 방법을 보여줍니다.
"""

import os
import json
from datetime import datetime, timedelta
import pandas as pd
from tabulate import tabulate

# 프로젝트 루트 경로를 파이썬 경로에 추가
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom import KiwoomOpenAPI


def print_response(response, title='응답'):
    """응답 데이터를 예쁘게 출력"""
    print(f"\n===== {title} =====")
    if isinstance(response, dict) and 'data' in response:
        # 데이터가 너무 많을 경우 일부만 출력
        if isinstance(response['data'], list) and len(response['data']) > 5:
            print(f"상태: {response.get('status', 'N/A')}")
            print(f"메시지: {response.get('message', 'N/A')}")
            print(f"데이터: (처음 5개 항목만 표시)")
            for item in response['data'][:5]:
                print(f"  {item}")
            print(f"  ... 외 {len(response['data'])-5}개 항목")
        else:
            print(json.dumps(response, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(response, indent=2, ensure_ascii=False))
    print("=" * (len(title) + 13))


def print_table(data, title='데이터 테이블'):
    """데이터를 테이블 형식으로 출력"""
    if not data or not isinstance(data, list) or not data:
        print(f"출력할 {title} 데이터가 없습니다.")
        return
    
    # 데이터프레임 생성
    df = pd.DataFrame(data)
    
    # 테이블 출력
    print(f"\n===== {title} =====")
    print(tabulate(df.head(), headers='keys', tablefmt='psql'))
    if len(df) > 5:
        print(f"... 외 {len(df)-5}개 항목")
    print("=" * (len(title) + 13))


def main():
    """메인 함수"""
    # KiwoomOpenAPI 인스턴스 생성
    api = KiwoomOpenAPI()
    
    # 로그인 인증
    auth_result = api.auth_login()
    print_response(auth_result, "인증 결과")
    
    if auth_result['status'] != 'success':
        print("인증에 실패했습니다. 프로그램을 종료합니다.")
        return
    
    # 1. 국내 주식 종목 기본정보 조회 (삼성전자: 005930)
    print("\n1. 국내 주식 종목 기본정보 조회 (삼성전자)")
    stock_info = api.get_stock_info('005930')
    print_response(stock_info, "삼성전자 기본정보")
    
    # 2. 해외 주식 종목 기본정보 조회 (애플: AAPL, 나스닥: NAS)
    print("\n2. 해외 주식 종목 기본정보 조회 (애플)")
    overseas_stock_info = api.get_overseas_stock_info('AAPL', 'NAS')
    print_response(overseas_stock_info, "애플 기본정보")
    
    # 3. 거래정지종목 조회
    print("\n3. 거래정지종목 조회")
    suspended_stocks = api.get_suspended_stocks()
    print_response(suspended_stocks, "거래정지종목 목록")
    
    # 4. 관리종목 조회
    print("\n4. 관리종목 조회")
    managed_stocks = api.get_managed_stocks()
    print_response(managed_stocks, "관리종목 목록")
    
    # 5. 종목별 공시정보 조회 (삼성전자, 최근 7일)
    print("\n5. 종목별 공시정보 조회 (삼성전자, 최근 7일)")
    today = datetime.now().strftime('%Y%m%d')
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y%m%d')
    disclosure_info = api.get_stock_disclosure('005930', week_ago, today)
    print_response(disclosure_info, "삼성전자 공시정보")
    
    # 6. 종목 검색 (검색어: "삼성")
    print("\n6. 종목 검색 (검색어: '삼성')")
    search_result = api.search_stock("삼성")
    print_response(search_result, "검색 결과")
    
    # 7. 해외 종목 검색 (검색어: "Apple")
    print("\n7. 해외 종목 검색 (검색어: 'Apple')")
    overseas_search_result = api.search_overseas_stock("Apple")
    print_response(overseas_search_result, "해외 종목 검색 결과")
    
    # 8. 종목 재무정보 조회 (삼성전자)
    print("\n8. 종목 재무정보 조회 (삼성전자)")
    financial_info = api.get_stock_financial_info('005930')
    print_response(financial_info, "삼성전자 재무정보")
    
    # 9. 종목별 투자자 동향 조회 (삼성전자, 최근 30일)
    print("\n9. 종목별 투자자 동향 조회 (삼성전자, 최근 30일)")
    month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    investor_trend = api.get_stock_investor_trend('005930', month_ago, today)
    print_response(investor_trend, "삼성전자 투자자 동향")
    
    # 10. 시장별 종목 목록 조회 (KOSPI)
    print("\n10. 시장별 종목 목록 조회 (KOSPI)")
    kospi_stocks = api.get_market_stock_list('KOSPI')
    print_response(kospi_stocks, "KOSPI 종목 목록")
    
    # 11. 업종별 종목 목록 조회 (반도체)
    print("\n11. 업종별 종목 목록 조회 (반도체 업종)")
    semiconductor_stocks = api.get_industry_stock_list('03')  # 반도체 업종 코드 예시
    print_response(semiconductor_stocks, "반도체 업종 종목 목록")
    
    # 12. 종목 시세정보 상세 조회 (삼성전자)
    print("\n12. 종목 시세정보 상세 조회 (삼성전자)")
    price_info = api.get_stock_price_info('005930')
    print_response(price_info, "삼성전자 시세정보")


if __name__ == "__main__":
    main() 