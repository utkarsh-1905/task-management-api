import zoneinfo

import django.utils.timezone as tz


class NormalizeTime:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            if request.GET.get('time_zone'):
                try:
                    tz.activate(zoneinfo.ZoneInfo(
                        request.GET.get('time_zone')))
                except zoneinfo.ZoneInfoNotFoundError:
                    # when zone info is not found, set to UTC
                    tz.activate(zoneinfo.ZoneInfo('UTC'))
            else:
                tz.activate(zoneinfo.ZoneInfo('Asia/Kolkata'))
        response = self.get_response(request)
        return response
