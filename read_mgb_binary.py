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
# function to make datetime indexes skipping 29-fev inleap years
def times_365(dstart,nt):

    #dstart = datetime(2015,1,1)
    #nt = 23725
    times = [dstart]
    for i in range(nt):
        d = d + timedelta(days=1)
        
        if (calendar.isleap(d.year) and d.day ==29 and d.month==2):
            continue # will skip the date
        
        # else..store data
        times.append(d)
    
    return times
