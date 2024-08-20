from datetime import datetime,timedelta
import calendar
# function to make acalendar without 29-feb in leapyears
def times_365(dstart,nt):
    times = [dstart]
    it = 1
    d = dstart
    while it<nt:
        # next day
        d = d + timedelta(days=1)
        # check if will skip the date
        if (calendar.isleap(d.year) and d.day ==29 and d.month==2):
            continue        
        # we're good, store data and update the counter
        times.append(d)
        it = it +1
    
    return times

# testing
#t365 = times_365(datetime(2015,1,1),23725)
#print(len(t365))
