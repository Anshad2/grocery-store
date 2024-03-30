      
from django.shortcuts import redirect
from django.contrib import messages
from gros.models import BasketItem

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"inavlid session")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper


def owner_permission_required(fn):

    def wrapper(request,*args,**kwargs):
        id=kwargs.get("pk")
        basket_item_object=BasketItem.objects.get(id=id)
        if request.user!=basket_item_object.basket_object.owner:
            messages.error(request,"permission denied")
            return redirect("signin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper
      