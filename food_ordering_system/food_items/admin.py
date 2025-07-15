from django.contrib import admin
from .models import MenuItem,OrderItem,Order
# Register your models here.

class MenuItemAdmin(admin.ModelAdmin):
    list_display=('category','image','name','description','price')

class orderitemadmin(admin.ModelAdmin):
    list_display=('menu_item','quantity')

class orderadmin(admin.ModelAdmin):
    list_display=('get_items','customer_name','phone','address','order_date')

    def get_items(self, obj):
        return ", ".join([f"{i.menu_item.name} x{i.quantity}" for i in obj.items.all()])
    get_items.short_description = 'Items'

admin.site.register(MenuItem,MenuItemAdmin)
admin.site.register(OrderItem,orderitemadmin)
admin.site.register(Order,orderadmin)