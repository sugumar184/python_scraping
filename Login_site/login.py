# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


login_url= 'login_url'
main_url = 'main_url'


with requests.Session() as s:
    cont = s.get(login_url)
    soup = BeautifulSoup(cont.text,'html.parser')
    token = soup.find('input',attrs={'name':'YII_CSRF_TOKEN'}).get('value')
    user_ip = soup.find('input',attrs={'name':'UserLogin[ip]'}).get('value')
    
    payload = {
        'UserLogin[office_mail]': 'mail_id',
        'UserLogin[password]': 'password',
        'YII_CSRF_TOKEN': token,
        'UserLogin[ip]': user_ip,
        'yt0': 'Login'
    }
    
    
    
    
    
    
    
    p = s.post(login_url,headers=headers,data=payload)
    print('p_status:: ',p.status_code)
    # print the html returned or something more intelligent to see if it's a successful login page.
    #print (p.text)
    main_cont = s.get(status_url,headers=headers,cookies=cookies)
    print('main_status:: ',main_cont.status_code)
    with open('p_cont.html','w') as f:
        f.write(main_cont.text)
    # An authorised request.
#     r = s.get(status_url)
#     print (r.text)