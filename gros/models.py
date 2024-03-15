from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.db.models.signals import post_save



# user profile
class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True,editable=False)
    profile_img = models.ImageField(upload_to="profile_img",blank=True,null=True)
    birth_date = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

 

    
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=255)
    adress = models.TextField()
    pin_code = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def _str_(self):
        return self.pin_code
    
    
class Category(models.Model):
    name = models.CharField(max_length=200,unique=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    




# class Quantity(models.Model):
#    name=models.CharField(max_length=255,unique=True)
#    created_date=models.DateTimeField(auto_now_add=True)
#    updated_date=models.DateTimeField(auto_now=True)
#    is_active=models.BooleanField(default=True)

#    def __str__(self):
#        return self.name

    

class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="product_images",default="default.jpg",null=True,blank=True)
    category_object = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="item")
    # qty=models.ManyToManyField(Quantity)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
# class Stock(models.Model):
#     product_object = models.OneToOneField(Product,on_delete=models.CASCADE)
#     # if stock=0 then show out of stock and stock-qty chnage
#     total_available_in_stock = models.PositiveIntegerField(default=1)
#     created_date = models.DateTimeField(auto_now_add=True)
#     updated_date = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)


# stock updates total stock-qty changes


# def update_stock(product_id, quantity_change):
#     stock = Stock.objects.get(product_id=product_id)
#     stock.quantity -= quantity_change
#     stock.save()
    

# one user one basket
class Basket(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name="cart")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)


class BasketItem(models.Model):
    product_object = models.ForeignKey(Product,on_delete=models.CASCADE)
    basket_object = models.ForeignKey(Basket,on_delete=models.CASCADE,related_name="cartitem")
    qty = models.PositiveIntegerField(default=1)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
  

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.rate}"
    
    
def create_basket(sender,instance,created,**kwargs):
    if created:
        Basket.objects.create(owner=instance)

post_save.connect(create_basket,sender=User)


class Order(models.Model):

    user_object=models.ForeignKey(User,on_delete=models.CASCADE,related_name="purchase")
    delivery_address=models.CharField(max_length=200)
    phone=models.CharField(max_length=12)
    email=models.CharField(max_length=255,null=True)
    is_paid=models.BooleanField(default=False)
    total=models.PositiveIntegerField()


class OrderItems(models.Model):
    order_object=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="purchaseitems")
    basket_item_object=models.ForeignKey(BasketItem,on_delete=models.CASCADE)
    option=(
        ("order-placed","order-placed"),
        ("intransit","intransit"),
        ("dispatched","dispatched"),
        ("delivered","delivered"),
        ("cancelled","cancelled")
    )
    status=models.CharField(max_length=200,choices=option,default="order-placed")
