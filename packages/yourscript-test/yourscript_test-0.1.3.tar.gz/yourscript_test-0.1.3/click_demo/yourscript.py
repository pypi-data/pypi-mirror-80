#!/user/bin/env python
# -*- coding: utf-8 -*-

"""
------------------------------------
@Project : click_cli
@Time    : 2020/9/21 11:27
@Auth    : luozhongwen
@Email   : luozw@inhand.com.cn
@File    : yourscript.py
@IDE     : PyCharm
------------------------------------
"""
import click


@click.command()
def cli():
    click.echo("Hello word")
