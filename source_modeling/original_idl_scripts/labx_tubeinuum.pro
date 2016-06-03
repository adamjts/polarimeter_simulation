FUNCTION labx_tubeinuum, E

@labx_common

; Simple Kramer's equation: (photons/sec per eV per steradian)
flux = (1./(4*!PI))*2.2E-9*lx_tZ*((lx_sV/E)-1)*lx_espermA*lx_sI


; DO NOT use for now
; Include self absorbtion (eq. (17) from Pella et al.)
; continuum = flux*pella_selfabs(E)

continuum = flux

; Set any values that are less than zero to zero
continuum = FLOAT(continuum GT 0.) * continuum


RETURN, continuum
END
