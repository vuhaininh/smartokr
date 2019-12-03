# from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.


def char_count(request):
    text = request.GET.get("text", "")
    return JsonResponse({"count": len(text)})