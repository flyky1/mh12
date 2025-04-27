#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 해외 주식 차트 데이터 조회 예제

이 예제는 키움 OpenAPI를 통해 해외 주식 차트 데이터를 조회하는 방법을 보여줍니다.
- 일봉 데이터 조회
- 주봉 데이터 조회
- 월봉 데이터 조회
- 분봉 데이터 조회
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
    """해외 주식 차트 데이터 조회 예제 실행"""
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
        # 애플 종목코드 (나스닥)
        stock_code = "AAPL"
        exch_cd = "NAS"  # 나스닥
        
        # 1. 일봉 데이터 조회 (최근 30일)
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        logger.info(f"애플({stock_code}) 일봉 데이터 조회 (최근 30일)")
        daily_data = api.chart.get_overseas_daily(
            bass_code=stock_code,
            exch_cd=exch_cd,
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if daily_data.get('rt_cd') == '0':
            output_data = daily_data.get('output')
            logger.info(f"일봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('ovrs_stck_oprc')}, "
                            f"고가: {item.get('ovrs_stck_hgpr')}, "
                            f"저가: {item.get('ovrs_stck_lwpr')}, "
                            f"종가: {item.get('ovrs_stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"일봉 데이터 조회 실패: {daily_data.get('msg1')}")
        
        # 2. 주봉 데이터 조회
        logger.info(f"\n애플({stock_code}) 주봉 데이터 조회")
        weekly_data = api.chart.get_overseas_weekly(
            bass_code=stock_code,
            exch_cd=exch_cd,
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if weekly_data.get('rt_cd') == '0':
            output_data = weekly_data.get('output')
            logger.info(f"주봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5주 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('ovrs_stck_oprc')}, "
                            f"고가: {item.get('ovrs_stck_hgpr')}, "
                            f"저가: {item.get('ovrs_stck_lwpr')}, "
                            f"종가: {item.get('ovrs_stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"주봉 데이터 조회 실패: {weekly_data.get('msg1')}")
        
        # 3. 월봉 데이터 조회
        logger.info(f"\n애플({stock_code}) 월봉 데이터 조회")
        monthly_data = api.chart.get_overseas_monthly(
            bass_code=stock_code,
            exch_cd=exch_cd,
            inq_strt_dd=(datetime.now() - timedelta(days=365)).strftime('%Y%m%d'),  # 1년 전
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if monthly_data.get('rt_cd') == '0':
            output_data = monthly_data.get('output')
            logger.info(f"월봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5개월 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('ovrs_stck_oprc')}, "
                            f"고가: {item.get('ovrs_stck_hgpr')}, "
                            f"저가: {item.get('ovrs_stck_lwpr')}, "
                            f"종가: {item.get('ovrs_stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"월봉 데이터 조회 실패: {monthly_data.get('msg1')}")
        
        # 4. 분봉 데이터 조회
        logger.info(f"\n애플({stock_code}) 분봉 데이터 조회 (5분봉)")
        
        # 현재 시간 기준 조회 시간 설정
        end_time = datetime.now().strftime('%Y%m%d%H%M%S')
        start_time = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d%H%M%S')
        
        minute_data = api.chart.get_overseas_minute(
            bass_code=stock_code,
            exch_cd=exch_cd,
            inq_strt_dtm=start_time,
            inq_end_dtm=end_time,
            time_interval_cd="5"  # 5분봉
        )
        
        # 응답 데이터 출력
        if minute_data.get('rt_cd') == '0':
            output_data = minute_data.get('output')
            logger.info(f"분봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5건 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시간: {item.get('time')}, "
                            f"시가: {item.get('ovrs_stck_oprc')}, "
                            f"고가: {item.get('ovrs_stck_hgpr')}, "
                            f"저가: {item.get('ovrs_stck_lwpr')}, "
                            f"종가: {item.get('ovrs_stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"분봉 데이터 조회 실패: {minute_data.get('msg1')}")
            
        # 5. 테슬라 주식 조회 (뉴욕 증권거래소)
        stock_code = "TSLA"
        exch_cd = "NYSE"  # 뉴욕 증권거래소
        
        logger.info(f"\n테슬라({stock_code}) 일봉 데이터 조회 (최근 30일)")
        tesla_data = api.chart.get_overseas_daily(
            bass_code=stock_code,
            exch_cd=exch_cd,
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if tesla_data.get('rt_cd') == '0':
            output_data = tesla_data.get('output')
            logger.info(f"테슬라 일봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('ovrs_stck_oprc')}, "
                            f"고가: {item.get('ovrs_stck_hgpr')}, "
                            f"저가: {item.get('ovrs_stck_lwpr')}, "
                            f"종가: {item.get('ovrs_stck_clpr')}, "
                            f"거래량: {item.get('acml_vol')}")
        else:
            logger.error(f"테슬라 일봉 데이터 조회 실패: {tesla_data.get('msg1')}")
            
    except Exception as e:
        logger.exception(f"에러 발생: {e}")


if __name__ == "__main__":
    main() 