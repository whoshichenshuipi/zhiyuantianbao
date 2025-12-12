from datetime import datetime


def ryNoParams():
    print(f'执行无参方法--------------{datetime.now()}')


def ryParams(params):
    print(f'执行有参方法： {params}---------------{datetime.now()}')


def ryMultipleParams(arg):
    print(f'执行多参方法： {arg}--------------------{datetime.now()}')