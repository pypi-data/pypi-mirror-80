# -*- coding: utf-8 -*-

import uuid
import click
import datetime
import random
import importlib.resources as pkg_resources
from . import notebook_deploy
from . import templates


@click.group()
def main():
    pass

def gen_ukey():
    return uuid.uuid4()

@main.command(help='生成随机 uuid')
def ukey():
    click.echo(gen_ukey())

def random_year():
    return random.randint(2016, 2019)

def random_month():
    return random.randint(1, 12)

def random_day():
    return random.randint(1, 29)

def gen_udate(date):
    if date == 'no':
        return ''
    l = len(date)
    if l < 4:
        d = datetime.date(random_year(), random_month(), random_day())
    elif l < 6:
        d = datetime.date(int(date[0:4]), random_month(), random_day())
    else:
        d = datetime.date(int(date[0:4]), int(l[4:6]), int(l[6:8]))
    return d.strftime('%Y-%m-%d')


@main.command(help='生成随机日期')
@click.argument('date', default='.')
def udate(date):
    click.echo(gen_udate(date))

@main.command(help='生成新文档')
@click.argument('title')
@click.option('--layout', default='article')
@click.option('--date', default='')
@click.option('--out', default='.')
def new(title, layout, date, out):
    date = gen_udate(date)
    if date:
        filename = date + ' ' + title + '.md'
    else:
        filename = title + '.md'
    k = gen_ukey()
    tpl = pkg_resources.read_text(templates, 'notebook.md')
    content = str.format(tpl, title=title, layout=layout, ukey=k)
    with open(out + '/' + filename, 'w') as w:
        w.write(content)
    click.echo('Successfully create ' + filename)

@main.command(help='发布文档到博客')
@click.option('--notebook_dir', default='/Users/albert/vscode/notebook')
@click.option('--blog_dir', default='/Users/albert/vscode/blog')
@click.option('--tags', default='posts,wiki,question')
def deploy(notebook_dir, blog_dir, tags):
    notebook_deploy.deploy(notebook_dir, blog_dir, tags)
    click.echo('Successfully deploy ' + blog_dir)
