from simhash import Simhash
import csv

# Đọc dữ liệu whitelist từ file CSV
whitelist = set()
with open('top-1m.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        url = row[0]  # Giả sử URL được lưu ở cột đầu tiên
        # Tính toán Simhash cho URL và thêm vào whitelist
        simhash = Simhash(url)
        whitelist.add(simhash.value)

# Kiểm tra độ tương đồng giữa một URL mới và whitelist
new_url = "https://www.facebook.com"
new_simhash = Simhash(new_url)
if new_simhash.value in whitelist:
    print("URL này nằm trong whitelist!")
else:
    print("URL này không nằm trong whitelist.")
    
    
