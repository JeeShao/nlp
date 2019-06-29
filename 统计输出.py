import os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import brown
import re
import collections


def eachFile(filepath,outpath1,outpath2):
    total = 0                                                        #用于对统计过的文章计数
    fnum = 0                                                         # 用于统计文件夹中txt文件的个数
    pathdir = os.listdir(filepath)                                   # 获取当前路径下的文件名，返回List
    for s in pathdir:
        newdir = os.path.join(filepath, s)                           # 将文件名加入到当前文件路径后面
        if os.path.isfile(newdir):                                   # 如果是文件
            if os.path.splitext(newdir)[1] == ".txt":               # 判断是否是txt
                fnum += 1
    print('此文件夹下共有 '+str(fnum)+' 个TXT文档')


    for s in pathdir:
        newdir = os.path.join(filepath, s)                           # 将文件命加入到当前文件路径后面
        if os.path.isfile(newdir):                                   # 如果是文件
            if os.path.splitext(newdir)[1] == ".txt":               # 判断是否是txt
                result = open(outpath1,'a')          #开最终结果TXT,其中filepath+'/result.txt'是文件路径，全部删除后替换注意最后要是.txt文件
                result1 = open(outpath2,'a')
                op1 = open(newdir)                                   # 开每个需要统计的TXT，
                r1 = op1.read()                                      #读取
                rds = re.split(r'[\t\n]',r1)                        #正则化分句子
                total = total+1
                print('第 '+str(total)+' 篇文章 '+s+' 共有' +str(len(rds))+' 行')      #本文共多少行


                row = len(rds)
                for i in range(row):                                #对单个txt中的每一行
                    rlen = len(rds[i])                               #标齐统计的结果
                    if rlen<=80:
                        blank = (80-rlen)*' '
                    if ((rlen>80) and (rlen<=122)):
                        blank = ((122-rlen)+80)*' '
                    if rlen > 122:
                        blank = (80-(rlen-122))*' '
                    result1.write(rds[i]+blank)

                    for t in pathdir:
                        newdir1 = os.path.join(filepath, t)          # 将文件名加入到当前文件路径后面
                        if os.path.isfile(newdir1):                  # 如果是文件
                            if os.path.splitext(newdir1)[1] == ".txt":  # 判断是否是txt
                                op2 = open(newdir1)                   #遍历包括所有文件夹下的所有TXT
                                r2 = op2.read()
                                rds2 = re.split(r'[\t\n]',r2)         #正则化分句

                                for k in range(len(rds2)-1):            #如果与本句相等则在最终结果TXT中写入文章的名字
                                    if(rds[i] == rds2[k]):
                                        result.write(t+', ')
                                        result1.write(t+',')
                                        break
                    result.write('\n')
                    result1.write('\n')
                print('完成统计')
        op1.close()                                                    #关TXT
    result.close()                                                     #关最终结果TXT
    result1.close()
    print('\n全部完成统计( ^ v ^ )')

print('Please input your file path :',end = '')
path = input()
print('Please input your out path :',end = '')
out = input()
out1 = out+'/result.txt'
out2 = out+'/result1.txt'
eachFile(path,out1,out2)

