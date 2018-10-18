#-*-coding:utf-8-*-
import os
# def getdir(path):
#     all_file=[]
#     all_name=[]
#     for root,dirs,files in os.walk(path):
#         for file in files:
#             file=file.encode('utf-8').decode('utf-8')
#             all_file.append(root+'\\'+file)
#             all_name.append(file)
#     return all_file,all_name

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
# 
# if __name__=='__main__':
    # all_file, all_name = getdir(r'C:\Users\jee_s\Desktop\助研\附码语料库')
    # print (all_file[0].split('\\'))
