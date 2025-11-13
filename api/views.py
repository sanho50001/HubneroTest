import requests
import time
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from .models import UsdRate
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv('SECRET_KEY')  # https://openexchangerates.org/signup

@csrf_exempt
@require_http_methods(["GET"])
def get_current_usd(request):
    recent_rates = UsdRate.objects.all()[:10]

    if recent_rates.exists():
        last_request_time = recent_rates[0].timestamp
        time_diff = (timezone.now() - last_request_time).total_seconds()
        if time_diff < 10:
            return JsonResponse({
                "error": "The pause between requests must be at least 10 seconds.",
                "last_request": last_request_time.isoformat(),
                "remaining_seconds": round(10 - time_diff, 1)
            }, status=429)

    try:
        url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()
        usd_rate = data['rates']['RUB']

        rate_record = UsdRate.objects.create(rate=usd_rate)

        return JsonResponse({
            "current_usd_rate": float(usd_rate),
            "timestamp": datetime.now().isoformat(),
            "recent_requests": [
                {"rate": float(r.rate), "timestamp": r.timestamp.isoformat()}
                for r in recent_rates
            ]
        })

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

