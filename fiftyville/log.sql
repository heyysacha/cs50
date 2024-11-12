-- Keep a log of any SQL queries you execute as you solve the mystery.
-- All you know is that the theft took place on July 28, 2023 and that it took place on Humphrey Street.

--As suggested, checking the crime scene reports to find one matching the day and place
SELECT * FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
-- this says the crime took place at 10:15 am at the Humphrey Street Bakery - 3 witnesses interviewed so now I will check the interview table
SELECT * FROM interviews WHERE month = 7 AND day = 28 AND id = 161 OR id = 162 OR id = 163;
--tightened up the query to only show me the relevant interviews. one person said to check security footage to find the car that drove away at the time
--another person saw them earlier in the morning at the Leggett St ATM withdrawing money
--and the last witness said the person was on the phone and taking the earliest flight out of fiftyville tomorrow
SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute < 30;
-- if the crime took place at 10:15, the most likely license plate is 5P2BI95.
SELECT * FROM atm_transactions WHERE month = 7 AND day = 28 AND atm_location = 'Leggett Street';
--lots of withdrawls that day so going to keep looking elsewhere
SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60;
-- a few phone calls less than a minute assuming duration is in seconds
SELECT * FROM airports;
--getting fiftyville's id
SELECT * FROM flights WHERE origin_airport_id = 8 AND month = 7 AND day = 29 ORDER BY hour;
--earliest flight out is flight id 36
SELECT * FROM passengers WHERE flight_id = 36;
--okay so going to make a query to find who's in common between the license plates, phone records, passenger list
SELECT name FROM people WHERE
    phone_number IN (
        SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60
    )
    AND passport_number IN (
        SELECT passport_number FROM passengers WHERE flight_id = 36
    )
    AND license_plate IN (
        SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute < 20
    );
--Bruce is the thief
SELECT * FROM flights WHERE id = 36;
SELECT * FROM airports where id = 4;
--queries for finding the city
SELECT * FROM people WHERE
    phone_number IN (
        SELECT caller FROM phone_calls WHERE month = 7 AND day = 28 AND duration < 60
    )
    AND passport_number IN (
        SELECT passport_number FROM passengers WHERE flight_id = 36
    )
    AND license_plate IN (
        SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute < 20
    );
--used to find bruce's phone number: (367) 555-5533
SELECT * FROM phone_calls WHERE month = 7 AND day = 28 AND caller = '(367) 555-5533';
--used to find reciever's phone number: (375) 555-8161
SELECT name FROM people WHERE phone_number = '(375) 555-8161';
