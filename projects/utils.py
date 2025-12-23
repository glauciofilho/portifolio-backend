import requests


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):
    return request.META.get('HTTP_USER_AGENT', '')


def get_country_from_ip(ip):
    try:
        response = requests.get(
            f"https://ipapi.co/{ip}/json/",
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("country_name", "")
    except Exception:
        pass

    return ""