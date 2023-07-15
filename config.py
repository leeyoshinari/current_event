#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
ip = "127.0.0.1"
port = "5678"
serverContext = "/cn"
admin = "admin"
urls = {
    "ren_min_ri_bao": [
        {"type": "ren_min_shi_ping", "selector": ".t11", "desc": "人民时评", "url": "http://opinion.people.com.cn/GB/8213/353915/353916/index.html"},
        {"type": "ren_min_lun_tan", "selector": ".t10l14bl", "desc": "人民论坛", "url": "http://opinion.people.com.cn/GB/8213/49160/49220/index.html"},
        {"type": "ren_min_zhong_heng", "selector": ".t11", "desc": "人民纵横", "url": "http://opinion.people.com.cn/GB/8213/353915/355231/index.html"},
        {"type": "ren_min_lai_lun", "selector": ".t11", "desc": "人民来论", "url": "http://opinion.people.com.cn/GB/8213/353915/354155/index.html"}
    ],
    "ban_yue_tan": [
        {"type": "ban_yue_tan_ping_lun", "selector": ".mt30", "desc": "半月谈评论", "url": "http://www.banyuetan.org/byt/banyuetanpinglun/index.html"},
        {"type": "ban_yue_tan_jin_ri_tan", "selector": ".mt30", "desc": "半月谈今日谈", "url": "http://www.banyuetan.org/byt/jinritan/index.html"}
    ],
    "hu_bei_ri_bao": [
        {"type": "hu_bei_ri_bao", "selector": ".nav-list", "desc": "湖北日报", "url": "https://epaper.hubeidaily.net/pc/column/{}/{}"}
    ]
}

selector = {"ren_min_shi_ping": "人民日报-人民时评",
            "ren_min_lun_tan": "人民日报-人民论坛",
            "ren_min_lai_lun": "人民日报-人民来论",
            "ren_min_zhong_heng": "人民日报-人民纵横",
            "ban_yue_tan_ping_lun": "半月谈-评论",
            "ban_yue_tan_jin_ri_tan": "半月谈-今日谈",
            "hu_bei_ri_bao": "湖北日报"
            }
