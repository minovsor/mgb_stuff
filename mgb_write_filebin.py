#xmat[nt,nc]
filebin='xtudo.bin'
_ = np.array(xmat, order = 'F', dtype='<f4').tofile(filebin)
