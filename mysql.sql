CREATE TABLE Equipment (
    equipment_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    threshold INT NOT NULL,
    condition1 VARCHAR(50) NOT NULL,
    status VARCHAR(50),
    last_serviced_date DATE
);

CREATE TABLE user1 (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('member', 'manager') NOT NULL
);


-- Table: Orders
CREATE TABLE Orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    order_type ENUM('New Order', 'Usage Request') NOT NULL,
    quantity_ordered INT NOT NULL,
    order_date DATE NOT NULL,
    requested_by INT NOT NULL,
    status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
    approval_date DATE,
    dealer_id INT,
    room_requested VARCHAR(255),
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id),
    FOREIGN KEY (dealer_id) REFERENCES Dealers(dealer_id)
);

-- Table: Service
CREATE TABLE Service (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    equipment_id INT,
    service_date DATE NOT NULL,
    issue_description TEXT,
    status ENUM('Pending', 'In Progress', 'Completed') DEFAULT 'Pending',
    technician_assigned VARCHAR(255),
    completion_date DATE,
    FOREIGN KEY (equipment_id) REFERENCES Equipment(equipment_id)
);

-- Table: Dealers
CREATE TABLE Dealers (
    dealer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    contact_info VARCHAR(255),
    address TEXT,
    equipment_types TEXT

);

-- Table: Management_Team
CREATE TABLE Management_Team (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    role ENUM('Hospital Member', 'Manager') NOT NULL,
    contact_info VARCHAR(255),
    last_login DATETIME,
    actions_taken TEXT
);

USE hospital_inventory;

INSERT INTO Equipment (name, quantity, threshold, condition1, status, last_serviced_date) 
VALUES 
('Heart Monitor', 10, 2, 'Good', 'Operational', '2024-10-10'),
('Ultrasound Machine', 3, 1, 'Fair', 'In Service', '2024-09-20'),
('ECG Machine', 5, 1, 'Excellent', 'Operational', '2024-08-15'),
('X-Ray Machine', 2, 1, 'Poor', 'Needs Repair', '2024-07-30'),
('Defibrillator', 8, 3, 'Good', 'Operational', '2024-10-01'),
('Ventilator', 4, 2, 'Fair', 'Operational', '2024-09-25'),
('Blood Pressure Monitor', 15, 5, 'Good', 'Operational', '2024-10-05'),
('Surgical Light', 6, 2, 'Excellent', 'Operational', '2024-09-10'),
('Infusion Pump', 7, 3, 'Good', 'Operational', '2024-10-12'),
('Oxygen Concentrator', 5, 2, 'Fair', 'Operational', '2024-09-22');


INSERT INTO Dealers (dealer_id, name, contact_info, address) VALUES 
(1, 'Medical Supply Co.', '123-456-7890', '123 Medical St, City, State, 12345'),
(2, 'Healthcare Solutions', '234-567-8901', '456 Healthcare Ave, City, State, 23456'),
(3, 'Global Medical Supplies', '345-678-9012', '789 Global Rd, City, State, 34567'),
(4, 'Innovative Health Supplies', '456-789-0123', '321 Innovative Blvd, City, State, 45678'),
(5, 'Vital Equipment Providers', '567-890-1234', '654 Vital Way, City, State, 56789');

INSERT INTO Service (equipment_id, service_date, issue_description, status, technician_assigned, completion_date) 
VALUES 
(1, '2024-10-15', 'Routine maintenance', 'Completed', 'John Doe', '2024-10-16'),
(2, '2024-10-20', 'Repair broken display', 'In Progress', 'Jane Smith', NULL),
(3, '2024-10-25', 'Battery replacement', 'Pending', 'Mike Johnson', NULL),
(4, '2024-10-28', 'Calibration issue', 'Completed', 'Emily Davis', '2024-10-29'),
(5, '2024-11-01', 'Software update required', 'Pending', NULL, NULL);


INSERT INTO user1 (name, password, role) VALUES ('John Doe', 'password123', 'member');
INSERT INTO user1 (name, password, role) VALUES ('Jane Smith', 'mypassword', 'manager');
INSERT INTO Users (name, password, role) VALUES ('Alice Johnson', 'alicepass', 'member');

ALTER TABLE Orders 
ADD COLUMN approval_status ENUM('Pending', 'Approved', 'Rejected') DEFAULT 'Pending',
ADD COLUMN description TEXT;

use hospital_inventory;

SELECT * FROM orders;


SELECT * FROM user1;

INSERT INTO Equipment (name, quantity, threshold, condition1, status, last_serviced_date) 
VALUES 
('pulse', 1, 2, 'Good', 'Operational', '2024-10-10');

update equipment set quantity = 5 where equipment_id = 1;

