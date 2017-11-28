#!/usr/bin/env python
# coding=utf-8

import argparse

from jinja2 import Environment
from template import TEMPLATE

TPL = Environment().from_string(TEMPLATE)

VERSION = "VERSION 0.0.1"


def get_parser():
    """ 解析命令行参数
    """
    parser = argparse.ArgumentParser(
        description='树图渲染命令行工具-利用 JSON 数据生成 HTML 格式的树图',
        add_help=False)
    parser.add_argument('-i', '--input', type=str,
                        help='JSON 数据路径.')
    parser.add_argument('-o', '--output', type=str, default="TreeMap.html",
                        help='输出 HTML 文件路径.(默认为`.\TreeMap.html`)')
    parser.add_argument('-d', '--direction', type=str, default="LR",
                        help='树图的布局方向, '
                             '有 LR/RL/H/TB/BT/V 可选.(默认为 LR)')
    parser.add_argument('-t', '--type', type=int, default=1,
                        help='树图类型, 1.分层树 2.缩进树 3.生态树.(默认为 1)')
    parser.add_argument('-v', '--version', action='store_true',
                        help='版本信息')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='帮助页面')
    return parser


def command_line_runner():
    """ 执行命令行操作
    """
    parser = get_parser()
    args = vars(parser.parse_args())

    if args['version']:
        print(VERSION)
        return

    shape = "smooth"
    vgap, hgap = 10, 100

    if args['type'] == 2:
        shape = 'VH'
        layout = 'IndentedTree'
        vgap, hgap = 5, 18
    elif args['type'] == 1:
        layout = 'CompactBoxTree'
    else:
        layout = 'Dendrogram'

    if not args['input']:
        parser.print_help()
    else:
        render(
            input=args['input'],
            output=args["output"],
            direction=args["direction"],
            kwargs=locals(),
        )


def render(input, direction="LR", output="TreeMap.html", kwargs=None):
    """ 渲染数据生成网页

    :param input: 输入 json 文件路径
    :param direction: 树图方向，有 LR/RL/H/TB/BT/V 可选
    :param output: 输出 html 文件路径
    """
    json_data = ""
    try:
        with open(input, "r", encoding="utf8") as fread:
            json_data = fread.read()
    except FileNotFoundError:
        print("File Not Found!")

    try:
        with open(output, "w+", encoding="utf-8") as fout:
            fout.write(
                TPL.render(direction=direction,
                           json_data=json_data,
                           vgap=kwargs['vgap'],
                           hgap=kwargs['hgap'],
                           shape=kwargs['shape'],
                           layout=kwargs['layout']
                           ))
    except OSError:
        print("Invalid file path!")


if __name__ == "__main__":
    command_line_runner()
