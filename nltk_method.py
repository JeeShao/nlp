# coding:UTF-8
'''
对文本及逆行分句分词，然后标注词性。
'''
import nltk
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize

count_org , count= 0, 0
english_punctuations = ['(', '[', '<', ')', ']','>',',', '.', ':',
						';', '?', '!', '@', '#', '%', '$', '*',' ','','\n']
f=open('demo.txt','r',encoding='UTF-8')
lines=f.readlines()
f.close()
ff=open('demo1.txt','w',encoding='UTF-8')
for line in lines:
	#统计原文词数
	line_list = line.split()
	words_list = [i for i in line_list if i not in english_punctuations]
	count_org += len(words_list) 
	for w in words_list:  #处理Prob(source =l) 
		if '(' in w and w[0]!='(' and w[-1]!='(':
			print(w)
			count_org += 1
		elif ')' in w and w[0]!=')' and w[-1]!=')' and w[-1] not in english_punctuations[6:12]: #(2016),
			print(w)
			count_org += 1

	line_str, pre_word = '',''
	res = pos_tag_sents([word_tokenize(i) for i in sent_tokenize(line)])
	for sents in res:  #每一个分句
		for word_tuple in sents: #每个分句的分词
			if word_tuple[0] in english_punctuations:
				word = ''.join([' ' for i in english_punctuations[0:3] if word_tuple[0]==i]) + word_tuple[0]
			else:
				if pre_word in [' '+ j for j in english_punctuations[0:3]]:
					word = "_".join(word_tuple)
				else:
					word = ' '+"_".join(word_tuple)
				count += 1
			# print("_".join(word_tuple))
			pre_word = word
			line_str += word
	ff.write(line_str)
	ff.write('\n')
	# print("--".join(wordpunct_tokenize(line)))
	# print([word_tokenize(t) for t in sent_tokenize(line)])
ff.close()
print("原文总词数",count_org," 附码后总词数：",count)