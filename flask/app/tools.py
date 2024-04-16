from flask import jsonify
import pytz


def convert_timezone(timestamp, zone):
    '''Convert timestamp to local timezone. Default timezone is `Australia/Perth`'''
    utc = timestamp.replace(tzinfo=pytz.utc)
    timezone = pytz.timezone(zone if zone else 'Australia/Perth')
    format = '%a %d %B %Y %H:%M:%S'
    return utc.astimezone(timezone).strftime(format)

def json_response(status:str, message:str, opts:dict=None):
    '''Return a JSON response with `status` and `message`, and optional `data`.'''
    response = {"status": status, "message": message}

    if opts is None:
        return jsonify({"status": status, "message": message})
    
    for key, value in opts.items():
        response[key] = value

    return jsonify(response)