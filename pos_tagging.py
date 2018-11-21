##对原文章进行附码
import os
import csv
import time
import nltk
import traceback
from  Util import getdir,mkdir
from nltk.tag import pos_tag, pos_tag_sents
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize

orgDir = "语料库简版"
tagDir  = "附码语料库"

def posTagging(orgFile,targetFile):
	count_org , count= 0, 0
	english_punctuations = ['(', '[', '<', ')', ']','>',',', '.', ':',
							';', '?', '!', '@', '#', '%', '$', '*',' ','','\n']
	try:	
		f=open(orgFile,'r')
		lines=f.readlines()
	# except Exception as e:
		# print(orgFile,"文件解码错误\n",traceback.format_exc())
	except UnicodeDecodeError:
		print("Error:",orgFile,"文件解码错误")
		return 2,1
	else:
		f.close()

	ff=open(targetFile,'w')
	for line in lines:
		#统计原文词数
		line_list = line.split()
		words_list = [i for i in line_list if i not in english_punctuations]
		count_org += len(words_list) 
		for w in words_list:  #处理Prob(source =l) 
			if '(' in w and w[0]!='(' and w[-1]!='(':
				# print(w)
				count_org += 1
			elif ')' in w and w[0]!=')' and w[-1]!=')' and w[-1] not in english_punctuations[6:12]: #(2016),
				# print(w)
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
				pre_word = word
				line_str += word
		ff.write(line_str)
		ff.write('\n')
	ff.close()
	if count==0:
		print(orgFile,"文件总词数为0")
		return 2,1
	return count_org,count
	print("原文总词数",count_org," 附码后总词数：",count)	



def markPos():
	csvHeader = ["文件名","源文件词数","附码文件词数","词数差","差词占比"]
	for subDir in os.listdir(orgDir):  #子目录
		data = []
		pathname = os.path.join(orgDir, subDir)
		if (os.path.isdir(pathname)):
			new_pathname = os.path.join(tagDir, subDir)
			mkdir(new_pathname)
			logFile = os.path.join(new_pathname,"log.csv")
			with open(logFile, "w", newline='') as f:
			        # with open(birth_weight_file, "w") as f:
			        writer = csv.writer(f) 
			        now = time.strftime("%Y-%m-%d %H:%M:%S")
			        writer.writerows([[now]])
			        writer.writerows([csvHeader])
			        f.close()
			for filename in os.listdir(pathname): #遍历文件
				if os.path.splitext(filename)[1][1:] =='txt':
					orgFile = os.path.join(pathname,filename)
					targetFile = os.path.join(new_pathname,filename)
					print(orgFile)
					orgCount,newCount = posTagging(orgFile,targetFile)
					if newCount==2:
						precent = 'ERROR'
					else:
						precent = abs(orgCount-newCount),str(round(abs(orgCount-newCount)/newCount*100))+'%'
					data.append([filename,orgCount,newCount,precent])
					# with open(logFile,'a',newline='') as f:
					# 	writer = csv.writer(f)
					# 	writer.writerows([[filename,orgCount,newCount,abs(orgCount-newCount),str(round(abs(orgCount-newCount)/newCount*100))+'%']])
					# 	f.close()
			with open(logFile,'a',newline='') as f:
				writer = csv.writer(f)
				writer.writerows(data)
				f.close()



if __name__ == '__main__':
	markPos()

	
					
