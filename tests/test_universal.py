import sys

sys.path.insert(0, "../")
import xalpha as xa


def test_get_xueqiu():
    df = xa.get_daily(start="20200302", end="2020-03-07", code="HK01810")
    assert round(df.iloc[-1]["close"], 2) == 12.98
    df = xa.get_daily(start="2020/03/02", end="20200307", code="PDD")
    assert round(df.iloc[0]["close"], 2) == 37.51
    df = xa.get_daily(start="20200301", end="20200307", code="SZ112517")
    # note how this test would fail when the bond is matured
    assert round(df.iloc[0]["close"], 2) == 98
    df = xa.get_daily(start="20200222", end="20200301", code="SH501018")
    assert round(df.iloc[-1]["close"], 3) == 0.965


def test_get_rmb():
    df = xa.get_daily(start="20180101", end="2020-03-07", code="USD/CNY")
    assert len(df) == 528
    df = xa.get_daily(code="EUR/CNY", end="20200306")
    assert round(df.iloc[-1]["close"], 4) == 7.7747


def test_get_fund():
    df = xa.get_daily(code="F100032")
    assert round(df[df["date"] == "2020-03-06"].iloc[0]["close"], 3) == 1.036
    df = xa.get_daily(code="M002758", start="20200201")
    assert round(df.iloc[1]["close"], 3) == 1.134


def test_get_investing():
    df1 = xa.get_daily(code="indices/germany-30")
    df2 = xa.get_daily(code="172")
    assert (
        df1.iloc[-2]["close"] == df2.iloc[-2]["close"]
    )  ## never try -1, today's data is unpredictable
    df = xa.get_daily(code="/currencies/usd-cny", end="20200307")
    assert round(df.iloc[-1]["close"], 4) == 6.9321


def test_get_xueqiu_rt():
    assert xa.get_rt("PDD")["currency"] == "USD"
    assert xa.get_rt("03333")["name"] == xa.get_rt("HK03333")["name"]
    assert isinstance(xa.get_rt("SH501018")["percent"], float)


def test_get_investing_rt():
    assert xa.get_rt("currencies/usd-cny")["currency"] == None
    assert xa.get_rt("/indices/germany-30")["name"] == "德国DAX30指数 (GDAXI)"
    assert isinstance(xa.get_rt("equities/pinduoduo")["current_ext"], float)


def test_cache():
    get_daily_cache = xa.universal.cached("20190101")(xa.get_daily)
    l1 = get_daily_cache("EUR/CNY", start="20200101")
    l2 = get_daily_cache("EUR/CNY", start="20190101")
    l3 = get_daily_cache("EUR/CNY", start="20180101")
    assert l2.iloc[0]["date"] == l3.iloc[0]["date"]
