import pandas as pd
import re
import json
import time
from library import count, console, conf
from datetime import datetime
from pandas.util.testing import _network_error_classes
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

THE_FIELDS = ['code', 'symbol', 'name', 'changepercent', 'trade', 'open', 'high', 'low', 'settlement', 'volume', 'turnoverratio']
CLASSIFY_COLS = ['code']


def get_json(sub):
    if sub == "industry":
        url = 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php'
        df = _get_type_data(url)
    elif sub == "concept":
        url = 'http://money.finance.sina.com.cn/q/view/newFLJK.php?param=class'
        df = _get_type_data(url)
    elif sub == "hot":
        df = _get_new_type_data()
    return df


def get_industry_classified(f):
    "由于tushare的延时会导致ip被封，提取该方法至脚本中"
    url = 'http://vip.stock.finance.sina.com.cn/q/view/newSinaHy.php'
    df = _get_type_data(url)
    for row in df.values:
        try:
            if _check_refresh(f, row[0]) is False:
                continue
            _add_data(f, row[0], row[1])
        except Exception as er:
            print(str(er))
            break
    return


def get_concept_classified(f):
    "由于tushare的延时会导致ip被封，提取该方法至脚本中"
    url = 'http://money.finance.sina.com.cn/q/view/newFLJK.php?param=class'
    df = _get_type_data(url)
    for row in df.values:
        try:
            if _check_refresh(f, row[0]) is False:
                continue
            _add_data(f, row[0], row[1])
        except Exception as er:
            print(str(er))
            break
    return


def get_hot_classified(f):
    "由于tushare的延时会导致ip被封，提取该方法至脚本中"
    df = _get_new_type_data()
    for row in df.values:
        try:
            if _check_refresh(f, row[0]) is False:
                continue
            _add_data(f, row[0], row[1])
        except Exception as er:
            print(str(er))
            break
    return


def _add_data(f, tag, name):
    row_df = get_detail(tag, name, retry_count=1, pause=conf.REQUEST_BLANK)
    if row_df is not None:
        # 判断该类别的组是否存在
        cpath = './' + tag
        if f.get(cpath) is None:
            f.create_group(cpath)
        f_c = f[cpath]

        # 判断该类别的code list内容是否存在
        if f_c.get(conf.HDF5_CLASSIFY_DS_CODE) is not None:
            del f_c[conf.HDF5_CLASSIFY_DS_CODE]

        # 获取code list并储存
        data = row_df['code'].values.astype('S').tolist()
        f_c.create_dataset(conf.HDF5_CLASSIFY_DS_CODE, (len(data), 1), data=data)
        f_c[conf.HDF5_CLASSIFY_DS_CODE].attrs[conf.HDF5_CLASSIFY_NAME_ATTR] = name
        f_c[conf.HDF5_CLASSIFY_DS_CODE].attrs[conf.HDF5_CLASSIFY_REFRESH_ATTR] = datetime.now().strftime('%Y-%m-%d')
        count.inc_by_index(conf.HDF5_COUNT_GET)


def _check_refresh(f, tag):
    d = datetime.now()
    cpath = './' + tag
    if f.get(cpath) is None:
        return True
    f_c = f[cpath]

    if f_c.get(conf.HDF5_CLASSIFY_DS_CODE) is not None and f_c[conf.HDF5_CLASSIFY_DS_CODE].attrs.get(conf.HDF5_CLASSIFY_REFRESH_ATTR) is not None:
        last_datetime_str = f_c[conf.HDF5_CLASSIFY_DS_CODE].attrs[conf.HDF5_CLASSIFY_REFRESH_ATTR]
        last_datetime = datetime.strptime(last_datetime_str, '%Y-%m-%d')
        diff = d - last_datetime
        if diff.days < conf.HDF5_CLASSIFY_REFRESH_DAYS_BLANK:
            count.inc_by_index(conf.HDF5_COUNT_PASS)
            return False
    return True


def _get_new_type_data():
    try:
        url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodes#'
        request = Request(url)
        data_str = urlopen(request, timeout=10).read()
        data_str = data_str.decode('GBK')
        regex = re.compile(r'\\(?![/u"])')
        data_str = regex.sub(r"\\\\", data_str)
        data_json = json.loads(data_str)
        # TODO 健壮性，判断数据是否合理
        hot_data_json = data_json[1][0][1][3][1]
        df = pd.DataFrame(
            [[row[2], row[0]] for row in hot_data_json],
            columns=['tag', 'name']
        )
        return df
    except Exception as er:
        print(str(er))


def _get_type_data(url):
    try:
        request = Request(url)
        data_str = urlopen(request, timeout=10).read()
        data_str = data_str.decode('GBK')
        data_str = data_str.split('=')[1]
        data_json = json.loads(data_str)
        df = pd.DataFrame(
            [[row.split(',')[0], row.split(',')[1]] for row in data_json.values()],
            columns=['tag', 'name']
        )
        return df
    except Exception as er:
        print(str(er))


def get_detail(tag, name, retry_count=3, pause=conf.REQUEST_BLANK):
    url = 'http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/Market_Center.getHQNodeData?page=%s&num=1000&sort=symbol&asc=1&node=%s&symbol=&_s_r_a=page'
    dfc = pd.DataFrame()
    p = 0
    while(True):
        p = p + 1
        for _ in range(retry_count):
            time.sleep(pause)
            try:
                request = Request(url % (p, tag))
                text = urlopen(request, timeout=10).read()
                text = text.decode('gbk')
            except _network_error_classes:
                pass
            else:
                break
        reg = re.compile(r'\,(.*?)\:')
        text = reg.sub(r',"\1":', text)
        text = text.replace('"{symbol', '{"symbol')
        text = text.replace('{symbol', '{"symbol"')
        jstr = json.dumps(text)
        js = json.loads(jstr)
        df = pd.DataFrame(pd.read_json(js, dtype={'code': object}), columns=THE_FIELDS)
        df.index.name = name
        dfc = pd.concat([dfc, df])
        console.write_exec()
        return dfc
