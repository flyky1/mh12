#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
차트 데이터 검색 예제

이 예제는 키움 OpenAPI를 사용하여 국내 및 해외 주식의 차트 데이터를 검색하는 방법을 보여줍니다.
"""

import os
import json
from datetime import datetime, timedelta
import pandas as pd
from matplotlib import pyplot as plt

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


def plot_chart_data(data, title="주가 차트"):
    """차트 데이터를 시각화"""
    if not data or 'data' not in data or not data['data']:
        print("시각화할 데이터가 없습니다.")
        return
    
    chart_data = data['data']
    
    # 데이터프레임 생성
    df = pd.DataFrame(chart_data)
    
    # stck_bsop_date 또는 bass_dt를 날짜 형식으로 변환
    date_column = 'stck_bsop_date' if 'stck_bsop_date' in df.columns else 'bass_dt'
    if date_column in df.columns:
        df[date_column] = pd.to_datetime(df[date_column])
        df = df.sort_values(by=date_column)
    
    # 종가 열 이름 결정
    close_column = None
    for possible_column in ['stck_prpr', 'ovrs_prpr', 'prpr']:
        if possible_column in df.columns:
            close_column = possible_column
            break
    
    if close_column is None:
        print("종가 데이터를 찾을 수 없습니다.")
        return
    
    # 차트 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(df[date_column], df[close_column])
    plt.title(title)
    plt.xlabel('날짜')
    plt.ylabel('가격')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


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
    
    # 국내 주식 일봉 데이터 검색 (삼성전자: 005930)
    print("\n1. 국내 주식 일봉 데이터 검색 (삼성전자)")
    today = datetime.now().strftime('%Y%m%d')
    three_months_ago = (datetime.now() - timedelta(days=90)).strftime('%Y%m%d')
    
    daily_chart = api.get_domestic_daily_chart('005930', three_months_ago, today)
    print_response(daily_chart, "국내 주식 일봉 데이터")
    plot_chart_data(daily_chart, "삼성전자 일봉 차트")
    
    # 국내 주식 주봉 데이터 검색
    print("\n2. 국내 주식 주봉 데이터 검색 (삼성전자)")
    six_months_ago = (datetime.now() - timedelta(days=180)).strftime('%Y%m%d')
    weekly_chart = api.get_domestic_weekly_chart('005930', six_months_ago, today)
    print_response(weekly_chart, "국내 주식 주봉 데이터")
    plot_chart_data(weekly_chart, "삼성전자 주봉 차트")
    
    # 국내 주식 분봉 데이터 검색
    print("\n3. 국내 주식 분봉 데이터 검색 (삼성전자)")
    now = datetime.now()
    today_start = now.replace(hour=9, minute=0, second=0).strftime('%Y%m%d%H%M%S')
    now_str = now.strftime('%Y%m%d%H%M%S')
    
    minute_chart = api.get_domestic_minute_chart('005930', today_start, now_str, "10")
    print_response(minute_chart, "국내 주식 10분봉 데이터")
    plot_chart_data(minute_chart, "삼성전자 10분봉 차트")
    
    # 해외 주식 일봉 데이터 검색 (애플: AAPL)
    print("\n4. 해외 주식 일봉 데이터 검색 (애플)")
    overseas_daily_chart = api.get_overseas_daily_chart('AAPL', 'NAS', three_months_ago, today)
    print_response(overseas_daily_chart, "해외 주식 일봉 데이터")
    plot_chart_data(overseas_daily_chart, "애플 일봉 차트")
    
    # 해외 주식 분봉 데이터 검색
    print("\n5. 해외 주식 분봉 데이터 검색 (애플)")
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    yesterday_start = f"{yesterday}090000"
    yesterday_end = f"{yesterday}160000"
    
    overseas_minute_chart = api.get_overseas_minute_chart('AAPL', 'NAS', yesterday_start, yesterday_end, "5")
    print_response(overseas_minute_chart, "해외 주식 5분봉 데이터")
    plot_chart_data(overseas_minute_chart, "애플 5분봉 차트")


if __name__ == "__main__":
    main() 