#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 테마 정보 조회 예제

이 예제는 키움 OpenAPI를 통해 테마 정보를 조회하는 방법을 보여줍니다.
"""

import os
import sys
import datetime
import pandas as pd
from pprint import pprint

# 상위 디렉토리 추가 (프로젝트 루트 디렉토리)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom import KiwoomOpenAPI


def main():
    """테마 정보 조회 예제 메인 함수"""
    
    print("키움 OpenAPI 테마 정보 조회 예제를 시작합니다.")
    
    # 키움 OpenAPI 인스턴스 생성
    kiwoom = KiwoomOpenAPI()
    
    # 로그인
    result = kiwoom.auth_login()
    if result['status'] != 'success':
        print("로그인에 실패했습니다:", result['message'])
        return
    
    print("로그인에 성공했습니다.")
    
    # 예제 1: 전체 테마 목록 조회
    print("\n===== 전체 테마 목록 조회 =====")
    theme_list = kiwoom.get_theme_list()
    
    if 'thema_grp' in theme_list:
        themes = theme_list['thema_grp']
        print(f"총 {len(themes)}개의 테마가 있습니다.")
        
        # 상위 10개 테마 출력
        print("\n상위 10개 테마:")
        for i, theme in enumerate(themes[:10], 1):
            print(f"{i}. 테마명: {theme.get('thema_nm', '정보 없음')}")
            print(f"   테마코드: {theme.get('thema_grp_cd', '정보 없음')}")
            print(f"   종목수: {theme.get('stk_num', '정보 없음')}")
            print(f"   등락률: {theme.get('flu_rt', '정보 없음')}%")
            print(f"   상승종목수: {theme.get('rising_stk_num', '정보 없음')}")
            print(f"   하락종목수: {theme.get('fall_stk_num', '정보 없음')}")
            print(f"   기간수익률: {theme.get('dt_prft_rt', '정보 없음')}%")
            print(f"   주요종목: {theme.get('main_stk', '정보 없음')}")
            print("")
    else:
        print("테마 목록을 조회할 수 없습니다.")
    
    # 예제 2: 특정 테마 검색 (예: '2차전지' 관련 테마)
    print("\n===== '2차전지' 관련 테마 검색 =====")
    battery_themes = kiwoom.search_themes("2차전지")
    
    if 'thema_grp' in battery_themes:
        themes = battery_themes['thema_grp']
        print(f"총 {len(themes)}개의 '2차전지' 관련 테마가 있습니다.")
        
        # 모든 2차전지 관련 테마 출력
        for i, theme in enumerate(themes, 1):
            print(f"{i}. 테마명: {theme.get('thema_nm', '정보 없음')}")
            print(f"   테마코드: {theme.get('thema_grp_cd', '정보 없음')}")
            print(f"   등락률: {theme.get('flu_rt', '정보 없음')}%")
            print(f"   종목수: {theme.get('stk_num', '정보 없음')}")
            print(f"   주요종목: {theme.get('main_stk', '정보 없음')}")
            print("")
    else:
        print("2차전지 관련 테마를 검색할 수 없습니다.")
    
    # 예제 3: 테마 구성 종목 조회 (예: 메타버스 테마)
    # 실제 테마 코드는 예시이므로 실행 시 유효한 테마 코드로 변경 필요
    theme_code = "238"  # 가상의 메타버스 테마 코드
    print(f"\n===== 테마 코드 {theme_code} 구성 종목 조회 =====")
    
    try:
        theme_stocks = kiwoom.get_theme_stocks(theme_code)
        
        # 테마 정보 출력
        print(f"등락률: {theme_stocks.get('flu_rt', '정보 없음')}%")
        print(f"기간수익률: {theme_stocks.get('dt_prft_rt', '정보 없음')}%")
        
        # 구성 종목 출력
        if 'thema_comp_stk' in theme_stocks:
            stocks = theme_stocks['thema_comp_stk']
            print(f"\n구성 종목 ({len(stocks)}개):")
            
            # 상위 10개 종목 출력
            for i, stock in enumerate(stocks[:10], 1):
                print(f"{i}. 종목명: {stock.get('stk_nm', '정보 없음')} ({stock.get('stk_cd', '정보 없음')})")
                print(f"   현재가: {stock.get('cur_prc', '정보 없음')}")
                print(f"   전일대비: {stock.get('pred_pre', '정보 없음')} ({stock.get('flu_rt', '정보 없음')}%)")
                print(f"   거래량: {stock.get('acc_trde_qty', '정보 없음')}")
                print("")
                
            # 데이터프레임으로 변환하여 분석
            df = pd.DataFrame(stocks)
            
            # 필요한 컬럼이 있을 경우에만 처리
            if 'cur_prc' in df.columns and 'flu_rt' in df.columns:
                # 문자열을 숫자로 변환
                df['cur_prc'] = pd.to_numeric(df['cur_prc'], errors='coerce')
                df['flu_rt'] = pd.to_numeric(df['flu_rt'], errors='coerce')
                
                # 등락률 기준 상위 5개 종목
                print("\n등락률 상위 5개 종목:")
                top_rise = df.sort_values(by='flu_rt', ascending=False).head(5)
                print(top_rise[['stk_nm', 'stk_cd', 'cur_prc', 'flu_rt']])
        else:
            print("테마 구성 종목을 조회할 수 없습니다.")
    except Exception as e:
        print(f"테마 구성 종목 조회 중 오류 발생: {str(e)}")
    
    # 예제 4: 종목별 테마 조회 (예: 삼성전자)
    print("\n===== 삼성전자 관련 테마 조회 =====")
    samsung_themes = kiwoom.get_stock_themes("005930")
    
    if 'thema_grp' in samsung_themes:
        themes = samsung_themes['thema_grp']
        print(f"삼성전자가 속한 테마는 총 {len(themes)}개입니다.")
        
        # 모든 테마 출력
        for i, theme in enumerate(themes, 1):
            print(f"{i}. 테마명: {theme.get('thema_nm', '정보 없음')}")
            print(f"   테마코드: {theme.get('thema_grp_cd', '정보 없음')}")
            print(f"   등락률: {theme.get('flu_rt', '정보 없음')}%")
            print(f"   기간수익률: {theme.get('dt_prft_rt', '정보 없음')}%")
            print(f"   주요종목: {theme.get('main_stk', '정보 없음')}")
            print("")
    else:
        print("삼성전자 관련 테마를 조회할 수 없습니다.")
    
    # 예제 5: 기간수익률 상위 테마 조회
    print("\n===== 기간수익률 상위 테마 조회 =====")
    top_themes = kiwoom.get_theme_list(flu_pl_amt_type='1')  # 상위기간수익률 기준
    
    if 'thema_grp' in top_themes:
        themes = top_themes['thema_grp']
        
        # 데이터프레임으로 변환하여 분석
        df = pd.DataFrame(themes)
        
        if 'dt_prft_rt' in df.columns and 'thema_nm' in df.columns:
            # 문자열을 숫자로 변환
            df['dt_prft_rt'] = pd.to_numeric(df['dt_prft_rt'], errors='coerce')
            
            # 기간수익률 기준 상위 10개 테마
            print("\n기간수익률 상위 10개 테마:")
            top_profit = df.sort_values(by='dt_prft_rt', ascending=False).head(10)
            
            for i, (_, row) in enumerate(top_profit.iterrows(), 1):
                print(f"{i}. 테마명: {row.get('thema_nm', '정보 없음')}")
                print(f"   기간수익률: {row.get('dt_prft_rt', '정보 없음')}%")
                print(f"   테마코드: {row.get('thema_grp_cd', '정보 없음')}")
                print(f"   종목수: {row.get('stk_num', '정보 없음')}")
                print("")
    else:
        print("기간수익률 상위 테마를 조회할 수 없습니다.")


if __name__ == "__main__":
    main() 