-- Clear Existing Data
SET FOREIGN_KEY_CHECKS = 0;

DELETE FROM Delivered;
DELETE FROM ItemIn;
DELETE FROM Ordered;
DELETE FROM Piece;
DELETE FROM DonatedBy;
DELETE FROM Item;
DELETE FROM Location;
DELETE FROM Act;
DELETE FROM Role;
DELETE FROM PersonPhone;
DELETE FROM Person;
DELETE FROM Category;

SET FOREIGN_KEY_CHECKS = 1;


-- Insert into Category
INSERT INTO Category (mainCategory, subCategory, catNotes)
VALUES
('Furniture', 'Chair', 'Seating furniture for all purposes'),
('Furniture', 'Table', 'Various types of tables'),
('Electronics', 'Laptop', 'Electronic devices used for computing'),
('Electronics', 'Phone', 'Handheld communication devices');

-- Insert into Person
INSERT INTO Person (userName, password, fname, lname, email)
VALUES
('ian', 'password', 'Ian', 'Davoren', 'ian@nyu.edu'),
('jdoe', 'password123', 'John', 'Doe', 'jdoe@example.com'),
('asmith', 'securepass', 'Alice', 'Smith', 'asmith@example.com'),
('bwayne', 'batman123', 'Bruce', 'Wayne', 'bwayne@example.com'),
('ckent', 'superman321', 'Clark', 'Kent', 'ckent@example.com');

-- Insert into PersonPhone
INSERT INTO PersonPhone (userName, phone)
VALUES
('jdoe', '1234567890'),
('asmith', '5556667777'),
('bwayne', '9998887777'),
('ckent', '3332221111');

-- Insert into Role
INSERT INTO Role (roleID, rDescription)
VALUES
('Staff', 'Full-time or part-time staff member'),
('Volunteer', 'Volunteer worker'),
('Client', 'Individual receiving services'),
('Donor', 'Individual donating items');

-- Insert into Act
INSERT INTO Act (userName, roleID)
VALUES
('ian', 'Staff'),
('jdoe', 'Staff'),
('asmith', 'Volunteer'),
('bwayne', 'Client'),
('ckent', 'Donor');

-- Insert into Location
INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES
(101, 1, 'A', 'Shelf A in Room 101'),
(101, 2, 'B', 'Shelf B in Room 101'),
(102, 1, 'A', 'Shelf A in Room 102'),
(102, 2, 'B', 'Shelf B in Room 102');

-- Insert into Item
INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)
VALUES
('Office Chair', 'chair.jpg', 'Black', TRUE, TRUE, 'Metal', 'Furniture', 'Chair'),
('Dining Table', 'table.jpg', 'Brown', TRUE, TRUE, 'Wood', 'Furniture', 'Table'),
('Gaming Laptop', 'laptop.jpg', 'Silver', TRUE, TRUE, 'Plastic', 'Electronics', 'Laptop'),
('Smartphone', 'phone.jpg', 'Gray', TRUE, TRUE, 'Glass', 'Electronics', 'Phone');

-- Insert into DonatedBy
INSERT INTO DonatedBy (ItemID, userName, donateDate)
VALUES
(1, 'ckent', '2023-01-15'),
(2, 'ckent', '2023-02-20'),
(3, 'ckent', '2023-03-10'),
(4, 'ckent', '2023-04-05');

-- Insert into Piece
INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
VALUES
-- Office Chair (1 piece)
(1, 1, 'Office Chair', 50, 50, 100, 101, 1, 'Ergonomic office chair'),

-- Dining Table (multiple pieces)
(2, 1, 'Tabletop', 120, 60, 5, 101, 2, 'Main tabletop'),
(2, 2, 'Leg 1', 10, 10, 70, 101, 2, 'Table leg'),
(2, 3, 'Leg 2', 10, 10, 70, 101, 2, 'Table leg'),
(2, 4, 'Leg 3', 10, 10, 70, 101, 2, 'Table leg'),
(2, 5, 'Leg 4', 10, 10, 70, 101, 2, 'Table leg'),

-- Gaming Laptop (1 piece)
(3, 1, 'Laptop', 35, 25, 2, 102, 1, 'Gaming laptop with RGB keyboard'),

-- Smartphone (1 piece)
(4, 1, 'Smartphone', 15, 7, 1, 102, 2, 'High-end smartphone');

-- Insert into Ordered
INSERT INTO Ordered (orderID, orderDate, orderNotes, supervisor, client)
VALUES
(1, '2023-05-01', 'Standard delivery', 'jdoe', 'bwayne');

-- Insert into ItemIn
INSERT INTO ItemIn (ItemID, orderID, found)
VALUES
(1, 1, TRUE);

-- Insert into Delivered
INSERT INTO Delivered (userName, orderID, status, date)
VALUES
('asmith', 1, 'Delivered', '2023-05-03');
