import requests
import json
import os
import redis
import time

# Redis 연결
r = redis.Redis(host='localhost', port=6379, db=0)

# 환경변수에서 키움 API 키 가져오기
appkey = os.environ.get('kiwoom_appkey')
secretkey = os.environ.get('kiwoom_secretkey')

# 접근토큰 발급
def get_access_token():
    host = 'https://api.kiwoom.com'
    endpoint = '/oauth2/token'
    url = host + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
    }

    params = {
        'grant_type': 'client_credentials',
        'appkey': appkey,
        'secretkey': secretkey,
    }

    response = requests.post(url, headers=headers, json=params)

    print(response.text)
    
    if response.status_code == 200:
        token_data = response.json()
        r.set('kiwoom_token', token_data['token'])
        r.set('kiwoom_token_expires', token_data['expires_dt'])
        return token_data['token']
    else:
        print(f'토큰 발급 실패: {response.status_code}')
        print(f'응답: {response.text}')
        return None

# 거래대금상위요청
def get_trading_volume_rank(token, cont_yn='N', next_key=''):
    host = 'https://api.kiwoom.com'
    endpoint = '/api/dostk/rkinfo'
    url = host + endpoint

    headers = {
        'Content-Type': 'application/json;charset=UTF-8',
        'authorization': f'Bearer {token}',
        'cont-yn': cont_yn,
        'next-key': next_key,
        'api-id': 'ka10032',
    }

    params = {
        'mrkt_tp': '000',  # 시장구분: 전체
        'mang_stk_incls': '1',  # 관리종목 포함
        'stex_tp': '3',  # 거래소구분: 통합
    }

    response = requests.post(url, headers=headers, json=params)
    
    if response.status_code == 200:
        result = response.json()
        
        # 헤더 정보 저장
        header_info = {
            'cont_yn': response.headers.get('cont-yn', 'N'),
            'next_key': response.headers.get('next-key', '')
        }
        
        # 결과 출력
        print('======= 거래대금 상위 종목 =======')
        if 'trde_prica_upper' in result:
            for item in result['trde_prica_upper']:
                print(f"{item['now_rank']}. {item['stk_nm']} ({item['stk_cd']}) - 현재가: {item['cur_prc']}, 거래대금: {item['trde_prica']}")
        
        return result, header_info
    else:
        print(f'조회 실패: {response.status_code}')
        print(f'응답: {response.text}')
        return None, {'cont_yn': 'N', 'next_key': ''}

# 메인 함수
def main():
    # 토큰 발급
    token = get_access_token()
    if not token:
        print('토큰 발급에 실패했습니다.')
        return

    print(f'토큰이 성공적으로 발급되었습니다: {token[:10]}...')
    
    # 연속 조회를 위한 변수 초기화
    cont_yn = 'N'
    next_key = ''
    
    # 거래대금 상위 연속 조회
    page = 1
    
    while True:
        print(f'\n===== {page}페이지 조회 중 =====')
        result, header_info = get_trading_volume_rank(token, cont_yn, next_key)
        
        if not result:
            break
            
        cont_yn = header_info['cont_yn']
        next_key = header_info['next_key']
        
        # 연속 조회 여부 확인
        if cont_yn != 'Y':
            print('\n모든 데이터를 조회했습니다.')
            break
            
        page += 1
        time.sleep(1)  # API 호출 간격 (초)

if __name__ == '__main__':
    main()
