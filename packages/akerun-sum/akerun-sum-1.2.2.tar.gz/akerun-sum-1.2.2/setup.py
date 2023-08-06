# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akerun_sum']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1']

entry_points = \
{'console_scripts': ['akerun-sum = akerun_sum.cli:main']}

setup_kwargs = {
    'name': 'akerun-sum',
    'version': '1.2.2',
    'description': 'Enter and leave data totalization program for Akerun',
    'long_description': '[![Build Status](https://travis-ci.org/osstech-jp/akerun-sum.svg?branch=master)](https://travis-ci.org/osstech-jp/akerun-sum)\n\n### 入退出集計プログラム\nNFCカードのドアキー[アケルン](https://akerun.com/)の入退出記録から、勤務日数や勤務時間を集計するプログラムです。\n\n### 以下の環境で動作確認\n  * Windows 10 Home, Python 3.4.3\n  * Ubuntu 16.04.2 LTS, Python 3.5.2\n\n### 使用方法\n`akerun-sum.py -i inputfile -o outputfile -d yyyymm [-f n]`  \n##### 引数\n    -i  入力ファイル名\n    -o  出力ファイル名\n    -d  集計期間 yyyymm の形式で指定\n    -f  出力タイプ 初期値は0\n        0  出力パターン1\n        1  出力パターン2\n\n### 実行例\n\n    akerun-sum.py -i input-euc.csv -o output-euc.csv -d 201610\n    akerun-sum.py -i input-anotherformat.csv -o output-anotherformat.csv -d 201610\u3000-f 1\n\n社員数やレコードの数はリストで管理しているため無制限\n\n\n### 想定している入力ファイル\nDATE,AKERUN,USER,LOCK,CLIENTのカラムを持つCSVファイル\n\n##### DATE\n日付データ  \n`yyyy/mm/dd hh:mm`と`yyyy-mm-dd hh:mm:ss`の2パターンに対応  \n昇順にソートされていることが前提\n##### AKERUN\n本プログラムでは使用していない\n##### USER\n社員名データ\n##### LOCK\n* 入室：オフィスに入った\n* 退室：オフィスから出た\n* 解錠：オフィスに入室したか退室のどちらか\n* 施錠：鍵を締めた（本プログラムでは使用していない）\n\n##### CLIENT\n鍵の種類（本プログラムでは使用していない）\n\n### 出力ファイル\n出力ファイルは2パターンあり、引数によって切替可能  \n文字コードは入力ファイルに合わせる\n\n##### 出力パターン1\nExcelファイルで開くことを想定\n\n|氏名|就業日数|就業時間|yyyy/mm/dd入|yyyy/mm/dd退|yyyy/mm/dd時|…|\n|:-:|:-:|:-:|:-:|:-:|:-:|:-:|\n|山田太郎|2|13.5|8:47|10:12|1.25|…|\n|山田次郎|2|20.5|8:47|20:12|11.25|…|\n|:|:|:|:|:|:|:|\n\n##### 出力パターン2\n通常のCSVファイル\n\n|||||\n|:-:|:-:|:-:|:-:|\n|氏名|山田太郎|||\n|集計期間|yyyymm|||\n|就業日数|2|||\n|就業時間|13.5|||\n|月日|入室時刻|退室時刻|就業時間|\n|yyyy/mm/dd|8:47|10:12|1.25|\n|:|:|:|:|\n|||||\n|氏名|山田次郎|||\n|集計期間|yyyymm|||\n|就業日数|2|||\n|就業時間|13.5|||\n|月日|入室時刻|退室時刻|就業時間|\n|yyyy/mm/dd|8:47|20:12|11.25|\n|:|:|:|:|\n',
    'author': 'KAWAI Shun',
    'author_email': 'shun@osstech.co.jp',
    'maintainer': 'KAWAI Shun',
    'maintainer_email': 'shun@osstech.co.jp',
    'url': 'https://github.com/osstech-jp/akerun-sum',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
