from django.shortcuts import render
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from .views import *
from .views_api import *

app_name = 'books'

# Create your views here.

urlpatterns = [
	path('', homepage, name="homepage"),
	path('report/', view_report, name="view-report"),
	path('report/items/<str:code>/list/', view_item_list, name='view-item-list'),
	path('report/items/<str:code>/', view_stock_detail, name='view-stock-detail'),
	path('report/items/<str:code>/details/', view_stock_detail, name='view-stock-detail'),
	path('report/items/<str:code>/<str:start_date>/<str:end_date>/', view_report_range, name='view-report-range'),

	path('api/purchase/<str:code>/details/', PurchaseDetailViewSet.as_view({'get': 'list', 'get': 'retrieve'}), name='purchase-detail'),
	path('api/sell/<str:code>/details/', SellDetailViewSet.as_view({'get': 'list', 'get': 'retrieve'}), name='sell-detail'),
	path('api/report/<str:code>/', ReportDetailViewSet.as_view({'get': 'list', 'get': 'retrieve'}), name='report-detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
