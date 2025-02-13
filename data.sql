drop database database;
create database scl;
use scl;


INSERT INTO app1_timeslottemplate VALUES
('TMP01', 'Monday', '05:00-17:00', 60, 70, 60, 'available'),
('TMP02', 'Monday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP03', 'Monday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP04', 'Tuesday', '05:00-17:00', 60, 70, 60, 'available'),
('TMP05', 'Tuesday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP06', 'Tuesday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP07', 'Wednesday', '05:00-17:00', 60, 70, 60, 'available'),
('TMP08', 'Wednesday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP09', 'Wednesday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP10', 'Thursday', '05:00-17:00', 60, 70, 60, 'available'),
('TMP11', 'Thursday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP12', 'Thursday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP13', 'Friday', '05:00-17:00', 60, 70, 60, 'available'),
('TMP14', 'Friday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP15', 'Friday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP16', 'Saturday', '05:00-17:00', 90, 100, 90, 'available'),
('TMP17', 'Saturday', '17:00-22:00', 110, 120, 110, 'available'),
('TMP18', 'Saturday', '22:00-24:00', 60, 60, 60, 'available'),
('TMP19', 'Sunday', '05:00-17:00', 100, 100, 100, 'available'),
('TMP20', 'Sunday', '17:00-22:00', 100, 100, 100, 'available'),
('TMP21', 'Sunday', '22:00-24:00', 120, 120, 120, 'available');


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
INSERT INTO app1_revenuereport (revenueReport_id, total_revenue, generated_at, badminton_hall_id) VALUES
('R0001', 500000000.00, '2024-01-01 10:00:00.000000', 'H0001'),
('R0002', 550000000.00, '2024-02-01 10:00:00.000000', 'H0001'),
('R0003', 600000000.00, '2024-03-01 10:00:00.000000', 'H0002'),
('R0004', 580000000.00, '2024-04-01 10:00:00.000000', 'H0002'),
('R0005', 620000000.00, '2024-05-01 10:00:00.000000', 'H0001'),
('R0006', 700000000.00, '2024-06-01 10:00:00.000000', 'H0003'),
('R0007', 720000000.00, '2024-07-01 10:00:00.000000', 'H0003'),
('R0008', 750000000.00, '2024-08-01 10:00:00.000000', 'H0002');
INSERT INTO app1_revenuereport_payments (revenuereport_id, payment_id) VALUES
('R0001', 'P0001'),
('R0001', 'P0002'),
('R0002', 'P0003'),
('R0002', 'P0004'),
('R0003', 'P0005'),
('R0003', 'P0006'),
('R0004', 'P0007'),
('R0004', 'P0008'),
('R0005', 'P0009'),
('R0005', 'P0010');
INSERT INTO app1_payment (payment_id, amount, payment_date, status, booking_id_id, customer_id_id, payment_account_id) VALUES
('P0001', 500000.00, '2024-01-01 08:30:00.000000', 1, 'B0001', 'C0001', 1001),
('P0002', 300000.00, '2024-01-02 10:15:00.000000', 1, 'B0002', 'C0002', 1002),
('P0003', 450000.00, '2024-02-05 14:45:00.000000', 1, 'B0003', 'C0003', 1003),
('P0004', 600000.00, '2024-02-10 09:20:00.000000', 1, 'B0004', 'C0004', 1004),
('P0005', 350000.00, '2024-03-03 16:00:00.000000', 0, 'B0005', 'C0005', 1005),
('P0006', 700000.00, '2024-03-15 11:10:00.000000', 1, 'B0006', 'C0006', 1006),
('P0007', 250000.00, '2024-04-01 17:30:00.000000', 0, 'B0007', 'C0007', 1007),
('P0008', 800000.00, '2024-04-10 13:50:00.000000', 1, 'B0008', 'C0008', 1008),
('P0009', 400000.00, '2024-05-05 15:40:00.000000', 1, 'B0009', 'C0009', 1009),
('P0010', 900000.00, '2024-05-20 12:25:00.000000', 1, 'B0010', 'C0010', 1010);

