from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import math

"""
    Tạo ma trận khoảng cách 
"""
def compute_euclidean_distance_matrix(locations):
    distances = {}
    for from_counter, from_node in enumerate(locations):
        distances[from_counter] = {}
        for to_counter, to_node in enumerate(locations):
            if from_counter == to_counter:
                distances[from_counter][to_counter] = 0
            else:
                distances[from_counter][to_counter] = math.hypot(
                    from_node[0] - to_node[0],
                    from_node[1] - to_node[1]
                )
    return distances

"""
    Giải bài toán MDVRP

    Args:
        depots: List tọa độ các depot [(x1,y1), (x2,y2), ...]
        customers: List tọa độ khách hàng [(x1,y1), (x2,y2), ...]
        num_vehicles_per_depot: Số xe mỗi depot
        vehicle_capacities: List capacity của từng xe (optional)
        demands: List nhu cầu của từng khách (optional, mặc định = 1)
    """
def solve_mdvrp(depots, customers, num_vehicles_per_depot, vehicle_capacities=None, demands=None):
    all_locations = depots + customers
    num_depots = len(depots)
    num_vehicles = num_vehicles_per_depot * num_depots

    # Tạo starts và ends cho mỗi: mỗi depot có num_vehicles_per_depot xe
    starts = []
    ends = []
    for depot_idx in range(num_depots):
        for _ in range(num_vehicles_per_depot):
            starts.append(depot_idx)
            ends.append(depot_idx)

    data = {
        "distance_matrix": compute_euclidean_distance_matrix(all_locations),
        "num_vehicles": num_vehicles,
        "starts": starts,
        "ends": ends,
        "demands": demands if demands else [0] * num_depots + [1] * len(customers),
        "vehicle_capacities": vehicle_capacities if vehicle_capacities else [100] * num_vehicles
    }

    # Tạo manager với starts và ends
    manager = pywrapcp.RoutingIndexManager(
        len(all_locations),
        num_vehicles,
        data['starts'],
        data['ends']
    )
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return int(data['distance_matrix'][from_node][to_node] * 100)  # Scale up để tránh làm tròn

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Thêm capacity constraint
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],
        True,  # start cumul to zero
        'Capacity'
    )

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_parameters.time_limit.seconds = 30

    # Giải
    solution = routing.SolveWithParameters(search_parameters)

    routes = []
    total_distance = 0

    if solution:
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(previous_index, index, vehicle_id)

            # Thêm depot cuối
            route.append(manager.IndexToNode(index))

            # Chỉ thêm route có khách hàng
            if len(route) > 2:
                routes.append({
                    'vehicle_id': vehicle_id,
                    'depot': data['starts'][vehicle_id],
                    'route': route,
                    'distance': route_distance / 100  # Scale back
                })
                total_distance += route_distance

        # print(f"Tổng khoảng cách: {total_distance / 100:.2f}")
        return {
            'status': 'success',
            'total_distance': total_distance / 100,
            'routes': routes
        }
    else:
        # print("Không tìm thấy giải pháp!")
        return {
            'status': 'failed',
            'message': 'No solution found!'
        }

    return routes


# # Test
# if __name__ == "__main__":
#     depots = [(0, 0), (100, 100)]
#     customers = [(20, 30), (40, 50), (60, 20), (80, 80), (30, 70)]
#
#     routes = solve_mdvrp(depots, customers, num_vehicles_per_depot=1)
#
#     for route_info in routes:
#         print(f"Xe {route_info['vehicle_id']} (Depot {route_info['depot']}): "
#               f"{route_info['route']} - Khoảng cách: {route_info['distance']:.2f}")