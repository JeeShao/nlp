#-*-coding:utf-8-*-
import sys
from  Util import getdir
import os

def readtxt(path):
    '''
    读取每一句 每一句为一行 每一句的上一行为<s>下一行为</s>
    path:文章文件路径
    return：文章分句数组datas[]
    '''
    datas=[]
    with open(path) as file:
        rows=file.readlines()
        for row in rows:
            data=row.strip().split(' ')
            if  data[0].upper() not in ['<S>','</S>']:
                datas.append(data)
    return datas

def data_split(data):
    '''
    将数据的单词和词性分离
    data:文章分句数组data[] data[i]为每一句的空格分割单词list
    return:dat--全文单词list  voc--全文词性list
    '''
    dat=[]#每一篇文章的单词list 每一个元素为每一句的单词list
    voc=[]#每一篇文章的词性list 每一个元素为每一句的词性list
    for i in range(len(data)): #每一行（每一句）
        arg1=[] #每一句的单词
        arg2=[] #每一句的词性
        for j in range(len(data[i])):#每一个词
            if '_' in data[i][j] and data[i][j][0] != '_': #过滤没有'_'和首字符为'_'的词
                row=data[i][j].split('_')#分割每个词的单词和词性
                if row[0][0]=='(': #删除单词前面的'('
                    row[0]=row[0].replace('(','')
                arg1.append(row[0]) #单词
                row[1]=''.join(list(filter(str.isalpha, row[1]))) #删除非字母字符
                arg2.append(row[1]) #词性
                print(row)
        dat.append(arg1)
        voc.append(arg2)
    return dat,voc


def mkdir(path):
    # 去除首位空格
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

def tans_sentence(data):
    '''
    提取主谓结构的词
    方法：从前往后遍历，遇到一个谓词，停止，截取前面的所有单词
    :param data:
    :return:
    '''
    da, vol = data_split(data)
    pre_data=[]
    for i in range(len(vol)):
        for j in range(len(vol[i])):
            if vol[i][j].upper() in ['VB','VBD','VBP','VBZ']:###########此处词性码已改
                #如果动词前面一个是做定语的词，则要截取下一个谓语动词
                if j>0 and da[i][j-1].upper() in ['WHO','WHOSE','THAT','WHICH']:
                    continue
                k=j
                while k>=0 and vol[i][k].upper() not in ['DT', 'EX', 'FW', 'NN', 'NNP', 'NNPS', 'NNS', 'PRP']:###########此处词性码已改
                    ############加入疑问词，备选
                    ############while k>=0 and vol[i][k].upper() not in ['DT', 'EX', 'FW', 'NN', 'NNP', 'NNPS', 'NNS', 'PRP', 'WDT', 'WP','WP$', 'WRB']:
                    k-=1
                if k>0:
                    pre_data.append(da[i][k:j+1])
                break
    return pre_data

def save_to_txt(pre_data,path):
    '''
    将数据保存在指定文件夹下
    :param pre_data:
    :return:
    '''
    f=open(path,'w')
    for row in pre_data:
        f.write(' '.join(row)+'\n')
    f.close()


def tran_sentense(data):
    '''
    data:文章分句数组 data[i]为每一句空格分割后的单词list
    '''
    da, vol = data_split(data)
    # 所有动词
    v_a = ['IN', 'VVN', 'TO', 'RP', 'VB','VBD','VBP','VBZ'] ###########此处词性码已改
################## 此处往下的词性码没有改
    new_data=[]
    for i in range(len(vol)): #每一文章的词性行数
        j,f,beg,end=0,0,0,0
        while j<len(vol[i]):#每一行的词性数
            #如果动词不是have----'VH0','VHZ'
            ############# 与CLAWS不同的是，NLTK中没有给出助动词have特别的词性码,
            ############# NLTK： have_VBP, had_VBD，has_VBZ
            # if vol[i][j].upper() in ['VBDR','VBDZ','VBI','VBM','VBR','VBZ','VD0','VDD','VDZ','VHD','VV0','VVD','VVI','VVZ']:
            if vol[i][j].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']:
                print(da[i][j]+'_'+vol[i][j])
                #找到动词后
                #1：确定前面
                # 如果前面有标点符号则截取到标点符号后,或者出现连词则截取到连词后
                #################CLAWS的标点之前有空格，且赋码，NLTK的标点是紧跟之前单词，无空格
                beg=end=j
                # while beg>=f and vol[i][beg] not in [',','.','!','?',':','"','-','CC','CS','CCB','CSA','CSW','CSN','CST']:
                while beg>=f and (vol[i][beg] not in [',','.','!','?',':','"','-','CC'] or da[i][beg].upper() in ['AND','OR']): #This endeavour assists and is assisted by
                    beg=beg-1
                #2:确定后面的单词
                #have/has/had (not) been……
                if j<(len(vol[i])-3) and da[i][j].upper() in ['HAVE','HAS','HAD','DO','DOES','DID'] and vol[i][j+1] in ['VB','VBD','VBG','VBN','VBP','VBZ']: #I do/have been/decided
                    end = j+1
                    if vol[i][j+2] in ['TO','IN'] or da[i][j+2].upper()=='THAT':#have focused on
                        end += 1
                elif j<(len(vol[i])-3) and da[i][j].upper() in ['HAVE','HAS','HAD','DO','DOES','DID'] and vol[i][j+1]=='RB' and vol[i][j+2] in ['VB','VBD','VBG','VBN','VBP','VBZ']:#I do/have not been/decided
                    end = j+2
                    if vol[i][j+3] in ['TO','IN'] or da[i][j+3].upper()=='THAT':#have not focused on
                        end += 1
                #动词+动词+TO/that
                elif j<(len(vol[i])-3) and (vol[i][j+1].upper() in ['TO','IN'] or da[i][j+1].upper()=='THAT'): # I think that 
                    end=j+1
                # if j<(len(vol[i])-3) and vol[i][j+1].upper() in ['VBDR','VBDZ','VBI','VBM','VBR','VBZ','VD0','VDD','VDZ','VH0','VHD','VHZ','VV0','VVN','VVD','VVI','VVZ'] and da[i][j+2].upper() in ['TO','THAT']:
                elif j<(len(vol[i])-3) and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ','JJ',] and (da[i][j+2].upper() in ['TO','THAT'] or vol[i][j+2].upper()=='IN'): # It is important to
                    end=j+2
                elif j==(len(vol[i])-2) and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']:#句尾
                    end=j+1
                #不管后面是否有，我们都需要截取到动词故，end应该是当前j+1
                # if end-beg>2:
                if end-beg>=2:
                    new_data.append(da[i][beg+1:end+1])
                    f=end+1
                    break

            #如果动词是have类型,如果后面是v截取到动词
            # if j<(len(vol[i])-2) and vol[i][j].upper() in ['VH0','VHZ']:
            # ############# 同上，have/has/had done 型式
            #     beg = end = j
            #     # 如果前面有标点符号则截取到标点符号后,或者出现连词则截取到连词后
            #     #####################同上，标点
            #     while beg >= f and vol[i][beg] not in [',', '.', '!', '?', ':', '"', '-', 'CC', 'CS', 'CCB', 'CSA','CSW', 'CSN', 'CSI']:
            #         beg = beg - 1
            #     if vol[i][j+1] in v_a:
            #         if da[i][j+2].upper() in ['TO','THAT']:
            #             end=j+2
            #         else:
            #             end = j + 1
            #     else:
            #         end=j
            #     if end - beg >=2:
            #         new_data.append(da[i][beg+1:end+1])

            j+=1

    return new_data



if __name__=='__main__':
    orgDir = "分句语料库"
    toDir  = "主干语料库"
    # files=getdir(r'C:\Users\jee_s\Desktop\助研\分句语料库')
    all_dirs, all_files, all_names = getdir(orgDir)
    for i in all_dirs: #创建子目录
        mkdir(os.path.join(toDir,i)) 
    for i in all_files[0:1]: 
        print(i)
        file_route = i.split('\\')
        file_route[0] = toDir
        file = "\\".join(file_route)
        data = readtxt(i) #len(data)=文章句数  data[i]为每一句以空格分割后的单词List
        pre_data = tran_sentense(data)
        save_to_txt(pre_data, file)