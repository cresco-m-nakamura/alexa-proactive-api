import requests
import logging
import urllib
import urllib.parse

from datetime import datetime, timezone, timedelta
from http.client import HTTPConnection


class Proactive:
    __proactive_url = 'https://api.fe.amazonalexa.com/v1/proactiveEvents/stages/development'
    __token_url = 'https://api.amazon.com/auth/o2/token'
    __client_id = ""
    __client_secret = ""

    def __init__(self, client_id, client_secret):
        self.set_client_info(client_id, client_secret)

    @classmethod
    def set_client_info(self, client_id, client_secret):
        self.__client_id = client_id
        self.__client_secret = client_secret

    @classmethod
    def enable_logging(cls):
        log = logging.getLogger('urllib3')
        log.setLevel(logging.DEBUG)
        # logging from urllib3 to console
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        log.addHandler(ch)
        # print statements from `http.client.HTTPConnection` to console/stdout
        HTTPConnection.debuglevel = 1

    @classmethod
    def get_token_body(cls):
        return {
            'grant_type': 'client_credentials',
            'client_id': cls.__client_id,
            'client_secret': cls.__client_secret,
            'scope': 'alexa::proactive_events'
        }

    @classmethod
    def get_token_header(cls):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    @classmethod
    def request_token(cls):
        body = urllib.parse.urlencode(cls.get_token_body())
        headers = cls.get_token_header()
        r = requests.post(url=cls.__token_url, headers=headers, data=body)
        if 200 != r.status_code:
            assert 'bad request'

        return r.json()

    @classmethod
    def get_access_token(cls):
        message = cls.request_token()
        return message['access_token']

    @classmethod
    def make_body_4_weather_alert(cls):
        now_time = datetime.now()
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
                    'locale': 'ja-JP',
                    'source': 'Example Weather Corp'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_sports(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.SportsEvent.Updated',
                'payload': {
                    'update': {
                        'scoreEarned': 1,
                        'teamName': 'アップルズ'
                    },
                    'sportsEvent': {
                        'eventLeague': {
                            'name': 'localizedattribute:eventLeagueName'
                        },
                        'homeTeamStatistic': {
                            'team': {
                                'name': 'オレンジズ'
                            },
                            'score': 1
                        },
                        'awayTeamStatistic': {
                            'team': {
                                'name': 'アップルズ'
                            },
                            'score': 2
                        }
                    }
                }
            },
            'localizedAttributes': [
                {
                    'locale': 'ja-JP',
                    'eventLeagueName': 'Example Weather Corp'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_message(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.MessageAlert.Activated',
                'payload': {
                    'state': {
                        'status': 'UNREAD',
                        'freshness': 'NEW'
                    },
                    'messageGroup': {
                        'creator': {
                            'name': 'sentakuki...'
                        },
                        'count': 1,
                        'urgency': 'URGENT'
                    }
                }
            },
            'localizedAttributes': [
                {
                    'locale': 'ja-JP',
                    'sellerName': 'Amazon'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_order(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.OrderStatus.Updated',
                'payload': {
                    'state': {
                        'status': 'PREORDER_RECEIVED'
                    },
                    'order': {
                        'seller': {
                            'name': 'localizedattribute:sellerName'
                        }
                    }
                }
            },
            'localizedAttributes': [
                {
                    'locale': 'ja-JP',
                    'sellerName': 'Amazon'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_occasion(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.Occasion.Updated',
                'payload': {
                    'state': {
                        'confirmationStatus': 'CONFIRMED'
                    },
                    'occasion': {
                        'occasionType': 'APPOINTMENT',
                        'subject': 'localizedattribute:subject',
                        'provider': {
                            'name': 'localizedattribute:providerName'
                        },
                        'bookingTime': '2018-11-20T19:16:31Z',
                        'broker': {
                            'name': 'localizedattribute:brokerName'
                        }
                    }
                }
            },
            'localizedAttributes': [
                {
                    'locale': 'ja-JP',
                    'subject': '根管治療',
                    'providerName': 'XYZ歯科',
                    'brokerName': 'XYZ歯科'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_media(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.MediaContent.Available',
                'payload': {
                    'availability': {
                        'startTime': '2020-05-20T21:00:00Z',
                        'provider': {
                          'name': 'localizedattribute:providerName'
                        },
                        'method': 'AIR'
                    },
                    'content': {
                        'name': 'localizedattribute:contentName',
                        'contentType': 'GAME'
                    }
                }
            },
            'localizedAttributes': [
                {
                  'locale': 'ja-JP',
                  'providerName': 'soko',
                  'contentName': 'sentakuki...'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_game(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.SocialGameInvite.Available',
                'payload': {
                    'invite': {
                        'relationshipToInvitee': 'FRIEND',
                        'inviter': {
                            'name': 'Max'
                        },
                        'inviteType': 'CHALLENGE'
                    },
                    'game': {
                        'offer': 'GAME',
                        'name': 'localizedattribute:gameName'
                    }
                }
            },
            'localizedAttributes': [
                {
                    'locale': 'ja-JP',
                    'gameName': 'The Red'
                }
            ],
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body_4_trash(cls):
        now_time = datetime.now()
        del_time = now_time + timedelta(minutes=60)

        return {
            'timestamp': now_time.isoformat(),
            'referenceId': 'id',
            'expiryTime': del_time.isoformat(),
            'event': {
                'name': 'AMAZON.TrashCollectionAlert.Activated',
                'payload': {
                    'alert': {
                        'garbageTypes': [
                            'COMPOSTABLE',
                            'RECYCLABLE_PLASTICS'
                        ],
                        'collectionDayOfWeek': 'TUESDAY'
                    }
                }
            },
            'relevantAudience': {
                'type': 'Multicast',
                'payload': {}
            }
        }

    @classmethod
    def make_body(cls, notify_type):
        body = ""
        if notify_type == 'weather':
            body = cls.make_body_4_weather_alert()
        elif notify_type == 'sports':
            body = cls.make_body_4_sports()
        elif notify_type == 'message':
            body = cls.make_body_4_message()
        elif notify_type == 'order':
            body = cls.make_body_4_order()
        elif notify_type == 'occasion':
            body = cls.make_body_4_occasion()
        elif notify_type == 'trash':
            body = cls.make_body_4_trash()
        elif notify_type == 'media':
            body = cls.make_body_4_media()
        elif notify_type == 'game':
            body = cls.make_body_4_game()
        else:
            body = cls.make_body_4_message()
        return body

    def send_notification_to_alexa(self, notify_type):
        # enable_logging()
        #self.enable_logging()

        token = self.get_access_token()
        body = self.make_body(notify_type)
        headers = {'Authorization': 'Bearer {}'.format(token)}
        r = requests.post(self.__proactive_url, headers=headers, json=body)
        if 200 != r.status_code and 202 != r.status_code:
            print(r.json())

