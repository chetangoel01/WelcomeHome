use donationdb;

-- Clear existing data
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
(20001, 'iPhone 14', 'iphone.png', 'Black', TRUE, TRUE, 'Metal', 'Electronics', 'Phones'),
(20002, 'MacBook Pro', 'macbook.png', 'Silver', TRUE, TRUE, 'Aluminum', 'Electronics', 'Laptops'),
(30001, 'Cooking Pot', 'pot.png', 'Grey', FALSE, TRUE, 'Stainless Steel', 'Kitchen', 'Pots'),
(40001, 'Charcoal Grill', 'grill.png', 'Black', TRUE, TRUE, 'Steel', 'Outdoor', 'Grills'),
(50001, 'Dining Chair', 'chair.png', 'Brown', FALSE, TRUE, 'Wood', 'Furniture', 'Chairs'),
(50002, 'Dining Table', 'table.png', 'White', TRUE, TRUE, 'Wood', 'Furniture', 'Tables'),
(60001, 'War and Peace', 'warpeace.png', 'Blue', FALSE, TRUE, 'Paper', 'Books', 'Novels'),
(60002, 'Calculus Textbook', 'calculus.png', 'Green', TRUE, TRUE, 'Paper', 'Books', 'Textbooks');

-- Person
INSERT INTO Person VALUES 
('johndoe', '993a1259776cbffdd84ebab034545d9da656ba588491193f8ce556cc4462e604', '729921fe612577672d19c876783e5ccb', 'John', 'Doe', 'john.doe@example.com'),
('janedoe', 'a845a2fbed12fe9458a845654ceb926d5a1d40af9e3115723a835358d8bcb105', '588925961c9f0ec683ca6a41d0224398', 'Jane', 'Doe', 'jane.doe@example.com'),
('michaelb', '6c12465ed98c39a176b36f67b2353428a4fc9445d0d1f7516e0c39ee972020e3','8661a9f90cc7c40c2072ee56e09a18fa',  'Michael', 'Brown', 'michael.brown@example.com'),
('sarahc', '8c0d9000274335d3e7d654a3772868d880ad548f879454656b8416e80d853dfe', '7feaeee42b710771bb3c6479444dcf4d', 'Sarah', 'Connor', 'sarah.connor@example.com'),
('alicew', '8360ed1c20455b69168c5da687ff4991ed1079c1e8dd961e9dfcb6e7e8f07886', '8462ea598d926563b53fe599c0e2bba2', 'Alice', 'Walker', 'alice.walker@example.com'),
('robertp', '9a3233f8c3111844f8da50e830fdf67b50b507d277ccc2218076e5098c6a2ac5', 'a8a3e39131d4bb54e92ccdefc9919290', 'Robert', 'Pattinson', 'robert.pattinson@example.com');

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
(20001, 1, 'iPhone Body', 150, 75, 7, 1, 1, 'iPhone'),
(20002, 1, 'MacBook Body', 1200, 800, 50, 1, 1, 'MacBook'),
(30001, 1, 'Pot Body', 300, 200, 150, 2, 1, 'Main cooking pot'),
(30001, 2, 'Pot Lid', 300, 200, 50, 2, 1, 'Lid of the cooking pot'),
(40001, 1, 'Grill Body', 600, 400, 300, 3, 1, 'Main body of the grill'),
(40001, 2, 'Grill Grate', 600, 400, 10, 3, 1, 'Grate of the grill'),
(50001, 1, 'Chair Frame', 600, 500, 700, 4, 1, 'Frame of the dining chair'),
(50001, 2, 'Chair Cushion', 600, 500, 50, 4, 1, 'Cushion of the dining chair'),
(50002, 1, 'Table Top', 1200, 800, 50, 4, 1, 'Top surface of the dining table'),
(50002, 2, 'Table Leg 1', 50, 50, 700, 4, 1, 'First leg of the dining table'),
(50002, 3, 'Table Leg 2', 50, 50, 700, 4, 1, 'Second leg of the dining table'),
(50002, 4, 'Table Leg 3', 50, 50, 700, 4, 1, 'Third leg of the dining table'),
(50002, 5, 'Table Leg 4', 50, 50, 700, 4, 1, 'Fourth leg of the dining table'),
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
