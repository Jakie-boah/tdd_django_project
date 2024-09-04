from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item


def home_page(request):
    if request.method == "POST":
        new_item = request.POST.get("item_text", "")
        Item.objects.create(text=new_item)
        return redirect("/lists/only-one/")

    items = Item.objects.all()

    return render(
        request,
        "home.html",
        {
            "items": items,
        },
    )


def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
