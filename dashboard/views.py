from datetime import datetime
import json

from django.http import JsonResponse
from django.shortcuts import render

from .services import initial_data

START_DATE = '"2018-01-01T00:00:00.000Z"'
END_DATE = '"2018-01-31T00:00:00.000Z"'


def index(request):
    start_date = START_DATE[1:-1]
    end_date = END_DATE[1:-1]
    return render(
        request, 'dashboard/index.html',
        {'data': json.dumps(initial_data(start_date=start_date, end_date=end_date), default=str)})


def data(request):
    print(request.GET)
    buyer = request.GET.get('buyer')
    department = request.GET.get('department')
    member = request.GET.get('member')
    start_date = request.GET.get('startDate', START_DATE)[1:-1]
    end_date = request.GET.get('endDate', END_DATE)[1:-1]

    return JsonResponse(
        {'data': initial_data(buyer, department, member, start_date, end_date)}
    )
