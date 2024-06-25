#!/usr/bin/env python3

# Python script to process Discover Card CSV statements for Skrooge
# by Rob Bruce 2024.
# Feel free to use/modify/adapt/republish this script any way you want.
# You need to modify this script to use _your_ Skrooge Discover account name:
# i.e., change the name in the "df2['account'] = " line to the _exact_ name used by Skrooge --
# it's important that this matches so data gets imported into existing account,
# otherwise Skrooge will happily create a new account with all these transactions in it.
# (Don't worry if you do, just delete the new extraneous account and try again.)
# The resulting output file is a minimal csv that can be imported into Skrooge.
# Pass filenames of input and output csv as arguments . . .
# Usage:
# > disc_convert.py inputcsv.csv outputcsv.csv 
# . . . use your own filenames, of course.
# There is no error checking of the command input.
# There is no checking to prevent clobbering an existing output file.

import sys
import pandas as pd
import datetime
import numpy as np

# Sanity check of input arguments for user . . .
print('Input file: '+sys.argv[1])
print('Output file: '+sys.argv[2])

df = pd.read_csv(sys.argv[1])
df.head()
# Rename some columns for Skrooge import . . .
# If you like the way that Discover categorizes transactions, then keep the 'Category' column as 'Category'.
df2 = df.rename(columns = {'Trans. Date': 'date', 'Post Date':' ', 'Description':'payee', 'Amount':'neg amount', 'Category':'Comment'}, inplace = False)
# Change this line to _exactly_ match _your_ Discover account name in Skrooge
# This creates a new column named account with _your_ account name in every row
df2['account'] = 'Discover Card - Rob'
# The cvs from Discover uses +/- oppositely from what Skrooge expects . . .
# . . . so create a new 'amount' column with the value from Discover * -1
df2['amount'] = np.multiply(df2['neg amount'],-1)
# The 'mode' column isn't absolutely needed for import -- remove this line to leave it blank on import.
# Leave this line in to create the 'mode' column with value based on the sign in the 'amount' column.
# You could also assign other mode names if you like, Skrooge won't care . . .
df2['mode'] = np.where(df2['amount']<0, "debit", "credit")
# Finally write to CSV file
df2.to_csv(sys.argv[2])
print('Done.')

