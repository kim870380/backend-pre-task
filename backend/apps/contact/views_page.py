from django.shortcuts import render

def contact_list_page(request):
    return render(request, 'list.html', {})

def contact_detail_page(request, pk: int):
    return render(request, 'detail.html', {"pk": pk})

def contact_create_page(request):
    return render(request, 'create.html')