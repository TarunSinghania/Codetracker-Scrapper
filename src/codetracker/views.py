from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.http import HttpResponse
from django.core import serializers
  
import multiprocessing
from multiprocessing import Process, Manager
from selenium import webdriver
import urllib.request 
from urllib.request import urlopen
from bs4 import BeautifulSoup
import threading 
import os 
import time
import json




#	return HttpResponse(codeforces_future)
#	return JsonResponse(codeforces_future)	
#  posts_serialized = serializers.serialize('json', codeforces_future)


def spliter(s,spl,ind):
    indx=[i for i,j in enumerate(s) if j==spl][ind-1]
    return [s[:indx],s[indx+1:]]
#codechef
def contest(tr):
	td = tr.find_all('td')
	tdlist = []
	for i in td:
		tdlist.append(i.text)
	contest_samplea = {'name':'','full_name':'','start_date':'','start_time':'','end_date':'','end_time':'','contest_duration':''}
	contest_samplea['name'] = tdlist[0]
	contest_samplea['full_name'] = tdlist[1]
	contest_samplea['start_date'] = spliter(tdlist[2],' ',3)[0]
	contest_samplea['start_time'] = spliter(tdlist[2],' ',3)[1]
	contest_samplea['end date']	 = spliter(tdlist[3],' ',3)[0]
	contest_samplea['end_time']	 = spliter(tdlist[3],' ',3)[1]
	return contest_samplea


#codeforces
def contest2(tr):
	td = tr.find_all('td')
	tdlist = []
	for i in td:
		tdlist.append(i.text.strip())
	contest_sampleb = {'name':'','full_name':'','start_date':'','start_time':'','end_date':'','end_time':'','contest_duration':''}
	contest_sampleb['name'] = tdlist[0]
	contest_sampleb['start_date'] = spliter(tdlist[2],' ',1)[0]
	contest_sampleb['start_time'] = spliter(tdlist[2],' ',1)[1]
	contest_sampleb['contest_duration'] = tdlist[3]
	return contest_sampleb

#hackerrank
def contest3(tr):
	name0 =tr.find('div',class_='contest-name head-col truncate txt-navy')
	name1 =tr.find('span',{"itemprop":"name"})
	start_date_time = tr.find('meta',{'itemprop':'startDate'})
	end_date_time = tr.find('meta',{'itemprop':'endDate'})
	contest_samplec = {'name':'','full_name':'','start_date':'','start_time':'','end_date':'','end_time':'','contest_duration':''}
	if(name0) :
		contest_samplec['name'] = name0.text

	if(name1):
		contest_samplec['name'] =name1.text
		
	if(start_date_time):
		contest_samplec['start_date']=spliter(start_date_time['content'],'T',1)[0]
		contest_samplec['start_time']=spliter(start_date_time['content'],'T',1)[1]

	if(end_date_time):
		contest_samplec['end_date']=spliter(end_date_time['content'],'T',1)[0]
		contest_samplec['end_time']=spliter(end_date_time['content'],'T',1)[1]

	return contest_samplec



#codechef
hdr = {'User-Agent': 'Chrome/34.0.1271.64',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}



def task1(codechef_future,codechef_present):
	url = "http://www.codechef.com/contests"
	reque=urllib.request.Request(url,None,hdr) 
	html = urlopen(reque)	

	soup = BeautifulSoup(html, 'lxml')


	table = soup.findAll('table', {'class': 'dataTable'})
	table1 = table[0] # present
	table2 = table[1] # upcoming


	present_table_rows = table1.find_all('tr')
	lenr = len(present_table_rows)
	#ignore first row headings range 1 to len 
	for i in range(1,lenr): 
		tr = present_table_rows[i]
		codechef_present.append(contest(tr).copy())
		
	#print(codechef_present)

	future_table_rows = table2.find_all('tr')
	lenr = len(future_table_rows)
	for i in range(1,lenr): 
		tr = future_table_rows[i]
		codechef_future.append(contest(tr).copy())
		

	

def task2(codeforces_future):

	url2 = "http://www.codeforces.com/contests"

	reque2=urllib.request.Request(url2,None,hdr) 
	html = urlopen(reque2)	

	soup = BeautifulSoup(html, 'lxml')



	table = soup.findAll('table')
	table1 = table[0] #upcoming 

	

	future_table_rows = table1.find_all('tr')
	lenr = len(future_table_rows)
	for i in range(1,lenr): 
		tr = future_table_rows[i]
		codeforces_future.append(contest2(tr).copy())
		

	#print(codeforces_future)


def task3(hackerrank_future):
	url3 = "https://www.hackerrank.com/contests"

	reque3=urllib.request.Request(url3,None,hdr) 
	html = urlopen(reque3)	


	soup = BeautifulSoup(html, 'lxml')
	#print(soup)


	active = soup.find('div',class_='active_contests')
	

	li_list = active.find_all('li')

	for tr in li_list:	
		hackerrank_future.append(contest3(tr).copy())
		

	#print(hackerrank_future)

def process2(codeforces_future,codechef_present,hackerrank_future,codechef_future):
	t1 = threading.Thread(target=task1, name='t1',args=(codechef_future,codechef_present)) 
	t2 = threading.Thread(target=task2, name='t2',args=(codeforces_future,))  
	t3 = threading.Thread(target=task3, name='t3',args=(hackerrank_future,)) 
	t1.start()
	t2.start()
	t3.start()

	t1.join()
	t2.join()
	t3.join()

def process1(hackerearth_ongoing,hackearth_upcoming):
	contest_sample = {'name':'','full_name':'','start_date':'','start_time':'','end_date':'','end_time':'','contest_duration':''}
	options = webdriver.ChromeOptions()
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
	#options.add_argument('--no-sandbox')
	browser = webdriver.Chrome(chrome_options=options)
	browser.get("https://www.hackerearth.com/challenges/competitive/")

	soup = BeautifulSoup(browser.page_source, 'lxml')
	#print(soup)



	active = soup.find('div',class_='ongoing challenge-list')
	upcoming = soup.find('div',class_='upcoming challenge-list')


	active_list = active.find_all('div',class_='challenge-card-modern')
	upcoming_list = upcoming.find_all('div',class_='challenge-card-modern')

	for tr in active_list: 
	    name = tr.find('div',class_='challenge-name ellipsis dark')
	    #print(name)
	    #one zerp 12mins
	    end_time_minutes_one= tr.find('div',{'id':'minutes-1'})
	    end_time_minutes_zero= tr.find('div',{'id':'minutes-0'})
	    end_time_hours_one=tr.find('div',{'id':'hours-1'})
	    end_time_hours_zero=tr.find('div',{'id':'hours-0'})
	    end_time_days_one=tr.find('div',{'id':'days-1'})
	    end_time_days_zero=tr.find('div',{'id':'days-0'})
	    if(end_time_minutes_zero):
	        end_time_minutes = end_time_minutes_one.text +end_time_minutes_zero.text
	        end_time_hours = end_time_hours_one.text + end_time_hours_zero.text
	        end_time_days = end_time_days_one.text + end_time_days_zero.text
	        contest_sample['end_time'] = end_time_days+':'+end_time_hours+':'+end_time_minutes 
	    contest_sample['name'] = name.text
	    hackerearth_ongoing.append(contest_sample.copy())

	    #print(contest_sample)
	    
	for tr in upcoming_list:
	    for key in contest_sample:
	        contest_sample[key] = ''
	    name = tr.find('div',class_='challenge-name ellipsis dark')
	    #print(name)
	    starts_in = tr.find('div',class_='date less-margin dark')
	    #print(starts_in)
	    contest_sample['start_date'] =  spliter(starts_in.text,',',1)[0]
	    contest_sample['start_time'] =  spliter(starts_in.text,',',1)[1]
	    contest_sample['name'] = name.text
	    hackearth_upcoming.append(contest_sample.copy())
	    #print(contest_sample)

	
		  

def index(request):
	
	manager = Manager()
	codechef_present   =manager.list()
	codechef_future    =manager.list()
	hackerrank_future  =manager.list()
	codeforces_future  =manager.list()
	hackearth_upcoming =manager.list()
	hackerearth_ongoing=manager.list()


	p1 = multiprocessing.Process(target=process1,args=(hackerearth_ongoing,hackearth_upcoming)) 
	p2 = multiprocessing.Process(target=process2,args=(codeforces_future,codechef_present,hackerrank_future,codechef_future)) 

	# starting process 1 
	p1.start() 
	# starting process 2 
	p2.start() 

	# wait until process 1 is finished 
	p1.join() 
	# wait until process 2 is finished 
	p2.join()
	y = codechef_present[0:len(codechef_present)]
	json.dumps(y)
	z = codechef_future[0:len(codechef_future)]
	json.dumps(z)
	c = codeforces_future[0:len(codeforces_future)]
	json.dumps(c)
	h = hackerrank_future[0:len(hackerrank_future)]
	json.dumps(h)
	a= hackearth_upcoming[0:len(hackearth_upcoming)]
	json.dumps(a)
	b=hackerearth_ongoing[0:len(hackerearth_ongoing)]
	json.dumps(b)
	#return HttpResponse(hackearth_upcoming)
	return JsonResponse({'codechef_present':y,'codechef_future':z,'codeforces_future':c,'hackerrank_future':h,'hackearth_upcoming':a,'hackerearth_ongoing':b},safe=False) 

		
		
		