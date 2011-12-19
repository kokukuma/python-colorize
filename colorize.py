#!/usr/bin/python
# coding=utf-8

import yaml
import codecs
import sys
import re



# 設定ファイルを読み込む関数
def Read_Color_Scheme(cs):
    """ Import Color rule"""
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
        array = []
        reg = re.compile(r'(^.*:".*" )')
        scheme_array = reg.split(string)

        # regularとcolorを抜き出し配列に格納
        for str in scheme_array:
            if str == "":
                continue
            if str.find('regular') >= 0:
                key1 = reg_key1.search(str).group('match')
                val1 = '(' + reg_val1.search(str).group('match') + ')'
                array.append([key1, val1])
            elif str.find('color') >= 0:
                key2 = reg_key2.search(str).group('match')
                val2 = reg_val2.search(str).group('match')
                array.append([key2, val2])
        dics = dict(array)
        return dics

    # 設定ファイル読み込み
    handle = codecs.open("config.yml", "r", "utf-8")

    try:
        # yml読み込み
        scheme = yaml.load(handle)

        # 指定されたスキームを読み込み・辞書化
        color_scheme = dict(scheme[cs])

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
        errorprint.color_scheme_error()


# 正規表現にしたがって色をつける関数
def Colorize(target, regular, color):
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


# エラー文言を出力するためのクラス
class errorprint:
    """error print"""
    @staticmethod
    def argument_error():
        print
        print 'Illegal argument'
        print 'colorize -r Color-scheme Target-string'
        print '         -a Color-name Targe-string'
        quit()
    @staticmethod
    def color_scheme_error():
        handle = codecs.open("config.yml", "r", "utf-8")
        scheme = yaml.load(handle)
        print
        print u"--- color scheme ---"
        for rcs, rule in scheme.items():
            print "+", rcs
        quit()
    @staticmethod
    def color_error():
        print
        print u"--- color ---"
        print u"black"
        print u"red"
        print u"green"
        print u"yellow"
        print u"blue"
        print u"purple"
        print u"cyan"
        print u"under"
        quit()


# main
if __name__ == '__main__':
    argvs = sys.argv
    argc  = len(argvs)

    # 引数を取得
    option = argvs[1]
    color  = argvs[2]

    # コマンドラインの引数として受け取る場合
    if (argc == 4 and option == '-r'):
        # 引数を取得
        target = argvs[3]

        # カラースキーム取得
        color_scheme = Read_Color_Scheme(color)

        # カラースキーム毎に色を変更
        for scheme in color_scheme:
            target = Colorize(target, scheme['regular'], scheme['color'])

        # 出力
        print target

    # コマンドラインの引数として受け取る場合
    elif argc == 4 and option == '-a':
        # 引数を取得
        target = argvs[3]

        # 色をつけて返却
        print Colorize(target, r'(^.*$)', color)

    # パイプラインで受け取る場合
    elif argc == 3 and option == '-r':
        # カラースキーム取得
        color_scheme = Read_Color_Scheme(color)

        # 標準入力を取得
        for target in iter(sys.stdin.readline, ""):
            # カラースキーム毎に色を変更
            for scheme in color_scheme:
                target = Colorize(target, scheme['regular'], scheme['color'])

            # 出力
            print target,

    else:
        errorprint.argument_error()

