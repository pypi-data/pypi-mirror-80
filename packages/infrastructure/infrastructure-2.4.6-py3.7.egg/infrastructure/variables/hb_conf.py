# -*- coding: utf-8 -*-
# @Author: yongfanmao
# @Date:   2020-05-29 19:01:35
# @E-mail: maoyongfan@163.com
# @Last Modified by:   yongfanmao
# @Last Modified time: 2020-08-17 17:21:35

JAVA_COV = {
	"jacocoDir": "/home/maoyongfan10020/jc/lib",
	"repoDir": '/home/maoyongfan10020/jc/repo',
	"serviceRepoDir": '/home/maoyongfan10020/jc/repo/{service_name}',
	"destfileBack": '/home/maoyongfan10020/jc/{service_name}/jacoco-it-back.exec',
	"jarDir": "/home/maoyongfan10020/jc/{service_name}",

	"destfile": "/home/maoyongfan10020/jc/{service_name}/destfile",
	"jacocoIt" : "/home/maoyongfan10020/jc/{service_name}/destfile/{index}.exec",
	"mergeFile": "/home/maoyongfan10020/jc/{service_name}/mergeFile",
	"mdestfile": "/home/maoyongfan10020/jc/{service_name}/mdestfile",
	"reportDir": "/home/maoyongfan10020/jc/{service_name}/report/{recordID}",
	"mergeReportDir": "/home/maoyongfan10020/jc/{service_name}/mergeReport/{recordID}",
	"copySourceDir": "/home/maoyongfan10020/jc/{service_name}/source",	
	"restJacoco": "cd {jacocoDir};java -jar jacococli.jar dump --address {ip} --port {port} --reset --retry 3 --destfile ",
	"dumpJacoco": "cd {jacocoDir};java -jar jacococli.jar dump --address {ip} --port {port} --retry 3 --destfile "
}