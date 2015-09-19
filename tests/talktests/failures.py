
d = defer.succeed(None)
d.addCallback(raise_exception)

# callback skipped because the last callback
# raised, so resolved to a Failure
d.addCallback(never_get_here) 

# "error-callbacks" catch Failures and resolve them if they can
# then the chain goes back to the success-case
d.addErrback(recover)

d.addCallback(everythings_great_again)
