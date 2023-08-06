class HuoYanLibRequestsError(Exception):
    """Nothing"""


def _raise_huoyanlibrequesterror_sys():
    raise HuoYanLibRequestsError(
        'length of object \'sys.argv\' is not enough, please use 360 explorer -- xueersi running this function'
    )
