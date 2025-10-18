# import json
# import random
# import os
# import math
# from shapely.geometry import shape, Point
#
# # --- CÁC THAM SỐ CẤU HÌNH ---
# NUM_DEPOTS = 250
# NUM_CUSTOMERS = 800
# NUM_DRIVERS = 500
# OUTPUT_DIR = "data"
# BOUNDARY_FILE = os.path.join(OUTPUT_DIR, "mr7_boundary.geojson")
#
# # --- DỮ LIỆU ĐỂ TẠO ĐỊA CHỈ ĐA DẠNG ---
# # (Giữ nguyên các danh sách phường và đường)
# WARDS_IN_DISTRICT_7 = [
#     "Tân Thuận Đông", "Tân Thuận Tây", "Tân Kiểng", "Tân Hưng",
#     "Bình Thuận", "Tân Quy", "Phú Thuận", "Tân Phú", "Tân Phong", "Phú Mỹ"
# ]
# STREET_NAMES = [
#     "Nguyễn Thị Thập", "Huỳnh Tấn Phát", "Lê Văn Lương", "Nguyễn Hữu Thọ",
#     "Trần Xuân Soạn", "Lâm Văn Bền", "Phạm Hữu Lầu", "Nguyễn Lương Bằng"
# ]
#
#
# # --- HÀM MỚI ĐỂ TẠO TỌA ĐỘ AN TOÀN ---
#
# def load_boundary_polygon(filepath):
#     """Tải ranh giới từ file GeoJSON và trả về một đối tượng Polygon."""
#     try:
#         with open(filepath, 'r', encoding='utf-8') as f:
#             geojson_data = json.load(f)
#         # Giả sử file geojson chỉ có 1 feature là Polygon
#         return shape(geojson_data['features'][0]['geometry'])
#     except Exception as e:
#         print(f"Lỗi: Không thể tải file ranh giới '{filepath}'. Lỗi: {e}")
#         return None
#
#
# def generate_random_point_in_polygon(polygon):
#     """Tạo một điểm ngẫu nhiên chắc chắn nằm trong Polygon cho trước."""
#     min_lon, min_lat, max_lon, max_lat = polygon.bounds
#     while True:
#         # Tạo điểm ngẫu nhiên trong bounding box
#         random_point = Point(random.uniform(min_lon, max_lon), random.uniform(min_lat, max_lat))
#         # Kiểm tra xem điểm có nằm trong ranh giới không
#         if polygon.contains(random_point):
#             return round(random_point.y, 6), round(random_point.x, 6)  # Trả về (latitude, longitude)
#
#
# # --- CÁC HÀM GENERATE ĐƯỢC CẬP NHẬT ---
#
# def generate_random_address():
#     # ... (Hàm này giữ nguyên)
#     street = random.choice(STREET_NAMES)
#     ward = random.choice(WARDS_IN_DISTRICT_7)
#     house_number = random.randint(1, 1500)
#     if random.random() < 0.3:
#         return f"{house_number}/{random.randint(1, 50)} {street}, P. {ward}, Quận 7, TP. HCM"
#     return f"{house_number} {street}, P. {ward}, Quận 7, TP. HCM"
#
#
# def generate_depots_data(num_depots, polygon):
#     """Tạo dữ liệu kho với tọa độ an toàn."""
#     depots_list = []
#     print(f"Đang tạo {num_depots} depots...")
#     for i in range(num_depots):
#         depot_id = i + 1
#         lat, lon = generate_random_point_in_polygon(polygon)  # SỬ DỤNG HÀM MỚI
#         depot = {
#             "id": f"{depot_id:02d}",
#             "name": f"Kho Quân khu 7 - {depot_id:02d}",
#             "address": generate_random_address(),
#             "latitude": lat,
#             "longitude": lon
#         }
#         depots_list.append(depot)
#     print("-> Tạo depots thành công!")
#     return depots_list
#
#
# def generate_customers_data(num_customers, polygon):
#     """Tạo dữ liệu khách hàng với tọa độ an toàn."""
#     customers_list = []
#     print(f"Đang tạo {num_customers} customers...")
#     # ... (danh sách tên giữ nguyên)
#     for i in range(num_customers):
#         customer_id = i + 1
#         lat, lon = generate_random_point_in_polygon(polygon)  # SỬ DỤNG HÀM MỚI
#         customer = {
#             "id": customer_id,
#             "name": f"Khách hàng {customer_id}",  # Sửa lại tên cho đơn giản
#             "phone": f"09{random.randint(10000000, 99999999)}",
#             "email": f"customer.{customer_id}@example.com",
#             "address": generate_random_address(),
#             "latitude": lat,
#             "longitude": lon
#         }
#         customers_list.append(customer)
#     print("-> Tạo customers thành công!")
#     return customers_list
#
#
# def generate_drivers_data(num_drivers):
#     # ... (Hàm này giữ nguyên, vì không chứa tọa độ)
#     drivers_list = []
#     print(f"Đang tạo {num_drivers} drivers...")
#     for i in range(num_drivers):
#         driver_id = i + 1
#         depot_id = math.floor(i / 2) + 1
#         driver = {
#             "id": f"{driver_id:03d}",
#             "name": f"Tài xế {driver_id}",
#             "phone": f"09{random.randint(10000000, 99999999)}",
#             "depot_id": f"{depot_id:02d}"
#         }
#         drivers_list.append(driver)
#     print("-> Tạo drivers thành công!")
#     return drivers_list
#
#
# def save_to_json(data, filename):
#     # ... (Hàm này giữ nguyên)
#     if not os.path.exists(OUTPUT_DIR):
#         os.makedirs(OUTPUT_DIR)
#     filepath = os.path.join(OUTPUT_DIR, filename)
#     with open(filepath, 'w', encoding='utf-8') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#     print(f"Đã lưu thành công dữ liệu vào file: {filepath}\n")
#
#
# # --- CHƯƠNG TRÌNH CHÍNH ---
# if __name__ == "__main__":
#     # 1. Tải ranh giới Quân khu 7
#     mr7_polygon = load_boundary_polygon(BOUNDARY_FILE)
#
#     if mr7_polygon:
#         print("Tải ranh giới địa lý thành công!")
#
#         # 2. Tạo dữ liệu drivers (không cần ranh giới)
#         drivers_data = generate_drivers_data(NUM_DRIVERS)
#         save_to_json(drivers_data, "drivers.json")
#
#         # 3. Tạo depots và customers với tọa độ được đảm bảo
#         depots_data = generate_depots_data(NUM_DEPOTS, mr7_polygon)
#         save_to_json(depots_data, "depots.json")
#
#         customers_data = generate_customers_data(NUM_CUSTOMERS, mr7_polygon)
#         save_to_json(customers_data, "customers.json")
#
#         print("Hoàn tất! Đã tạo 3 file JSON với tọa độ chính xác.")
#     else:
#         print("Không thể tạo dữ liệu do không tải được file ranh giới.")