#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움 OpenAPI 업종 정보 조회 예제

이 예제는 키움 OpenAPI를 통해 업종 정보를 조회하는 방법을 보여줍니다.
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
    """업종 정보 조회 예제 메인 함수"""
    
    print("키움 OpenAPI 업종 정보 조회 예제를 시작합니다.")
    
    # 키움 OpenAPI 인스턴스 생성
    kiwoom = KiwoomOpenAPI()
    
    # 로그인
    result = kiwoom.auth_login()
    if result['status'] != 'success':
        print("로그인에 실패했습니다:", result['message'])
        return
    
    print("로그인에 성공했습니다.")
    
    # 예제 1: 코스피 지수 현재가 조회
    print("\n===== 코스피 지수 현재가 조회 =====")
    kospi_price = kiwoom.get_sector_price("0", "001")
    pprint(kospi_price)
    
    # 예제 2: 코스닥 지수 현재가 조회
    print("\n===== 코스닥 지수 현재가 조회 =====")
    kosdaq_price = kiwoom.get_sector_price("1", "101")
    pprint(kosdaq_price)
    
    # 예제 3: KOSPI200 지수 현재가 조회
    print("\n===== KOSPI200 지수 현재가 조회 =====")
    kospi200_price = kiwoom.get_sector_price("2", "201")
    pprint(kospi200_price)
    
    # 예제 4: 업종별 투자자 순매수 정보 조회 (코스피)
    print("\n===== 코스피 업종별 투자자 순매수 정보 조회 =====")
    today = datetime.datetime.now().strftime("%Y%m%d")
    kospi_investor_trend = kiwoom.get_sector_investor_trend("0", "0", today)
    pprint(kospi_investor_trend)
    
    # 예제 5: 업종별 투자자 순매수 정보 조회 (코스닥)
    print("\n===== 코스닥 업종별 투자자 순매수 정보 조회 =====")
    kosdaq_investor_trend = kiwoom.get_sector_investor_trend("1", "0", today)
    pprint(kosdaq_investor_trend)
    
    # 예제 6: 섹터 지수 정보 조회 (코스피)
    print("\n===== 코스피 섹터 지수 정보 조회 =====")
    kospi_sector_index = kiwoom.get_sector_index("0")
    pprint(kospi_sector_index)
    
    # 예제 7: 업종 구성 종목 조회 (코스피 전기전자)
    print("\n===== 코스피 전기전자 업종 구성 종목 조회 =====")
    electronics_components = kiwoom.get_sector_components("0", "008")
    pprint(electronics_components)
    
    # 예제 8: 업종 시세 정보 조회 (코스피 전기전자)
    print("\n===== 코스피 전기전자 업종 시세 정보 조회 =====")
    electronics_price_info = kiwoom.get_sector_price_info("008")
    pprint(electronics_price_info)
    
    # 예제 9: 프로그램 매매 정보 조회 (삼성전자)
    print("\n===== 삼성전자 프로그램 매매 정보 조회 =====")
    samsung_program_trading = kiwoom.get_sector_program_trading("005930")
    pprint(samsung_program_trading)
    
    # 데이터프레임으로 변환하여 분석하는 예제
    print("\n===== 업종별 투자자 순매수 데이터프레임 변환 예제 =====")
    try:
        # 업종별 투자자 순매수 정보를 가져와서 데이터프레임으로 변환
        sector_investor_data = kiwoom.get_sector_investor_trend("0", "0", today)
        
        # API 응답 구조에 따라 적절히 추출
        if 'inds_netprps' in sector_investor_data:
            df = pd.DataFrame(sector_investor_data['inds_netprps'])
            print(df.head())
            
            # 외국인 순매수 상위 5개 업종
            if 'frgnr_netprps' in df.columns and 'inds_nm' in df.columns:
                df['frgnr_netprps'] = pd.to_numeric(df['frgnr_netprps'], errors='coerce')
                top_foreign_buying = df.sort_values(by='frgnr_netprps', ascending=False)[['inds_nm', 'frgnr_netprps']].head(5)
                print("\n외국인 순매수 상위 5개 업종:")
                print(top_foreign_buying)
            
            # 기관 순매수 상위 5개 업종
            if 'orgn_netprps' in df.columns and 'inds_nm' in df.columns:
                df['orgn_netprps'] = pd.to_numeric(df['orgn_netprps'], errors='coerce')
                top_institution_buying = df.sort_values(by='orgn_netprps', ascending=False)[['inds_nm', 'orgn_netprps']].head(5)
                print("\n기관 순매수 상위 5개 업종:")
                print(top_institution_buying)
        else:
            print("적절한 업종별 투자자 순매수 데이터가 없습니다.")
    except Exception as e:
        print(f"데이터프레임 변환 중 오류 발생: {str(e)}")


if __name__ == "__main__":
    main() 