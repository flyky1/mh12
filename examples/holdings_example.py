#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Example script to check holdings in a Kiwoom mock account."""

import os
import json
from kiwoom_api import KiwoomClient


def main():
    """Fetch and print account holdings using the mock trading environment."""
    appkey = os.environ.get("kiwoom_appkey")
    secretkey = os.environ.get("kiwoom_secretkey")
    cano = os.environ.get("kiwoom_cano")
    acnt_prdt_cd = os.environ.get("kiwoom_acnt_prdt_cd")

    if not all([appkey, secretkey, cano, acnt_prdt_cd]):
        print("환경 변수에 API 키와 계좌 정보를 설정해주세요.")
        print("필요 변수: kiwoom_appkey, kiwoom_secretkey, kiwoom_cano, kiwoom_acnt_prdt_cd")
        return

    client = KiwoomClient(appkey, secretkey, is_mock=True)

    response = client.account.get_account_balance(
        cano=cano,
        acnt_prdt_cd=acnt_prdt_cd,
    )

    print(json.dumps(response, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
