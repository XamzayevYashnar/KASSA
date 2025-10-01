from django.http import JsonResponse
from django.shortcuts import render
import datetime

def scan_dashboard(request):
    return render(request, "scanner/scan_dashboard.html")

def submit_code(request):
    if request.method == "POST":
        product_code = request.POST.get("productCode")

        if not product_code:
            return JsonResponse({"status": "error", "message": "Mahsulot kodi yuborilmadi"})

        with open("scans.txt", "a", encoding="utf-8") as f:
            f.write(f"{product_code} | {datetime.datetime.now()}\n")

        print(f"📩 SMS yuborildi: {product_code}")

        return JsonResponse({"status": "success", "message": f"{product_code} qabul qilindi"})
    return JsonResponse({"status": "error", "message": "Faqat POST so'rov yuboring"})
