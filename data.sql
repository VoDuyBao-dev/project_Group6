drop database tmp;
create database tmp;
use tmp;

INSERT INTO auth_group value
(4, "Customer"),
(1, "Admin"),
(3, "Manager"),
(2, "Court_staff");

# Sau khi chạy xong lệnh này trong terminal shell thì sẽ tự động tạo được người dùng và tạo nhóm
python manage.py shell

from django.contrib.auth.models import User

# Danh sách người dùng cần tạo
users_data = [
    {'username': 'customer1', 'password': 'p1', 'email': 'customer1@example.com', 'first_name': 'c1', 'last_name': 'One', 'is_staff': False, 'is_superuser': False},
    {'username': 'customer2', 'password': 'p2', 'email': 'customer2@example.com', 'first_name': 'c2', 'last_name': 'Two', 'is_staff': False, 'is_superuser': False},
    {'username': 'manager1', 'password': 'p3', 'email': 'manager1@example.com', 'first_name': 'm1', 'last_name': 'One', 'is_staff': False, 'is_superuser': False},
    {'username': 'manager2', 'password': 'p4', 'email': 'manager2@example.com', 'first_name': 'm2', 'last_name': 'Two', 'is_staff': False, 'is_superuser': False},
    {'username': 'admin1', 'password': 'p5', 'email': 'admin1@example.com', 'first_name': 'Admin', 'last_name': 'One', 'is_staff': True, 'is_superuser': True},
    {'username': 'staff1', 'password': 'p6', 'email': 'staff1@example.com', 'first_name': 's1', 'last_name': 'One', 'is_staff': False, 'is_superuser': False},
    {'username': 'staff2', 'password': 'p7', 'email': 'staff2@example.com', 'first_name': 's2', 'last_name': 'Two', 'is_staff': False, 'is_superuser': False},
]

# Tạo người dùng trong Django
for user_data in users_data:
    user = User.objects.create_user(
        username=user_data['username'],
        password=user_data['password'],  # Mật khẩu sẽ được mã hóa tự động
        email=user_data['email'],
        first_name=user_data['first_name'],
        last_name=user_data['last_name'],
		is_staff = user_data['is_staff'],
		is_superuser = user_data['is_superuser'],
    )

print("Người dùng đã được tạo thành công!")



-- Insert data into app1_paymentaccount
INSERT INTO app1_paymentaccount (id, accountHolder, accountNumber, paymentMethod, created_at, updated_at) VALUES
('1', 'Nguyen Van A', '123456789', 'bank', NOW(), NOW()),
('2', 'Tran Thi B', '987654321', 'momo', NOW(), NOW());

-- Insert data into app1_customer
INSERT INTO app1_customer (customer_id, user_id) VALUES
('CUS01', 1),
('CUS02', 2);

-- Insert data into app1_courtmanager
INSERT INTO app1_courtmanager (courtManager_id, user_id, payment_account_id) VALUES
('CM001', 3, 1),
('CM002', 4, 2);

-- Insert data into app1_systemadmin
INSERT INTO app1_systemadmin (systemAdmin_id, user_id) VALUES
('SA001', 5);


-- Nếu bảng này có đã có dữ liệu thì xóa đi rồi chạy 
INSERT INTO auth_user_groups (id, user_id, group_id) VALUES
(1, 1, 4),
(2, 2, 4),
(3, 3, 3),
(4, 4, 3),
(5, 5, 1),
(6, 6, 2),
(7, 7, 2);

INSERT INTO app1_badmintonhall (badminton_hall_id, name, address) VALUES
('H0001', 'Sunshine Badminton Hall', '123 Main Street, Hanoi'),
('H0002', 'Galaxy Badminton Hall', '456 Nguyen Trai, Ho Chi Minh City');

INSERT INTO app1_court (court_id, badminton_hall_id, name, image, status) VALUES
('C0001', 'H0001', 'Court A1', NULL, 'empty'),
('C0002', 'H0001', 'Court A2', NULL, 'booked'),
('C0003', 'H0001', 'Court A3', NULL, 'under_maintenance'),
('C0004', 'H0002', 'Court B1', NULL, 'empty'),
('C0005', 'H0002', 'Court B2', NULL, 'booked'),
('C0006', 'H0002', 'Court B3', NULL, 'under_maintenance');

-- Insert data into app1_courtstaff
INSERT INTO app1_courtstaff (court_staff_id, user_id, court_id) VALUES
('CS001', 6, 'C0001'),
('CS002', 6, 'C0002'),
('CS003', 6, 'C0003'),
('CS004', 7, 'C0004'),
('CS005', 7, 'C0005'),
('CS006', 7, 'C0006');

INSERT INTO app1_timeslottemplate VALUES
('TMP01', 'Monday', '05h - 17h', 60, 70, 60, 'available'),
('TMP02', 'Monday', '17h - 22h',110, 120, 110, 'available'),
('TMP03', 'Monday', '22h - 24h', 60, 60, 60, 'available'),
('TMP04', 'Tuesday', '05h - 17h', 60, 70, 60, 'available'),
('TMP05', 'Tuesday', '17h - 22h', 110, 120, 110, 'available'),
('TMP06', 'Tuesday', '22h - 24h', 60, 60, 60, 'available'),
('TMP07', 'Wednesday', '05h - 17h', 60, 70, 60, 'available'),
('TMP08', 'Wednesday', '17h - 22h', 110, 120, 110, 'available'),
('TMP09', 'Wednesday', '22h - 24h', 60, 60, 60, 'available'),
('TMP10', 'Thursday', '05h - 17h', 60, 70, 60, 'available'),
('TMP11', 'Thursday', '17h - 22h', 110, 120, 110, 'available'),
('TMP12', 'Thursday', '22h - 24h', 60, 60, 60, 'available'),
('TMP13', 'Friday', '05h - 17h', 60, 70, 60, 'available'),
('TMP14', 'Friday', '17h - 22h', 110, 120, 110, 'available'),
('TMP15', 'Friday', '22h - 24h', 60, 60, 60, 'available'),
('TMP16', 'Saturday', '05h - 17h', 90, 100, 90, 'available'),
('TMP17', 'Saturday', '17h - 22h', 110, 120, 110, 'available'),
('TMP18', 'Saturday', '22h - 24h', 60, 60, 60, 'available'),
('TMP19', 'Sunday', '05h - 17h', 100, 100, 100, 'available'),
('TMP20', 'Sunday', '17h - 22h', 100, 100, 100, 'available'),
('TMP21', 'Sunday', '22h - 24h', 120, 120, 120, 'available');

-- Insert data into app1_booking
INSERT INTO app1_booking (booking_id, customer_id, court_id, booking_type, date, start_time, end_time, status, amount) VALUES
('B0001', '1', 'C0001', 'fixed', '2025-02-14', '08:00', '10:00', TRUE, 120.00),
('B0002', '1', 'C0002', 'daily', '2025-02-15', '18:00', '20:00', FALSE, 150.00);

-- Insert data into app1_payment
INSERT INTO app1_payment (payment_id, booking_id, payment_account_id, payment_date, status) VALUES
('P0001', 'B0001', '1', NOW(), TRUE),
('P0002', 'B0002', '2', NOW(), FALSE);


-- Insert data into app1_booking
INSERT INTO app1_booking (booking_id, customer_id, court_id, booking_type, date, start_time, end_time, status, amount) VALUES
('B0003', '1', 'C0003', 'flexible', '2025-02-16', '09:00:00', '11:00:00', TRUE, 130.00),
('B0004', '2', 'C0004', 'fixed', '2025-02-17', '07:00:00', '09:00:00', TRUE, 140.00),
('B0005', '3', 'C0005', 'daily', '2025-02-18', '16:00:00', '18:00:00', FALSE, 110.00),
('B0006', '3', 'C0006', 'flexible', '2025-02-19', '10:00:00', '12:00:00', TRUE, 125.00),
('B0007', '4', 'C0003', 'fixed', '2025-02-20', '12:00:00', '14:00:00', TRUE, 135.00),
('B0008', '2', 'C0004', 'daily', '2025-02-21', '14:00:00', '16:00:00', FALSE, 145.00),
('B0009', '1', 'C0001', 'flexible', '2025-02-22', '11:00:00', '13:00:00', TRUE, 150.00),
('B0010', '1', 'C0002', 'fixed', '2025-02-23', '08:00:00', '10:00:00', TRUE, 115.00),
('B0011', '1', 'C0003', 'daily', '2025-02-24', '17:00:00', '19:00:00', FALSE, 160.00),
('B0012', '2', 'C0005', 'flexible', '2025-02-25', '13:00:00', '15:00:00', TRUE, 155.00),
('B0013', '4', 'C0002', 'fixed', '2025-02-26', '09:00:00', '11:00:00', TRUE, 125.00),
('B0014', '2', 'C0004', 'daily', '2025-02-27', '15:00:00', '17:00:00', FALSE, 135.00),
('B0015', '4', 'C0003', 'flexible', '2025-02-28', '10:00:00', '12:00:00', TRUE, 140.00);

-- Insert data into app1_payment
INSERT INTO app1_payment (payment_id, booking_id, payment_account_id, payment_date, status) VALUES
('P0003', 'B0003', '1', NOW(), TRUE),
('P0004', 'B0004', '2', NOW(), TRUE),
('P0005', 'B0005', '2', NOW(), FALSE),
('P0006', 'B0006', '2', NOW(), TRUE),
('P0007', 'B0007', '1', NOW(), TRUE),
('P0008', 'B0008', '2', NOW(), FALSE),
('P0009', 'B0009', '1', NOW(), TRUE),
('P0010', 'B0010', '1', NOW(), TRUE),
('P0011', 'B0011', '1', NOW(), FALSE),
('P0012', 'B0012', '2', NOW(), TRUE),
('P0013', 'B0013', '1', NOW(), TRUE),
('P0014', 'B0014', '2', NOW(), FALSE),
('P0015', 'B0015', '1', NOW(), TRUE);

-- Insert data into app1_revenuereport
INSERT INTO app1_revenuereport (revenueReport_id, badminton_hall_id, total_revenue, generated_at) VALUES
('RR001', 'H0001', 270.00, NOW()),
('RR002', 'H0002', 150.00, NOW());












