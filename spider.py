#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import re
import time
import traceback
import requests
from bs4 import BeautifulSoup
from pymysql.err import IntegrityError
from config import urls
from dataBase import insert_data
from logger import logger

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"}

def get_ren_min(cursor, con, data):
    try:
        res = requests.get(data['url'], headers = header)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, features="lxml")
        t11 = soup.select(data['selector'])
        if data['type'] == 'ren_min_lun_tan':
            rows = t11[0].select("a")[1:]
            public_times = re.findall("(\d+年\d+月\d+)日", t11[0].text.replace('\n', ''))
        else:
            public_times = re.findall("(\d+月\d+)日", t11[0].text.replace('\n', ''))
            rows = t11[0].select("a")
        year = time.strftime("%Y-")
        for r, t in zip(rows, public_times):
            href = 'http://opinion.people.com.cn/' + r.attrs['href']
            title = r.text
            public_time = t.replace(title, '').strip()
            if data['type'] == 'ren_min_lun_tan':
                public_time = public_time.replace('年', '-').replace('月', '-')
            else:
                public_time = year + public_time.replace('月', '-')
            data_in = {"title": title, "url": href, "public_time": public_time, "type": data['type'], "create_time": time.strftime("%Y-%m-%d %H:%M:%S")}
            try:
                insert_data(cursor, con, data_in)
                logger.info(f"写入成功，{data_in}")
            except IntegrityError:
                logger.warning(f"重复数据，{data_in}")
                break
            except:
                logger.error(f"写入失败，{data_in}")
                logger.error(traceback.format_exc())
                break
    except:
        logger.error(traceback.format_exc())

def get_ban_yue_tan(cursor, con, data):
    try:
        res = requests.get(data['url'], headers=header)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, features="lxml")
        mt30 = soup.select(data['selector'])
        bty_tbtj_list = mt30[0].select(".bty_tbtj_list")
        rows = bty_tbtj_list[0].select("li")
        for r in rows:
            h3 = r.select("h3")
            a = h3[0].select("a")
            href = a[0].attrs['href']
            title = a[0].text
            span = r.select("span")
            public_time = span[0].text
            data_in = {"title": title, "url": href, "public_time": public_time, "type": data['type'], "create_time": time.strftime("%Y-%m-%d %H:%M:%S")}
            try:
                insert_data(cursor, con, data_in)
                logger.info(f"写入成功，{data_in}")
            except IntegrityError:
                logger.warning(f"重复数据，{data_in}")
                break
            except:
                logger.error(f"写入失败，{data_in}")
                logger.error(traceback.format_exc())
                break
    except:
        logger.error(traceback.format_exc())

def get_hu_bei_ri_bao(cursor, con, data):
    try:
        res = requests.get(data['url'].format(time.strftime("%Y%m/%d"), 'node_01.html'), headers=header)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, features="lxml")
        selector = soup.select(data['selector'])
        rows = selector[0].select("li")
        target_url = [r.select("a")[0].attrs['href'] for r in rows if r.text.strip().endswith("评论") or r.text.strip().endswith("武汉观察")]
        for r in target_url:
            res = requests.get(data['url'].format(time.strftime("%Y%m/%d"), r), headers=header)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, features="lxml")
            selector = soup.select(".resultList")
            for rr in selector:
                a = rr.select("a")
                href = "https://epaper.hubeidaily.net/pc/" + a[0].attrs['href'].replace("../","")
                title = a[0].text.strip()
                public_time = time.strftime("%Y-%m-%d")
                data_in = {"title": title, "url": href, "public_time": public_time, "type": data['type'], "create_time": time.strftime("%Y-%m-%d %H:%M:%S")}
                try:
                    insert_data(cursor, con, data_in)
                    logger.info(f"写入成功，{data_in}")
                except IntegrityError:
                    logger.warning(f"重复数据，{data_in}")
                    break
                except:
                    logger.error(f"写入失败，{data_in}")
                    logger.error(traceback.format_exc())
                    break
    except:
        logger.error(traceback.format_exc())


def run_spider(cursor, con):
    while True:
        if time.strftime("%M") == "20":
            for k, v in urls.items():
                if k == "ren_min_ri_bao":
                    for d in v:
                        get_ren_min(cursor, con, d)
                if k == "ban_yue_tan":
                    for d in v:
                        get_ban_yue_tan(cursor, con, d)
                if k == "hu_bei_ri_bao":
                    for d in v:
                        get_hu_bei_ri_bao(cursor, con, d)
        time.sleep(30)

if __name__ == "__main__":
    pass
    # get_ren_min({"type": "ren_min_zhong_heng", "selector": ".t11", "desc": "人民纵横", "url": "http://opinion.people.com.cn/GB/8213/353915/355231/index.html"})
