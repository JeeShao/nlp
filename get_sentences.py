import nltk
import nltk.data
import os
import sys

def getdir(path):
    all_file=[]
    all_name=[]
    all_dirs = []
    for root,dirs,files in os.walk(path):
        all_dirs.extend(dirs)
        for file in files:
            file=file.encode('utf-8').decode('utf-8')
            all_file.append(root+'\\'+file)
            all_name.append(file)
    return all_dirs,all_file,all_name

# orgDir = "附码语料库"
# for subDir in os.listdir(orgDir):  #子目录
#       data = []
#       pathname = os.path.join(orgDir, subDir)
#       if (os.path.isdir(pathname)):
#           new_pathname = os.path.join(tagDir, subDir)
#           mkdir(new_pathname):
#           logFile = os.path.join(new_pathname,"log.csv")
#           with open(logFile, "w", newline='') as f:
#                   # with open(birth_weight_file, "w") as f:
#                   writer = csv.writer(f) 
#                   now = time.strftime("%Y-%m-%d %H:%M:%S")
#                   writer.writerows([[now]])
#                   writer.writerows([csvHeader])
#                   f.close()
#           for filename in os.listdir(pathname): #遍历文件
#               if os.path.splitext(filename)[1][1:] =='txt':
#                   orgFile = os.path.join(pathname,filename)
#                   targetFile = os.path.join(new_pathname,filename)
#                   print(orgFile)
#                   orgCount,newCount = posTagging(orgFile,targetFile)
#                   if newCount==2:
#                       precent = 'ERROR'


def splitSentence(file):
    '''
    返回文章的分句list
    '''
    data = []
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    f=open(file,'r')
    lines=f.readlines()
    for line in lines:
        line = line.strip().split()
        if len(line):  #删除每段前后<>
            for i in [0,-1]:
                if '<' in line[i] and '>' in line[i]:
                    line[i]=''
            line = ' '.join(line).strip()
            # if len(line):
            sentences = tokenizer.tokenize(line)
            sentences = [i for i in sentences if len(i.strip().split())>1] #删除只有一个词的句子
            data.extend(sentences)
    f.close()
    return data
    # for i in data:
    #   print(i)

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
 
if __name__ == '__main__':
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
