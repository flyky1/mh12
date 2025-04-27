# 키움 증권 OpenAPI 예제

이 디렉토리에는 키움 증권 OpenAPI를 사용하는 다양한 예제가 포함되어 있습니다.

## 예제 목록

1. **chart_example.py**: 국내 및 해외 주식의 차트 데이터를 조회하는 예제
   - 일봉, 주봉, 월봉 데이터 조회
   - 분봉 데이터 조회
   - 데이터 시각화

2. **stock_info_example.py**: 국내 및 해외 주식의 종목 정보를 조회하는 예제
   - 기본 종목 정보 조회
   - 거래정지종목, 관리종목 조회
   - 종목 검색 및 재무정보 조회
   - 투자자 동향 조회

## 사용 방법

1. 환경 변수 설정
   ```bash
   # Windows
   set kiwoom_appkey=발급받은_앱키
   set kiwoom_secretkey=발급받은_비밀키
   
   # macOS/Linux
   export kiwoom_appkey=발급받은_앱키
   export kiwoom_secretkey=발급받은_비밀키
   ```

2. 필요 패키지 설치
   ```bash
   pip install -r requirements.txt
   ```

3. 예제 실행
   ```bash
   # 차트 데이터 조회 예제
   python chart_example.py
   
   # 종목 정보 조회 예제
   python stock_info_example.py
   ```

## 주의사항

- 실제 API 요청은 키움 증권에서 발급받은 API 키가 필요합니다.
- 예제 실행 전 환경 변수에 API 키를 설정해야 합니다.
- 실제 거래(매수/매도) 예제는 테스트 환경에서만 실행하시기 바랍니다. 