#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
키움증권 지수 차트 데이터 조회 예제

이 예제는 키움 OpenAPI를 통해 지수 차트 데이터를 조회하는 방법을 보여줍니다.
- KOSPI, KOSDAQ 지수 일봉 데이터 조회
- KOSPI 지수 분봉 데이터 조회
- 섹터 지수 일봉 데이터 조회
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
    """지수 차트 데이터 조회 예제 실행"""
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
        # 1. KOSPI 지수 일봉 데이터 조회 (최근 30일)
        end_date = datetime.now().strftime('%Y%m%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
        
        logger.info("KOSPI 지수 일봉 데이터 조회 (최근 30일)")
        kospi_daily = api.chart.get_domestic_index_daily(
            stk_id_cd="U001",  # KOSPI 지수 코드
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if kospi_daily.get('rt_cd') == '0':
            output_data = kospi_daily.get('output')
            logger.info(f"KOSPI 지수 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('bstp_nmix_oprc')}, "
                            f"고가: {item.get('bstp_nmix_hgpr')}, "
                            f"저가: {item.get('bstp_nmix_lwpr')}, "
                            f"종가: {item.get('bstp_nmix_clpr')}")
        else:
            logger.error(f"KOSPI 지수 데이터 조회 실패: {kospi_daily.get('msg1')}")
        
        # 2. KOSDAQ 지수 일봉 데이터 조회 (최근 30일)
        logger.info("\nKOSDAQ 지수 일봉 데이터 조회 (최근 30일)")
        kosdaq_daily = api.chart.get_domestic_index_daily(
            stk_id_cd="U201",  # KOSDAQ 지수 코드
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if kosdaq_daily.get('rt_cd') == '0':
            output_data = kosdaq_daily.get('output')
            logger.info(f"KOSDAQ 지수 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('bstp_nmix_oprc')}, "
                            f"고가: {item.get('bstp_nmix_hgpr')}, "
                            f"저가: {item.get('bstp_nmix_lwpr')}, "
                            f"종가: {item.get('bstp_nmix_clpr')}")
        else:
            logger.error(f"KOSDAQ 지수 데이터 조회 실패: {kosdaq_daily.get('msg1')}")
        
        # 3. KOSPI 지수 분봉 데이터 조회 (최근 1일)
        logger.info("\nKOSPI 지수 분봉 데이터 조회 (5분봉)")
        
        # 현재 시간 기준 조회 시간 설정
        end_time = datetime.now().strftime('%Y%m%d%H%M%S')
        start_time = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d%H%M%S')
        
        kospi_minute = api.chart.get_domestic_index_minute(
            stk_id_cd="U001",  # KOSPI 지수 코드
            tick_kind_cd="5",  # 5분봉
            inq_strt_dtm=start_time,
            inq_end_dtm=end_time
        )
        
        # 응답 데이터 출력
        if kospi_minute.get('rt_cd') == '0':
            output_data = kospi_minute.get('output')
            logger.info(f"KOSPI 지수 분봉 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5건 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시간: {item.get('stck_cntg_hour')}, "
                            f"시가: {item.get('bstp_nmix_oprc')}, "
                            f"고가: {item.get('bstp_nmix_hgpr')}, "
                            f"저가: {item.get('bstp_nmix_lwpr')}, "
                            f"종가: {item.get('bstp_nmix_clpr')}")
        else:
            logger.error(f"KOSPI 지수 분봉 데이터 조회 실패: {kospi_minute.get('msg1')}")
        
        # 4. 섹터 지수 일봉 데이터 조회 (반도체 섹터)
        logger.info("\n섹터 지수 일봉 데이터 조회 (반도체)")
        sector_daily = api.chart.get_domestic_index_daily(
            stk_id_cd="U203",  # 반도체 섹터 지수 코드
            inq_strt_dd=start_date,
            inq_end_dd=end_date
        )
        
        # 응답 데이터 출력
        if sector_daily.get('rt_cd') == '0':
            output_data = sector_daily.get('output')
            logger.info(f"반도체 섹터 지수 데이터 {len(output_data)} 건 조회 성공")
            
            # 최근 5일 데이터만 출력
            for item in output_data[:5]:
                logger.info(f"일자: {item.get('stck_bsop_date')}, "
                            f"시가: {item.get('bstp_nmix_oprc')}, "
                            f"고가: {item.get('bstp_nmix_hgpr')}, "
                            f"저가: {item.get('bstp_nmix_lwpr')}, "
                            f"종가: {item.get('bstp_nmix_clpr')}")
        else:
            logger.error(f"반도체 섹터 지수 데이터 조회 실패: {sector_daily.get('msg1')}")
            
    except Exception as e:
        logger.exception(f"에러 발생: {e}")


if __name__ == "__main__":
    main() 