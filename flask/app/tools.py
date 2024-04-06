import pytz


def convert_timezone(timestamp, zone):
    '''Convert timestamp to local timezone. Default timezone is `Australia/Perth`'''
    utc = timestamp.replace(tzinfo=pytz.utc)
    timezone = pytz.timezone(zone if zone else 'Australia/Perth')
    format = '%a %d %B %Y %H:%M:%S'
    return utc.astimezone(timezone).strftime(format)