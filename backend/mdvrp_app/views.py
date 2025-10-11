from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .mdvrp_solver import solve_mdvrp
from .utils import get_coordinates
import json

def calculate_routes(request):
    # body = json.loads(request.body)
    # depots = [get_coordinates(d) for d in body['depots']]
    # customers = [get_coordinates(c) for c in body['customers']]
    # num_vehicle = body.get('vehicles_per_depot', 2)
    #
    # routes = solve_mdvrp(depots, customers, num_vehicle)
    # return JsonResponse({'routes': routes})
    if request.method == 'GET':
        # Nhận dữ liệu JSON từ frontend
        body = json.loads(request.body.decode('utf-8'))
        name = body.get('name', 'Guest')

        # Trả dữ liệu JSON về client
        return JsonResponse({
            'message': f'Hello, {name}!',
            'status': 'success'
        })

        # Nếu không phải POST
    return JsonResponse({'error': 'Only POST allowed'}, status=405)
