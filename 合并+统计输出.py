import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
import re
import collections

def eachFile(filepath):#,outpath1,outpath2):

    fnum = 0  # 用于统计所有txt文件的个数
    txtall = []
    nameall = []
    delete = 0  #用于统计有多少句子多余

    opentxtall = open(filepath + '/AllTxts.txt', 'a')  # 开全内容+文件名txt
    opennameall = open(filepath + '/AllNames.txt','a')  #开全文件名txt
    have_deleted = open(filepath + '/HaveDeleted.txt','a')  #开被删除的句子的统计txt

    pathdir1 = os.listdir(filepath)  # 获取当前路径下的文件名，返回List，第一层
    for s1 in pathdir1:
        newdir1 = os.path.join(filepath, s1)  # 将文件名加入到当前文件路径后面

        if os.path.isfile(newdir1) is not True:  # 如果是文件夹而不是其他文件
            pathdir2 = os.listdir(newdir1)  # 获取当前路径下的文件名，返回List，第二层
            for s2 in pathdir2:
                newdir2 = os.path.join(newdir1, s2)  # 将文件名加入到当前文件路径后面

                if os.path.splitext(newdir2)[1] == ".txt":  # 判断是否是txt
                    fnum += 1
                    opentxt = open(newdir2,'r')  # 开每个需要统计的TXT

                    readtxt = opentxt.read()  # 读取
                    readtxtsplit = re.split(r'[\t\n]', readtxt)  # 正则化分句子
                    for k in range(len(readtxtsplit)):    #k为每篇文章分句后的元素
                        same_sentence = 0    #用于判断是否有相同的句子
                        if readtxtsplit[k] != '':

                            for ta in range(len(txtall)):    #txtall 是一个列表
                                if txtall[ta] == readtxtsplit[k]:
                                    same_sentence = 1
                                    delete += 1
                                    print('"'+readtxtsplit[k] + '"  在  '+ s2 + '  中的第  ' + str(k) + '  行，与全部句子的第  '+ str(ta)+ '  行重复')
                                    have_deleted.write('"'+readtxtsplit[k] + '"  在  '+ s2 + '  中的第  ' + str(k) + '  行，与全部句子的第  '+ str(ta)+ '  行重复' + '\n')
                                    if nameall[ta] != s2:
                                        nameall[ta] = nameall[ta]+','+s2
                                    break
                            if same_sentence == 0:
                                #opentxtall.write(readtxtsplit[k]+'     '+s2+'\n')
                                txtall.append(readtxtsplit[k])
                                nameall.append(s2)
                    opentxt.close()

        for ss in range(len(txtall)):  #将句子列表+文件名列表写入txtall文档
            opentxtall.write(txtall[ss] + '     ' + nameall[ss] + '\n')
        for sn in range(len(txtall)):  #将句子列表+文件名列表写入txtall文档n
            opennameall.write(nameall[sn] + '\n')

    opentxtall.close()
    opennameall.close()
    have_deleted.close()

    print(fnum + delete)
    #print(txtall)

eachFile('E:\source\主干语料库')