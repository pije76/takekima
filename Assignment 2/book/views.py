from django.shortcuts import render, redirect

from .models import *
from .serializers import *

import requests
import json

# Create your views here.
def homepage(request):
	title = "Homepage"
	context = {
		'title': title,
	}

	return render(request, 'homepage.html', context)

def view_report(request):
	url = "http://127.0.0.1:8000/api/items/"
	resp = requests.get(url)
	json_resp = resp.json()

	title = "Item List"

	code = request.GET.get('code', None)
	start_date = request.GET.get('start_date', None)
	end_date = request.GET.get('end_date', None)

	if request.method == 'POST':

		context = {
			'title': title,
		}

		return redirect('books:view-report-range', code=code, start_date=start_date, end_date=end_date)

	else:

		context = {
			"title" : title,
			"item_data" : json_resp,
		}

		return render(request, 'view_report.html', context)

def view_item_list(request, code=None):
	title = "Transaction List"

	url = "http://127.0.0.1:8000/api/items/" + code
	url_item_purchase = "http://127.0.0.1:8000/api/purchase/"
	url_item_sell = "http://127.0.0.1:8000/api/sell/"

	resp = requests.get(url)
	resp_purchase = requests.get(url_item_purchase)
	resp_sell = requests.get(url_item_sell)

	json_resp = resp.json()
	json_resp_purchase = resp_purchase.json()
	json_resp_sell = resp_sell.json()

	resp_item = []
	resp_list = []

	for buy in json_resp_purchase:
		if buy["details"]["item_code"] == code:
			resp_list.append(buy)

	for sell in json_resp_sell:
		if sell["details"]["item_code"] == code:
			resp_list.append(sell)

	context = {
		'title': title,
		'datas': json_resp,
		'item_data': resp_list,
	}

	if request.method == 'GET':
		return render(request, 'view_item_list.html', context)
	else:
		pass

def view_stock_detail(request, code=None):
	title = "Transaction Detail"

	get_code = code.split()[0][0]

	if get_code == "I":
		url_item = "http://127.0.0.1:8000/api/items/" + code
	if get_code == "P":
		url_item = "http://127.0.0.1:8000/api/purchase/" + code + "/details"
	if get_code == "S":
		url_item = "http://127.0.0.1:8000/api/sell/" + code + "/details"

	resp = requests.get(url_item)
	json_resp = resp.json()

	if request.method == 'GET':

		context = {
			'title': title,
			# 'datas': datas,
			'item_data': json_resp,
		}

		return render(request, 'view_stock_detail.html', context)

	else:
		return redirect('books:view-report')

def view_report_range(request, code=None, start_date=None, end_date=None):

	get_code = request.POST.get('code', None)
	url_report_detail = "http://127.0.0.1:8000/api/report/" + code + "/?start_date=" + start_date + "&end_date=" + end_date
	resp_report = requests.get(url_report_detail)

	if resp_report.ok:

		json_resp_report = resp_report.json()

		data_transactions = []

		title = "Stock Report"
		data_stock = json_resp_report['result']['items']
		summary = json_resp_report['result']['summary']

		datas = json_resp_report['result']

		print("summary", summary)
		print("data_stock", type(data_stock))
		print("data_stock", len(data_stock))

		if request.method == 'POST':

			context = {
				'title': title,
				'datas': datas,
				'item_data': data_stock,
				'summary': summary,
			}

			return render(request, 'view_item_range.html', context)

		else:
			return redirect('books:view-report')
	else:
		return redirect('books:view-report')
