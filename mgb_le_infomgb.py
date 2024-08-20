# -*- coding: utf-8 -*-
"""
LEITURA INFOMGB.SIM

@author: MINO SORRIBAS
"""
from datetime import datetime


def le_infomgb(fil_infomgb = 'infoMGB.sim'):

    with open(fil_infomgb) as f:
        lidos = f.readlines()
        
        line_project_name = 2
        line_simstart = 5
        line_nt_dt = 8
        line_nc_nu = 11
        line_calib = 14
        
        # nome do projeto
        name = lidos[line_project_name]
        
        # data de inicio
        simstart = tuple(map(int,lidos[line_simstart].split()))
        simstart_to_dt = lambda x: datetime(x[2],x[1],x[0],x[3])
        dt_simstart = simstart_to_dt(simstart)
        
        # nt dt
        nt_dt = lidos[line_nt_dt].split()
        nt,dt = tuple(map(float,nt_dt))
        nt = int(nt)
        
        # nc, nu, etc..
        nc,nu,nb,ncli,cru_ind,reserv,flood,alpha = lidos[line_nc_nu].split()
        nc,nu,nb,ncli,cru_ind,reserv,flood = tuple(map(int,[nc,nu,nb,ncli,cru_ind,reserv,flood]))
        alpha = float(alpha) 
        
        # modo de simulacao
        icalib = int ( lidos[line_calib].split()[0] )   
        
        # clima mensal e diario (se existir)
        if (ncli<0):
            line_mediascli = 19
            dayclim = None
        elif (ncli>0):
            line_dayclim = 17
            lines_dayclim = [line_dayclim + i for i in range(ncli)]
            line_mediascli = 19 + ncli-1
            
            dayclim = [lidos[i] for i in lines_dayclim] #NEEDS TESTING
            
        medias_cli = lidos[line_mediascli]
        
        # vazoes observadas
        line_qobs = line_mediascli + 3
        line_miniqobs = line_qobs + 3    
        
        n_qobs = int( lidos[line_qobs].split()[0] )
        mini_qobs = tuple( map(int, lidos[line_miniqobs].split()) )
        
        # vazoes simuladas
        line_n_qsim = line_miniqobs + 3
        n_qsim = int( lidos[line_n_qsim].split()[0] )
        line_mini_qsim = line_n_qsim + 3
        lines_mini_qsim = [line_mini_qsim + i for i in range(n_qsim)]
        mini_qsim = tuple( [int (lidos[i]) for i in lines_mini_qsim] )
        
        # monta dicinario de resultados
        dout = {}
        dout['name'] = name
        dout['simstart'] = dt_simstart
        dout['nt'] = nt
        dout['dt'] = dt
        dout['nc'] = nc
        dout['nu'] = nu
        dout['nb'] = nb
        dout['ncli'] = ncli
        dout['cru_ind'] = cru_ind
        dout['reserv'] = reserv
        dout['flood'] = flood
        dout['alpha'] = alpha
        dout['icalib'] = icalib
        dout['medias_cli'] = medias_cli
        dout['dayclim'] = dayclim
        dout['n_qobs'] = n_qobs
        dout['mini_qobs'] = mini_qobs
        dout['n_qsim'] = n_qsim
        dout['mini_qsim'] = mini_qsim
        
        return dout


"""
EXEMPLO: infoMGB.sim

'GENERAL INFORMATIONS FILE FOR LARGE SCALE HYDROLOGIC MODEL\n',
'!\n',
'Project MGB\n',
'!\n',
'       DAY       MOUNTH       YEAR      HOUR          !SIMULATION START\n',
'        1        9      1970         0\n',
'\n',
'        NT        DT       !TIME INTERVALS AND INTERVALS SIZE IN SECONDS\n',
'     19480    86400.\n',
'\n',
'\t    NC        NU        NB      NCLI   CRU_IND    RESERV     FLOOD ALPHA*100 !NUMBER OF CATCHMENTS, HRUs, SUB-BASINS, CLIMATE STATIONS, CRU_INDEX (1 USES CRU CLIMATE DATA), RESERVOIR INDEX, FLOOD ROUTING METHOD\n',
'       189         9        16       -34         0         0         0        30\n',
'\n',
'    ICALIB    !INDICATES IF IT IS GONNA BE USED AUTOMATIC CALIBRATION (1) OR NOT (0) \n',
'         0    !OR IF IT WILL MAKE THE FORECAST (2)\n',
'\n',
'FILENAME WITH DAILY METEOROLOGICAL DATA\n',
'\n',
'!FILENAME WITH AVERAGE MONTHLY METEOROLOGICAL DATA\n',
'medias.cli \n',
'\n',
'!STATIONS WITH OBSERVED FLOW DATA, FILENAME WITH DATA\n',
'2  QOBS.qob\n',
'\n',
'!NUMBER OF CELLS THAT CORRESPONDS TO FLU GAUGE WITH DATA\n',
'140  152\n',
'\n',
'!NUMBER OF POINTS TO RECORD HYDROGRAPHS\n',
'15 \n',
'\n',
'!CELLS THAT CORRESPONDS TO THOSE POINTS \n',
'140\n',
'152\n',
'\n',
'!Number of cells where calculated flow must be substituted for the one read from file and filename\n',
'0  QSUBST.qsb\n',
'\n',
'!Cells which flow data will be substituted\n'
"""
