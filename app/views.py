# -*- coding: utf-8 -*-
from flask import render_template,request,jsonify
from app import app
import requests,os,subprocess,time,webbrowser,platform
from bs4 import BeautifulSoup

@app.route("/",methods=["GET","POST"])
@app.route("/index",methods=["GET","POST"])
def index():
	if request.method == "GET":
		return render_template("/index.html")

@app.route("/geneList",methods=["GET","POST"])
def geneList():
	if request.method == "GET":
		root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		scripts_path = os.path.join(root_path,"Auty","scripts","scripts")
		selection = []
		for i in os.walk(scripts_path):
			for fileName in i[2:3][0]:
				filePath = os.path.join(i[0],fileName)
				if(check_if_python(filePath)):
					selection.append(filePath)
		result = {}
		result["script_paths"] = selection
		return jsonify(result)

@app.route("/startTest",methods=["POST"])
def startTest():
	if request.method == "POST":
		selection = request.form.getlist('selection[]')
		root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		#Generate the selection.txt file under the selections folder.
		gene_selection(root_path,selection)
		#Start the auty.
		start_time = time.mktime(time.localtime())
		#print start_time
		time.sleep(1)
		auty_start_file_path = os.path.join(root_path,"Auty","start.py")
		results_folder_path = os.path.join(root_path,"Auty","results")
		start_size = getDirSize(results_folder_path)
		#print start_size
		shell = "python "+auty_start_file_path
		subprocess.Popen(shell,shell=True)
		while getDirSize(results_folder_path) == start_size:
			time.sleep(1)
		#print getDirSize(results_folder_path)
		result_file_path = ""
		for i in os.walk(results_folder_path):
			for fileName in i[2:3][0]:
				filePath = os.path.join(i[0],fileName)
				if(check_if_html(filePath)):
					result_file_time = os.path.basename(filePath).replace(" test_result.html","").replace("_",":")
					result_file_time = time.mktime(time.strptime(result_file_time, "%Y-%m-%d %H:%M:%S"))
					#print result_file_time
					if (start_time < result_file_time):
						result_file_path = filePath
		if result_file_path != "":
			return result_file_path
		#Analyse the result html.

@app.route("/result",methods=["POST"])
def result():
	if request.method == "POST":
		result_file_path = request.form.get("result_file_path")
		script_path = request.form.get("script_path")
		return_result = []
		return_dic = {}
		with open(result_file_path) as result:
			soup = BeautifulSoup(result.read(),"html.parser")
			trs = soup.find_all("tr")
			for tr in trs:
				tds = tr.find_all("td")
				for td in tds:
					if script_path in td.string:
						for td in tr:
							return_result.append(td.text)
		if ("failed" or "xception") in return_result[len(return_result)-1]:
			return_result.append("failed")
		else:
			return_result.append("passed")
		return_dic["result"] = return_result
		return jsonify(return_dic)

#Util Methods.
def check_if_python(fileName):
	if fileName.endswith('.py'):
		return True

def check_if_html(fileName):
	if fileName.endswith(".html"):
		return True

def gene_selection(root_path,selection):
	with open(os.path.join(root_path,"Auty","scripts","selections","selection.txt"),"w") as content:
		for sele in selection:
			content.write(sele+"\n")

def getDirSize(dir_path):
	size = 0
	for root, dirs, files in os.walk(dir_path):
		size += sum([os.path.getsize(os.path.join(root, name)) for name in files])
		return size