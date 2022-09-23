import requests
from bs4 import BeautifulSoup #web scraping
import smtplib #send email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime


now = datetime.datetime.now()

#email content placeholder
content = ''

#EXTRACTION
def extract_news(url):
    print("Extracting Hacker News Stories...")
    cnt = ''
    cnt +=('<b>HN Top Stories: <b>\n' + '<br>'+ "-"*50+ '<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i,tag in enumerate(soup.find_all('td', attrs={'class':'title', 'valign': '' })):
        cnt += ((str(i+1)+ ' :: ' + tag.text + "\n" + '<br>') if tag.text!='More' else '')

    return(cnt)

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>------<br>')
content += ('<br><br> End of Message')

#sending emails

print("composing email")

#update email details

SERVER = 'smtp.gmail.com'
PORT = 587
FROM = ''
TO = ''
PASS = ''

msg= MIMEMultipart()

msg['Subject'] = 'TOP NEWS HACKERNEWS' + ' ' + str(now.day) + '-'+ str(now.month) + '-'+ str(now.year) + '-'
msg['From'] = FROM
msg['To'] = TO


msg.attach(MIMEText(content, 'html'))

#fp.close()

print('Initializing server')

server = smtplib.SMTP(SERVER, PORT)

server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print("Email Sent")

server.quit()