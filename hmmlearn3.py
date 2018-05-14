import json
import time
import sys
start_time = time.time()
#path = 'corpus_2.txt'
path =sys.argv[1]
#path = 'zh_train_tagged.txt'
tagged_data_file = open(path, encoding = "utf8")
tagged_data = tagged_data_file.read().splitlines()
d= dict()
tag_count=dict()
word=['','']
unique_tags=[]
transition = dict()
sums = dict()
sums['start']=0
sums['stop']=0
w=['','']
for x,val in enumerate(tagged_data):
	line = val.split()
	length=len(line)
	for y,l in enumerate(line):
		word_t=l.split()
		index = word_t[0].rfind('/')
		
		word[0]=word_t[0][:index]
		word[1]=word_t[0][index+1:]
		
		if word[0] in d:
			if word[1] in d[word[0]]:
				d[word[0]][word[1]]=d[word[0]][word[1]]+1
			else:
				d[word[0]][word[1]]=1
		else:
			d[word[0]]=dict()
			d[word[0]][word[1]]=1
			
		if word[1] in tag_count:
			tag_count[word[1]]=tag_count[word[1]]+1
		else:
			tag_count[word[1]]=1
		
		w[0]=word_t[0][:index]
		w[1]=word_t[0][index+1:]
		
		if w[1] not in unique_tags:
			unique_tags.append(w[1])
		
		if y==0:
			sums['start']=sums['start']+1
			if x==0:
				transition['start']= dict()
			if w[1] in transition['start']:
				transition['start'][w[1]]=transition['start'][w[1]]+1
			else:
				transition['start'][w[1]]=1			
		if y+1 != length:
			next=line[y+1].split('/');
			if w[1] in transition:
				sums[w[1]]=sums[w[1]]+1
				if next[1] in transition[w[1]]:
					transition[w[1]][next[1]]=transition[w[1]][next[1]]+1
				else:
					transition[w[1]][next[1]]=1
			else:
				transition[w[1]]=dict()
				transition[w[1]][next[1]]=1
				sums[w[1]]=1
		elif y == length-1:
			if w[1] in sums:
				sums[w[1]]=sums[w[1]]+1
			else: 
				sums[w[1]]=dict()
				sums[w[1]]=1
			if 'stop' in transition:
				if w[1] in transition['stop']:
					transition['stop'][w[1]]=transition['stop'][w[1]]+1
				else:
					transition['stop'][w[1]]=1
			else:
				transition['stop']=dict()
				transition['stop'][w[1]]=1
			#print (y)			
		else:
				break

				
k=3

for t in unique_tags:
	if t not in transition:
		transition[t] = dict()	
		for each_tag in unique_tags:
			transition[t][each_tag]= k

for f in transition.keys():
	for t in unique_tags:
		if t != 'start' and t != 'stop':
			sums[f]=sums[f]+k
			if t not in transition[f]:
				transition[f][t]=k			
			else:
				transition[f][t]=transition[f][t]+k
				
for i in d:
	for j in d[i]:
		d[i][j]= d[i][j]/tag_count[j]		
				
for i in transition:
	for j in transition[i]:
		if i!='stop':
			transition[i][j]=transition[i][j]/sums[i]
		else:
			transition[i][j]=transition[i][j]/sums[j]

final_probs = dict()
final_probs["emission"]=d
final_probs["transition"]=transition
with open('hmmmodel.txt','w') as fp:
	json.dump(final_probs,fp)
tagged_data_file.close()
fp.close()
#print("--- %s seconds ---" % (time.time() - start_time))