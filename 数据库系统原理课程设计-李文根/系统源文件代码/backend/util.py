import pytz

def getLocalTimeString(datetime):
    utc_dt = datetime.replace(tzinfo=pytz.utc)
    shanghai_dt = utc_dt.astimezone(pytz.timezone('Asia/Shanghai'))
    formatted_time = shanghai_dt.strftime('%Y/%m/%d %H:%M')
    return formatted_time