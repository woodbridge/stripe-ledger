import requests, stripe
from datetime import datetime
import json
import os, sys

DB_PATH = os.path.join(os.environ.get('HOME'), '.stripe-ledger.json')
DB = None

def open_db():
    if os.path.exists(DB_PATH):
        return json.loads(open(DB_PATH).read())
    else:
        print "No existing database found.  Starting new one."
        fresh_db = {}
        api_key = ''
        while not api_key:
            api_key = raw_input("What's your Stripe api key? ")
        fresh_db['stripe_key'] = api_key
        save_db(fresh_db)
        print "Saved api key."
        return fresh_db

def save_db(content):
    blob = json.dumps(content)
    open(DB_PATH, 'w').write(blob)

def format_dollars(pennies):
    return '$' + str(pennies / 100)

def print_transfer_report():
    print "Loading Stripe transactions..."

    transfers = stripe.Transfer.all().data
    sorted_transfers = sorted(transfers, key=lambda k: k.date)

    try:
        cutoff = DB['last_processed_transfer']
    except KeyError:
        cutoff = None

    paid_transfers = []
    pending_transfers = []

    paid_transfer_count = 0

    for transfer in sorted_transfers:
        new = True
        if cutoff and transfer.status == 'paid' and transfer.date <= cutoff:
            paid_transfer_count += 1
            new = False
        if new:
            if transfer.status == 'paid':
                paid_transfers.append(transfer)
            elif transfer.status == 'pending':
                pending_transfers.append(transfer)
        DB[transfer.id] = transfer.status

    amount_to_transfer = 0
    for paid in paid_transfers:
        amount_to_transfer += paid.amount

    DB['outstanding_amount'] = amount_to_transfer

    amount_to_transfer = amount_to_transfer / 100

    try:
        last_paid_transfer = sorted(paid_transfers, key=lambda k: k.date)[-1]
        DB['last_paid_transfer_date'] = last_paid_transfer.date
    except IndexError:
        DB['last_paid_transfer_date'] = None

    print
    print "${0} waiting to be put into account.".format(amount_to_transfer)
    print
    print "--------------------------------"

    num_pending_transfers = len(pending_transfers)
    transfer_label = 'transfers' if num_pending_transfers > 0 else 'transfer'

    print
    print "* {0} {1} are pending.".format(num_pending_transfers, transfer_label)
    print "* {0} transfers have been paid and processed so far.".format(paid_transfer_count)
    print

def clear_transfer_balance():
    if DB['outstanding_amount'] == 0:
        print "No outstanding balance."
        sys.exit()
    else:
        print "Marked balance of {0} as processed.".format(format_dollars(DB['outstanding_amount']))
        DB['outstanding_amount'] = 0
        DB['last_processed_transfer'] = DB['last_paid_transfer_date']

DB = open_db()
stripe.api_key = DB['stripe_key']

if len(sys.argv) < 2:
    print_transfer_report()
else:
    if sys.argv[1] == 'record':
        clear_transfer_balance()
    else:
        print "Unknown command."

save_db(DB)