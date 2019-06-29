import nltk
import nltk.data
import os
import sys
from  Util import getdir,mkdir



def splitSentence(file):
    '''
    返回文章的分句list
    '''
    data = []
    sen_list=[]
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    f=open(file,'r')
    lines=f.readlines()
    for line in lines:
        sen_list=[]
        line = line.strip().split()
        if len(line):  #删除每段前后<>
            for i in [0,-1]:
                if '<' in line[i] and '>' in line[i]:
                    line[i]=''
            line = ' '.join(line).strip()
            # if len(line):
            sentences = tokenizer.tokenize(line)
            #print(str(sentences))

            #*****Refinement***********************************
            # 合并句末有et al或etc的句子
            #原程序无法解决连续et al.的问题
            total = len(sentences)
            syg = 0            #表示“上一个”有et al.结尾的
            for i in range(total-1):
                    sentens_list = sentences[i].strip().split()
                    i1 = i+1
                    if i1 > (total-1):
                        i1 = i

                    sentens_list1 = sentences[i1].strip().split()
                    if len(sentens_list)>1:
                        if ('’_' in sentens_list1[0]):
                            sentences[i] = " ".join([sentences[i], sentences[i+1]])
                            sentences[i+1] = ''
                            #sen_list[-1] = sentences[i]


                        if ('etc_' in sentens_list[-1] or ( 'al_' in sentens_list[-1] and 'et_' in sentens_list[-2])):
                            if syg == 1:                     #如果上一个也有，就把上一句和下一句连在一起，并在sen_list里代替最后一个句子
                                sentences[i] = " ".join([sentences[i-1], sentences[i + 1]])
                                sentences[i + 1] = ''
                                sen_list[-1] = sentences[i]
                                continue

                            sentences[i] = " ".join([sentences[i], sentences[i + 1]])
                            sentences[i + 1] = ''  #
                            syg = 1
                        else:
                            syg = 0

                    sen_list.append(sentences[i])  #
            #*********************************************************************************************
            #以下是原程序
            #合并句末有et al或etc的句子
            # for i,element in enumerate(sentences):
            #     sentens_list=element.strip().split()
            #     if len(sentens_list)>1:
            #         if ('etc_' in sentens_list[-1] or ('al_' in sentens_list[-1] and 'et_' in sentens_list[-2])) and i<len(sentences)-1:#句末有et al 或 etc的句子补上下一句
            #             sentences[i]=" ".join([sentences[i],sentences[i+1]])  #
            #             print('连句子'+sentences[i])
            #             sentences[i+1]=''   #
            #         sen_list.append(sentences[i])#
            #************************************************************************************************
            #下面一句本来就是注释掉的
            # sentences = [i for i in sentences if len(i.strip().split())>1] #删除只有一个词的句子


            data.extend(sen_list)
    f.close()
    return data
    # for i in data:
    #   print(i)

def save_file(pre_data,path):
    '''
    将数据保存在指定文件夹下
    :param pre_data:
    :return:
    '''
    f=open(path,'w')
    for row in pre_data:
        f.write(row+'\n')
    f.close()
 
def get_sentences():
    data = []
    orgDir = "附码语料库"
    toDir  = "分句语料库"
    all_dirs, all_files, all_names = getdir(orgDir)
    for i in all_dirs: #创建子目录
        mkdir(os.path.join(toDir,i)) 
    for i in all_files:
        print(i)
        file_route = i.split('\\')
        file_route[0] = toDir
        file = "\\".join(file_route)
        data = splitSentence(i) #获取每个文章分句list
        save_file(data,file)
if __name__ == '__main__':
    get_sentences()
