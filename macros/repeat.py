"""
Either the callback must return something falsy or
the num_times param must be set to a finite number
for this function to terminate.
"""
def repeatedly(action_func, num_times=float('inf')):
    i=1
    keep_repeating=True
    while(keep_repeating and i<=num_times):
        keep_repeating=action_func(i)
        i+=1