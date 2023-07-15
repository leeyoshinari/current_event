#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: leeyoshinari
import hashlib

CREATE_TEBLE = """
CREATE TABLE IF NOT EXISTS `current_event` (
    `id` VARCHAR(32) NOT NULL,
    `type` VARCHAR(32) NOT NULL,
    `title` VARCHAR(64) NOT NULL,
    `url` VARCHAR(256) NOT NULL,
    `public_time` DATETIME NOT NULL,
    `create_time` DATETIME,
    PRIMARY KEY (`id`),
    INDEX (`public_time`)
);
"""

INSERT_INTO = """INSERT INTO current_event (id, type, title, url, public_time, create_time) VALUES ('{}', '{}', '{}', '{}', '{}', '{}');"""
SELECT_ALL = """SELECT id, type, title, url, public_time FROM current_event ORDER BY create_time DESC LIMIT {} OFFSET {};"""
SELECT_BY = """SELECT id, type, title, url, public_time FROM current_event WHERE type = '{}' ORDER BY create_time DESC LIMIT {} OFFSET {};"""
COUNT_ALL = """SELECT COUNT(1) FROM current_event;"""
COUNT_BY = """SELECT COUNT(1) FROM current_event WHERE type = '{}';"""
DELETE_DATA = """DELETE FROM current_event WHERE id = '{}';"""

def create_table(cursor):
    cursor.execute(CREATE_TEBLE)

def query_data(cursor, data):
    try:
        if data['type']:
            cursor.execute(COUNT_BY.format(data['type']))
            total_page = cursor.fetchall()
            cursor.execute(SELECT_BY.format(data['type'], data['page_size'], (data['page'] - 1) * data['page_size']))
            results = cursor.fetchall()
        else:
            cursor.execute(COUNT_ALL)
            total_page = cursor.fetchall()
            cursor.execute(SELECT_ALL.format(data['page_size'], (data['page'] - 1) * data['page_size']))
            results = cursor.fetchall()
    except:
        raise
    return results, total_page[0][0]

def insert_data(cursor, con, data):
    try:
        cursor.execute(INSERT_INTO.format(count_md5(data['url']), data['type'], data['title'], data['url'], data['public_time'], data['create_time']))
        con.commit()
    except:
        raise

def delete_data(cursor, con, event_id):
    try:
        cursor.execute(DELETE_DATA.format(event_id))
        con.commit()
    except:
        raise

def count_md5(data: str):
    return hashlib.md5(data.encode(encoding='utf-8')).hexdigest()
