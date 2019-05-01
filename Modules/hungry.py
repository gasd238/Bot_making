import requests
import datetime
import re
from bs4 import BeautifulSoup
import discord

weekend_string = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

def hungry():
    now=datetime.datetime.now()
    def get_nextMeal(now):
        time = [480, 780, 1140]
        
        for i in range(len(time)):
            if (now.hour * 60 + now.minute) < time[i]:
                return i
        return len(time)
    try:
            now = now.replace(day = now.day + int(get_nextMeal(now) / 3)) 
    except ValueError: 
        try:
            now = now.replace(month = now.month + 1, day = 1, hour = 0) 
        except ValueError: 
            now = now.replace(year = now.year + 1, month = 1, day = 1, hour = 0) 
    soup=BeautifulSoup(requests.get("http://www.gsm.hs.kr/xboard/board.php?tbnum=8&sYear=%s&sMonth=%s" % (now.year, now.month)).text, 'html.parser')
    temp=soup.find_all('div', class_="food_list_box")
    if now.weekday() == 4 and now.hour>=13 or now.weekday() == 5 or now.weekday() == 6 and now.hour < 19:
        meal = '급식이 없느니라...'
    elif now.weekday() >= 0  and now.weekday() < 5 or now.weekday() == 6 and now.hour >= 19:
        if now.hour>=19:
            today = temp[now.day].find_all('div', class_="content_info")
        else:
            today = temp[now.day - 1].find_all('div', class_="content_info")
        if now.hour>=19 or now.hour<8:
            meal=today[0].getText()
            tm = '아침'
        elif now.hour>=8 and now.hour<13:
            meal=today[1].getText()
            tm ='점심'
        elif now.hour>=13 and now.hour<19:
            meal=today[2].getText()
            tm = '저녁'
    meal=meal.split('\n')
    for i in range(0, len(meal)):
        if re.compile('[0-9]+').match(meal[i]):
            del meal[i]
        if meal[i].startswith('*'):
            del meal[i:]
            break
    cmeal=[]
    descriptions = ''
    for i in range(0,len(meal)):
        meal[i]=meal[i].split('\xa0')
        meal[i][0] = meal[i][0].strip('/')
        meal[i][0] = meal[i][0].strip('*')
        meal[i][0] = meal[i][0].strip('..')
        if meal[i][0] == '생일을':
            continue
        cmeal.append(meal[i][0])
    if len(cmeal)==1:
            descriptions=cmeal[0]
    else:
        for i in range(0, len(cmeal)):
            descriptions=descriptions+'- '+cmeal[i]+'\n'
    embed = discord.Embed(title="%s년 %s월 %s일 %s의 %s 식단표이니라~~" % (now.year, now.month, now.day, weekend_string[int(now.weekday())], tm),description=descriptions, colour=0xf7cac9)
    return embed
