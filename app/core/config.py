from pytz import timezone

TIME_ZONE = 'Asia/Shanghai'

def get_time_zone():
    return timezone(TIME_ZONE)