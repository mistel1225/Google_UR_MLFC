import json
import re
import itertools
import pandas as pd
import csv
from pandas import read_csv

## Part 1: Read json file and split into 8 categories of json files
## Can make into comment lines once done splitting

# df=pd.read_json(r'~/data35000.json'))
# d='{}'

# with open('camera.json', mode='w', encoding='utf-8') as feedsjson:    
#   z=json.loads(d)
#   for row in df:
#     if((((df[row]['category']).split(","))[0])=='Camera'):
#       y=df[row]
#       z.update(y)
#       json.dump(z,feedsjson)
#       feedsjson.write('\n')


# Part 2: split words and count their respective frequencies(no repetition)
# Can make into comment lines once done counting to speed up program

# wordlist=[]
# wordfreq=[] 
# with open('camera.json', mode='r', encoding='utf-8') as f:
#   for row in f:
#     y=json.loads(row)
#     x = y["content"]
#     k=re.split(r"[)(/,-. \n]\s*",x)
#     for word in k:
#       wordlist.append(word)

# for w in wordlist:
# 	wordfreq.append(wordlist.count(w))

# x=list(zip(wordlist, wordfreq))

# with open('camerajson_counted.csv','w') as f:
#   write = csv.writer(f)
#   write.writerows(x)

# df = read_csv('camerajson_counted.csv')
# df.columns = ['word', 'freq']
# df.sort_values(by=["freq"], ascending=False, inplace=True)
# df.drop_duplicates(subset=['word'], inplace=True)
# df.to_csv('camera_analysis.csv')

## Part 3: Fill in the list with keywords 
## Do not comment this part, since txt file will be edited
filterlist=[]				
f = open('keywords.txt','r')
for x in f:
	filterlist.append(x.rstrip('\n'))

## Part 4: Print top N (default=10) keywords with highest frequencies
counter = 0
fd = 'datasets/cnb_analysis.csv'
k = read_csv(fd)		##change csv file as input
k = k.loc[:, ~k.columns.str.contains('^Unnamed')]
print(fd+"\n")
for g in range(len(k['word'])):
	for m in filterlist:
		if(m == k['word'][g]):
			counter +=1
			# print(k[k.word==m])
			if(len(m)<9):
				print(str(m) + "\t\t" + str(k['freq'][g]))
			else:
				print(str(m) + "\t" + str(k['freq'][g]))
	if (counter == 10):		##print the first N keywords with their respective frequencies
		break

