#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import os
import asyncio
import threading
import jinja2
import pymysql
from aiohttp import web
import aiohttp_jinja2
from logger import logger
from dataBase import query_data, create_table
from spider import run_spider
from config import serverContext, ip, port, selector

con = pymysql.connect(host='127.0.0.1', user='root', port=3306, password='123456', database='test', autocommit=True)
cursor = con.cursor()
create_table(cursor)

async def home(request):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    types = request.query.get('type')
    page = request.query.get('page')
    page = int(page) if page else 1
    data = {'type': types, 'page': page, 'page_size': 15}
    results, total_page = query_data(cursor, data)
    logger.info(f'{host} - {user_agent}')
    return aiohttp_jinja2.render_template('index.html', request, context={'context': serverContext, 'total': total_page,
           'results': results, 'type': types, "selector": selector, 'page': page})


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


t = threading.Thread(target=run_spider, args=(cursor, con, ), daemon=True)
t.start()
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()
