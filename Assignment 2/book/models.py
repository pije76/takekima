from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime

# Create your models here.
class Item(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=50, blank=True, null=True)
	name = models.CharField(max_length=255, blank=True, null=True)
	unit = models.CharField(max_length=255, blank=True, null=True)
	description = models.TextField(blank=True, null=True)
	stock = models.PositiveIntegerField(default=0, blank=True, null=True)
	balance = models.PositiveIntegerField(default=0, blank=True, null=True)
	created_at = models.DateField(auto_now_add=True, auto_now=False, blank=True, null=True)
	updated_at = models.DateField(auto_now=True, blank=True, null=True)
	is_deleted = models.BooleanField(default=False, blank=True, null=True)

	def __str__(self):
		return str(self.code)

	def in_qty(self):
		return 0

	def out_qty(self):
		return 0

	def balance_qty(self):
		return 0

@receiver(post_save, sender=Item)
def create_code(sender, instance, created, **kwargs):
	if created:
		if instance.id is not None:
			instance.code = f"I-"+str(instance.id)
			instance.save()


class Purchase(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=50, blank=True, null=True)
	date = models.DateField(default=datetime.date.today)
	description = models.TextField(blank=True, null=True)
	item_code = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
	quantity = models.PositiveIntegerField(default=0)
	unit_price = models.PositiveIntegerField(default=0)
	header_code = models.ForeignKey('self', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
	created_at = models.DateField(auto_now_add=True, auto_now=False)
	updated_at = models.DateField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.code)

	def in_qty(self):
		return self.quantity

	def in_price(self):
		return self.unit_price

	def in_total(self):
		return self.quantity * self.unit_price

	def out_qty(self):
		return 0

	def out_price(self):
		return 0

	def out_total(self):
		return 0

	def stock_qty(self):
		return 0

	def stock_price(self):
		return 0

	def stock_total(self):
		return 0

	def balance_qty(self):
		return 0

	def balance(self):
		return 0


@receiver(post_save, sender=Purchase)
def create_code(sender, instance, created, **kwargs):
	if created:
		if instance.id is not None:
			set_code = f"P-"+str(instance.id)
			instance.code = set_code
			instance.save()
		if instance.code is not None:
			Purchase.objects.filter(id=instance.id).update(header_code=instance.id)


class Sell(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=50, blank=True, null=True)
	# date = models.DateField(auto_now_add=True, auto_now=False)
	date = models.DateField(default=datetime.date.today)
	description = models.TextField(blank=True, null=True)

	item_code = models.ForeignKey(Item, on_delete=models.CASCADE, blank=True, null=True)
	quantity = models.PositiveIntegerField(default=0)
	header_code = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

	created_at = models.DateField(auto_now_add=True, auto_now=False)
	updated_at = models.DateField(auto_now=True)
	is_deleted = models.BooleanField(default=False)

	def __str__(self):
		return str(self.code)

	def in_qty(self):
		return 0

	def in_price(self):
		return 0

	def in_total(self):
		return 0

	def out_qty(self):
		return self.quantity

	def out_price(self):
		return 0

	def out_total(self):
		return 0

	def stock_qty(self):
		return 0

	def stock_price(self):
		return 0

	def stock_total(self):
		return 0

	def balance_qty(self):
		return 0

	def balance(self):
		return 0

@receiver(post_save, sender=Sell)
def create_code(sender, instance, created, **kwargs):
	if created:
		if instance.id is not None:
			set_code = f"S-"+str(instance.id)
			instance.code = set_code
			instance.save()
		if instance.code is not None:
			Sell.objects.filter(id=instance.id).update(header_code=instance.id)

