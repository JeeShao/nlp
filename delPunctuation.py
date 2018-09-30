# coding:UTF-8
'''
对经CLAWS附码后的文本进行清理，删除多余内容并统计词数
'''
f=open('demo.txt','r')
lines=f.readlines()
f.close()

str1 = "<s>\n</s>\n"
count = 0
ff=open('demo1.txt','w')
for line in lines:
	# print(line)
	strs = ''
	words = line.split(' ')
	for word in words:
		# print(word)
		if word in str1:
			continue
		elif len(word)==3 and word[0]==word[2]:
			word=word[0]
		else:
			word=' '+word
			count += 1
		if strs=='':
			strs+=word.strip()
		else:
			strs += word
	if strs:
		print(strs)
		ff.write(strs)
		ff.write('\n')
print("行数：",len(lines)," 总词数：",count)
ff.close() 