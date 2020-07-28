import requests
import logging
import urllib
import urllib.parse

from datetime import datetime, timezone, timedelta
from http.client import HTTPConnection


proactive_url = 'https://api.fe.amazonalexa.com/v1/proactiveEvents/stages/development'
token_url = 'https://api.amazon.com/auth/o2/token'
client_id = ''
client_secret = ''


def enable_logging():
    log = logging.getLogger('urllib3')
    log.setLevel(logging.DEBUG)
    # logging from urllib3 to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    # print statements from `http.client.HTTPConnection` to console/stdout
    HTTPConnection.debuglevel = 1


def get_token_body():
    return {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret':  client_secret,
        'scope': 'alexa::proactive_events'
    }


def get_token_header(body):
    return {
        'Content-Type': 'application/x-www-form-urlencoded',
    }


def request_token():
    body = urllib.parse.urlencode(get_token_body())
    headers = get_token_header(body)
    r = requests.post(url=token_url, headers=headers, data=body)
    if 200 != r.status_code:
        return r.json()

    return r.json()


def get_access_token():
    message = request_token()
    return message['access_token']


def make_body_4_weather_alert():
    now_time = datetime.now(timezone.utc)
    del_time = now_time + timedelta(minutes=60)

    return {
        'timestamp': now_time.isoformat(),
        'referenceId': 'id',
        'expiryTime': del_time.isoformat(),
        'event': {
            'name': 'AMAZON.WeatherAlert.Activated',
            'payload': {
                'weatherAlert': {
                    'source': 'localizedattribute:source',
                    'alertType': 'HURRICANE'
                }
            }
        },
        'localizedAttributes': [
            {
                'locale': 'en-US',
                'source': 'Example Weather Corp'
            }
        ],
        'relevantAudience': {
            'type': 'Multicast',
            'payload': {}
        }
    }


def main():
    #enable_logging()
    token = get_access_token()
    body = make_body_4_weather_alert()
    headers = {'Authorization': 'Bearer {}'.format(token)}
    r = requests.post(proactive_url, headers=headers, json=body)


if __name__ == '__main__':
    main()



