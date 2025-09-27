import random
import math
import time
from typing import List, Tuple, Dict


class MDVRP_Simple:
    """
    Multiple Depot Vehicle Routing Problem Solver - Version đơn giản
    Chỉ sử dụng thư viện built-in của Python
    """

    def __init__(self, depots: List[Tuple[float, float]],
                 customers: List[Tuple[float, float]],
                 vehicle_capacity: int = 100,
                 max_vehicles_per_depot: int = 5):
        """Khởi tạo bài toán MDVRP"""
        self.depots = depots
        self.customers = customers
        self.vehicle_capacity = vehicle_capacity
        self.max_vehicles_per_depot = max_vehicles_per_depot

        # Tạo nhu cầu ngẫu nhiên cho khách hàng
        self.demands = [random.randint(1, 20) for _ in customers]

        # Ma trận khoảng cách
        self.distance_matrix = self._calculate_distance_matrix()

        # Kết quả
        self.best_routes = []
        self.best_cost = float('inf')

    def _calculate_distance_matrix(self) -> List[List[float]]:
        """Tính ma trận khoảng cách Euclidean"""
        all_points = self.depots + self.customers
        n = len(all_points)
        matrix = [[0.0 for _ in range(n)] for _ in range(n)]

        for i in range(n):
            for j in range(n):
                if i != j:
                    x1, y1 = all_points[i]
                    x2, y2 = all_points[j]
                    matrix[i][j] = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        return matrix

    def _calculate_route_cost(self, route: List[int], depot_idx: int) -> float:
        """Tính chi phí của một tuyến đường"""
        if len(route) == 0:
            return 0

        cost = 0
        # Từ kho đến khách hàng đầu tiên
        cost += self.distance_matrix[depot_idx][route[0] + len(self.depots)]

        # Giữa các khách hàng
        for i in range(len(route) - 1):
            customer1 = route[i] + len(self.depots)
            customer2 = route[i + 1] + len(self.depots)
            cost += self.distance_matrix[customer1][customer2]

        # Từ khách hàng cuối về kho
        cost += self.distance_matrix[route[-1] + len(self.depots)][depot_idx]

        return cost

    def _is_route_feasible(self, route: List[int]) -> bool:
        """Kiểm tra tuyến đường có khả thi không"""
        total_demand = sum(self.demands[i] for i in route)
        return total_demand <= self.vehicle_capacity

    def solve_greedy(self) -> Dict:
        """Giải thuật Greedy đơn giản"""
        print("🚀 Bắt đầu giải thuật Greedy...")
        start_time = time.time()

        # Khởi tạo routes cho mỗi kho
        depot_routes = {i: [] for i in range(len(self.depots))}
        unassigned_customers = list(range(len(self.customers)))

        # Gán khách hàng vào kho gần nhất
        while unassigned_customers:
            customer = unassigned_customers.pop(0)
            best_depot = None
            best_cost = float('inf')

            # Thử gán vào từng kho
            for depot_idx in range(len(self.depots)):
                if len(depot_routes[depot_idx]) >= self.max_vehicles_per_depot:
                    continue

                cost = self._get_insertion_cost(customer, depot_idx, depot_routes[depot_idx])

                if cost < best_cost:
                    best_cost = cost
                    best_depot = depot_idx

            # Gán khách hàng vào kho tốt nhất
            if best_depot is not None:
                self._insert_customer_to_depot(customer, best_depot, depot_routes)

        # Chuyển đổi format kết quả
        result = self._format_solution(depot_routes)

        end_time = time.time()
        result['solve_time'] = end_time - start_time
        result['algorithm'] = 'Greedy'

        print(f"✅ Hoàn thành! Thời gian: {result['solve_time']:.2f}s")
        print(f"💰 Chi phí tổng: {result['total_cost']:.2f}")

        return result

    def _get_insertion_cost(self, customer: int, depot_idx: int, current_routes: List[List[int]]) -> float:
        """Tính chi phí để chèn khách hàng vào kho"""
        if not current_routes:
            return self.distance_matrix[depot_idx][customer + len(self.depots)] * 2

        best_cost = float('inf')
        for route in current_routes:
            if self._can_add_to_route(customer, route):
                temp_route = route + [customer]
                cost = self._calculate_route_cost(temp_route, depot_idx)
                if cost < best_cost:
                    best_cost = cost

        if best_cost == float('inf'):
            best_cost = self.distance_matrix[depot_idx][customer + len(self.depots)] * 2

        return best_cost

    def _can_add_to_route(self, customer: int, route: List[int]) -> bool:
        """Kiểm tra có thể thêm khách hàng vào route không"""
        total_demand = sum(self.demands[i] for i in route) + self.demands[customer]
        return total_demand <= self.vehicle_capacity

    def _insert_customer_to_depot(self, customer: int, depot_idx: int, depot_routes: Dict):
        """Chèn khách hàng vào kho tối ưu"""
        if not depot_routes[depot_idx]:
            depot_routes[depot_idx] = [[customer]]
            return

        best_route_idx = None
        best_cost = float('inf')

        for i, route in enumerate(depot_routes[depot_idx]):
            if self._can_add_to_route(customer, route):
                temp_route = route + [customer]
                cost = self._calculate_route_cost(temp_route, depot_idx)
                if cost < best_cost:
                    best_cost = cost
                    best_route_idx = i

        if best_route_idx is not None:
            depot_routes[depot_idx][best_route_idx].append(customer)
        else:
            if len(depot_routes[depot_idx]) < self.max_vehicles_per_depot:
                depot_routes[depot_idx].append([customer])

    def _format_solution(self, depot_routes: Dict) -> Dict:
        """Chuyển đổi solution sang format chuẩn"""
        routes = []
        total_cost = 0

        for depot_idx, depot_route_list in depot_routes.items():
            for route in depot_route_list:
                if route:
                    route_info = {
                        'depot': depot_idx,
                        'customers': route,
                        'cost': self._calculate_route_cost(route, depot_idx),
                        'load': sum(self.demands[i] for i in route)
                    }
                    routes.append(route_info)
                    total_cost += route_info['cost']

        return {
            'routes': routes,
            'total_cost': total_cost,
            'num_vehicles': len(routes),
            'utilization': sum(r['load'] for r in routes) / (len(routes) * self.vehicle_capacity) if routes else 0
        }

    def print_solution_details(self, solution: Dict):
        """In chi tiết giải pháp - chỉ dùng print"""
        print("\n" + "=" * 60)
        print("📊 CHI TIẾT GIẢI PHÁP MDVRP")
        print("=" * 60)

        print(f"🚚 Tổng số xe sử dụng: {solution['num_vehicles']}")
        print(f"💰 Tổng chi phí: {solution['total_cost']:.2f}")
        print(f"📦 Tỷ lệ sử dụng tải trọng: {solution['utilization']:.1%}")
        print(f"⏱️  Thời gian giải: {solution.get('solve_time', 0):.2f}s")

        print(f"\n🏭 Chi tiết {len(self.depots)} kho hàng:")
        for i, depot in enumerate(self.depots):
            print(f"   Kho {i + 1}: Tọa độ ({depot[0]:.1f}, {depot[1]:.1f})")

        print(f"\n👥 Chi tiết {len(self.customers)} khách hàng:")
        for i, (customer, demand) in enumerate(zip(self.customers, self.demands)):
            print(f"   KH {i + 1}: Tọa độ ({customer[0]:.1f}, {customer[1]:.1f}) - Nhu cầu: {demand}")

        print("\n📋 Chi tiết từng tuyến:")
        for i, route_info in enumerate(solution['routes']):
            depot = route_info['depot']
            customers = route_info['customers']
            cost = route_info['cost']
            load = route_info['load']

            customer_list = " → ".join([f"KH{c + 1}" for c in customers])
            print(f"  🚛 Xe {i + 1}: Kho {depot + 1} → {customer_list} → Kho {depot + 1}")
            print(f"      💸 Chi phí: {cost:.2f}")
            print(f"      📦 Tải trọng: {load}/{self.vehicle_capacity} ({load / self.vehicle_capacity:.1%})")

    def simple_visualization(self, solution: Dict):
        """Visualization đơn giản bằng text"""
        print("\n" + "=" * 80)
        print("🗺️  BẢN ĐỒ TUYẾN ĐƯỜNG (TEXT VERSION)")
        print("=" * 80)

        # Tìm min/max để scale
        all_x = [p[0] for p in self.depots + self.customers]
        all_y = [p[1] for p in self.depots + self.customers]
        min_x, max_x = min(all_x), max(all_x)
        min_y, max_y = min(all_y), max(all_y)

        print(f"📍 Phạm vi tọa độ: X({min_x:.1f} → {max_x:.1f}), Y({min_y:.1f} → {max_y:.1f})")
        print()

        # In thông tin kho
        print("🏭 CÁC KHO HÀNG:")
        for i, depot in enumerate(self.depots):
            routes_from_depot = [r for r in solution['routes'] if r['depot'] == i]
            print(f"   Kho {i + 1} tại ({depot[0]:.1f}, {depot[1]:.1f}) - Phục vụ {len(routes_from_depot)} tuyến")

        print()

        # In thông tin tuyến
        depot_symbols = ['🔴', '🔵', '🟢', '🟠', '🟣', '🟤']
        for i, route_info in enumerate(solution['routes']):
            depot_idx = route_info['depot']
            symbol = depot_symbols[depot_idx % len(depot_symbols)]
            customers = route_info['customers']

            print(f"{symbol} TUYẾN {i + 1} (Kho {depot_idx + 1}):")
            route_path = f"   Kho{depot_idx + 1}"
            for customer_idx in customers:
                customer_pos = self.customers[customer_idx]
                demand = self.demands[customer_idx]
                route_path += f" → KH{customer_idx + 1}({customer_pos[0]:.1f},{customer_pos[1]:.1f},D:{demand})"
            route_path += f" → Kho{depot_idx + 1}"
            print(route_path)
            print(f"   💰 Chi phí: {route_info['cost']:.2f} | 📦 Tải: {route_info['load']}")
            print()


def create_sample_problem():
    """Tạo bài toán mẫu để test"""
    print("🎯 Tạo bài toán MDVRP mẫu...")

    # Tạo 3 kho hàng
    depots = [
        (10, 10),  # Kho 1 - Tây Nam
        (80, 20),  # Kho 2 - Đông Nam
        (50, 80)  # Kho 3 - Bắc
    ]

    # Tạo 12 khách hàng với tọa độ cụ thể
    random.seed(42)  # Để có kết quả lặp lại
    customers = [
        (15, 25), (25, 15), (5, 30),  # Gần kho 1
        (75, 35), (85, 15), (90, 25),  # Gần kho 2
        (45, 75), (55, 85), (40, 70),  # Gần kho 3
        (50, 40), (60, 50), (30, 60)  # Ở giữa
    ]

    print(f"✅ Đã tạo bài toán với {len(depots)} kho và {len(customers)} khách hàng")

    return MDVRP_Simple(depots, customers, vehicle_capacity=60, max_vehicles_per_depot=3)


# =================== CHẠY THỬ NGHIỆM ===================
if __name__ == "__main__":
    print("🚀 KHỞI ĐỘNG CHƯƠNG TRÌNH MDVRP - VERSION ĐỠN GIẢN")
    print("=" * 60)
    print("📝 Chỉ sử dụng thư viện built-in của Python!")
    print("=" * 60)

    # Bước 1: Tạo bài toán
    mdvrp = create_sample_problem()

    # Bước 2: Hiển thị thông tin bài toán
    print(f"\n🎲 THÔNG TIN BÀI TOÁN:")
    print(f"   🏭 Số kho hàng: {len(mdvrp.depots)}")
    print(f"   👥 Số khách hàng: {len(mdvrp.customers)}")
    print(f"   🚚 Tải trọng xe: {mdvrp.vehicle_capacity}")
    print(f"   🔢 Số xe tối đa/kho: {mdvrp.max_vehicles_per_depot}")

    # Bước 3: Giải bằng thuật toán Greedy
    solution = mdvrp.solve_greedy()

    # Bước 4: Hiển thị kết quả chi tiết
    mdvrp.print_solution_details(solution)

    # Bước 5: Vẽ bản đồ text
    mdvrp.simple_visualization(solution)

    print("\n🎉 HOÀN THÀNH! Framework cơ bản đã sẵn sàng!")
    print("\n💡 HƯỚNG DẪN TIẾP THEO:")
    print("1. ✅ Chạy code này trước để hiểu cơ bản")
    print("2. 📚 Cài numpy, matplotlib để có visualization đẹp")
    print("3. 🧬 Thêm thuật toán Genetic Algorithm")
    print("4. 🔥 Thêm thuật toán Simulated Annealing")
    print("5. 📊 So sánh hiệu quả các thuật toán")

    print(f"\n🔧 ĐỂ CÀI ĐẶT THƯ VIỆN (chạy trong terminal):")
    print(f"   pip install numpy matplotlib")

    print(f"\n📈 SAU KHI CÀI XONG:")
    print(f"   → Bạn sẽ có biểu đồ đẹp thay vì text map")
    print(f"   → Dễ dàng phát triển thêm tính năng")