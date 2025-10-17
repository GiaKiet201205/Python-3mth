import json
import random
import os
import math

# --- CÁC THAM SỐ CẤU HÌNH ---
NUM_DEPOTS = 250
NUM_CUSTOMERS = 800
NUM_DRIVERS = 500
OUTPUT_DIR = "data"

# --- DỮ LIỆU ĐỊA CHỈ CHO TOÀN BỘ QUÂN KHU 7 ---

# CẬP NHẬT: Danh sách các tỉnh/thành phố thuộc Quân khu 7
PROVINCES_IN_QK7 = [
    "TP. Hồ Chí Minh", "Đồng Nai", "Bà Rịa - Vũng Tàu", "Bình Dương",
    "Bình Phước", "Tây Ninh", "Lâm Đồng", "Bình Thuận", "Long An"
]

# CẬP NHẬT: Danh sách các quận/huyện/thành phố tương ứng với mỗi tỉnh
DISTRICTS_BY_PROVINCE = {
    "TP. Hồ Chí Minh": ["Quận 1", "Quận 3", "Quận Gò Vấp", "TP. Thủ Đức", "Huyện Củ Chi", "Huyện Bình Chánh"],
    "Đồng Nai": ["TP. Biên Hòa", "TP. Long Khánh", "Huyện Long Thành", "Huyện Nhơn Trạch", "Huyện Trảng Bom"],
    "Bà Rịa - Vũng Tàu": ["TP. Vũng Tàu", "TP. Bà Rịa", "Thị xã Phú Mỹ", "Huyện Châu Đức", "Huyện Xuyên Mộc"],
    "Bình Dương": ["TP. Thủ Dầu Một", "TP. Dĩ An", "TP. Thuận An", "Thị xã Bến Cát", "Huyện Dầu Tiếng"],
    "Bình Phước": ["TP. Đồng Xoài", "Thị xã Phước Long", "Thị xã Bình Long", "Huyện Bù Đăng", "Huyện Chơn Thành"],
    "Tây Ninh": ["TP. Tây Ninh", "Thị xã Hòa Thành", "Thị xã Trảng Bàng", "Huyện Dương Minh Châu", "Huyện Gò Dầu"],
    "Lâm Đồng": ["TP. Đà Lạt", "TP. Bảo Lộc", "Huyện Đức Trọng", "Huyện Di Linh", "Huyện Lâm Hà"],
    "Bình Thuận": ["TP. Phan Thiết", "Thị xã La Gi", "Huyện Hàm Thuận Bắc", "Huyện Tuy Phong", "Huyện Bắc Bình"],
    "Long An": ["TP. Tân An", "Thị xã Kiến Tường", "Huyện Bến Lức", "Huyện Đức Hòa", "Huyện Cần Giuộc"]
}

# CẬP NHẬT: Danh sách tên đường phổ biến ở nhiều thành phố Việt Nam
STREET_NAMES = [
    "Trần Hưng Đạo", "Lê Lợi", "Nguyễn Huệ", "Phan Bội Châu", "Lý Thường Kiệt",
    "Quang Trung", "Hùng Vương", "Cách Mạng Tháng Tám", "30/4", "Điện Biên Phủ",
    "Võ Thị Sáu", "Phạm Văn Đồng", "Nguyễn Trãi", "Lê Duẩn", "Trần Phú"
]

# CẬP NHẬT: Tọa độ bao phủ toàn bộ khu vực Quân khu 7
LATITUDE_RANGE = (10.20, 12.40)
LONGITUDE_RANGE = (105.50, 108.85)


def generate_random_address():
    """Tạo ra một chuỗi địa chỉ ngẫu nhiên, đa dạng trong Quân khu 7."""
    # THAY ĐỔI: Logic tạo địa chỉ
    province = random.choice(PROVINCES_IN_QK7)
    district = random.choice(DISTRICTS_BY_PROVINCE[province])
    street = random.choice(STREET_NAMES)
    house_number = random.randint(1, 1500)

    # 30% địa chỉ sẽ có hẻm (sẹc)
    if random.random() < 0.3:
        return f"{house_number}/{random.randint(1, 50)} {street}, {district}, {province}"
    return f"{house_number} {street}, {district}, {province}"


def generate_depots_data(num_depots):
    """Tạo dữ liệu cho các kho."""
    depots_list = []
    print(f"Đang tạo {num_depots} depots...")
    for i in range(num_depots):
        depot_id = i + 1
        depot = {
            "id": f"{depot_id:03d}",  # Tăng lên 3 chữ số cho nhất quán
            "name": f"Kho Trung tâm - {depot_id:03d}",
            "address": generate_random_address(),
            "latitude": round(random.uniform(*LATITUDE_RANGE), 6),
            "longitude": round(random.uniform(*LONGITUDE_RANGE), 6)
        }
        depots_list.append(depot)
    print("-> Tạo depots thành công!")
    return depots_list


def generate_drivers_data(num_drivers):
    """Tạo dữ liệu cho các tài xế."""
    drivers_list = []
    print(f"Đang tạo {num_drivers} drivers...")

    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ"]
    middle_names = ["Văn", "Thị", "Minh", "Thuỳ", "Bảo", "Gia", "Đức", "Ngọc", "Thanh", "Mạnh"]
    last_names = ["An", "Bình", "Cường", "Dung", "Hải", "Linh", "Minh", "Nga", "Phương", "Quân"]

    for i in range(num_drivers):
        driver_id = i + 1
        # Cứ 2 tài xế chung 1 kho, đảm bảo depot_id không vượt quá số lượng kho
        depot_id = (i // 2 % NUM_DEPOTS) + 1
        driver = {
            "id": f"{driver_id:04d}",  # Tăng lên 4 chữ số
            "name": f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}",
            "phone": f"09{random.randint(10000000, 99999999)}",
            "depot_id": f"{depot_id:03d}"
        }
        drivers_list.append(driver)
    print("-> Tạo drivers thành công!")
    return drivers_list


def generate_customers_data(num_customers):
    """Tạo dữ liệu cho các khách hàng."""
    customers_list = []
    print(f"Đang tạo {num_customers} customers...")

    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ"]
    middle_names = ["Văn", "Thị", "Minh", "Thuỳ", "Bảo", "Gia", "Đức", "Ngọc", "Thanh", "Mạnh"]
    last_names = ["An", "Bình", "Cường", "Dung", "Hải", "Linh", "Minh", "Nga", "Phương", "Quân"]

    for i in range(num_customers):
        customer = {
            "id": f"C{i + 1:04d}",
            "name": f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}",
            "address": generate_random_address(),
            "phone": f"09{random.randint(10000000, 99999999)}",
            "latitude": round(random.uniform(*LATITUDE_RANGE), 6),
            "longitude": round(random.uniform(*LONGITUDE_RANGE), 6),
        }
        customers_list.append(customer)
    print("-> Tạo customers thành công!")
    return customers_list


def save_to_json(data, filename):
    """Lưu dữ liệu vào file JSON trong thư mục đầu ra."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Đã tạo thư mục: {OUTPUT_DIR}")

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu thành công dữ liệu vào file: {filepath}\n")


# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    # Tạo và lưu file depots
    depots_data = generate_depots_data(NUM_DEPOTS)
    save_to_json(depots_data, "depots.json")

    # Tạo và lưu file drivers
    drivers_data = generate_drivers_data(NUM_DRIVERS)
    save_to_json(drivers_data, "drivers.json")

    # Tạo và lưu file customers
    customers_data = generate_customers_data(NUM_CUSTOMERS)
    save_to_json(customers_data, "customers.json")

    print("Hoàn tất! Đã tạo thành công 3 file JSON với dữ liệu trong phạm vi Quân khu 7.")