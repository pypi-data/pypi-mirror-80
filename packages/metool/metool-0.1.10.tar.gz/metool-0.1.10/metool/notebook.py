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

@main.command(help='生成随机 UUID')
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
    if not date:
        d = datetime.date.today()
        return d.strftime('%Y-%m-%d')
    elif date.startswith('random-'):
        date = date.replace('random-', '')
        l = len(date)
        if l < 4:
            d = datetime.date(random_year(), random_month(), random_day())
        elif l < 6:
            d = datetime.date(int(date[0:4]), random_month(), random_day())
        elif l < 9:
            d = datetime.date(int(date[0:4]), int(date[4:6]), random_day())
        else:
            d = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
        return d.strftime('%Y-%m-%d')
    else:
        raise RuntimeError

@main.command(help='生成随机日期, "" 会生成当前日期, "no" 不会生成日期, "random-2016" 会生成2016年随机日期, "random-201612" 会生成2016年12月随机日期 ')
@click.argument('date', default='')
def udate(date):
    click.echo(gen_udate(date))

@main.command(help='生成新文档')
@click.argument('title')
@click.option('--layout', default='article', help='文档的布局, jekyll 中使用, 默认: article')
@click.option('--date', default='', help='文档日期, 会附带到文件名上, 参考 udate 命令参数格式')
@click.option('--out', default='.', help='文档生成的目录, 默认当前目录')
def new(title, layout, date, out):
    """

    :param title: 文档标题
    :param layout: 布局
    :param date:
    :param out:
    :return:
    """
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
@click.option('--notebook_dir', default='/Users/albert/vscode/notebook', help='笔记文件夹目录, 默认: /Users/albert/vscode/notebook')
@click.option('--blog_dir', default='/Users/albert/vscode/blog', help='博客文件目录, 默认: /Users/albert/vscode/blog')
@click.option('--tags', default='posts,wiki,question', help='被选中的标签, 默认: posts,wiki,question')
def deploy(notebook_dir, blog_dir, tags):
    notebook_deploy.deploy(notebook_dir, blog_dir, tags)
    click.echo('Successfully deploy ' + blog_dir)
