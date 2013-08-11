### A small tool for your Stripe transfers
by Justin Woodbridge

Problem: Stripe transfers your money to a bank account.  You need to then transfer that money to a different bank account before it's accessible and spendable.  Keeping track of those states is annoying.

So I made this little script.  It's not much, but it does the trick for me.  It might for you, too.

**Here's how it works**:

First, you can just run the program to get a report of how much money is waiting in your middleman account.  Then, you can see how many transfer are still pending tranfer into it.  Finally, there's a fun little counter of how many transfers you have processed into your final, spendable account.  I like stats.

    $ python ledger.py
    Loading Stripe transactions...

    $774 waiting to be put into account.

    --------------------------------

    * 0 transfer are pending.
    * 0 transfers have been paid and processed so far.

Once you've transfered the latest balance from your middleman account to your final account, you can do this to tell the ledger:

    $ python ledger.py record

    Marked balance of $774 as processed.

Now when you run the report again, it'll know that you cleared the balance.

    Loading Stripe transactions...

    $0 waiting to be put into account.

    --------------------------------

    * 0 transfer are pending.
    * 10 transfers have been paid and processed so far.

### Install:

1. Drop the script into your `PATH`.  I like to keep these kinds of small tools in `~/bin`.
2. Install the dependencies: ```pip install requests stripe```

Now you should be good to go.


Your data is stored in `~/.stripe-ledger.json`.

### License

MIT.

-------

If you actually find this little shiv useful, I'd love to hear it.  Send me any ideas you have, too.
