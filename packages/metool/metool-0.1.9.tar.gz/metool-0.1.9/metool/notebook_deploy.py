# -*- coding: utf-8 -*-

from pathlib import Path
import shutil

ignore = ['.DS_Store', '.git']

prefix = 'tags: ['
suffix = ']'

def md_content(path):
    result = []
    with open(path.absolute(), 'r') as r:
        for i in r.readlines():
            result.append(i)
    return result


def md_tags(lines):
    result = []
    for l in lines:
        s = l.strip()
        if s and s.startswith(prefix) and s.endswith(suffix):
            s = l.replace(prefix, '').replace(suffix, '')
            for i in s.split(','):
                if i.strip():
                    result.append(i.strip())
    return result


def is_ignore(path):
    for i in ignore:
        if path.match(i):
            return True
    if path.is_file() and not path.name.endswith(".md"):
        return True
    return False


def copy(sr, dest, deploy_tags):
    name = sr.stem.replace(' ', '-') + '.md'
    p = dest.joinpath(name)
    lines = md_content(sr)
    tags = md_tags(lines)
    if len(sr.parts) > 2:
        tag = sr.parts[-2]
        tags.append(tag)
    tags = [i for i in tags if i.lower() not in deploy_tags]

    with open(p, 'w') as w:
        for l in lines:
            s = l.strip()
            if s.startswith(prefix):
                w.write(prefix)
                w.write(','.join(tags))
                w.write(suffix)
                w.write('\n')
            else:
                w.write(l)


def deploy(notebook_dir, blog_dir, tags):
    notebook = Path(notebook_dir)
    deploy_tags = [i for i in tags.split(',')]
    deploy_paths = {}
    for deploy_tag in deploy_tags:
        d = Path(blog_dir + '/_' + deploy_tag)
        if d.exists():
            shutil.rmtree(d)
        d.mkdir()
        deploy_paths[deploy_tag] = d

    for i in notebook.iterdir():
        if not i.is_dir() or is_ignore(i):
            continue
        for j in i.iterdir():
            if is_ignore(j):
                continue
            lines = md_content(j)
            tags = md_tags(lines)
            if tags:
                # print(f'{j} {tags}')
                for t in tags:
                    p = deploy_paths.get(t)
                    if p:
                        copy(j, p, deploy_tags)
