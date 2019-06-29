#-*-coding:utf-8-*-
import sys
from  Util import getdir,mkdir
import os
import re

def remove_punctuation(line):
    rule = re.compile("[^a-zA-Z0-9]")
    line = rule.sub('',line)
    return line

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
                if row[0] in ['“','“']: #双引号重新附码QQ
                    row[-1] = 'QQ'
                    # print(row)

                arg1.append(row[0]) #单词
                #此处用row[-1]而不用row[1]是因为存在love_这种词 附码后为love__NN 此时row[1]并非NN
                pos=''.join(list(filter(str.isalpha, row[-1]))) #删除非字母字符
                arg2.append(pos) #词性
                if row[-1][-1] in [',','.','!','?',':']:#提取标点
                    arg1.append(row[-1][-1])
                    arg2.append(row[-1][-1])
                # arg1[0] = ''.join(list(filter(str.isalnum,arg1[0])))
                arg1[0] = remove_punctuation(arg1[0])#删除居首特殊符号 【 ——
                if arg1[0]=='':
                    del(arg1[0])
                    del(arg2[0])


                # print(arg2)
        dat.append(arg1)
        voc.append(arg2)
    return dat,voc


def save_to_txt(pre_data,path,vbFile):
    '''
    将数据保存在指定文件夹下
    :param pre_data:
    :return:
    '''
    f=open(path,'w')
    vb_f = open(vbFile,'w')
    for row in pre_data:
        if row[-1] == 'VB_PDZ': #句首动词
            row.pop()
            vb_f.write(' '.join(row)+'\n')
        else:
            f.write(' '.join(row)+'\n')
    f.close()
    vb_f.close()


def tran_sentense(data):
    '''
    data:文章分句数组 data[i]为每一句空格分割后的单词list
    '''
    trunks_num,not_trunks = 0, 0  #可以提取主干的行数 和 没有主干的行数
    da, vol = data_split(data)
    # print(da[283])
    # print(vol[283])
    # 所有动词
    v_a = ['IN', 'VVN', 'TO', 'RP', 'VB','VBD','VBP','VBZ'] ###########此处词性码已改
################## 此处往下的词性码没有改
    new_data=[]
    sp = 0###############
    for i in range(len(vol)): #每一文章的词性行数
        j,f,beg,end=0,0,0,0
        while j<len(vol[i]):#每一行的词性数
            #如果动词不是have----'VH0','VHZ'
            ############# 与CLAWS不同的是，NLTK中没有给出助动词have特别的词性码,
            ############# NLTK： have_VBP, had_VBD，has_VBZ
            # if vol[i][j].upper() in ['VBDR','VBDZ','VBI','VBM','VBR','VBZ','VD0','VDD','VDZ','VHD','VV0','VVD','VVI','VVZ']:


            #*******************TESTING*********************************************
            # if da[i][j] == 'Note':
            #     print(da[i])
            #     print(vol[i])


            #**Refinemnt************************************************************************************

            if da[i][j] in ['encounters'] and vol[i][j-1] in ['NNP','VBG','JJ']:#AP1806:As so  often during the first months of her stay, Julie’s story-opening encounters  trouble with recipiency .
                vol[i][j] = 'VBZ'                                                   #针对“encounders”类既有动词又有名词赋码的词，并以前面一个词的词性为判断条件
                                                                                    #局限性比较大，需添加具体词汇和前面词性
            if vol[i][j] in ['VB','VBD','VBP','VBZ'] and da[i][j-1] == '‘':
                vol[i][j] = 'NN'

            if da[i][j] == '’':                #AP1806: The mais ‘but’ is here not  used to introduce a disagreement or a contrast,
                if vol[i][j-1] == 'CC':
                     vol[i][j-1] = 'CCX'             #其中but词性是CC，以下判断截取开头里含CC的条件，所以自定义命名一个CCX，无含义

            if da[i][j] == '‘':               # ‘ 被赋成VBZ,VBP的情况
                vol[i][j] = 'NN'

            if len(da[i][j]) == 1 and vol[i][j] not in [',','.','!','?',':','"','-','CC']:   #Note that the patterns v it ADJ that and v it ADJ to-inf are used with  verbs such as think  and also verbs such as make .
                 vol[i][j] = 'NN'     #the patterns v it ADJ that and v it ADJ to-inf are used with
            #***********************************************************************************


            if vol[i][j].upper() in ['VB','VBD','VBP','VBZ'] and da[i][j - 1].upper() != 'TO' and da[i][j] not in ['et','’','’s','s']:  #*******Refinement******To do the reverse transformation, we adapt the algorithm in ...针对To + 动词开头从句，真正主干在后面附加后面一个判断条件
                # print(da[i][j]+'_'+vol[i][j])
                #找到动词后
                #1：确定前面
                # 如果前面有标点符号则截取到标点符号后,或者出现连词则截取到连词后
                #################CLAWS的标点之前有空格，且赋码，NLTK的标点是紧跟之前单词，无空格

                beg=end=j

                # while beg>=f and vol[i][beg] not in [',','.','!','?',':','"','-','CC','CS','CCB','CSA','CSW','CSN','CST']:
                while beg>=f and (vol[i][beg] not in [',','.','!','?',':','"','-','CC'] or da[i][beg].upper() in ['AND','OR'] ): #This endeavour assists and is assisted by
                    beg=beg-1

                #******Refinement*************************************************************
                if da[i][beg+1] == '’' and vol[i][beg+2] != ',':  #Examples such as ‘A drink or a cuppa sound goods good to me!’  showed how
                    beg -= 1
                    while beg >= f and (vol[i][beg] not in [',', '.', '!', '?', ':', '"', '-', 'CC'] or da[i][beg].upper() in ['AND', 'OR']):
                        beg = beg - 1

                if vol[i][beg] in [','] and (vol[i][beg+1] in ['VB','VBD','VBP','VBZ'] or (vol[i][beg+1] in ['RB'] and vol[i][beg+2] in ['VB','VBD','VBP','VBZ'])):#‘,are used by speakers to
                    #print(str(da[i])+'\n'+str(da[i][beg-1]))
                    if vol[i][beg +2] != ',':
                        while beg >= f  and (vol[i][beg] not in [ '.', '!', '?', ':', '"', '-', 'CC'] or da[i][beg].upper() in ['AND', 'OR']):
                            beg = beg - 1
                #------modify-Jee 20190611-------#
                if vol[i][beg] in [','] and vol[i][beg+1] in ['DT','EX','NN','NNP','NNS','NNPS','PDT','PRP','PRP$']:
                   pass
                #------modify-Jee 20190611-------#
                elif vol[i][beg] in [','] and vol[i][beg+2] in ['VB','VBD','VBP','VBZ'] and (vol[i][beg+1][0] != 'N' or (vol[i][beg+1][0] != 'P' and vol[i][beg+1][1:] not in ['NQO','NX1','PHO1','PHO2','PIO1','PIO2','PX1','PX2'])):#A full list of the types of  metonymy identified, along with quantitative data and an example of each  type from our corpus, can be found in
                    while beg >= f  and (vol[i][beg] not in [ '.', '!', '?', ':', '"', '-', 'CC'] or da[i][beg].upper() in ['AND', 'OR']):
                        beg = beg - 1

                if beg > -1:
                    if da[i][beg - 1] == 'al':
                        beg = beg - 3
                        while beg >= f and (vol[i][beg] not in [',','.','!','?',':','"','-','CC'] or da[i][beg].upper() in ['AND','OR']): #This endeavour assists and is assisted by
                            beg=beg-1

                if vol[i][beg] == ',' and da[i][beg + 1] == 'and' and da[i][beg + 2] in ['1','2','3','4','5','6','7','8','9','10','11','12','13','14']:                  #Meaning Groups 6 , 12 , and 14 are not included because
                    while beg >= f and vol[i][beg +1] not in ['.','!','?',':','"','-'] and da[i][beg + 1].upper() not in ['TABLES']:                          #由于没有“，”遮挡，针对CL1712的Tables *，*，and*情况附加最后一个判断条件
                         beg = beg -1

                if vol[i][beg] == ',' and da[i][beg + 1] == 'and' and da[i][beg + 2] in ['‘']:#In this section the terms ‘pattern grammar’, ‘construction grammar’, ‘local  grammar’, and ‘evaluation’ are defined
                    while beg >= f and vol[i][beg + 1] not in ['.', '!', ':', '"', '-']:
                        beg = beg - 1
                    #beg = beg + 1
                    # if vol[i][beg] == '’':
                    #     while vol[i][beg] not in ['.', ':', '"', '-']:
                    #         beg = beg - 1

                if da[i][beg + 1] in ['1','2','3','4','5','6','7','8','9','10'] and vol[i][beg] in  ['.','!','?',':','"','-']:     #针对  2 The meaning of the pattern ADJ about n seems to  和  4 ‘ the paintings were sold 类问题，去前面数字
                    beg = beg +1
                #******Refinement***********************************************************************
                if da[i][beg + 1] in ['among']:
                    while (vol[i][beg] not in ['.', '!', '?', ':', '"', '-', 'CC']):
                        beg -= 1

                lian_ci = 1           #去除句首连词
                # ------modify-Jee 20190611-------#
                # while(lian_ci):
                while (beg<len(da[i])-1 and lian_ci):
                # ------modify-Jee 20190611-------#
                    if da[i][beg+1].upper() in ['FURTHERMORE','FINALLY','FIRST','AND','OR','ALTHOUGH','SINCE','THOUGH','HOWEVER','HERE','INDEED','THUS','CLEARLY','POWER ...','STATISTICALLY']:
                        beg += 2
                        lian_ci = 1
                        continue
                    if da[i][beg+1].upper() in ['FOR','IN','AS','LATER'] and da[i][beg+2].upper() in ['SUCH','EXAMPLE','PARTICULAR','CONVERSATIONS','INSTANCE','ON']:
                        beg += 3
                        lian_ci = 1
                        continue
                    if da[i][beg+1].upper() in ['AS','IN','TO'] and da[i][beg+2].upper() in ['THE','DO','A','ENCOURAGING'] and da[i][beg+3].upper() in ['FOLLOWING','RESULT','UPTAKE','SO']:
                        beg += 4
                        lian_ci = 1
                        continue
                    if da[i][beg + 1].upper() in ['IN'] and da[i][beg + 2].upper() in ['LIGHT'] and da[i][beg + 3].upper() in ['OF'] and da[i][beg + 4].upper() in ['THIS']:
                        beg += 5
                        lian_ci = 1
                        continue
                    if da[i][beg+1].upper() in ['FOLLOWING','DATE','TURNING']:#Turning now to the TRANSITIVITY patterns in the discourse of Girl A , we find
                        # ------modify-Jee 20190611-------#
                        # while(vol[i][beg+1] != ','):
                        while(beg<len(vol[i])-1 and vol[i][beg+1] != ','):
                        # ------modify-Jee 20190611-------#
                            beg += 1
                        beg += 1
                        lian_ci = 1
                        continue

                    lian_ci = 0
                #***Refinement***************************************************
                # ------modify-Jee 20190611-------#
                if beg + 1 <len(da[i]):
                # ------modify-Jee 20190611-------#
                    if da[i][beg + 1][1:2] == '.':  # 去除以序号1.~ 9.开头
                        da[i][beg + 1] = da[i][beg + 1][2:]
                    if da[i][beg + 1][2:3] == '.':  # 去除以序号10.~ 99.开头
                        da[i][beg + 1] = da[i][beg + 1][3:]
                    # if da[i][beg + 2].upper() in ['I','SHE','THEY','WE','HE','YOU']:   #针对AP1701 去除句首多余的介词（in）
                    #     beg = beg + 1
                    if da[i][beg + 1] in ['[','—','[…','…','ii','iii','‘',',','’']:
                        beg = beg + 1
                    if da[i][beg + 1][0:1] in ['[']:
                        da[i][beg + 1] = da[i][beg + 1][1:]
                     #***************************************************************

                if j<len(vol[i]) and da[i][j] == '‘':
                   # print(da[i][j-1])
                  #  print(da[i][j])
                  #  print(da[i][j+1])
                    end = j - 1
                    sp = 1
                #2:确定后面的单词
                if sp == 0:

                    #********Refinement*************************************************************************
                    if j<(len(vol[i])-2) and vol[i][j].upper() in ['VB','VBD','VBP','VBZ'] and da[i][j+1] == '‘':   #An example of metadiscourse is ‘ according to  （去掉‘ according to ）
                        end = j
                    #*******************************************************************************************

                    elif j<(len(vol[i])-4) and da[i][j+1].upper() in ['AND','OR','BUT'] and vol[i][j+2].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']:#She laughed and eat
                        end=j+2
                        if vol[i][j+3].upper() in ['TO','IN'] or da[i][j+3]=='THAT':#She laughed and look at
                            end=end+1
                        elif vol[i][j+3].upper() in ['PRP','PRP$','NN','NNS','NNP','NNPS'] and (vol[i][j+4].upper() in ['TO','IN'] or da[i][j+4]=='THAT'):#She laughed and tell him to
                            end=end+2
                    elif j<(len(vol[i])-1) and da[i][j+1].upper() in ['THAT','WHOSE','HOW','WHEN','WHICH','WHAT','WHERE']:#动词后跟定语从句
                        end = j+1
                    elif j<(len(vol[i])-3) and da[i][j].upper() in ['IS','ARE','WAS','WERE'] and vol[i][j+1] not in [',','?','!','.',':'] and vol[i][j+2] not in [',','?','!','.',':'] and (vol[i][j+3].upper() in ['TO','IN'] or da[i][j+3].upper()=='THAT'):#It is [immediately apparent] that
                        end = j+3
                    elif j<(len(vol[i])-4) and da[i][j].upper() in ['IS','ARE','WAS','WERE'] and vol[i][j+1] not in [',','?','!','.',':'] and vol[i][j+2] not in [',','?','!','.',':'] and vol[i][j+3] not in [',','?','!','.',':'] and (vol[i][j+4].upper() in ['TO','IN'] or da[i][j+4].upper()=='THAT'):#It is [therefore closely related] to
                        end = j+4


                    #have/has/had (not) been……
                    elif j<(len(vol[i])-3) and da[i][j].upper() in ['HAVE','HAS','HAD','DO','DOES','DID','IS','ARE','WAS','WERE'] and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']: #I do/have been/decided
                        end = j+1
                        if da[i][j+1].upper()=='BEEN' and vol[i][j+2] in ['VB','VBD','VBN']: #have been [done]
                            end = end+1
                        elif vol[i][j+2].upper() in ['RB','RBR','RBS'] and (vol[i][j+3].upper() in ['TO','IN'] or da[i][j+3].upper()=='THAT'):#It_PRP was_VBD developed_VBN originally_RB to_TO
                            end = end+2
                        elif vol[i][j+2].upper() in ['TO','IN'] or da[i][j+2].upper()=='THAT':#have focused on
                            end += 1
                    elif j<(len(vol[i])-3) and da[i][j].upper() in ['HAVE','HAS','HAD','DO','DOES','DID','IS','ARE','WAS','WERE'] and vol[i][j+1].upper()=='RB' and vol[i][j+2].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']:#I do/have not been/decided
                        end = j+2
                        if vol[i][j+2].upper() in ['RB','RBR','RBS'] and (vol[i][j+3].upper() in ['TO','IN'] or da[i][j+3].upper()=='THAT'):#It_PRP was_VBD not_RB developed_VBN originally_RB to_TO
                            end = end+2
                        elif vol[i][j+3] in ['TO','IN'] or da[i][j+3].upper()=='THAT':#have not focused on
                            end += 1
                    #动词+动词+TO/that

                    elif j<(len(vol[i])-3) and (vol[i][j+1].upper() in ['TO','IN'] or da[i][j+1].upper()=='THAT'): # I think that
                        end=j+1
                    elif j<(len(vol[i])-3) and vol[i][j+1] not in [',','?','!','.',':'] and (vol[i][j+2].upper() in ['TO','IN'] or da[i][j+2].upper()=='THAT'): # The results show differences in
                        end=j+2
                    elif j<(len(vol[i])-3) and vol[i][j+1] not in [',','?','!','.',':'] and vol[i][j+2] not in [',','?','!','.',':'] and (vol[i][j+3].upper() in ['TO','IN'] or da[i][j+3].upper()=='THAT'): # The results show significant differences in
                        end=j+3
                    # if j<(len(vol[i])-3) and vol[i][j+1].upper() in ['VBDR','VBDZ','VBI','VBM','VBR','VBZ','VD0','VDD','VDZ','VH0','VHD','VHZ','VV0','VVN','VVD','VVI','VVZ'] and da[i][j+2].upper() in ['TO','THAT']:
                    elif j<(len(vol[i])-3) and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ','JJ','JJR','JJS','RB','RBR','RBS'] and (da[i][j+2].upper() in ['TO','THAT'] or vol[i][j+2].upper()=='IN'): # It is important to
                        end=j+2
                    elif j<(len(vol[i])-4) and da[i][j+1].upper()=='NOT' and vol[i][j+2].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ','JJ','JJR','JJS','RB','RBR','RBS'] and (da[i][j+3].upper() in ['TO','THAT'] or vol[i][j+3].upper()=='IN'): # It is not important to
                        end=j+3
                    elif j<(len(vol[i])-2) and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ'] and vol[i][j+2].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']: #Suggestions for the application of this approach to language teaching [are offered]
                        end=j+2
                    elif j==(len(vol[i])-2) and vol[i][j+1].upper() in ['VB','VBD','VBG','VBN','VBP','VBZ']:#句尾
                        end=j+1
                    #不管后面是否有，我们都需要截取到动词故，end应该是当前j+1
                    # if end-beg>2:
                if end-beg>=2 or sp == 1:
                    strs = da[i][beg+1:end+1]
                    sp = 0
                    if vol[i][beg+1] in ['VBP','VBD','VBZ']: #句首该三种动词另存文件 在句末加标识
                        strs.append('VB_PDZ')
                    # ------modify-Jee 20190629-------#
                    elif strs[1]==',' and (vol[i][beg+1] in ['RB','DT','PDT','CD','IN']): #删除居首逗号前 介词 数词等 Therefore , what is deemed most relevant in
                        del(strs[:2]) #删除居首介词/数词/限定词/副词+,

                    elif len(strs)>6 and (vol[i][beg+1] in ['IN']) and (',' in strs[2:6]):# 删除逗号前介词短语 in some cases , the configuration-pattern mapping , or construction , is consistent only if
                        del(strs[:strs.index(',')+1])
                    # ------modify-Jee 20190629-------#
                    if "“" in strs and "”" not in strs:
                        del (strs[strs.index('“')])
                    if "”" in strs and "“" not in strs:
                        del (strs[strs.index('”')])
                    strs[0] = remove_punctuation(strs[0])  # 删除居首特殊符号 【 ——
                    if strs[0] == '':
                        del (strs[0])

                    strs[-1] = remove_punctuation(strs[-1])  # 删除居尾特殊符号 【 ——
                    if strs[-1] == '':
                        del (strs[-1])
                    # ------modify-Jee 20190629-------#
                    if len(strs)>1:#删除只有一个词的句干
                        new_data.append(strs)
                        trunks_num += 1
                    # ------modify-Jee 20190629-------#
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
    not_trunks = len(vol)-trunks_num
    return new_data,not_trunks

def extract_trunk():
    orgDir = "分句语料库"
    toDir  = "主干语料库"
    vbDir  = "句首动词文件"
    # files=getdir(r'C:\Users\jee_s\Desktop\助研\分句语料库')
    all_dirs, all_files, all_names = getdir(orgDir)
    for i in all_dirs: #创建子目录
        mkdir(os.path.join(toDir,i))
        mkdir(os.path.join(vbDir,i))
    for i in all_files:
    # for i in ['分句语料库\Computational Linguistics\CL1810.txt']:
        print(i)
        file_route = i.split('\\')
        file_route[0] = toDir
        file = "\\".join(file_route)
        file_route[0] = vbDir
        vbFile = "\\".join(file_route)
        data = readtxt(i) #len(data)=文章句数  data[i]为每一句以空格分割后的单词List
        pre_data,not_trunks = tran_sentense(data)
        print(i+"文件没有主干行数：",not_trunks)

        save_to_txt(pre_data, file, vbFile)
if __name__=='__main__':
    extract_trunk()