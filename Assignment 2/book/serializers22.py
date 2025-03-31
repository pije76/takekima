from django.core import serializers as serial
from django.core.serializers import json
from django.core import serializers as srl

from rest_framework import serializers
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from book.models import *
import json as jsn

import datetime

class ItemSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	code = serializers.CharField(read_only=True)

	class Meta:
		model = Item
		fields = ('id', 'code', 'name', 'unit', 'description', 'stock', 'balance')

class DetailPurchaseSerializer(serializers.ModelSerializer):
	# id = serializers.IntegerField(read_only=True)
	# item_code = serializers.CharField(read_only=True)
	# item_code = serializers.CharField(read_only=True)
	# header_code = serializers.CharField(read_only=True)
	header_code = serializers.CharField(source='code', read_only=True)
	# quantity = serializers.IntegerField()
	# unit_price = serializers.IntegerField()

	class Meta:
		model = Purchase
		fields = ('item_code', 'quantity', 'unit_price', 'header_code')

	# def to_representation(self, instance):
	# 	rep = super().to_representation(instance)
	# 	# rep['header_code'] = instance.header_code.code
	# 	rep['item_code'] = instance.item_code.code
	# 	return rep

class DetailSellSerializer(serializers.Serializer):
	header_code = serializers.CharField(read_only=True)
	item_code = serializers.CharField(read_only=True)

	def to_representation(self, instance):
		rep = super().to_representation(instance)
		rep['header_code'] = instance.header_code.code
		return rep

# class PurchaseSerializer(serializers.Serializer):
class PurchaseSerializer(serializers.ModelSerializer):
	id = serializers.IntegerField(read_only=True)
	code = serializers.CharField(read_only=True)
	date = serializers.DateField()
	description = serializers.CharField()
	# header_code = serializers.CharField(read_only=True)
	details = DetailPurchaseSerializer(source='*')

	class Meta:
		model = Purchase
		fields = ('id', 'code', 'date', 'description', 'details')
		# fields = ('code', 'date', 'description', 'item_code', 'header_code', 'quantity', 'unit_price', 'details')

class SellSerializer(serializers.ModelSerializer):
	code = serializers.CharField(read_only=True)
	details = DetailSellSerializer(source='*')

	class Meta:
		model = Sell
		fields = ('code', 'date', 'description', 'details')

# class ResultedSerializer(serializers.Serializer):
class ResultedSerializer(serializers.ModelSerializer):

	class Meta:
		model = Purchase
		fields = (
			'date',
			'description',
			'code',
			'in_qty',
			'in_price',
			'in_total',
			'out_qty',
			'out_price',
			'out_total',
			'stock_qty',
			'stock_price',
			'stock_total',
			'balance_qty',
			'balance',
		)


class NestedItemSerializer(serializers.Serializer):

	def to_representation(self, instance):
		request = self.context.get("request")
		get_start_date = request.GET.get("start_date",None)
		get_end_date = request.GET.get("end_date",None)

		queryset_purchase = Purchase.objects.filter(item_code=instance.id).filter(date__range=[get_start_date, get_end_date])
		queryset_sell = Sell.objects.filter(item_code=instance.id).filter(date__range=[get_start_date, get_end_date])

		if len(queryset_purchase) > 0:
			first_purchase = queryset_purchase.order_by('id')[:1]
			last_purchase = queryset_purchase.order_by('-id')[:1]

			purchase_stock_price = [item.stock_price() for item in queryset_purchase]
			purchase_stock_total = [item.stock_total() for item in queryset_purchase]

			first_in_qty = [item.in_qty() for item in first_purchase][0]
			first_in_price = [item.in_price() for item in first_purchase][0]
			first_in_total = [item.in_total() for item in first_purchase][0]

			first_stock_qty = [item.stock_qty() for item in first_purchase][0]
			first_stock_price = [item.stock_price() for item in first_purchase][0]
			first_stock_total = [item.stock_total() for item in first_purchase][0]

			# first_out_price = [item.out_price() for item in first_purchase][0]

			last_in_qty = [item.in_qty() for item in last_purchase][0]
			last_in_price = [item.in_price() for item in last_purchase][0]
			last_in_total = [item.in_total() for item in last_purchase][0]

			last_stock_qty = [item.stock_qty() for item in last_purchase][0]
			last_stock_price = [item.stock_price() for item in last_purchase][0]
			last_stock_total = [item.stock_total() for item in last_purchase][0]

			sell_in_qty = [item.in_qty() for item in queryset_sell][0]
			sell_in_price = [item.in_price() for item in queryset_sell][0]
			sell_in_total = [item.in_total() for item in queryset_sell][0]

			sell_stock_qty = [item.stock_qty() for item in queryset_sell][0]
			sell_stock_price = [item.stock_price() for item in queryset_sell][0]
			sell_stock_total = [item.stock_total() for item in queryset_sell][0]

			purch_stock_price = []
			purch_stock_total = []

			for item in first_purchase:
				item.stock_qty = [item.in_qty() for item in first_purchase]
				item.stock_price = [item.in_price() for item in first_purchase]
				item.stock_total = [item.in_total() for item in first_purchase]
				item.balance_qty = item.in_qty()
				item.balance = item.in_total()

			for item in last_purchase:
				item.stock_qty = [item.in_qty() for item in queryset_purchase]
				purch_stock_price.append(first_in_price)
				purch_stock_price.append(item.in_price())
				item.stock_price = purch_stock_price
				purch_stock_total.append(first_in_total)
				purch_stock_total.append(item.in_total())
				item.stock_total = purch_stock_total
				item.balance_qty = sum([item.in_qty() for item in queryset_purchase])
				item.balance = sum([item.in_total() for item in queryset_purchase])

			sell_first_stock_qty = []
			sell_first_stock_price = []
			sell_first_stock_total = []

			sell_last_stock_qty = []
			sell_last_stock_price = []
			sell_last_stock_total = []

			for item in queryset_sell:

				if item.out_qty() > first_in_qty:

					item.out_qty = first_in_qty
					item.out_price = first_in_price
					item.out_total = first_in_total

					sell_first_stock_qty.append(last_stock_qty)
					sell_first_stock_qty.append(item.out_qty)
					sell_first_stock_price.append(item.in_price())
					sell_first_stock_price.append(last_in_price)
					sell_first_stock_total.append(item.in_total())
					sell_first_stock_total.append(last_in_total)

					item.stock_qty = sell_first_stock_qty
					item.stock_price = sell_first_stock_price
					item.stock_total = sell_first_stock_total
					# item.balance_qty = item.out_qty()
					item.balance_qty = first_in_qty
					# item.balance = item.out_qty * item.out_price
					item.balance = last_in_total


					last_sell = queryset_sell.distinct()

					for last in last_sell:
						last.out_qty = last.out_qty() - first_in_qty
						last.out_price = last_in_price
						last.out_total = last_in_total

						sell_last_stock_qty.append(last.in_qty())
						sell_last_stock_qty.append(last.out_qty)
						sell_last_stock_price.append(last.in_price())
						sell_last_stock_price.append(last.out_price)
						sell_last_stock_total.append(last.in_total())
						sell_last_stock_total.append(last.out_qty * last.out_price)

						last.stock_qty = sell_last_stock_qty
						last.stock_price = sell_last_stock_price
						last.stock_total = sell_last_stock_total

						last.balance_qty = last.out_qty
						last.balance = last.out_qty * last.out_price

			all_query = list(first_purchase) + list(last_purchase) + list(queryset_sell) + list(last_sell)
			data_serializers = ResultedSerializer(all_query, many=True, context=self.context).data
			return data_serializers

		else:
			print(len(queryset_purchase))
			pass



class NestedSummarySerializer(serializers.ModelSerializer):

	class Meta:
		model = Item
		fields = (
			'in_qty',
			'out_qty',
			'balance_qty',
			'balance',
		)

	def to_representation(self, instance):
		request = self.context.get("request")
		get_start_date = request.GET.get("start_date",None)
		get_end_date = request.GET.get("end_date",None)
		queryset_purchase = Purchase.objects.filter(item_code=instance.id).filter(date__range=[get_start_date, get_end_date])
		queryset_sell = Sell.objects.filter(item_code=instance.id).filter(date__range=[get_start_date, get_end_date])
		rep = super().to_representation(instance)
		rep['in_qty'] = sum([item.in_qty() for item in queryset_purchase])
		rep['out_qty'] = sum([item.out_qty() for item in queryset_sell])
		rep['balance_qty'] = instance.stock
		rep['balance'] = instance.balance
		return rep


class ItemDetailSerializer(serializers.ModelSerializer):
	items = NestedItemSerializer(source='*', read_only=True)
	item_code = serializers.CharField(source='code')
	summary = NestedSummarySerializer(source='*')


	class Meta:
		model = Item
		fields = (
			'items',
			'item_code',
			'name',
			'unit',
			'summary',
		)


class ReportDetailSerializer(serializers.Serializer):
	result = ItemDetailSerializer(source='*')

