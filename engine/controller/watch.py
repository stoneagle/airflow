from watch.ts import five as tsfive
from watch.bitmex import five as bmfive
from library import basic
import os
basic.import_env()


def tushare(code_list):
    backtest = os.environ.get("BACKTEST")
    if not backtest:
        backtest = False
    rewrite = os.environ.get("REWRITE")
    if not rewrite:
        rewrite = False
    tsfive.exec(code_list, backtest, rewrite)
    return


def bitmex(code_list):
    backtest = os.environ.get("BACKTEST")
    if not backtest:
        backtest = False
    rewrite = os.environ.get("REWRITE")
    if not rewrite:
        rewrite = False
    bmfive.exec(code_list, backtest, rewrite)
    return
