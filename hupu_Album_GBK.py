#!/usr/bin/env python
#coding: GBK
#author: xavierskip
#date:10-13-2012

import os,sys,urllib2,re

def get_pages(home,homepage):
	match = re.match(r'http://my\.hupu\.com([\S]+?)(?:\-[\d]\.html|\.html)',home) 
	if match == None:
		print 'some thing wrong!\n˵���˲�Ҫ�����߰����url����Ϸ�ҵģ�'
		exit()
	path = match.group(1)    #Album path
	pat  = path+ r'-([\d]+).html(?:\'|\")>'
	P_nums = re.findall(pat,homepage)
	if P_nums==[]:
		page_list = [home]
		return page_list
	else:
		P_max = int(P_nums[-1])    #�ж���ҳ
		#�����������ҳ�棬���ö����й��ɵġ���|||
		page_list = [r'http://my.hupu.com%s-%d.html' %(path,i) for i in xrange(1,P_max+1)]
		return page_list

def get_content(url):
	content = urllib2.urlopen(url).read()
	print '%s  ---page done!' %url
	return content


def get_urls(content):
	pat = r'http://i[\d]{1}\.hoopchina\.com\.cn/.+small\.(?:jpg|gif|png|jpeg)'
	url_list = re.findall(pat,content)    #parse img url
	print '�õ�%d��ͼƬURL' %len(url_list)
	urls = '\n'.join(url_list)
	urls = re.sub(r'small\.',r'big.',urls)
	return urls

def dowm_img(urls):
	pass

def main():
	#�ű��ɴ�url����
	if len(sys.argv)<=1:
		home = r'http://my.hupu.com/jackson817/photo/a82914-1.html'    #�ű����û�������ַ
	else:
		home = sys.argv[1]
	homepage = urllib2.urlopen(home).read()    #�ַ������淳��
	title    = re.search(r'<title>(.+)</title>',homepage).group(1)
	print '����ץȡ���>>>��%s��' %title
	page_list = get_pages(home,homepage)    #�õ���������ҳ��
	content = ''
	for i in page_list:
		content +=get_content(i)     #�õ�����ҳ������
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
	os.system(r'wget -i "%s/urls" -P "%s" ' %(title,title) )


if __name__ == '__main__':
    main()
