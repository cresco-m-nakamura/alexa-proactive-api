import proactive

client_id = ''
client_secret = ''


def main():
    pa = proactive.Proactive(client_id, client_secret)
    pa.send_notification_to_alexa('game')


if __name__ == '__main__':
    main()



