from django.shortcuts import render,redirect
from django.views.generic import View,DetailView,TemplateView,ListView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


from gros.forms import RegistrationForm,LoginForm
from gros .models import Product,BasketItem,Order,OrderItems
from gros.decorators import signin_required,owner_permission_required
# Create your views here.

   
# url:localhost:8000/register
# method,get,post
# form_class :registartionform


class SignUpView(View):


    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("signin")
        else:
          return render(request,"register.html",{"form":form})
        

# url:localhost:8000/
# method,get,post
# form_class :loginform
        
class SignInView(View):

    def get(self,request,*args,**kwargs):
     form=LoginForm()
     return render(request,"login.html",{"form":form})
    def post(self,request,*args,**kwargs):
       form=LoginForm(request.POST)
       if form.is_valid():
          u_name=form.cleaned_data.get("username")
          pwd=form.cleaned_data.get("password")
          user_object=authenticate(request,username=u_name,password=pwd)
          if user_object:
            login(request,user_object)
            return redirect("home")
       messages.error(request,"invalid credentails")
       return render(request,"login.html",{"form":form})



@method_decorator([signin_required,never_cache],name="dispatch")
class IndexView(View):
    def get(self,request,*args,**kwargs):
     qs=Product.objects.all()
     return render(request,"index.html",{"data":qs})



# url:localhost:8000/products/{id}
@method_decorator([signin_required,never_cache],name="dispatch")
class ProductDetailView(DetailView):
   
#    def get(self,request,*args,**kwargs):
#       id=kwargs.get("pk")
#       qs=Product.objects.get(id=id)
#       return render(request,"product_detail.html",{"data":qs})
   template_name="product_detail.html"
   model=Product
   context_object_name="data"
   
   

class HomeView(TemplateView):
   template_name="frontpage.html"
   

# add to basket/cart
# url:localhost:8000/product/{id}/add to basket
# method:post
@method_decorator([signin_required,never_cache],name="dispatch")
class AddToBasketView(View):
   

   def post(self,request,*args,**kwargs):
      qty=request.POST.get("qty")
      id=kwargs.get("pk")
      product_obj=Product.objects.get(id=id)
      BasketItem.objects.create(
         qty=qty,
         product_object=product_obj,
         basket_object=request.user.cart
      )
      return redirect("index")
   


# basket item list view
# url:localhost:8000/basketitems/all
# method get
@method_decorator([signin_required,never_cache],name="dispatch")
class BasketItemListView(ListView):
   
                     
   template_name="cart_list.html"
   model=BasketItem
   context_object_name="data"

   def get_queryset(self):
      qs=self.request.user.cart.cartitem.filter(is_order_placed=False)
      return qs
   

@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")
class BasketItemRemoveView(View):
   
   def get(self,request,*args,**kwargs):
      id=kwargs.get("pk")
      basket_item_object=BasketItem.objects.get(id=id)
      basket_item_object.delete()
      return redirect ("basket-items")
   



@method_decorator([signin_required,owner_permission_required,never_cache],name="dispatch")
class CartItemUpdateQuantityView(View):

   def post(self,request,*args,**kwargs):
      action=request.POST.get("counterButton")
      id=kwargs.get("pk")
      basket_item_object=BasketItem.objects.get(id=id)
      if action=="+":
         basket_item_object.qty+=1
         basket_item_object.save()
      else:
         basket_item_object.qty-=1
         basket_item_object.save()

      return redirect("basket-items")
      



@method_decorator([signin_required,never_cache],name="dispatch")
class CheckOutView(View):


   def get(self,request,*args,**kwargs):
      return render(request,"checkout.html")
   
   def post(self,request,*args,**kwargs):
      email=request.POST.get("email")
      phone=request.POST.get("phone")
      address=request.POST.get("address")

      # creating order instance
      order_obj=Order.objects.create(
         user_object=request.user,
         delivery_address=address,
         phone=phone,
         email=email,
         total=request.user.cart.cart_total
     )
       # creating ordertitems instance
   
      try:

         basket_items=request.user.cart.cart_items
         for bi in basket_items:
            OrderItems.objects.create(
            order_object=order_obj,
            basket_item_object=bi

         )
         bi.is_order_placed=True
         bi.save()

      except:
        
        order_obj.delete()
      
      finally:
        
        return redirect("index")
      


class OrderSummaryView(View):


   def get(self,request,*args,**kwargs):
      qs=Order.objects.filter(user_object=request.user).exclude(status="cancelled")
      return render(request,"summary.html",{"data":qs})
   

@method_decorator([signin_required,never_cache],name="dispatch")  
class SignOutView(View):

   def get(self,request,*args,**kwargs):
      logout(request)
      return redirect("signin")
