#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
ip = "127.0.0.1"
port = "5678"
serverContext = "/cn"
admin = "admin"
urls = {
    "ren_min_ri_bao": [
        {"type": "ren_min_ri_bao", "selector": ".list_14", "desc": "人民网评", "url": "http://opinion.people.com.cn/GB/223228/index.html"},
        {"type": "ren_min_ri_bao", "selector": ".list_14", "desc": "人民热评", "url": "http://opinion.people.com.cn/GB/436867/index.html"},
        {"type": "ren_min_ri_bao", "selector": ".list_14", "desc": "社会·民生", "url": "http://opinion.people.com.cn/GB/51863/index.html"},
        {"type": "ren_min_ri_bao", "selector": ".list_14", "desc": "人民来论", "url": "http://opinion.people.com.cn/GB/431649/index.html"}
    ],
    "ban_yue_tan": [
        {"type": "ban_yue_tan", "selector": ".mt30", "desc": "半月谈评论", "url": "http://www.banyuetan.org/byt/banyuetanpinglun/index.html"},
        {"type": "ban_yue_tan", "selector": ".mt30", "desc": "半月谈今日谈", "url": "http://www.banyuetan.org/byt/jinritan/index.html"}
    ],
    "hu_bei_ri_bao": [
        {"type": "hu_bei_ri_bao", "selector": ".nav-list", "desc": "湖北日报", "url": "https://epaper.hubeidaily.net/pc/column/{}/{}"}
    ],
    "ke_pu_shi_bao": [
        {"type": "ke_pu_shi_bao", "selector": ".bmname", "desc": "科普时报", "url": "http://digitalpaper.stdaily.com/http_www.kjrb.com/kjwzb/html/{}/{}"}
    ]
}

selector = {"ren_min_ri_bao": "人民日报",
            "ban_yue_tan": "半月谈",
            "hu_bei_ri_bao": "湖北日报",
            "ke_pu_shi_bao":"科普时报"
            }
