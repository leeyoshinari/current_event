#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import os
import asyncio
import jinja2
import pymysql
from aiohttp import web
from apscheduler.schedulers.background import BackgroundScheduler
import aiohttp_jinja2
from logger import logger
from dataBase import query_data, create_table, delete_data
from spider import run_spider
from config import serverContext, ip, port, selector, admin

con = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='123456', database='test', autocommit=True)
cursor = con.cursor()
create_table(cursor)

async def home(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    method = request.query.get('method')
    if method == 'del':
        event_id = request.query.get('id')
        delete_data(cursor, con, event_id)
        logger.info(f'删除 {event_id} 成功：{host} - {user_agent}')
    types = request.query.get('type')
    page = request.query.get('page')
    auth = request.query.get('auth')
    page = int(page) if page else 1
    data = {'type': types, 'page': page, 'page_size': 15}
    results, total_page = query_data(cursor, data)
    logger.info(f'{host} - {user_agent}')
    return aiohttp_jinja2.render_template('index.html', request, context={'context': serverContext, 'total': total_page,
           'results': results, 'type': types, "selector": selector, 'page': page, 'auth': auth, 'admin': admin,
            'total_page': (total_page + 14) // 15})


async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app, loader = jinja2.FileSystemLoader('templates'))
    app.router.add_static(f'{serverContext}/static/',
                          path=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static'),
                          append_version=True)
    app.router.add_route('GET', f'{serverContext}', home)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, ip, port)
    await site.start()


scheduler = BackgroundScheduler()
scheduler.add_job(run_spider, trigger='interval', args=(cursor, con, ), hours=1, id='job-1')
scheduler.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
