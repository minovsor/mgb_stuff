import numpy as np
import pandas as pd
from datetime import datetime,timedelta

def read_mgb_binary_as_dataframe(filebin, nt, nc, dstart):
    """ Read full binary (MGB format) as dataframe """

    # read from file
    #'<f4' indicates little-endian (<) float(f) 4 byte (4)
    dados = np.fromfile(filebin,'<f4').reshape(nt,nc)

    # make timeseries dataframe
    times = [dstart + timedelta(days=i) for i in range(nt)]
    df = pd.DataFrame(dados, columns=range(1,nc+1), index=times)
    
    return df


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
