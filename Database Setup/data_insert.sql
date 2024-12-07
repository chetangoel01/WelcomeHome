use donationdb;

-- Clear existing data
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE Delivered;
TRUNCATE TABLE ItemIn;
TRUNCATE TABLE Ordered;
TRUNCATE TABLE Piece;
TRUNCATE TABLE DonatedBy;
TRUNCATE TABLE Item;
TRUNCATE TABLE Location;
TRUNCATE TABLE Act;
TRUNCATE TABLE Role;
TRUNCATE TABLE PersonPhone;
TRUNCATE TABLE Person;
TRUNCATE TABLE Category;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert dummy data

-- Category
INSERT INTO Category VALUES 
('Electronics', 'Phones', 'Smartphones and Mobile Devices'),
('Electronics', 'Laptops', 'Portable Computers'),
('Kitchen', 'Pots', 'Cooking Pots'),
('Outdoor', 'Grills', 'Barbecue Grills'),
('Furniture', 'Chairs', 'Seating Solutions'),
('Furniture', 'Tables', 'Dining Tables'),
('Books', 'Novels', 'Fictional Books'),
('Books', 'Textbooks', 'Educational Books');

-- Item
INSERT INTO Item VALUES 
(20001, 'iPhone 14', 'iphone.png', 'Black', TRUE, FALSE, 'Metal', 'Electronics', 'Phones'),
(20002, 'MacBook Pro', 'macbook.png', 'Silver', TRUE, FALSE, 'Aluminum', 'Electronics', 'Laptops'),
(30001, 'Cooking Pot', 'pot.png', 'Grey', FALSE, FALSE, 'Stainless Steel', 'Kitchen', 'Pots'),
(40001, 'Charcoal Grill', 'grill.png', 'Black', TRUE, FALSE, 'Steel', 'Outdoor', 'Grills'),
(50001, 'Dining Chair', 'chair.png', 'Brown', TRUE, TRUE, 'Wood', 'Furniture', 'Chairs'),
(50002, 'Dining Table', 'table.png', 'White', TRUE, FALSE, 'Wood', 'Furniture', 'Tables'),
(60001, 'War and Peace', 'warpeace.png', 'Blue', TRUE, FALSE, 'Paper', 'Books', 'Novels'),
(60002, 'Calculus Textbook', 'calculus.png', 'Green', TRUE, FALSE, 'Paper', 'Books', 'Textbooks');

-- Person
INSERT INTO Person VALUES 
('johndoe', 'password123', 'John', 'Doe', 'john.doe@example.com'),
('janedoe', 'securepass', 'Jane', 'Doe', 'jane.doe@example.com'),
('michaelb', 'mypass', 'Michael', 'Brown', 'michael.brown@example.com'),
('sarahc', 'sarah123', 'Sarah', 'Connor', 'sarah.connor@example.com'),
('alicew', 'alicepass', 'Alice', 'Walker', 'alice.walker@example.com'),
('robertp', 'robertpass', 'Robert', 'Pattinson', 'robert.pattinson@example.com');

-- PersonPhone
INSERT INTO PersonPhone VALUES 
('johndoe', '1234567890'),
('janedoe', '9876543210'),
('michaelb', '5551234567'),
('sarahc', '4445556666'),
('alicew', '3334445555'),
('robertp', '1112223333');

-- Role
INSERT INTO Role VALUES 
('1', 'Client'),
('2', 'Staff'),
('3', 'Volunteer'),
('4', 'Donor');

-- Act
INSERT INTO Act VALUES 
('johndoe', '1'),
('janedoe', '2'),
('michaelb', '3'),
('sarahc', '4'),
('alicew', '1'),
('robertp', '2');

-- Location
INSERT INTO Location VALUES 
(1, 1, 'Electronics Shelf', 'Shelf for storing electronic items'),
(2, 1, 'Kitchen Shelf', 'Shelf for kitchen utensils and cookware'),
(3, 1, 'Outdoor Shelf', 'Shelf for outdoor equipment'),
(4, 1, 'Furniture Section', 'Area for storing furniture'),
(5, 1, 'Books Section', 'Area for storing books');

-- Piece
INSERT INTO Piece VALUES 
(20001, 1, 'iPhone Body', 150, 75, 7, 1, 1, 'Main body of the iPhone'),
(30001, 1, 'Pot Body', 300, 200, 150, 2, 1, 'Main cooking pot'),
(50001, 1, 'Chair Frame', 600, 500, 700, 4, 1, 'Frame of the dining chair'),
(50002, 1, 'Table Top', 1200, 800, 50, 4, 1, 'Top surface of the dining table'),
(60001, 1, 'Book Cover', 20, 30, 5, 5, 1, 'Cover of the book'),
(60002, 1, 'Book Spine', 20, 5, 50, 5, 1, 'Spine of the textbook');

-- DonatedBy
INSERT INTO DonatedBy VALUES 
(20001, 'johndoe', '2024-11-10'),
(30001, 'janedoe', '2024-11-12'),
(50001, 'michaelb', '2024-11-15'),
(60001, 'alicew', '2024-11-16');

-- Ordered
INSERT INTO Ordered VALUES 
(70001, '2024-11-18', 'John ordered a phone', 'janedoe', 'johndoe'),
(70002, '2024-11-19', 'Michael ordered a pot', 'sarahc', 'michaelb'),
(70003, '2024-11-20', 'Alice ordered a book', 'robertp', 'alicew');

-- ItemIn
INSERT INTO ItemIn VALUES 
(20001, 70001, TRUE),
(30001, 70002, FALSE),
(60001, 70003, TRUE);

-- Delivered
INSERT INTO Delivered VALUES 
('michaelb', 70001, 'DELIVERED', '2024-11-20'),
('michaelb', 70002, 'PENDING', '2024-11-21'),
('michaelb', 70003, 'DELIVERED', '2024-11-22');
