/*
Title: db.init.sql
Author: Kristin Bougrine
Date: February 24, 2023
Description: WhatABook database initialization script.
*/


-- create whatabook_user and grant them all privileges to the whatabook database 
CREATE USER 'whatabook_user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'MySQL8IsGreat!';

-- grant all privileges to the whatabook database to user whatabook_user on localhost 
GRANT ALL PRIVILEGES ON whatabook.* TO'whatabook_user'@'localhost';

/*
    Create tables
*/
CREATE TABLE store (
    store_id    INT             NOT NULL    AUTO_INCREMENT,
    locale      VARCHAR(500)    NOT NULL,
    PRIMARY KEY(store_id)
);

CREATE TABLE book (
    book_id     INT             NOT NULL    AUTO_INCREMENT,
    book_name   VARCHAR(200)    NOT NULL,
    author      VARCHAR(200)    NOT NULL,
    details     VARCHAR(500),
    PRIMARY KEY(book_id)
);

CREATE TABLE user (
    user_id         INT         NOT NULL    AUTO_INCREMENT,
    first_name      VARCHAR(75) NOT NULL,
    last_name       VARCHAR(75) NOT NULL,
    PRIMARY KEY(user_id) 
);

CREATE TABLE wishlist (
    wishlist_id     INT         NOT NULL    AUTO_INCREMENT,
    user_id         INT         NOT NULL,
    book_id         INT         NOT NULL,
    PRIMARY KEY (wishlist_id),
    CONSTRAINT fk_book
    FOREIGN KEY (book_id)
    REFERENCES book(book_id),
    CONSTRAINT fk_user
    FOREIGN KEY (user_id)
    REFERENCES user(user_Id)
);

/*
    insert store record 
*/
INSERT INTO store(locale)
    VALUES('8828 West Chapel Lane, Upland, CA 11373');

/*
    insert book records 
*/
INSERT INTO book(book_name, author, details)
    VALUES('Romeo and Juliet', 'William Shakespeare', 'A love tragedy');

INSERT INTO book(book_name, author, details)
    VALUES('Pride and Prejudice', 'Jane Austen', 'A trubulent love story');

INSERT INTO book(book_name, author, details)
    VALUES('The Adventures of Sherlock Holmes', 'Arthur Conan Doyle', 'Superb English Detective');

INSERT INTO book(book_name, author)
    VALUES('Dracula', 'Bram Stoker');

INSERT INTO book(book_name, author)
    VALUES('The Scarlet Letter', 'Nathaniel Hawthorne');

INSERT INTO book(book_name, author)
    VALUES('The War of the Worlds', 'H.G. Wells');

INSERT INTO book(book_name, author)
    VALUES('Winnie-the-Pooh', 'A.A. Milne');

INSERT INTO book(book_name, author)
    VALUES('Treasure Island', 'Robert Louis Stevenson');

INSERT INTO book(book_name, author)
    VALUES('Peter Pan', 'J.M. Barrie');

/*
    insert user
*/ 
INSERT INTO user(first_name, last_name) 
    VALUES('Jenna', 'Mooney');

INSERT INTO user(first_name, last_name)
    VALUES('Daisy', 'Cotton');

INSERT INTO user(first_name, last_name)
    VALUES('Penelope', 'Stone');

/*
    insert wishlist records 
*/
INSERT INTO wishlist(user_id, book_id) 
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Jenna'), 
        (SELECT book_id FROM book WHERE book_name = 'Dracula')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Daisy'),
        (SELECT book_id FROM book WHERE book_name = 'Peter Pan')
    );

INSERT INTO wishlist(user_id, book_id)
    VALUES (
        (SELECT user_id FROM user WHERE first_name = 'Penelope'),
        (SELECT book_id FROM book WHERE book_name = 'Treasure Island')
    );


/*SQL queries
*/
/*
    Select query to view a users wishlist items 
*/
SELECT user.user_id, user.first_name, user.last_name, book.book_id, book.book_name, book.author
FROM wishlist
    INNER JOIN user ON wishlist.user_id = user.user_id
    INNER JOIN book ON wishlist.book_id = book.book_id
WHERE user.user_id = 1;

/*
    Select query to view the store's location 
*/
SELECT store_id, locale from store;

/*
    Select query to view a full listing of the books WhatABook offers
*/
SELECT book_id, book_name, author, details from book;

/*
    Select query to view a listing of books not already in your a users wishlsit.
*/
SELECT book_id, book_name, author, details
FROM book
WHERE book_id NOT IN (SELECT book_id FROM wishlist WHERE user_id = 1);

/*
    Insert statement to add a new book to a users wishlist. 
*/
INSERT INTO wishlist(user_id, book_id)
    VALUES(1, 9)

/*
    Remove a book from the user's wishlist.
*/
DELETE FROM wishlist WHERE user_id = 1 AND book_id = 9;