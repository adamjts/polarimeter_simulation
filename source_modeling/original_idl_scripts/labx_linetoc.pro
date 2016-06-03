FUNCTION labx_linetoc, E, line_select
;
; This function calculates the line-to-continuum ratio for a given
; line type (Kalpha, etc.) using eq. (35) in Pella et al.
;
; 4/15/93 - dd
;

@labx_common

; Over voltage ratio
U = lx_sV/E

; Basic line to coninuum ratio
S = pella_s(lx_tZ, line_select, lx_tname)

; R' is small correction
linetoc = 1000.*(E*E/lx_akev) * pella_rprime(U) * S * pella_tau(U)

RETURN, linetoc
END
