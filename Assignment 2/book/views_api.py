from django.http import HttpResponseRedirect

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import *
from .serializers import *

# Create your views here.
class ItemViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Items Report"

	def create(self, request):
		data = request.data
		serializer = ItemSerializer(data=request.data, context={'request': request})

		if serializer.is_valid():
			serializer.save()
			get_data = serializer.data
			get_id = get_data['id']
			set_code = f"I-"+str(get_id)
			Item.objects.filter(id=get_id).update(code=set_code)
			return HttpResponseRedirect(redirect_to='/api/items')
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseViewSet(viewsets.ModelViewSet):
	queryset = Purchase.objects.all()
	serializer_class = PurchaseSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Purchases Report"

	def create(self, request):
		data = request.data
		serializer = PurchaseSerializer(data=data, context={'request': request})

		if serializer.is_valid():
			serializer.save()
			get_data = serializer.data
			get_id = get_data['id']
			set_code = f"P-"+str(get_id)
			Purchase.objects.filter(id=get_id).update(code=set_code)
			return HttpResponseRedirect(redirect_to='/api/purchase')
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellViewSet(viewsets.ModelViewSet):
	queryset = Sell.objects.all()
	serializer_class = SellSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Sells Report"

	def create(self, request):
		data = request.data
		serializer = SellSerializer(data=data, context={'request': request})

		if serializer.is_valid():
			serializer.save()
			get_data = serializer.data
			get_id = get_data['id']
			set_code = f"S-"+str(get_id)
			Sell.objects.filter(id=get_id).update(code=set_code)
			# obj = Sell.objects.get(id=get_id)
			# obj.header_code = set_code
			# obj.save()
			return HttpResponseRedirect(redirect_to='/api/sell')
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
	queryset = Item.objects.all()
	serializer_class = ItemSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Stock Report"



class PurchaseDetailViewSet(viewsets.ModelViewSet):
	serializer_class = PurchaseSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Purchases Detail Report"

	def get_queryset(self):
		get_item_code = self.kwargs['code']

		if get_item_code is not None:
			queryset_item = Purchase.objects.filter(code=get_item_code)
		return queryset_item

	def create(self, request):
		data = request.data
		serializer = PurchaseSerializer(data=data, context={'request': request})

		if serializer.is_valid():
			serializer.save()
			get_data = serializer.data
			get_id = get_data['id']
			set_code = f"P-"+str(get_id)
			Purchase.objects.filter(id=get_id).update(code=set_code)
			return HttpResponseRedirect(redirect_to='/api/purchase')
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellDetailViewSet(viewsets.ModelViewSet):
	serializer_class = SellSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Sell Detail Report"

	def get_queryset(self):
		get_item_code = self.kwargs['code']

		if get_item_code is not None:
			queryset_item = Sell.objects.filter(code=get_item_code)
		return queryset_item

	def create(self, request):
		data = request.data
		serializer = SellSerializer(data=data, context={'request': request})

		if serializer.is_valid():
			serializer.save()
			get_data = serializer.data
			get_id = get_data['id']
			set_code = f"S-"+str(get_id)
			Sell.objects.filter(id=get_id).update(code=set_code)
			return HttpResponseRedirect(redirect_to='/api/sell')
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReportDetailViewSet(viewsets.ModelViewSet):
	serializer_class = ReportDetailSerializer
	lookup_field = 'code'

	def get_view_name(self):
		return "Stock Report Detail"

	def get_queryset(self):
		get_item_code = self.kwargs['code']

		if get_item_code is not None:
			start_date = self.request.query_params.get('start_date', None)
			end_date = self.request.query_params.get('end_date', None)
			queryset_item = Item.objects.filter(code=get_item_code)
		return queryset_item

