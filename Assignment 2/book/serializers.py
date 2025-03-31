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
	code = serializers.CharField(read_only=True)

	class Meta:
		model = Item
		fields = ('code', 'name', 'unit', 'description', 'stock', 'balance')

class DetailPurchaseSerializer(serializers.Serializer):
# class DetailPurchaseSerializer(serializers.ModelSerializer):
	item_code = serializers.CharField(read_only=True)
	header_code = serializers.CharField(read_only=True)

	# class Meta:
	# 	model = Purchase
	# 	fields = ('item_code', 'quantity', 'unit_price', 'header_code')

	def to_representation(self, instance):
		rep = super().to_representation(instance)
		# rep['item_code'] = instance.item_code
		rep['header_code'] = instance.header_code.code
		return rep

class DetailSellSerializer(serializers.Serializer):
# class DetailSellSerializer(serializers.ModelSerializer):
	header_code = serializers.CharField(read_only=True)
	item_code = serializers.CharField(read_only=True)

	# class Meta:
	# 	model = Sell
	# 	fields = ('item_code', 'quantity', 'header_code')

	def to_representation(self, instance):
		rep = super().to_representation(instance)
		rep['header_code'] = instance.header_code.code
		return rep

class NestedSerializer(serializers.Serializer):
	# code = serializers.CharField(read_only=True)
	# date = serializers.DateField(read_only=True)
	# date = serializers.ModelField(model_field=Purchase()._meta.get_field('date'))

	# in_price = serializers.IntegerField(read_only=True)
	# details = DetailPurchaseSerializer(source='*')

	# def to_representation(self, instance):

	# 	return serialized_data

	def to_representation(self, instance):
		# print("self", self.context)
		# print("instance", instance)
		request = self.context.get("request")
		get_start_date = request.GET.get("start_date",None)
		get_end_date = request.GET.get("end_date",None)

		queryset_purchase = Purchase.objects.filter(item_code=instance).filter(date__range=[get_start_date, get_end_date])
		queryset_sell = Sell.objects.filter(item_code=instance).filter(date__range=[get_start_date, get_end_date])

		first_purchase = queryset_purchase.order_by('id')[:1]
		last_purchase = queryset_purchase.order_by('-id')[:1]

		first_in_qty = [item.in_qty() for item in first_purchase][0]
		first_in_price = [item.in_price() for item in first_purchase][0]
		first_in_total = [item.in_total() for item in first_purchase][0]

		first_out_qty = [item.out_qty() for item in first_purchase][0]
		first_out_price = [item.out_price() for item in first_purchase][0]
		first_out_total = [item.out_total() for item in first_purchase][0]

		last_in_qty = [item.in_qty() for item in last_purchase][0]
		last_in_price = [item.in_price() for item in last_purchase][0]
		last_in_total = [item.in_total() for item in last_purchase][0]

		last_out_qty = [item.out_qty() for item in last_purchase][0]
		last_out_price = [item.out_price() for item in last_purchase][0]
		last_out_total = [item.out_total() for item in last_purchase][0]

		for item in first_purchase:
			item.stock_qty = [item.in_qty() for item in first_purchase]
			item.stock_price = [item.stock_price() for item in first_purchase]
			item.stock_total = [item.in_total() for item in first_purchase]
			item.balance_qty = item.in_qty()
			item.balance = item.in_total()

		for item in last_purchase:
			item.stock_qty = [item.in_qty() for item in queryset_purchase]
			item.stock_price = [item.stock_price() for item in queryset_purchase]
			item.stock_total = [item.in_total() for item in queryset_purchase]
			item.balance_qty = sum([item.in_qty() for item in queryset_purchase])
			item.balance = sum([item.in_total() for item in queryset_purchase])

		list_purch_stock_qty = []
		list_purch_stock_price = []
		list_purch_stock_total = []

		list_sell_stock_qty = []
		list_sell_stock_price = []
		list_sell_stock_total = []

		for item in queryset_sell:
			item.stock_qty = list_purch_stock_qty
			item.stock_price = list_purch_stock_price
			item.stock_total = list_purch_stock_total
			item.balance_qty = item.out_qty()
			item.balance = item.out_total()

			if item.out_qty() > first_in_qty:

				item.out_qty = first_in_qty
				item.out_price = first_in_price
				item.out_total = first_in_total
				list_purch_stock_qty.append(first_out_qty)
				list_purch_stock_qty.append(item.out_qty)
				list_purch_stock_price.append(first_out_price)
				list_purch_stock_price.append(item.out_price)
				list_purch_stock_total.append(first_out_total)
				list_purch_stock_total.append(item.out_total)
				item.balance_qty = first_in_qty
				item.balance = item.out_total

				last_sell = queryset_sell.distinct()

				for last in last_sell:
					last.out_qty = last.out_qty() - first_in_qty
					sum_out_qty = last.out_qty - first_in_qty
					last.out_price = last_in_price
					last.out_total = last_in_total

					list_sell_stock_qty.append(last_out_qty)
					list_sell_stock_qty.append(last.out_qty)
					list_sell_stock_price.append(last_out_price)
					list_sell_stock_price.append(last.out_price)
					list_sell_stock_total.append(last_out_total)
					list_sell_stock_total.append(last.out_total)

					last.stock_qty = list_sell_stock_qty
					last.stock_price = list_sell_stock_price
					last.stock_total = list_sell_stock_total

					last.balance_qty = first_in_qty
					last.balance = last.out_total

		all_query = list(first_purchase) + list(last_purchase) + list(queryset_sell) + list(last_sell)

		data_serializers = ResultedSerializer(all_query, many=True, context=self.context).data

		return data_serializers

class PurchaseSerializer(serializers.ModelSerializer):
	code = serializers.CharField(read_only=True)
	details = DetailSellSerializer(source='*')

	class Meta:
		model = Purchase
		fields = ('code', 'date', 'description', 'details')


# class SellSerializer(serializers.HyperlinkedModelSerializer):
class SellSerializer(serializers.ModelSerializer):
	code = serializers.CharField(read_only=True)
	details = DetailSellSerializer(source='*')

	class Meta:
		model = Sell
		fields = ('code', 'date', 'description', 'details')


class ReportListSerializer(serializers.ModelSerializer):
	# name = serializers.CharField()

	class Meta:
		model = Item
		fields = ('code', 'name', 'description', 'stock', 'unit', 'balance')


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

class SummarySerializer(serializers.ModelSerializer):
	in_qty = serializers.SerializerMethodField()
	out_qty = serializers.SerializerMethodField()
	balance_qty = serializers.IntegerField(source='stock')

	class Meta:
		model = Item
		fields = (
			'in_qty',
			'out_qty',
			'balance_qty',
			'balance',
		)

	def get_in_qty(self, data):
		request = self.context.get("request")
		get_start_date = request.GET.get("start_date",None)
		get_end_date = request.GET.get("end_date",None)

		queryset_purchase = Purchase.objects.filter(item_code=data).filter(date__range=[get_start_date, get_end_date])
		queryset_sell = Sell.objects.filter(item_code=data).filter(date__range=[get_start_date, get_end_date])

		summary_in_qty_purch = sum([item.in_qty() for item in queryset_purchase])
		summary_in_qty_sell = sum([item.in_qty() for item in queryset_sell])

		get_qty = summary_in_qty_purch + summary_in_qty_sell

		return get_qty

	def get_out_qty(self, data):
		request = self.context.get("request")
		get_start_date = request.GET.get("start_date",None)
		get_end_date = request.GET.get("end_date",None)

		queryset_purchase = Purchase.objects.filter(item_code=data).filter(date__range=[get_start_date, get_end_date])
		queryset_sell = Sell.objects.filter(item_code=data).filter(date__range=[get_start_date, get_end_date])

		summary_out_qty_purch = sum([item.out_qty() for item in queryset_purchase])
		summary_out_qty_sell = sum([item.out_qty() for item in queryset_sell])

		get_qty = summary_out_qty_purch + summary_out_qty_sell

		return get_qty


class ItemDetailSerializer(serializers.ModelSerializer):
	# items = ResultedSerializer(source='*')
	# items = NestedSerializer(source='*')
	items = NestedSerializer(source='*', read_only=True)
	# items = serializers.SerializerMethodField()
	# items = NestedSerializer(source='purchase_codes', many=True)
	# items = ResultedSerializer(source='purchase_codes', many=True)
	item_code = serializers.CharField(source='code')
	# in_qty = serializers.Field(source='in_qty')
	summary = SummarySerializer(source='*')
	# summary = SummarySerializer(many=True)


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

