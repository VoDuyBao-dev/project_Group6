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
