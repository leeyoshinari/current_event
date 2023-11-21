#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari

import logging
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
import uvicorn
from fastapi import FastAPI, APIRouter, Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from logger import LOGGING
from dataBase import query_data, create_table, delete_data
from spider import run_spider
from config import serverContext, ip, port, selector, admin


logger = logging.getLogger("uvicorn")
con = sqlite3.connect('sqlite3.db')
cursor = con.cursor()
create_table(cursor, con)
app = FastAPI()
router = APIRouter(prefix=serverContext)

app.mount(f'{serverContext}/static/', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@router.api_route('/', methods=['GET'])
async def home(request: Request, page: int = 1, types: str = None, auth: str = None, method: str = None, eventId: str = None):
    host = request.headers.get('X-Real-IP')
    user_agent = request.headers.get('User-Agent')
    if method == 'del':
        delete_data(cursor, con, eventId)
        logger.info(f'删除 {eventId} 成功：{host} - {user_agent}')
    page = page if page > 0 else 1
    data = {'type': types, 'page': page, 'page_size': 15}
    results, total_page = query_data(cursor, data)
    logger.info(f"{request.headers.get('X-Real-IP')} - {request.query_params} - {request.headers.get('User-Agent')}")
    return templates.TemplateResponse(name='index.html', context={'request': request, 'context': serverContext, 'total': total_page,
           'results': results, 'type': types, "selector": selector, 'page': page, 'auth': auth, 'admin': admin,
            'total_page': (total_page + 14) // 15})


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_spider, trigger='interval', args=(cursor, con, ), hours=10, id='job-1')
    scheduler.start()
    app.include_router(router)
    uvicorn.run(app=app, host=ip, port=int(port), log_config=LOGGING)
