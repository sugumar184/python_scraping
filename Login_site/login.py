# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

with requests.Session() as s:
    cont = s.get(login_url)
    soup = BeautifulSoup(cont.text,'html.parser')
    token = soup.find('input',attrs={'name':'YII_CSRF_TOKEN'}).get('value')
    user_ip = soup.find('input',attrs={'name':'UserLogin[ip]'}).get('value')
    
    payload = {
        'UserLogin[office_mail]': 'sugumar.n@optisolbusiness.com',
        'UserLogin[password]': 'Sugu@123',
        'YII_CSRF_TOKEN': token,
        'UserLogin[ip]': user_ip,
        'yt0': 'Login'
    }
    
    p = s.post(login_url,headers=headers,data=payload)
    print('p_status:: ',p.status_code)
    try:
        while True:
            main_cont = s.get(status_url,headers=headers,cookies=cookies)
            print('main_status:: ',main_cont.status_code)
            sp = BeautifulSoup(main_cont.text,'html.parser')
            b = sp.select('div.col-md-12.dailystatus span.col-md-4')
            print(b[0].get_text())
            print(b[1].get_text())
            print(b[2].get_text())
            time.sleep(30)
    except KeyboardInterrupt:
            print('interrupted!')
       