#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 국내 주식 차트 데이터 조회 예제

이 예제는 키움 OpenAPI를 통해 국내 주식 차트 데이터를 조회하는 방법을 보여줍니다.
- 일봉, 주봉, 월봉 데이터 조회
- 분봉, 틱봉 데이터 조회
- 수정주가 여부 설정
"""

import os
import sys
import logging
from datetime import datetime, timedelta

# 상위 디렉토리 추가 (import를 위해)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kiwoom_api import KiwoomAPI


# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def main():
    """국내 주식 차트 데이터 조회 예제 실행"""
    # API 키 가져오기
    appkey = os.environ.get('kiwoom_appkey')
    secretkey = os.environ.get('kiwoom_secretkey')
    
    if not appkey or not secretkey:
        logger.error("환경 변수에 API 키가 설정되어 있지 않습니다.")
        logger.error("kiwoom_appkey와 kiwoom_secretkey를 환경 변수로 설정해주세요.")
        return
    
    # API 인스턴스 생성
    api = KiwoomAPI(appkey, secretkey)
    
    try:
        # 삼성전자 종목코드
        stock_code = "005930"
        
        # 1. 일봉 데이터 조회 (최근 30일)
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        logger.info(f"삼성전자({stock_code}) 일봉 데이터 조회 (최근 30일)")
        daily_data = api.chart.get_domestic_daily(
            stk_cd=stock_code,
            inq_strt_dd=start_date,
            inq_end_dd=end_date,
            adj_prc="1"  # 수정주가 적용
        )
        
        # 응답 데이터 출력
        if daily_data.get('rt_cd') == '0':
            output_data = daily_data.get('output')
            logger.info(f"일봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('stck_oprc')}, "
                            f"고가: {item.get('stck_hgpr')}, "
                            f"저가: {item.get('stck_lwpr')}, "
                            f"종가: {item.get('stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"일봉 데이터 조회 실패: {daily_data.get('msg1')}")
        
        # 2. 주봉 데이터 조회
        logger.info(f"\n삼성전자({stock_code}) 주봉 데이터 조회")
        weekly_data = api.chart.get_domestic_weekly(
            stk_cd=stock_code,
            inq_strt_dd=start_date,
            inq_end_dd=end_date,
            adj_prc="1"  #, # 수정주가 적용
        )
        
        # 응답 데이터 출력
        if weekly_data.get('rt_cd') == '0':
            output_data = weekly_data.get('output')
            logger.info(f"주봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5주 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('stck_oprc')}, "
                            f"고가: {item.get('stck_hgpr')}, "
                            f"저가: {item.get('stck_lwpr')}, "
                            f"종가: {item.get('stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"주봉 데이터 조회 실패: {weekly_data.get('msg1')}")
        
        # 3. 월봉 데이터 조회
        logger.info(f"\n삼성전자({stock_code}) 월봉 데이터 조회")
        monthly_data = api.chart.get_domestic_monthly(
            stk_cd=stock_code,
            inq_strt_dd=(datetime.now() - timedelta(days=365)).strftime('%Y%m%d'),  # 1년 전
            inq_end_dd=end_date,
            adj_prc="1"  # 수정주가 적용
        )
        
        # 응답 데이터 출력
        if monthly_data.get('rt_cd') == '0':
            output_data = monthly_data.get('output')
            logger.info(f"월봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5개월 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('stck_oprc')}, "
                            f"고가: {item.get('stck_hgpr')}, "
                            f"저가: {item.get('stck_lwpr')}, "
                            f"종가: {item.get('stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"월봉 데이터 조회 실패: {monthly_data.get('msg1')}")
        
        # 4. 분봉 데이터 조회
        logger.info(f"\n삼성전자({stock_code}) 분봉 데이터 조회 (5분봉)")
        
        # 현재 시간 기준 조회 시간 설정
        end_time = datetime.now().strftime('%Y%m%d%H%M%S')
        start_time = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d%H%M%S')
        
        minute_data = api.chart.get_domestic_minute(
            stk_cd=stock_code,
            tick_kind_cd="5",  # 5분봉
            inq_strt_dtm=start_time,
            inq_end_dtm=end_time,
            adj_prc="1"  # 수정주가 적용
        )
        
        # 응답 데이터 출력
        if minute_data.get('rt_cd') == '0':
            output_data = minute_data.get('output')
            logger.info(f"분봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5건 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시간: {item.get('stck_cntg_hour')}, "
                            f"시가: {item.get('stck_oprc')}, "
                            f"고가: {item.get('stck_hgpr')}, "
                            f"저가: {item.get('stck_lwpr')}, "
                            f"종가: {item.get('stck_clpr')}, "
                            f"거래량: {item.get('cntg_vol')}")
        else:
            logger.error(f"분봉 데이터 조회 실패: {minute_data.get('msg1')}")
        
        # 5. 틱 데이터 조회
        logger.info(f"\n삼성전자({stock_code}) 틱 데이터 조회 (1분 틱)")
        tick_data = api.chart.get_domestic_tick(
            stk_cd=stock_code,
            tick_kind_cd="1",  # 1분 틱
            inq_strt_dtm=start_time,
            inq_end_dtm=end_time,
            adj_prc="1"  # 수정주가 적용
        )
        
        # 응답 데이터 출력
        if tick_data.get('rt_cd') == '0':
            output_data = tick_data.get('output')
            logger.info(f"틱 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5건 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시간: {item.get('stck_cntg_hour')}, "
                            f"체결시간: {item.get('stck_prpr_tm')}, "
                            f"현재가: {item.get('stck_prpr')}, "
                            f"체결량: {item.get('cntg_vol')}")
        else:
            logger.error(f"틱 데이터 조회 실패: {tick_data.get('msg1')}")
            
    except Exception as e:
        logger.exception(f"에러 발생: {e}")


if __name__ == "__main__":
    main() 