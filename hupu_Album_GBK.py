#!/usr/bin/env python
#coding: GBK
#author: xavierskip
#version: 0.15
#date: 10-18-2012

import os,sys,urllib2,re

def get_pages(home,path):
	homepage = get_content(home)    #�ַ������淳��
	title    = re.search(r'<title>(.+)</title>',homepage).group(1)
	print '����ץȡ���>>>%s>>>' %title
	pat  = path+ r'-([\d]+).html(?:\'|\")>'       #ƥ��ʣ�µ����ҳ��
	P_nums = re.findall(pat,homepage)
	if P_nums==[]:
		page_list = [home]
		return page_list,title
	else:
		P_max = int(P_nums[-1])
		#�����������ҳ�棬���ö����й��ɵġ���|||
		page_list = [r'http://my.hupu.com%s-%d.html' %(path,i) for i in xrange(1,P_max+1)]
		return page_list,title

def get_urls(content):
	pat = r'http://i[\d]{1}\.hoopchina\.com\.cn/.+small\.(?:jpg|gif|png|jpeg|bmp)'
	url_list = re.findall(pat,content)    #parse img url
	#remove cover img url
	no_cover = []
	for i in url_list:
	    if i in no_cover:
	        pass
	    else:
	        no_cover.append(i)
	print '�������%s��ͼƬ' %len(no_cover)
	urls = '\n'.join(no_cover)
	urls = re.sub(r'small\.',r'big.',urls)
	return urls

def get_content(url):
	return urllib2.urlopen(url).read()

def dowm_img(urls):
	pass

def main():
	#�ű��ɴ�url����
	if len(sys.argv)<=1:
		home = r'http://my.hupu.com/jackson817/photo/a82914-1.html'    #�ű����û�������ַ
	else:
		home = sys.argv[1]
	# �ж�url�Ƿ���ȷ
	match = re.match(r'http://my\.hupu\.com(/[\S]+?/photo/a[\d]+?)(?:\-[\d]+\.html|\.html)',home) 
	if match == None:
		print 'some thing wrong!\n˵���˲�Ҫ�����߰����url����Ϸ�ҵģ�'
		exit()
	path = match.group(1)    #Album path
	print '\n','='*10,'��ʼץȡ','='*10,'\n'
	page_list,title = get_pages(home,path)    #�õ���������ҳ��
	P_num =  len(page_list)
	print '�������%dҳ��' %P_num
	content = ''
	current = 0
	for i in page_list:
		current +=1
		content +=get_content(i)     #�õ�����ҳ������
		print '%d/%d:page done:%s' %(current,P_num,i)
	urls = get_urls(content)
	os.system(r'mkdir "%s" ' %title)
	print '����"%s"�ļ��гɹ�' %title
	url_file = open(r'%s/urls' %title,'w')    #׷��:w+
	try:
		url_file.write(urls)
		print 'ͼƬurlд���ļ��ɹ�'
	finally:
		url_file.close()
	print '\n','='*10,'��ʼ����','='*10,'\n'
	end = os.system(r'wget -N -i "%s/urls" -P "%s" ' %(title,title) )
	if end == 1:
	    print 'ȱ��wget�����Դ�"%s"�ļ����µ�urls�ļ����������������������ع������أ�����Ѹ�׵�~' %title
	else:
	    print 'well done!'
		
if __name__ == '__main__':
    main()
