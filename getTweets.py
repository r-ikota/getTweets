import os, sys, time, datetime, json, calendar
from twitter import *

#%%
homedir = os.environ.get('HOME', 
                os.environ.get('USERPROFILE',
                ''
                ))

kf_path = os.path.join(homedir, '.dl-tweets')

with open(kf_path,'r') as keyfile:
    keys = json.load(keyfile)
    APP_NAME = keys['APP_NAME']
    CONSUMER_KEY = keys['CONSUMER_KEY']
    CONSUMER_SECRET = keys['CONSUMER_SECRET']


OAUTH_FILENAME = homedir + os.sep + '.twitter_log_oauth'

def twtime2seconds(t):
    hoge = time.strptime(t, "%a %b %d %H:%M:%S +0000 %Y")
    dateC1 = datetime.datetime(hoge.tm_year, hoge.tm_mon, hoge.tm_mday, hoge.tm_hour, hoge.tm_min)
    return calendar.timegm(dateC1.timetuple())

def time2date(t):
  weekday = (u'月曜日', u'火曜日', u'水曜日', u'木曜日', u'金曜日', u'土曜日', u'日曜日')
  datestring = (str(t.tm_year) + u'年' + str(t.tm_mon) + u'月' + str(t.tm_mday) + u'日 '
    + weekday[t.tm_wday] + ' ' + (u'%02d' % t.tm_hour) + ':' + (u'%02d' % t.tm_min))
  return datestring

def main():
    argvs = sys.argv
    argc = len(argvs)

    if (argc != 4):
        print('arguments must be like this: username 2017/12/01 2018/01/05')
        quit()

    screen_name = argvs[1]
    dateStr1 = argvs[2]
    dateStr2 = argvs[3]


    d1 = time.strptime(dateStr1, "%Y/%m/%d")
    d2 = time.strptime(dateStr2, "%Y/%m/%d")
    dateS1 = datetime.datetime(d1.tm_year, d1.tm_mon, d1.tm_mday)
    dateS2 = datetime.datetime(d2.tm_year, d2.tm_mon, d2.tm_mday)
    dateS2 = dateS2 + datetime.timedelta(days=1)

    print('from', dateS1.ctime(), '\nuntil', dateS2.ctime(), '\n\n')

    sec1 = time.mktime(dateS1.timetuple())
    sec2 = time.mktime(dateS2.timetuple())

    if sec1 > sec2:
        print('the first argument must be since-date!')
        quit()

    if not os.path.exists(OAUTH_FILENAME):

        oauth_dance(

            "the Python Twitter Logger", CONSUMER_KEY, CONSUMER_SECRET,

            OAUTH_FILENAME)

    oauth_token, oauth_token_secret = read_token_file(OAUTH_FILENAME)

    t = Twitter(
        auth=OAuth(
            oauth_token, oauth_token_secret, CONSUMER_KEY, CONSUMER_SECRET),
        domain='api.twitter.com')

    max_round = 40

    round = 0

    max_id = None

    to_record_msgs = []

    while round < max_round:
        kwargs = dict(screen_name=screen_name, include_rts=True)
        if max_id: kwargs['max_id'] = max_id
        tweets = t.statuses.user_timeline(**kwargs)

        for msg in tweets:
            max_id = msg['id']
            created_time = twtime2seconds(msg['created_at'])
            if sec1 <= created_time < sec2:
                to_record_msgs.append(msg)
            elif created_time < sec1:
                round=max_round
                break
        if max_id: max_id -= 1
        round += 1

    #tweets = t.statuses.user_timeline(screen_name=screen_name, count=20)

    fd = open('out.txt', 'wb')
    for s in to_record_msgs:

        rd_time = time.localtime(twtime2seconds(s[u'created_at']))
        rd_time_f = time2date(rd_time)
        link = 'https://twitter.com/' + screen_name + '/status/' + str(s[u'id'])
        ss = '\n' + s['text'] + '\n' + rd_time_f + '\n' + link + '\n\n'
        
        fd.write(ss.encode('utf-8'))

if __name__ == '__main__':
    main()