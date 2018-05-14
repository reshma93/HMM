import json
import sys
import time
from pprint import pprint

start_time = time.time()
with open('hmmmodel.txt', 'r') as fp:
	complete_dict = json.load(fp)

emission = dict()
emission = complete_dict["emission"]	
transition = complete_dict["transition"]

#path = 'test.txt'
path = sys.argv[1]
#path = 'zh_dev_raw.txt'
data_file = open(path, encoding = "utf8")
raw_data = data_file.read().splitlines()

f= open("hmmoutput.txt","w+",encoding='utf8')
no_of_lines = len(raw_data)
for x, val in enumerate(raw_data):
	line = val.split()
	prob = dict()	
	for y, word in enumerate(line):
		if word not in emission:			
			
			emission[word]=dict()
			if word.isdigit():
				emission[word]['CD']=1
			elif len(word) == 1 and word.isupper():
				emission[word]['NN']=1
			elif word.endswith(".net") or word.endswith(".com"):
				emission[word]['ADD']=1
			else:	
				for tag in transition['start']:
					emission[word][tag]=1
			'''max_prob=0
			if y==0:
				for tag in transition['start']:
					if max_prob < transition['start'][tag]:			
						max_prob = transition['start'][tag]
						predicted_tag = tag
							
			elif y==len(line)-1:
				for tag in transition['stop']:
					if max_prob < transition['stop'][tag]:
						max_prob = transition['stop'][tag]
						predicted_tag = tag
			else:
				for tag in emission[line[y-1]]:
					for t in transition[tag]:
						if max_prob < transition[tag][t]:
							max_prob = transition[tag][t]
							predicted_tag = t
			emission[word]=dict()
			emission[word][predicted_tag]=1'''
		prob[word+"_"+str(y)]=dict()
		if y==0:	
			for tag in emission[word]:
				if tag not in transition['start'] or tag not in emission[word]:
					if tag not in transition['start']:
						transition_prob=0	
					if tag not in emission[word]:
						emission_prob=0
				else:
					transition_prob=transition['start'][tag]
					emission_prob=emission[word][tag]
				
				prob_calc= transition_prob*emission_prob
				word_1= word+"_"+str(y)
				prob[word+"_"+str(y)][tag]=['start',prob_calc]
		else:
			intermediate_probs=dict()
			for tag in emission[word]:
				max=0
				tag_from=''
				for tag_1 in prob[line[y-1]+"_"+str(y-1)]:
					if tag not in transition[tag_1] or tag not in emission[word]:
						if tag not in transition[tag_1]:
							transition_prob=0	
						if tag not in emission[word]:
							emission_prob=0
					else:
						transition_prob=transition[tag_1][tag]
						emission_prob=emission[word][tag]
					
					lower_case = line[y-1]+"_"+str(y-1)
					intermediate_probs[tag_1]=transition_prob*emission_prob*prob[lower_case][tag_1][1]
					
					if max < intermediate_probs[tag_1]:
						tag_from= tag_1
						max= intermediate_probs[tag_1]
					
					word_1= word+"_"+str(y)
					prob[word_1][tag]=[tag_from,max]
	len_1 = len(line)
	list =[None]*len_1
	for y, word in enumerate(line):
		last_word = line[len_1-y-1]
		last_word_lower= last_word.lower()
		word_prob = dict()
		word_prob = prob[last_word+"_"+str(len_1-1-y)]
		if y==0:
			max =0
			for p in word_prob:
				if max < word_prob[p][1]:
					tag = p
					back_pointer = word_prob[p][0]
					max = word_prob[p][1]
			list[len_1-y-1]=last_word+"/"+tag
		else:
			list[len_1-y-1]=last_word+"/"+back_pointer
			back_pointer = word_prob[back_pointer][0]
	f.write(" ".join(list))
	if x != no_of_lines-1:
		f.write("\n")
f.close()
#print("--- %s seconds ---" % (time.time() - start_time))