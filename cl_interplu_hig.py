"""
==========================================
    Pre-processor for Interplu.HIG
==========================================
@author: MINO SORRIBAS


"""

from datetime import datetime
import pandas as pd


class InterpluPreProcessor():
    """
    Parameters
    ----------
    inidate_day : int
        day of initial date
    inidate_month : int    
        month of initial date
    inidate_year : int
        year of initial date
    enddate_day : int 
        day of initial date
    enddate_month : int
        month of end date
    enddate_year : int
        year of end date
    nt : int
        number of timesteps
    nu : int,
        number HRUs
    nc : int
        number of catchments    
    ng : int
        number of gauges
    df_gauges : pd.DataFrame
        dataframe with gauges information, with "ng" rows
            and columns ['lon','lat','file']
            where
                lon : float, longitude of each gauge
                lat : float, latitude of each gauge
                file : str,  name of file with gauge time-series.
    
    Returns
    -------
    None
    
    """   
    
    def __init__(self,
                 inidate_year,
                 inidate_month,
                 inidate_day,
                 enddate_year,
                 enddate_month,
                 enddate_day,
                 nt,
                 nu,
                 nc,
                 ng,
                 df_gauges,
                 filehig = 'INTERPLU.HIG',
                 ):

        self.inidate_year = inidate_year
        self.inidate_month = inidate_month
        self.inidate_day = inidate_day
        self.enddate_year = enddate_year
        self.enddate_month = enddate_month
        self.enddate_day = enddate_day
        self.nt = nt
        self.nu = nu
        self.nc = nc
        self.ng = ng
        self.df_gauges = df_gauges
        self.filehig = filehig
        
        # make content for "interplu.hig" and export 
        self.content = self._make_content()
        self.export_filehig(self.filehig)

    
    def _make_content(self):
        
        # just to get a cleaner code.
        inidate_day = self.inidate_day
        inidate_month = self.inidate_month
        inidate_year = self.inidate_year
        enddate_day = self.enddate_day
        enddate_month = self.enddate_month
        enddate_year = self.enddate_year
        nt = self.nt
        nu = self.nu
        nc = self.nc
        ng = self.ng
        df_gauges = self.df_gauges
   
        
        # check if nt makes sense
        enddate = datetime(enddate_year, enddate_month, enddate_day)
        inidate = datetime(inidate_year, inidate_month, inidate_day)
        ntx = (enddate - inidate).days + 1
        if ntx!=nt:
            return f' ERROR: CHECK NT={nt} != NTx={ntx}\n'
        
        # header lines
        line = '!start \n'
        line += 'DAY'.rjust(10) + 'MONTH'.rjust(10) + 'YEAR'.rjust(10) + '\n'
        line += f'{inidate_day}'.rjust(10) + f'{inidate_month}'.rjust(10) + f'{inidate_year}'.rjust(10) + '\n'    
        line += '!end \n'
        line += 'DAY'.rjust(10) + 'MONTH'.rjust(10) + 'YEAR'.rjust(10) + '\n'
        line += f'{enddate_day}'.rjust(10) + f'{enddate_month}'.rjust(10) + f'{enddate_year}'.rjust(10) + '\n'        
        line += 'NC'.rjust(10) + 'NU'.rjust(10) + 'NT'.rjust(10)  + 'NP'.rjust(10) + '     (number of cells, HRCs, time intervals, stations)\n'
        line += f'{nc}'.rjust(10) + f'{nu}'.rjust(10) + f'{nt}'.rjust(10) + f'{ng}'.rjust(10) + '\n'    
        line += '!FROM WHICH TIME INTERVAL DO YOU WANT TO START THE INTERPOLATION?\n'
        line += '1'.rjust(10) + f'        !CORRESPONDS TO {inidate_day}/{inidate_month}/{inidate_year}\n'        
        line += '!Grads file generation (1 to turn on - 0 turn off, matrix cell size) \n'    
        line += "         0       0.1     '09:00z01jan1968       1dy'\n"        
        line += "              code               long dec      lat dec \n"
        
        
        # gauges coordinates lines
        for i,row in df_gauges.iterrows():        
            line += row.file.rjust(19) + f'{row.lon:.3f}'.rjust(21) + f'{row.lat:.3f}'.rjust(19) +'\n'         
        
        # make interplu.hig "content"
        content = line
        return content


    def export_filehig(self, filehig):
        content = self.content
        with open(filehig,'w') as f:
            f.write(content)
        
        print('-----------------------')
        print(f'\n {content} \n')
        print(f'... EXPORTED TO {filehig}')
        print('-----------------------')
        return 


    def _testcase():                
        
        # simulation inputs        
        inidate_day, inidate_month, inidate_year = 1,1,1990
        enddate_day, enddate_month, enddate_year = 31,12,2014
        enddate = datetime(enddate_year, enddate_month, enddate_day)
        inidate = datetime(inidate_year, inidate_month, inidate_day)
        nt = (enddate - inidate).days + 1
        nu = 9
        nc = 100 
        
        # gauges dataframe
        dados = [
            [-43.850, -17.750,'00000000.txt'],
            [-43.750, -17.750,'00000001.txt'],
                ]
        df_gauges = pd.DataFrame(data = dados, columns=['lon','lat','file'])
        
        # get number of gauges
        ng = df_gauges.shape[0]
        
        # run
        _ = InterpluPreProcessor(
                    inidate_year, inidate_month, inidate_day,
                    enddate_year, enddate_month, enddate_day,
                    nt, nu, nc, ng, df_gauges
                    )
        pass


    def _dataframe_to_timeseries(df_ts,
                                 fileout,
                                 convert_to_ptbr = True):
        """
        Make time-series files for a given gauge
        
        Parameters
        ----------
        df_ts : pd.DataFrame
            contains daily timeseries indexed with datetime
        fileout: str
            fullpath to output file
        
        """
        fmt = {'datas':"{:>18}".format,
               'chuva':"{:>15,.6f}".format}        
        
        # set index name to work
        df_ts.index.name = 'datas'
        df_ts.columns = ['prec']

        # convert index to pt-br
        if convert_to_ptbr:
            f_datas_ptbr = lambda x: x.strftime('    %d    %m  %Y')
            df_ts.index = df_ts.index.map(f_datas_ptbr)
        
        # some final adjustment
        df_ts = df_ts.reset_index()
        df_ts['prec'] = df_ts['prec'].round(2)
        fileout = f'{fileout}'
        with open(fileout,'w') as f:
            f.write(df_ts.to_string(index = False, header = False, formatters = fmt))  
        
        pass
