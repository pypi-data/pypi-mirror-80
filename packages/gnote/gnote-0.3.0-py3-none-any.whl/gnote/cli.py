import platform
import subprocess
from enum import auto, Enum
from pathlib import Path
from typing import List

import click
import rich
from rich.markdown import Markdown

import gnote


class Opt(Enum):
    default = auto()
    version = auto()
    list = auto()
    edit = auto()
    test = auto()


def show_version():
    import toml
    cfg = toml.load("./pyproject.toml")
    print(cfg['tool']['poetry']['version'])


def show_docs():
    """
    查看文档列表
    """
    paths = __list_docs()
    for doc in paths:
        print(doc.name.replace('.md', ''))


def __list_docs():
    repo_path = gnote.repo_dir
    paths: List[Path] = []

    def list_file(p: Path):
        for sub in p.iterdir():
            if sub.name.startswith('.'):
                continue
            if sub.is_dir():
                list_file(sub)
            else:
                paths.append(sub)

    list_file(repo_path)
    return paths


def __call_pyvim(doc_path):
    cmd = ['powershell'] if 'windows' == platform.system().lower() else []
    subprocess.call(cmd + ['pyvim', doc_path])


def __check_and_sync():
    g = gnote.git_repo
    if g.is_dirty(untracked_files=True):
        g.git.add('.')
        g.git.commit(m='update')
        g.git.push()


def edit_doc(doc_name):
    """
    编辑文件
    """
    docs = __list_docs()
    dct_doc = {p.name.replace('.md', ''): p for p in docs}
    if doc_name in dct_doc.keys():
        __call_pyvim(dct_doc.get(doc_name))
    else:
        new_doc = Path(gnote.repo_dir).joinpath(Path(doc_name).with_suffix('.md'))
        __call_pyvim(new_doc)
    __check_and_sync()
    pass


def show(doc_name):
    docs = __list_docs()
    dct_doc = {p.name.replace('.md', ''): p for p in docs}
    if (p := dct_doc.get(doc_name, None)) is not None:
        content = Path(p).read_text()
        rich.print(Markdown(content))
    else:
        print("not %s doc" % doc_name)


@click.command()
@click.argument('words', nargs=-1, required=False)
@click.option('-v', '--version', 'opt', flag_value=Opt.version)
@click.option('-l', '--list', 'opt', flag_value=Opt.list)
@click.option('-e', '--edit', 'opt', flag_value=Opt.edit)
# @click.option('-t', '--test', 'opt', flag_value=Opt.test)
def entry(words, opt):
    if opt is not None:
        if opt == Opt.version:
            show_version()
        if opt == Opt.list:
            show_docs()
        if opt == Opt.edit and words[0] != '':
            edit_doc(words[0])
        # if opt == Opt.test:
        #     __check_and_sync()
        return
    else:
        text = ' '.join(words)
        show(text)
