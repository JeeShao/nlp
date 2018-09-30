import os
import csv
import time
tagDir = "附码语料库"
sectionDir = "分段语料库"
csvHeader = ["Filename","Title","Author","Abstract","Introduction",
			 "Method","Discussion","Conclusion","Acknowledgment"]

def mkdir(path):
    # 去除首尾空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path) 
        print (path+' 创建成功')
        return True
    else:
        print (path+' 目录已存在')
        return False
def cutEssay(orgFile,targetDir,logFile):
	count_abstract_JJ,count_acknowledgment_JJ = 0,0
	dicts = {'<title_NN>':'</title_NNP>',
		    '<author_NN>':'</author_NNP>',
		    '<abstract_NN>':'</abstract_NNP>',
		    '<abstract_JJ>':'</abstract_NN>', #AP1801
		    '<Introduction_NNP>':'</introduction_NN>', 
	        '<method_NN>':'</method_NNP>',
	        '<discussion_NN>':'</discussion_NN>',
	        '<conclusion_NN>':'</conclusion_NN>',
	        '<acknowledgment_JJ>':'</acknowledgment_NN>', #CL1705
	        '<acknowledgment_NN>':'</acknowledgment_NN>'}
	try:
		f=open(orgFile,'r')
		lines=f.readlines()
	except UnicodeDecodeError:
		print("Error:",orgFile,"文件解码错误")
		return
	else:
		f.close()
	ff = ''
	dict_key = ''
	data = dict((el,0) for el in csvHeader)
	# print(data)
	# v2 = dict.fromkeys(csvHeader,0)
	# print(v2)
	for line in lines:
		line_list = line.split()
		if line_list:
			# print (line_list[0])
			# print (dicts.keys())
			if line_list[0] in dicts.keys():
				data[(line_list[0].split('_')[0][1:]).title()] += 1
				if line_list[0] == '<abstract_JJ>':
					count_abstract_JJ+=1
				if line_list[0] == '<acknowledgment_JJ>':
					count_acknowledgment_JJ+=1
				dict_key = line_list[0]
				ff=open(os.path.join(targetDir,os.path.basename(orgFile).split('.')[0]+'_'+line_list[0].split('_')[0][1:]+'.txt'),'w')
			ff.write(line)
			ff.write('\n')
			if line_list[-1] in [dicts[dict_key],dicts[dict_key]+"\n"]:
				ff.close()
	print(count_abstract_JJ,' ',count_acknowledgment_JJ)
	print(data)
	data['Filename'] = os.path.basename(orgFile).split('.')[0]
	with open(logFile,'a',newline='') as f:
		writer = csv.DictWriter(f, fieldnames=csvHeader)
		# writer = csv.writer(f)
		# writer.writeheader()
		writer.writerow(data)
		f.close()
		

def main():
	mkdir(sectionDir)
	logFile = os.path.join(sectionDir,"log.csv")
	with open(logFile, "w", newline='') as f:
		writer = csv.writer(f)
		now = time.strftime("%Y-%m-%d %H:%M:%S")
		# writer.writerows([[now]])
		writer.writerows([csvHeader])
		f.close()

	for subDir in os.listdir(tagDir):
		pathname = os.path.join(tagDir, subDir)
		if (os.path.isdir(pathname)):
			new_pathname = os.path.join(sectionDir, subDir)
			mkdir(new_pathname)
			for filename in os.listdir(pathname):
				orgFile = os.path.join(pathname,filename)
				targetDir = os.path.join(new_pathname,filename.split('.')[0])
				mkdir(targetDir)
				cutEssay(orgFile,targetDir,logFile)

if __name__ == '__main__':
	main()
	