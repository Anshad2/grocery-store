from django.contrib import admin
from gros.models import Category,Product,OrderItems,Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
# admin.site.register(Quantity)
# admin.site.register(Stock)
admin.site.register(OrderItems)
admin.site.register(Order)
