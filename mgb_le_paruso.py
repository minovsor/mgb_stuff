# -*- coding: utf-8 -*-
"""
LE PARUSO e FAKE PARUSO

@author: Mino Sorribas
"""
import copy

def le_paruso(paruso = 'PARUSO.cal'):
    
    with open(paruso,'r') as f:
        # read all lines
        lido = f.readlines()
    
        # delete final empty lines
        reverse = lido[::-1]
        for i,v in enumerate(reverse):
            if 'qb' in v.lower():
                break
        lido = reverse[i:][::-1]
    
        # declare headers
        #wsh_header = 'Watershed <id>\n'
        #var_header = '       hru      Wm       b    Kbas    Kint      XL     CAP      Wc\n'
    
        # find number of HRU's
        for i,v in enumerate(lido):
            if 'wm' in v.lower(): # busca cabecalho
                ihru = i + 1
            if 'cs' in v.lower(): # busca fim das linhas de hru
                ics = i
                break
        nhru = ics - ihru
    
        # get HRU names
        hru_names = []
        for i in lido[ihru:ics]:
            hru_names.append(i.split()[0])
    
        # subbasin block size
        nlin = len(lido)
        nn = 2 + nhru + 4   # 2 headers, n-hru params, cs/ci/cb, qesp
        if nlin % nn !=0:
            print('something wrong in file')
            return None
    
        # split blocks
        i = 0
        nb = 0
        params = {}
        while (i+nn <=nlin):
            nb = nb + 1
            basin_block = lido[i:i+nn]
            params[nb] = basin_block
    
            # proximo
            j = i+nn
            i = j
    
        return params


def update_paruso(params, newval, ib, iu, parname, filout = None):
    new_params = copy.deepcopy(params)
    bacia = new_params[ib]
    nhru = len(bacia)-2-4

    if parname =='xl':
        parname = 'xlam'

    msglog = f"Updating parameter: {parname}\n"

    flag_iu = True
    if parname in ['cs', 'ci', 'cb','qesp']:
        msglog += "'iu' ignored.\n"
        flag_iu = False

    if flag_iu and (iu>nhru or iu<1):
        msglog += f'Error: iu {iu} incompatible with {nhru} HRUs\n'
        print(msglog)
        return None

    # parameter names
    names = ['wm', 'b', 'kbas', 'kint', 'xlam', 'cap', 'wc',
             'cs', 'ci', 'cb','qesp']
    ipar = names.index(parname)

    # formats
    #fmt_lbl = lambda x: f"{x:<10}"
    fmt_wm = lambda x: f"{x:8.1f}"
    fmt_other = lambda x: f"{x:8.2f}"
    fmt_qesp = lambda x: f"{x:9.3f}"

    # hru's
    if ipar<=6:
        ku = iu + 1
        ini = bacia[ku][:10 + 8*ipar]
        fim = bacia[ku][(10 + 8*(ipar+1)):]
        if ipar==0:
            new = fmt_wm(newval)
        else:
            new = fmt_other(newval)
        newtxt = ini + new + fim
        if ipar =='wc':
            newtxt += '\n'
        bacia[ku] = newtxt
    elif ( ipar>=7 ):
        kk = -4 + (ipar - 7)
        ini = bacia[kk][:10]
        new = fmt_other(newval)
        if ipar == 10:
            new = fmt_qesp(newval)
        newtxt = ini + new + '\n'
        bacia[kk] = newtxt

    # talvez nem precisasse essa atribuicao, dict é um perigo.
    new_params[ib] = copy.deepcopy(bacia)

    if filout:
        # dump to file
        msglog += f'writing to {filout}\n'
        with open(filout,'w') as f:
            txtout = ''.join([''.join(i) for i in new_params.values()])
            f.write(txtout)

    print(msglog)
    return new_params




def fake_paruso(nb, nu = 9, filout = 'paruso.fake', last_water = True,  **kwargs):

    hru_default = [f'HRU_{i+1}' for i in range(nu-1)] + ['WATER']
    hru_names = kwargs.get('hru_names',hru_default)
    wm = kwargs.get('wm', 500.)
    b = kwargs.get('b', 0.1)
    kbas = kwargs.get('kbas', 1.)
    kint = kwargs.get('kint', 2.)
    xlam = kwargs.get('xlam', 0.67)
    cap = kwargs.get('cap', 0.)
    wc = kwargs.get('wc', 0.1)
    cs = kwargs.get('cs', 6.)
    ci = kwargs.get('ci', 100.)
    cb = kwargs.get('cb', 500.)
    qesp = kwargs.get('qesp', 0.01)

    params_hru = [wm, b, kbas, kint, xlam, cap, wc]
    params_water =  [0., 0., 0., 0., 0., 0., 0.]

    rl_names = ['CS', 'CI', 'CB', 'QB_M3/SKM2']
    params_rl  = [cs, ci, cb, qesp]

    wsh_header = 'Watershed <id>\n'
    var_header = '       hru      Wm       b    Kbas    Kint      XL     CAP      Wc\n'

    fmt_lbl = lambda x: f"{x:<10}"
    fmt_wm = lambda x: f"{x:8.1f}"
    fmt_other = lambda x: f"{x:8.2f}"
    fmt_qesp = lambda x: f"{x:9.3f}"

    params = {}
    for ib in range(nb):
        kb = ib + 1
        txt = ''  # armazena uma bacia por vez (params)
        header = wsh_header.replace('<id>',f'{str(kb).zfill(3)}')
        txt += header
        txt += var_header
        #hrus
        for iu in range(nu):
            txt_lbl = fmt_lbl(hru_names[iu])
            ku = iu + 1
            if ku == nu and last_water:
                txt_wm = fmt_wm(params_water[0])
                txt_other = ''.join([fmt_other(i) for i in params_water[1:]])
            else:
                txt_wm = fmt_wm(params_hru[0])
                txt_other = ''.join([fmt_other(i) for i in params_hru[1:]])
            txt += f'{txt_lbl}{txt_wm}{txt_other}\n'

        #cs/ci/cb
        for i in range(3):
            txt_lbl = fmt_lbl(rl_names[i])
            txt_val = fmt_other(params_rl[i])
            txt += f'{txt_lbl}{txt_val}\n'
        # qesp
        txt_lbl = fmt_lbl(rl_names[3])
        txt_val = fmt_qesp(params_rl[3])
        txt += f'{txt_lbl}{txt_val}'

        # make as params dict
        txt_params = [i+'\n' for i in txt.split('\n')]

        params[kb] = txt_params

    # dump to file
    with open(filout,'w') as f:
        txtout = ''.join([''.join(i) for i in params.values()])
        f.write(txtout)

    return params