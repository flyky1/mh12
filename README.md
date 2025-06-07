# 키움증권 OpenAPI 클라이언트

키움증권의 REST API를 쉽게 사용할 수 있는 Python 클라이언트 라이브러리입니다. 국내 및 해외 주식 거래, 시세 조회, 차트 데이터 분석을 위한 다양한 기능을 제공합니다.

## 주요 기능

- **인증**: 키움증권 API에 접근하기 위한 OAuth 인증
- **주문**: 국내 및 해외 주식 주문, 정정, 취소 기능
- **계좌**: 계좌 정보, 잔고, 거래내역, 손익 조회
- **시세**: 국내 및 해외 주식 현재가, 호가, 체결 정보 조회
- **차트**: 국내/해외 주식의 일봉/주봉/월봉/분봉/틱 차트 데이터 조회
- **종목정보**: 종목 기본정보, 재무정보, 공시정보 조회
- **순위정보**: 거래량, 거래대금, 시가총액, 상승률 등 상위 종목 조회
- **ETF/ELW**: ETF/ELW 관련 정보 및 구성종목 조회
- **업종/테마**: 업종별, 테마별 종목 및 지수 정보 조회
- **조건검색**: 사용자 정의 조건식으로 종목 검색
- **실시간시세**: WebSocket을 통한 실시간 시세 데이터 구독

## 설치 방법

```bash
pip install kiwoom-openapi
```

## 빠른 시작

### 환경 변수 설정

```bash
# Windows
set kiwoom_appkey=발급받은_앱키
set kiwoom_secretkey=발급받은_비밀키

# macOS/Linux
export kiwoom_appkey=발급받은_앱키
export kiwoom_secretkey=발급받은_비밀키
```

모의투자 환경을 사용하려면 `KiwoomClient` 생성 시 `is_mock=True` 옵션을 지정합니다.
또한 보유종목 조회 예제를 실행하려면 계좌번호(`kiwoom_cano`)와 계좌상품코드(`kiwoom_acnt_prdt_cd`)도 환경 변수로 설정해야 합니다.

### 인증 및 시세 조회 예제

```python
from kiwoom import KiwoomOpenAPI

# API 인스턴스 생성
api = KiwoomOpenAPI()

# 로그인 인증
auth_result = api.auth_login()
if auth_result['status'] == 'success':
    print("인증에 성공했습니다.")
    
    # 삼성전자 현재가 조회
    stock_price = api.get_domestic_stock_price('005930')
    print(f"삼성전자 현재가: {stock_price}")
    
    # 애플 현재가 조회
    overseas_price = api.get_overseas_stock_price('AAPL', 'NAS')
    print(f"애플 현재가: {overseas_price}")
else:
    print("인증에 실패했습니다.")
```

### 차트 데이터 조회 예제

```python
from kiwoom import KiwoomOpenAPI
from datetime import datetime, timedelta

# API 인스턴스 생성
api = KiwoomOpenAPI()

# 로그인 인증
auth_result = api.auth_login()
if auth_result['status'] == 'success':
    # 일봉 데이터 조회 (삼성전자)
    today = datetime.now().strftime('%Y%m%d')
    one_month_ago = (datetime.now() - timedelta(days=30)).strftime('%Y%m%d')
    
    daily_chart = api.get_domestic_daily_chart('005930', one_month_ago, today)
    print("삼성전자 일봉 데이터:")
    print(daily_chart)
    
    # 분봉 데이터 조회 (삼성전자, 10분봉)
    today_start = datetime.now().replace(hour=9, minute=0, second=0).strftime('%Y%m%d%H%M%S')
    now_str = datetime.now().strftime('%Y%m%d%H%M%S')
    
    minute_chart = api.get_domestic_minute_chart('005930', today_start, now_str, "10")
    print("삼성전자 10분봉 데이터:")
    print(minute_chart)
```

### 주문 실행 예제

```python
from kiwoom import KiwoomOpenAPI

# API 인스턴스 생성
api = KiwoomOpenAPI()

# 로그인 인증
auth_result = api.auth_login()
if auth_result['status'] == 'success':
    # 계좌번호 조회
    accounts = api.get_account_list()
    account_no = accounts[0]  # 첫 번째 계좌 사용
    
    # 삼성전자 매수 주문
    order_result = api.place_domestic_order(
        account_no=account_no,
        stock_code='005930',  # 삼성전자
        order_type='00',      # 지정가
        trade_type='2',       # 매수
        quantity=1,           # 1주
        price=70000,          # 70,000원
        order_condition='0'   # 일반주문
    )
    
    print("주문 결과:", order_result)
```

### 실시간 시세 구독 예제

```python
from kiwoom import KiwoomOpenAPI
import time

# API 인스턴스 생성
api = KiwoomOpenAPI()

# 로그인 인증
auth_result = api.auth_login()
if auth_result['status'] == 'success':
    # 실시간 데이터 콜백 함수 정의
    def on_realtime_data(data_type, data):
        print(f"실시간 데이터 수신: {data_type}")
        print(data)
    
    # 콜백 등록
    api.set_realtime_callback(on_realtime_data)
    
    # 삼성전자 실시간 시세 구독
    api.subscribe_realtime_data(['005930'], ['체결', '호가'])
    
    # 10초간 데이터 수신
    time.sleep(10)
    
    # 구독 해지
    api.unsubscribe_realtime_data(['005930'], ['체결', '호가'])
```

## 예제

더 많은 예제는 `examples` 디렉토리를 참조하세요:

- `examples/basic_usage.py`: 기본 사용법 예제
- `examples/chart_example.py`: 국내 및 해외 주식 차트 데이터 조회 예제
- `examples/stock_info_example.py`: 종목 정보 조회 예제
- `examples/stock_chart_example.py`: 주식 차트 데이터 활용 예제
- `examples/overseas_stock_chart_example.py`: 해외 주식 차트 데이터 예제
- `examples/index_chart_example.py`: 지수 차트 데이터 예제
- `examples/realtime_example.py`: 실시간 시세 데이터 수신 예제
- `examples/condition_example.py`: 조건검색 활용 예제
- `examples/credit_order_example.py`: 신용주문 예제
- `examples/etf_example.py`: ETF 정보 조회 예제
- `examples/elw_example.py`: ELW 정보 조회 예제
- `examples/sector_example.py`: 업종 정보 조회 예제
- `examples/theme_example.py`: 테마 정보 조회 예제

## 모듈 구조

- `kiwoom/`: 메인 패키지
  - `__init__.py`: 패키지 초기화 및 통합 API 클래스
  - `auth.py`: 인증 관련 기능
  - `api/`: API 모듈
    - `base.py`: 기본 API 클래스
    - `account.py`: 계좌 관련 API
    - `order.py`: 주문 관련 API
    - `price.py`: 시세 관련 API
    - `chart.py`: 차트 데이터 API
    - `stock.py`: 종목정보 API
    - `ranking.py`: 순위정보 API
    - `etf.py`: ETF 관련 API
    - `elw.py`: ELW 관련 API
    - `sector.py`: 업종 관련 API
    - `theme.py`: 테마 관련 API
    - `condition.py`: 조건검색 API
    - `foreigner.py`: 기관/외국인 투자 정보 API
    - `credit_order.py`: 신용주문 API
  - `realtime.py`: 실시간 시세 관련 기능

## 환경 요구사항

- Python 3.7 이상
- requests
- websocket-client
- pandas (차트 데이터 처리용)
- numpy (데이터 분석용)

## 라이선스

MIT License

## 기여

이슈 및 풀 리퀘스트는 언제나 환영합니다! 프로젝트에 기여하시려면:

1. 이 저장소를 포크하세요
2. 새 브랜치에서 기능을 개발하세요
3. 변경사항을 커밋하세요
4. 원격 브랜치에 푸시하세요
5. 풀 리퀘스트를 제출하세요

## 면책 조항

이 라이브러리는 키움증권의 공식 제품이 아니며, 키움증권과 직접적인 관련이 없습니다.
실제 투자에 사용하기 전에 충분한 테스트를 거치시고, 투자의 책임은 사용자 본인에게 있습니다. 