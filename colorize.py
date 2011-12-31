#!/usr/bin/python
# coding=utf-8

import yaml
import codecs
import sys
import re
import os
from optparse import OptionParser


# 設定ファイルを読み込む関数
def read_color_scheme(color_scheme, config_path):
    """ Import Color scheme"""
    # 形式の変更用function
    # {regular:**** color:****} -> {regular:****, color:****}
    # のためだけに存在しているもの.消したい.
    def string2dict(string):
    # 正規表現のコンパイル
        reg_key1 = re.compile(r'^(?P<match>.*):".*"')
        reg_val1 = re.compile(r'^.*:"(?P<match>.*)"')
        reg_key2 = re.compile(r'^(?P<match>.*):.*$')
        reg_val2 = re.compile(r'^.*:(?P<match>.*)$')

        # regularとcolorを分割
        reg = re.compile(r'(^.*:".*" )')
        scheme_array = reg.split(string)
        dics = {}

        # regularとcolorを抜き出し配列に格納
        for str in scheme_array:
            if not str:
                continue
            if 'regular' in str:
                key1 = reg_key1.search(str).group('match')
                val1 = '(' + reg_val1.search(str).group('match') + ')'
                dics[key1] = val1

            #elif 'color' in str:
            if 'color' in str:
                key2 = reg_key2.search(str).group('match')
                val2 = reg_val2.search(str).group('match')
                dics[key2] = val2

        return dics

    # 設定ファイル読み込み
    handle = codecs.open(os.path.expanduser(config_path), "r", "utf-8")

    try:
        # yml読み込み
        scheme = yaml.load(handle)
        # 指定されたスキームを読み込み・辞書化
        color_scheme = dict(scheme[color_scheme])

        # 正規表現と色の組み合わせを配列にして返却
        array = []
        for name, scheme in color_scheme.items():
            scheme = string2dict(scheme)
            array.append(scheme)
        return array

    except IOError:
        print
        print u"There is no config.yml"

    except KeyError:
        sys.stderr.write("--- color scheme ---\n")
        for rcs, scheme in scheme.items():
            sys.stderr.write("+ " + rcs + "\n")
        quit()

# 正規表現にしたがって色をつける関数
def colorize(target, regular, color):
    """ colorize """
    # 色付けfunction
    def coloring(string, color):
        colors = {
            'clear': '\033[0m',
            'black': '\033[30m',
            'red': '\033[31m',
            'green': '\033[32m',
            'yellow': '\033[33m',
            'blue': '\033[34m',
            'purple': '\033[35m',
            'cyan': '\033[36m',
            'under': '\033[4m',
        }

        try:
            return colors[color] + string + colors['clear']

        except KeyError:
            return string

    # 正規表現に従い文字列置換
    reg = re.compile(regular)
    replacement = reg.sub(coloring(r'\1', color), target)
    return replacement

# option_parserを生成する関数
def build_option_parser():
    """Make Option Parser"""
    parser = OptionParser()
    parser.add_option(
            '-f', '--configuration-file-path',
            help="read configuration from. (default: '~/.colorize.yml')",
            default='~/.colorize.yml'
            )
    parser.add_option(
            '-s', '--color-scheme',
            help="set scheme of colorize. (default: 'all')",
            default="all"
            )
    parser.add_option(
            '-r', '--regular',
            help="set regular expression. (default: '^.*$')",
            default=r"^.*$"
            )
    parser.add_option(
            '-c', '--color',
            help="set color. (default: 'red')",
            default="red"
            )
    return parser

# main(use optperser)
def main():
    parser = build_option_parser()
    opts, args = parser.parse_args()

    # get options / color_scheme
    try:
        config_path = opts.configuration_file_path
        color_scheme = opts.color_scheme

        if color_scheme == 'all':
            color_scheme = [{
                    'regular':'(' + opts.regular + ')',
                    'color':opts.color
                    }]
        else:
            color_scheme = read_color_scheme(color_scheme, config_path)

    except Exception, e:
        parser.error(e)


    # 対象をコマンドラインから受け取る場合
    if (args):
        # 引数を取得
        target = args[0]

        # カラースキーム毎に色を変更
        for scheme in color_scheme:
            target = colorize(target, scheme['regular'], scheme['color'])
        print target

    # 対象を標準出力から受け取る場合
    else:
        # 標準入力を取得
        for target in iter(sys.stdin.readline, ""):
            # カラースキーム毎に色を変更
            for scheme in color_scheme:
                target = colorize(target, scheme['regular'], scheme['color'])
            sys.stdout.write(target)

if __name__ == '__main__':
    main()
