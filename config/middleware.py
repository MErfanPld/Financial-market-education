class APICorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # پیکربندی CORS
        response["Access-Control-Allow-Origin"] = "*"  # همه دامنه‌ها
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"  # متدهای مجاز
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-CSRFTOKEN"  # هدرهای مجاز
        response["Access-Control-Allow-Credentials"] = "true"  # اگر نیاز به ارسال کوکی‌ها دارید
        
        return response
