# DBs Project Part 3 Writeup

## Languages and Frameworks Used

- **Programming Language**: Python
- **Web Framework**: Flask (used to create application routes)
- **Frontend**: HTML (used for site pages)
- **Security**:
  - `Hashlib`: for user password hashing
  - `OS`: for salted password hashing (added security)
  - `re`: to prevent XSS and SQL injection
- **Database**:
  - `SQL`: for queries to mySQL database
  - `pyMySQL`: For Python integration of the database into the application

## Changes to the Schema

We added the attribute `salt` to the `Person` schema, which allowed us to create a random salt value for each person in the schema. This salt is appended to the password before it is hashed, increasing security by:

- Preventing attackers from reverse engineering plaintext passwords using a precomputed table of hash values for common passwords.
- Ensuring unique hashes for identical passwords.
- Making brute force attacks significantly harder.

We also removed the `auto_increment` from `orderID` in favor of a random orderID generator. This change made it easier to assign an orderID from the backend and enhanced security by preventing clients from guessing someone else's orderID. We retained `auto_increment` for `itemID` since there are no security issues with knowing other itemIDs (as any user can query any itemID).

## Additional Constraints, Triggers, Stored Procedures

- "Add to current order" can only be accessed after creating a new order (i.e., the current order). This leads to the "Add Order Items" page, where all added items are stored to that order.
- Once you exit this page and return to the homepage, you can no longer add items to the order, and you must start a new order as the old order is no longer current.

## Main Queries for Each Implemented Feature

### Login

```mySQL
SELECT password, salt
FROM person
WHERE username = "exampleUser";
```

### Registration

```SQL
SELECT userName
FROM Person
WHERE userName = "exampleNewUsername";
```
```Sql
INSERT INTO Person (userName, password, salt, fname, lname, email)
VALUES ("newUsername", "newHashedPassword", "newSalt", "newFName", "newLName", "newEmail");
```
```SQL
INSERT INTO Act (userName, roleID)
VALUES ("newUserName", "newRole");
```
### Find Single Item
```SQL
SELECT pieceNum, pDescription, roomNum, shelfNum, pNotes
FROM Piece
WHERE itemID = "exampleItemID";
```
### Find Order Items
```SQL
SELECT ItemIn.itemID, Piece.pieceNum, Piece.pDescription, Piece.roomNum, Piece.shelfNum, Piece.pNotes
FROM ItemIn
JOIN Piece ON ItemIn.itemID = Piece.itemID
WHERE ItemIn.orderID = "exampleOrderID";
```
### Accept Donation
```tsql
SELECT *
FROM Act
WHERE userName = "exampleUsername" AND roleID = roleIdAssociatedWithStaff;
```
```tsql
SELECT *
FROM Act
WHERE userName = "exampleUsername" AND roleID = roleIdAssociatedWithDonor;
```
```tsql
INSERT INTO Item (iDescription, photo, color, material, hasPieces, mainCategory, subCategory)
VALUES ("donationItemDescription", "donationPhoto", "donationColor", "donationMaterial", True, "donationMainCategory", "donationSubcategory");
```
```tsql
INSERT INTO DonatedBy (ItemID, userName, donateDate)
VALUES ("donationItemID", "donorUsername", CURDATE());
```
```tsql
INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
VALUES ("donatedItemID", "donatedPieceNum", "donatedPieceDescription", "donatedPieceLength", "donatedPieceWidth", "donatedPieceHeight", "donatedPieceRoomNum", "donatedPieceShelfNum", "donatedPieceLocationNotes");
```
### Start Order
```tsql
SELECT * 
FROM Act 
WHERE userName = “exampleUsername” AND roleID = “roleIdAssociatedWithStaff”
```
```tsql
SELECT *
FROM Act
WHERE userName = "exampleUsername" AND roleID = "roleIdAssociatedWithClient";
```
```tsql
SELECT orderID
FROM Ordered;
```
### User Tasks
```tsql
SELECT orderID, orderDate, orderNotes, supervisor, client
FROM Ordered
WHERE client = username;
```
```tsql
SELECT o.orderID, o.orderDate, o.orderNotes, o.supervisor, o.client
FROM Ordered o
WHERE o.supervisor = username;
```
```tsql
SELECT o.orderID, o.orderDate, d.status, d.date
FROM Delivered d
JOIN Ordered o ON d.orderID = o.orderID
WHERE d.userName = username;
```
Get Volunteer Ranking
```tsql
SELECT p.userName, p.fname, p.lname, COUNT(d.orderID) AS deliveries
FROM Person p
JOIN Act a ON p.userName = a.userName
JOIN Role r ON a.roleID = r.roleID
JOIN Delivered d ON p.userName = d.userName
WHERE r.rDescription = 'Volunteer'
AND d.date BETWEEN startDate AND endDate
GROUP BY p.userName
ORDER BY deliveries DESC;
```

### Update Order Status
```tsql
SELECT 1
FROM Delivered
WHERE orderID = orderID AND userName = username;
```
```tsql
SELECT 1
FROM Ordered
WHERE orderID = orderID AND supervisor = username;
```
```tsql
UPDATE Delivered
SET status = 'delivered'
WHERE orderID = 12345
AND (userName = username OR username IN (
    SELECT supervisor FROM Ordered WHERE orderID = orderID
));
```
### Add to Order
```tsql
SELECT DISTINCT mainCategory
FROM Category;
```
```tsql
SELECT DISTINCT subCategory
FROM Category
WHERE mainCategory = %s;
```
```tsql
SELECT *
FROM Item
WHERE itemID NOT IN (SELECT itemID FROM ItemIn)
AND mainCategory = %s
AND subCategory = %s;
```
```tsql
INSERT INTO Ordered VALUES (order_id, todays_Date, "new order created", staff_username, client_username);
```
```tsql
INSERT INTO ItemIn (orderID, ItemID)
VALUES (%s, %s);
```
```tsql
INSERT INTO ItemIn (orderID, ItemID)
VALUES (%s, %s);
```
```tsql
SELECT i.ItemID, i.iDescription, i.photo, i.color, i.isNew, i.hasPieces, i.material, i.mainCategory, i.subCategory
FROM ItemIn ii
JOIN Item i ON ii.ItemID = i.ItemID
WHERE ii.orderID = order_id;
```
### Year Report
```tsql
SELECT COUNT(client)
FROM Ordered
WHERE YEAR(orderDate) = current year;
```
```tsql
SELECT mainCategory, COUNT(ItemID)
FROM Item NATURAL JOIN DonatedBy
WHERE YEAR(donateDate) = currentYear
GROUP BY mainCategory;
```
```tsql
SELECT DISTINCT iDescription
FROM Item NATURAL JOIN ItemIn NATURAL JOIN Ordered
WHERE YEAR(orderDate) = currentYear;
```
## Difficulties Encountered and Lessons Learned
- Initial project setup was difficult 
- Flask was new to us, so we all learned how to use it
- Version control was difficult at times, and there were a few times where changes were lost (although recovered) since we were all working at the same time and making changes to the repository on top of each other. 

## Which Team Member Did What
- **Schema initialization script**: Chetan, Eli, Ian
- **Dummy data insert script**: Chetan, Eli, Ian
- **Home Page**: Chetan, Eli, Ian
- **Password hashing and salting**: Chetan
- **Login**: Chetan
- **Registration**: Chetan
- **Validate Input (protect against SQL injection and XSS)**: Eli
- **Find Single Item**: Eli
- **Find Order Items**: Eli
- **Accept Donation**: Eli
- **Start an Order**: Ian
- **Add to Order**: Ian
- **Year Report**: Ian
- **Rank System**: Chetan
- **Update enabled**: Chetan
- **Written report**: Eli, Ian