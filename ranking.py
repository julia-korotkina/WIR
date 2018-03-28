import sys 
import bs4 
import re
import string
import csv
from math import log
import pandas as pd

k1 = 1.2
bb = 0.75
avdl = 500
Numb = 1000000000
qtf = 1
s = 0.20
qf = 1

def vsm_relevance (tf, qtf, N, df, dl, avdl, s):
	if tf==0:
		tf = 1
	first =log((1.5 + log(tf))/(1-s+s*dl/avdl))
	third = log((N+1)/df)
	return ( 1+ first)*qtf*third

def bm25_relevance(df, tf, qf, N, dl, avdl):
	K = k1* (1-bb+ bb*(float(dl)/float(avdl)))
	idf = log((N-df+0.5)/(df+0.5))
	second = tf*(k1+1)/(tf+K)
	return idf*second

read_doc_frec = open('rankings/document_frequency.csv')
doc_frec = csv.DictReader(read_doc_frec)

query_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
for q in query_num:
	print(q)
	read_query = open ('rankings/Query_%d/urls.csv'%q)
	csv_list = csv.DictReader(read_query)
	result = []
	docs = []
	for row in csv_list:
		query = row['query text']
		docID = row['docID']
		query_description = row['query description']
		url = row['url']
		temp = [query,query_description, url, docID]
		if int(docID)!=-1:
			docs.append(docID)
			result.append(temp)
	read_query.close()
	searched_words = query.split(' ')
	len_sw = len(searched_words)

	rankScore = []
	for doc_number in docs:
		doc_n = int(doc_number)
		read_file = open('rankings/Query_%d/Documents/%d.html'%(q, doc_n), encoding='utf-8', errors='ignore')
		content = read_file.read().lower()
		dl = len(content.split())
		score = 0
		soup = bs4.BeautifulSoup(content, "html.parser")
		for word in searched_words:
			if len(word)>2 :
				for item in doc_frec:
					if word==item['term']:
						df = item['document frequency']
						break					
				results = soup.find_all(string=re.compile('.*{0}.*'.format(word)), recursive=True)
				tf = len(results)
				temp = bm25_relevance(int(df), tf, qf, Numb, dl, avdl)
				# temp_bm25 = vsm_relevance(tf, qtf, Numb, int(df), dl, avdl, s)
				score = score +temp
		rankScore.append(round(score, 3))
	sorted_val = sorted(rankScore,reverse=True)
	diction = dict(list(enumerate(sorted_val)))

	prepared = []
	for item in rankScore:
		for i in diction:
			if item==diction[i]:
				a = [i, item]
				prepared.append(a)

	to_add =[]
	n = 0
	for i in result:
		b = prepared[n]
		a= i+b
		to_add.append(a)
		n = n +1

	
	frame = pd.DataFrame(to_add, columns = ["query", "query_description", "url","docID", "rank", "rankScore"])
	frame.to_csv('results/RM_BM25_%d_2017400420.csv'%q,index=False)
	# frame.to_csv('results/RM_VSM_%d_2017400420.csv'%q,index=False)
