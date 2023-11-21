#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import time
import logging
import datetime
import traceback
import requests
from bs4 import BeautifulSoup
from sqlite3 import IntegrityError
from config import urls
from dataBase import insert_data


logger = logging.getLogger("uvicorn")
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57"}


def get_ren_min(cursor, con, data):
    try:
        res = requests.get(data['url'], headers = header)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, features="lxml")
        t11 = soup.select(data['selector'])[0]
        rows = t11.select("li")
        for row in rows:
            r = row.select("a")[0]
            href = 'http://opinion.people.com.cn/' + r.attrs['href']
            title = r.text
            public_time = row.select("i")[0].text.replace(title, '').strip() + ":00"
            data_in = {"title": title, "url": href, "public_time": public_time.split(' ')[0], "type": data['type'], "create_time": public_time}
            try:
                insert_data(cursor, con, data_in)
                logger.info(f"写入成功，{data_in}")
            except IntegrityError:
                logger.warning(f"重复数据，{data_in}")
                continue
            except:
                logger.error(f"写入失败，{data_in}")
                logger.error(traceback.format_exc())
                continue
            time.sleep(0.5)
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
            time.sleep(1)
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
                if "广告" in title:
                    continue
                data_in = {"title": title, "url": href, "public_time": time.strftime("%Y-%m-%d"), "type": data['type'], "create_time": time.strftime("%Y-%m-%d %H:%M:%S")}
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
                time.sleep(1)
    except:
        logger.error(traceback.format_exc())


def get_ke_pu_shi_bao(cursor, con, data):
    try:
        if datetime.datetime.now().weekday() == 4:
            res = requests.get(data['url'].format(time.strftime("%Y-%m/%d"), 'node_121.htm'), headers=header)
            res.encoding = res.apparent_encoding
            soup = BeautifulSoup(res.text, features="lxml")
            selector = soup.select(data['selector'])
            rows = selector[0].select("#pageLink")
            for r in rows:
                href = r.attrs['href']
                res = requests.get(data['url'].format(time.strftime("%Y-%m/%d"), href), headers=header)
                res.encoding = res.apparent_encoding
                soup = BeautifulSoup(res.text, features="lxml")
                selector = soup.select(".title")
                titles = selector[0].select("li")
                for ti in titles:
                    a = ti.select("a")[0]
                    href = 'http://digitalpaper.stdaily.com/http_www.kjrb.com/kjwzb/html/{}/{}'.format(time.strftime("%Y-%m/%d"), a.attrs['href'])
                    title = a.select('div')[0].text.strip()
                    data_in = {"title": title, "url": href, "public_time": time.strftime("%Y-%m-%d"),
                               "type": data['type'], "create_time": time.strftime("%Y-%m-%d %H:%M:%S")}
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
                    time.sleep(1)
    except:
        logger.error(traceback.format_exc())


def run_spider(cursor, con):
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
        if k == "ke_pu_shi_bao":
            for d in v:
                get_ke_pu_shi_bao(cursor, con, d)


if __name__ == "__main__":
    import sqlite3
    con = sqlite3.connect('sqlite3.db')
    cursor = con.cursor()
    get_ren_min(cursor, con, {"type": "ren_min_ri_bao", "selector": ".list_14", "desc": "人民网评", "url": "http://opinion.people.com.cn/GB/223228/index.html"})
