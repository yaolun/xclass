def getTransitionStrength(moldata, Q, freq, Ntot, Tex):
    """
    moldata: a dictionary contains the Einstein-A, Eu, nu0, and gu for the transitions
    freq: the frequency grid in Hz
    Ntot: the column density in cm-2
    Tex: excitation temperature in K
    Q: the partition functions in two columns, temp(K) and Q
    """

    import numpy as np
    import astropy.constants as const
    from scipy.interpolate import interp1d
    c = const.c.cgs.value
    k = const.k_B.cgs.value
    h = const.h.cgs.value

    def line_profile(freq, nu0, width):
        # width in FWHM and km/s
        width_f = width*1e5/c*nu0
        sigma = width_f/2.354
        return 1/(2*np.pi)**0.5*np.exp(-(freq-nu0)**2/(2*sigma**2))

    # linear interpolation for the partition function
    if (Tex > Q['temp(K)'].max()) or (Tex < Q['temp(K)'].min()):
        print('T_ex outside of the range of partition function')
        return None
    else:
        QT = interp1d(Q['temp(K)'], Q['Q'])
        Q_interp = QT(Tex)

    # select the valid moldata to use
    selector = (moldata['nu0'] >= freq.min()) & (moldata['nu0'] <= freq.max())

    # create zero Tmb array
    Tmb = np.zeros_like(freq)
    width = 3.5
    # width of channel
    width_chan = np.mean(freq[1:]-freq[:-1])
    # iternate through the transitions
    for i, (nu0, EA, El, gu) in enumerate(zip(moldata['nu0'][selector],
                                          moldata['Einstein-A'][selector],
                                          moldata['El'][selector],
                                          moldata['gu'][selector])):
        T_nu = c**2/(8*np.pi*freq)*h/k*EA*Ntot*gu/Q_interp*np.exp(-El/Tex)*\
               (1-np.exp(-h*nu0/k/Tex))/(np.exp(h*freq/k/Tex)-1)*line_profile(freq, nu0, width)
        Tmb = Tmb+T_nu/width_chan

    return Tmb
