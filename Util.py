#-*-coding:utf-8-*-
import os

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
# 
# if __name__=='__main__':
    # all_file, all_name = getdir(r'C:\Users\jee_s\Desktop\助研\附码语料库')
    # print (all_file[0].split('\\'))
