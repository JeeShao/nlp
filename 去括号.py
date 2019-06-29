import os
import re
import collections
import codecs

def eachFile(filepath):
      pathDir = os.listdir(filepath)      #获取当前路径下的文件名，返回List
      for s in pathDir:
          newdir=os.path.join(filepath,s)     #将文件名加入到当前文件路径后面

          if os.path.isfile(newdir) :         #如果是文件
              if os.path.splitext(newdir)[1]==".txt":  #判断是否是txt
                  op = open(newdir,'r+')
                  rd = op.read()
                  op.seek(0)      #定位到文档起始位置
                  op.truncate()   #从起始位置开始清空文档内容
                  op.close()
                  f1 = open(newdir, 'a')
                  null = 0
                  for word in rd:
                      if word == "(":
                        null = 1
                      if word == ')':
                          null = 0
                          continue

                      if word == "[":
                          null = 1
                      if word == ']':
                          null = 0
                          continue
                      #
                      # if word == "‘":
                      #     null = 1
                      # if word == '’':
                      #     null = 0
                      #     continue

                      if null == 1:
                          f1.write('')
                      if null == 0:
                        f1.write(word)
                  f1.close()
                  print(newdir)


eachFile('C:/Users/Administrator/Desktop/source/语料库简版/Applied Linguistics')
eachFile('C:/Users/Administrator/Desktop/source/语料库简版/Computational Linguistics')
eachFile('C:/Users/Administrator/Desktop/source/语料库简版/English for Specific Purposes')
eachFile('C:/Users/Administrator/Desktop/source/语料库简版/Journal of English for Academic Purposes')

# eachFile('语料库简版/Applied Linguistics')
# eachFile('语料库简版/Computational Linguistics')
# eachFile('语料库简版/English for Specific Purposes')
# eachFile('语料库简版/Journal of English for Academic Purposes')