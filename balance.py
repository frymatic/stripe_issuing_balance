# Calculation of Stripe Issuing Cardholder Account Balance
# ℳ° ƒrymatic
# Brazen Studios
 

import stripe
from live_keys import *

# get all transactions based on ARG ID
# retrieve transactions until all are gotten
lastID = None   # tail value denoting stopping point of the previous chunk of transactions

amount = 0  # sum of a chunk of transactions
spend = 0 # total amount spent by cardholder (e.g. Bryan)

stripe.api_key = sec_key  # turn the key

# load handsome
account = stripe.issuing.Cardholder.retrieve(test_id)
# get account limit
limit = account.spending_controls.spending_limits[0].amount

# get starting transaction object; need tx object for following while 
tx = stripe.issuing.Transaction.list(limit = 1)

#############################################################

# loop through transactions until there are no more, sum up all the transactions a we go
while tx.has_more:


	spend += amount

	
	# pull chunk of transactions
	tx = stripe.issuing.Transaction.list(
			limit = 100, 
			starting_after = lastID
		)
	
	lastID = tx.data[-1].id  # assign tail

	# balance calculation
	# list comprehension producing a list of all transactions by an individual
	tx_amounts = [tx.data[i].amount for i in range(0, len(tx.data)) if tx.data[i].cardholder == test_id]
	print("all transactions:")
	print(tx_amounts)

	amount = sum(tx_amounts) # add it up
	spend += amount

balance = limit + spend	# spend is a negative value, so add the two
print("Account Limit: ", limit)
print("Total Spend: ", spend)
print("Limit - Send = Balance: ", balance)

