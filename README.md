Python script to process Discover Card CSV statements for Skrooge import.
Written by Rob Bruce, 2024.

My motivation: 

Discover Financial Services stopped offering Quicken file format export for statements and transaction lists in 2023, so CSV was the next best option. 

The Problem: 

The exported CSV files don't contain enough info that's already formatted correctly to import directly into Skrooge. You can make some accomoations in Skrooge->Settings->Configure Skrooge->Import/Export->CSV, but not quite enough for this purpose because: 

  1. there are no "account" (or "number") columns and no "payee" column; 
  2. the sign of the credits and debits is reversed from what Skrooge expects; 
  3. there are two date columns in the CSV, but neither is named "date" or anything close enough for Skooge to guess.

My manual fix:
  
My initial solution was to edit the downloaded CSV in $my_favorite_spreadsheet. 
  1. I manually changed the 'Trans. Date' column name to 'date', the 'Description' to 'payee' and the 'Amount' to 'neg amount' since the amounts were the inverse of what Skrooge expected. Also, I changed 'Category' to 'Comment' since I didn't want to use Discover's categories but rather my own. 
  2. I then created a new 'account' column and set the value in every row to the name of the account in Skrooge. (Skrooge can also match on the 'Number' field to import the data into the correct account.) Then I created a new 'amount' column and populated it the the 'neg amount' column's value times -1 to give it the correct sign. 
  3. I created a 'mode' column which I filled with "credit" or "debit" depending on the sign of 'amount'. This isn't strictly necessary to get the file to import, I just wanted the mode to be filled in automatically on import. 
  Note. I didn't worry about any extraneous columns; Skrooge ignores them as long as they don't match anything in the Import/Export settings.

My automated script:

All this work every month got to be a PITA so I thought it'd be fun to figure out how to do some simple CSV manipulation in Python, automating the steps above. I chose the Pandas library for this purpose (you might need to install this library in your Python implementation). I ended up with this (rather short) python script that can be directly used to prepare your DFS statement CSVs for import in Skrooge. All you need to do is modify this script to use _your_ Skrooge Discover account name: i.e., change the name from 'Discover Card - Rob' to the _exact_ name used by Skrooge -- it's important that this matches so data gets imported into your existing account, otherwise Skrooge will happily create a new account with all these transactions in it.

The resulting output file is a minimal csv that can be imported into Skrooge.

Pass filenames of input and output csv as arguments.

Usage:

  disc_convert.py inputcsv.csv outputcsv.csv

. . . use your own filenames, of course.

Notes:

There's no configuration of this script except by changing the code, but I didn't figure I'd need to do that more than once.
There is no error checking of the command input.
There is no checking to prevent clobbering an existing output file.
Script assumes that transaction data is from only one account and that account name/number can be hardcoded.
This script doesn't make sure the CSV format hasn't changed. It will behave weirdly and wrong if the bank changes any names.
See comments in the .py file for more information.

Feel free to adapt this script to prepare other instutions' CSVs for Skrooge input. Share if you like. Improve it if you want to.
