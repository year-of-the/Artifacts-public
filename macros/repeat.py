def repeatedly(action_func, num_times=float('inf')):
    i=1
    keep_repeating=True
    while(keep_repeating and i<=num_times):
        keep_repeating=action_func(i)
        i+=1