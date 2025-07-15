from django.db import models

# Create your models here.

class MenuItem(models.Model):
    category_choices=[
        ('starter','starter'),
        ('Main','Main'),
        ('Desert','Desert')
    ]
    category=models.CharField(max_length=20,choices=category_choices)
    image=models.ImageField(upload_to='menu_images/', blank=True, null=True)
    name=models.CharField(max_length=50)
    description=models.TextField()
    price=models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"{self.name} - ₹{self.price}"

class OrderItem(models.Model):
    menu_item=models.ForeignKey(MenuItem,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField( null=False,blank=False,default=1)

    def __str__(self):
        return f"{self.menu_item.name} x {self.quantity}"

class Order(models.Model):
    items=models.ManyToManyField(OrderItem)
    customer_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=12)
    address=models.TextField()
    order_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer_name}"