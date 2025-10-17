import json
import random
import os
import math

# --- CÁC THAM SỐ CẤU HÌNH ---
NUM_DEPOTS = 250
NUM_CUSTOMERS = 800
NUM_DRIVERS = 500
OUTPUT_DIR = "data"

# --- DỮ LIỆU ĐỂ TẠO ĐỊA CHỈ ĐA DẠNG ---
# Danh sách 10 phường của Quận 7
WARDS_IN_DISTRICT_7 = [
    "Tân Thuận Đông", "Tân Thuận Tây", "Tân Kiểng", "Tân Hưng",
    "Bình Thuận", "Tân Quy", "Phú Thuận", "Tân Phú", "Tân Phong", "Phú Mỹ"
]

# Danh sách các tên đường phổ biến ở Quận 7
STREET_NAMES = [
    "Nguyễn Thị Thập", "Huỳnh Tấn Phát", "Lê Văn Lương", "Nguyễn Hữu Thọ",
    "Trần Xuân Soạn", "Lâm Văn Bền", "Phạm Hữu Lầu", "Nguyễn Lương Bằng",
    "Tôn Dật Tiên", "Đào Trí", "Gò Ô Môi", "Mai Văn Vĩnh",
    "Đường số 1", "Đường số 15", "Đường số 41", "Đường số 65"
]

# Tọa độ khu vực Quận 7
LATITUDE_RANGE = (10.71, 10.76)
LONGITUDE_RANGE = (106.69, 106.76)


def generate_random_address():
    """Tạo ra một chuỗi địa chỉ ngẫu nhiên, đa dạng trong Quận 7."""
    street = random.choice(STREET_NAMES)
    ward = random.choice(WARDS_IN_DISTRICT_7)
    house_number = random.randint(1, 1500)
    # Thêm 'sẹc' (hẻm) để địa chỉ trông thật hơn
    if random.random() < 0.3:  # 30% địa chỉ sẽ có hẻm
        return f"{house_number}/{random.randint(1, 50)} {street}, P. {ward}, Quận 7, TP. HCM"
    return f"{house_number} {street}, P. {ward}, Quận 7, TP. HCM"


def generate_depots_data(num_depots):
    """Tạo dữ liệu cho 250 kho."""
    depots_list = []
    print(f"Đang tạo {num_depots} depots...")
    for i in range(num_depots):
        depot_id = i + 1
        depot = {
            "id": f"{depot_id:02d}",  # Định dạng ID có 2 chữ số: 01, 02...
            "name": f"Kho Quận 7 - {depot_id:02d}",
            "address": generate_random_address(),
            "latitude": round(random.uniform(*LATITUDE_RANGE), 6),
            "longitude": round(random.uniform(*LONGITUDE_RANGE), 6)
        }
        depots_list.append(depot)
    print("-> Tạo depots thành công!")
    return depots_list


def generate_drivers_data(num_drivers):
    """Tạo dữ liệu cho 500 tài xế."""
    drivers_list = []
    print(f"Đang tạo {num_drivers} drivers...")

    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ"]
    middle_names = ["Văn", "Thị", "Minh", "Thuỳ", "Bảo", "Gia", "Đức", "Ngọc", "Thanh", "Mạnh"]
    last_names = ["An", "Bình", "Cường", "Dung", "Hải", "Linh", "Minh", "Nga", "Phương", "Quân"]

    for i in range(num_drivers):
        driver_id = i + 1
        depot_id = math.floor(i / 2) + 1  # Cứ 2 tài xế chung 1 kho
        driver = {
            "id": f"{driver_id:03d}",  # Định dạng ID có 3 chữ số: 001, 002...
            "name": f"{random.choice(first_names)} {random.choice(middle_names)} {random.choice(last_names)}",
            "phone": f"09{random.randint(10000000, 99999999)}",
            "depot_id": f"{depot_id:02d}"
        }
        drivers_list.append(driver)
    print("-> Tạo drivers thành công!")
    return drivers_list


def generate_customers_data(num_customers):
    """Tạo dữ liệu cho 800 khách hàng với tên riêng và ID > 0."""
    customers_list = []
    print(f"Đang tạo {num_customers} customers...")

    # ✅ Thêm danh sách tên để tạo ngẫu nhiên
    first_names = ["Nguyễn", "Trần", "Lê", "Phạm", "Hoàng", "Huỳnh", "Võ", "Đặng", "Bùi", "Đỗ"]
    middle_names = ["Văn", "Thị", "Minh", "Thuỳ", "Bảo", "Gia", "Đức", "Ngọc", "Thanh", "Mạnh"]
    last_names = ["An", "Bình", "Cường", "Dung", "Hải", "Linh", "Minh", "Nga", "Phương", "Quân"]

    for i in range(num_customers):
        customer = {
            # ✅ Sửa ở đây: Dùng i + 1 để ID bắt đầu từ C0001
            "id": f"C{i + 1:04d}",
            # ✅ Sửa ở đây: Tạo tên riêng ngẫu nhiên
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
    """Lưu dữ liệu vào file JSON trong thư mục data."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Đã tạo thư mục: {OUTPUT_DIR}")

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Đã lưu thành công dữ liệu vào file: {filepath}\n")


# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    # Tạo và lưu file drivers
    drivers_data = generate_drivers_data(NUM_DRIVERS)
    save_to_json(drivers_data, "drivers.json")

    # Tạo và lưu file depots
    depots_data = generate_depots_data(NUM_DEPOTS)
    save_to_json(depots_data, "depots.json")

    # Tạo và lưu file customers
    customers_data = generate_customers_data(NUM_CUSTOMERS)
    save_to_json(customers_data, "customers.json")

    print("Hoàn tất! Đã tạo thành công 3 file JSON với dữ liệu đa dạng.")