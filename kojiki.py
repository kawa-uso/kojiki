import requests, bs4, datetime, pickle
from send_mail import send_mail
from send_slack import send_slack

res = requests.get('https://leia.5ch.net/poverty/subback.html')
#res.encoding = res.apparent_encoding
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text.encode(res.encoding), 'html.parser')
trad_elems = soup.select('#trad > a')
trad_title_list = []
trad_url_list = []
for trad_text in trad_elems:
    trad_url = trad_text.get('href')[:-4]
    trad_title = trad_text.getText().split()
    if trad_title[1].startswith('【乞食'):
        trad_url_list.append(trad_url)
        trad_title_add = ' '.join(trad_title[1:-2])
        trad_title_list.append(trad_title_add)
file_path = '/home/otter/kojikimail/trad.dump'
try:
    with open(file_path, mode='rb') as f:
        trad_old = pickle.load(f)
except FileNotFoundError:
    trad_old = []
trad = list(zip(trad_title_list, trad_url_list))
trad_new = list(set(trad) - set(trad_old))
if trad_new:
    with open(file_path, mode='wb') as f:
        pickle.dump(trad, f)
    for trad_title, trad_url in trad_new:
        kenmei = trad_title 
        message = '{}\ntwinkle2ch://leia.5ch.net/test/read.cgi/poverty/{}'.format(trad_title, trad_url)
        message_slack = '{}\nhttps://leia.5ch.net/test/read.cgi/poverty/{}\ntwinkle2ch://leia.5ch.net/test/read.cgi/poverty/{}'.format(trad_title, trad_url, trad_url)
        send_mail(kenmei, message)
        send_slack(message_slack)
