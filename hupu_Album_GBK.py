#!/usr/bin/env python
#coding: GBK
#version: 0.2
import os,sys,urllib2,re

def get_pages(home,path):
	homepage = get_content(home)
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
	# sub smell to big pic and remove repeat img url
	# list(set(url_list))
	urls = []
	for i in url_list:
		if not i in urls:
			urls.append(i)
	return re.sub(r'small.', r'big.', '\n'.join(urls)),len(urls)

def get_content(url):
	return urllib2.urlopen(url).read()

def dowm_img(urls,path,pic_num):
	num = 0
	for url in urls.split('\n'):
		filename = url.split('/')[-1]
		print '[%s/%s]download>>>%s' %(num,pic_num,filename)
		data = get_content(url)
		f= open('%s/%s' %(path,filename),'wb')
		f.write(data)
		f.close()
		num+=1

def main():
	#�ű��ɴ�url����
	if len(sys.argv)<=1:
		print '��������Ҫ���ص�����ַ��'
		home = r'http://my.hupu.com/sunyatsen/photo/a135716.html'    #����
	else:
		home = sys.argv[1]
	# �ж�url�Ƿ���ȷ
	match = re.match(r'http://my\.hupu\.com(/[\S]+?/photo/a[\d]+?)(?:\-[\d]+\.html|\.html)',home) 
	if match == None:
		print '��URL����ʶ��\n�����뵥������ҳ���ַ��'
		exit()
	path = match.group(1)    #Album path
	print '\n','='*10,'��ʼץȡ','='*10,'\n'
	#�õ���������ҳ���ַ
	page_list,title = get_pages(home,path)
	P_num =  len(page_list)
	print '�������%dҳ��' %P_num
	content = ''
	current = 0
	for i in page_list:
		current +=1
		content +=get_content(i)
		print '%d/%d:page done:%s' %(current,P_num,i)
	#�����е�ҳ��������ץȡͼƬurl
	urls,pic_num = get_urls(content)
	os.system(r'mkdir "%s" ' %title)
	print '%s��ͼƬ��Ҫ����\n����"%s"�ļ���>>>' %(pic_num, title)
	with open(r'%s/urls' %title,'w') as urls_file:
		urls_file.write(urls)
		print 'ͼƬurlд���ļ��ɹ�'
	print '\n','='*10,'��ʼ����','='*10,'\n'
	end = os.system(r'wget -N -i "%s/urls" -P "%s" ' %(title,title) ) # if you have wget
	if end == 1:
	    dowm_img(urls,title,pic_num)
	else:
	    print 'wget�㶨!'
		
if __name__ == '__main__':
    main()
