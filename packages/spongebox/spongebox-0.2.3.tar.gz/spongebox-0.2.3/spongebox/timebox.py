import datetime
import time


def crossbar(date):
    """
    :param date: yyyymmdd:int
    :return: yyyy-mm-dd:str
    """
    return "{}-{}-{}".format(str(date)[0:4], str(date)[4:6], str(date)[6:])


def stamp():
    """
    :return: now() in "%Y%m%d%H%M%S":str
    """
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def interval(date1, date2):
    """
    :param date1: %Y-%m-%d[.*]:str or yyyymmdd:int
    :param date2: %Y-%m-%d[.*]:str or yyyymmdd:int
    :return:days:int between input dates
    """
    date1 = str(date1)
    if date1.isdigit():
        date1 = crossbar(date1)
    date2 = str(date2)
    if date2.isdigit():
        date2 = crossbar(date2)
    date1 = datetime.datetime.strptime(date1[0:10], "%Y-%m-%d")
    date2 = datetime.datetime.strptime(date2[0:10], "%Y-%m-%d")
    num = (date1 - date2).days
    return abs(num)


def add_days(date, n):
    """
    :param date: yyyy-mm-dd[.*]:str or yyyymmdd:int or datetime.datetime
    :param n: n days before/after date ( allow negative)
    :return: date before/after input date:datetime.datetime
    """
    date = str(date)
    if date.isdigit():
        date = crossbar(date)
    return datetime.datetime.strptime(date[0:10], "%Y-%m-%d") + datetime.timedelta(days=n)


def format(datetime, format="%Y-%m-%d %H:%m:%S"):
    """
    :param datetime: datetime.dateime
    :param format: default %Y-%m-%d %H:%m:%S
    :return: format time str
    """
    return datetime.strftime(format)


def timeit(func):
    def wrap(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print("#{}() cost:{}".format(func.__name__, te - ts))
        return result

    return wrap


if __name__ == "__main__":
    print(stamp())
    print(interval("2020-01-16", "2020-01-17"))
    print(add_days("2020-01-16", -1))
    # print(add_days("2020er33", -1))
    print(add_days(20200225, -1))
    # print(format(datetime.datetime.now()))
    #
    #
    # @timeit
    # def test_timeit(n):
    #     a = 1
    #     for i in range(n):
    #         a += 1
    #     print(a)
    #
    #
    # test_timeit(100000)
