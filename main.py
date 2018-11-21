from  Util import getdir,mkdir
from pos_tagging import markPos
from subsection import subsection
from get_sentences import get_sentences
from extract_trunk import extract_trunk

def main():
	markPos() #附码
	subsection() #分段
	get_sentences() #分句
	extract_trunk() #提取主干

if __name__ == '__main__':
	main()