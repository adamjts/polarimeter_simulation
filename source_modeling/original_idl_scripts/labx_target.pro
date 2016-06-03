PRO labx_target
;
; This procedure sets up the parameters for an x-ray target using
; the characters in lx_tName as the input.
;
; 4/15/93 - dd
; 12/21/94 dd Update energies from Bearden

@labx_common

; Default target
if n_elements(lx_tName) EQ 0 then lx_tName = 'Cu'

; Setup other constants needed
lx_akev = 12.39824		; keV Angstrom* product
lx_electron = 1.602E-19
lx_espermA = 0.001/lx_electron
lx_melectron = 9.11E-28
lx_mproton = 1.673E-24

; Setup target values as desired.

CASE lx_tName OF
    
    'Be': BEGIN
  lx_tZ = 4.
  lx_tA = 9.012
  lx_trho = 1.85 ; 
; lines from this target
  lx_tEKa = 0.1085
  lx_tEKb = -1
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
    END
    
    'B': BEGIN
  lx_tZ = 5.
  lx_tA = 10.81
  lx_trho = 2. ; Guess
; lines from this target
  lx_tEKa = 0.1833
  lx_tEKb = -1
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
    END
    
    'C': BEGIN
  lx_tZ = 6.
  lx_tA = 12.01
  lx_trho = 2.15 ; Graphite
; lines from this target
  lx_tEKa = 0.277366
  lx_tEKb = -1
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
    END
    
    'O': BEGIN
  lx_tZ = 8.
  lx_tA = 16.0
  lx_trho = 4.26 ; TiO2
; lines from this target
  lx_tEKa = 0.524904
  lx_tEKb = -1
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
    END

'Mg': BEGIN
  lx_tZ = 12.
  lx_tA = 24.3
  lx_trho = 1.74
; lines from this target
  lx_tEKa = 1.25361
  lx_tEKb = 1.30220
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

; Super-d-duper kludge to get MgO spectrum - what a hacker!
'MgO': BEGIN
  lx_tZ = 12.
  lx_tA = 24.3
  lx_trho = 1.74
; lines from this target
  lx_tEKa = 1.25361
  lx_tEKb = 1.30220
  lx_tELa = 0.524904
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Al': BEGIN
  lx_tZ = 13.
  lx_tA = 26.98
  lx_trho = 2.7
; lines from this target
  lx_tEKa = 1.48629
  lx_tEKb = 1.55757
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END
; Super-d-duper kludge to get AlO spectrum - what a hacker!
'AlO': BEGIN
  lx_tZ = 13.
  lx_tA = 26.98
  lx_trho = 2.7
; lines from this target
  lx_tEKa = 1.48629
  lx_tEKb = 1.55757
  lx_tELa = 0.524904
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Si': BEGIN
  lx_tZ = 14.
  lx_tA = 28.08
  lx_trho = 2.32
; lines from this target
  lx_tEKa = 1.73998
  lx_tEKb = 1.83594
  lx_tELa = -1
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END
; Super-d-duper kludge to get SiO2 spectrum - what a hacker!
'SiO': BEGIN
  lx_tZ = 14.
  lx_tA = 28.08
  lx_trho = 2.32
; lines from this target
  lx_tEKa = 1.73998
  lx_tEKb = 1.83594
  lx_tELa = 0.524904
  lx_tELb = -1
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Ti': BEGIN
  lx_tZ = 22.
  lx_tA = 47.9
  lx_trho = 4.5
; lines from this target
  lx_tEKa = 4.51090
  lx_tEKb = 4.93186
  lx_tELa = 0.452160
  lx_tELb = 0.458345
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END


'Cr': BEGIN
  lx_tZ = 24.
  lx_tA = 52.
  lx_trho = 7.14
; lines from this target
  lx_tEKa = 5.41479
  lx_tEKb = 5.94677
  lx_tELa = 0.572932
  lx_tELb = 0.582898
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Fe': BEGIN
  lx_tZ = 26.
  lx_tA = 56.
  lx_trho = 7.87
; lines from this target
  lx_tEKa = 6.400
  lx_tEKb = 7.059
  lx_tELa = 0.704
  lx_tELb = 0.717
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Ni': BEGIN
  lx_tZ = 28.
  lx_tA = 58.69
  lx_trho = 8.90
; lines from this target
  lx_tEKa = 7.47815
  lx_tEKb = 8.26466
  lx_tELa = 0.8515
  lx_tELb = 0.8688
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Cu': BEGIN
  lx_tZ = 29.
  lx_tA = 63.5
  lx_trho = 8.96
; lines from this target
  lx_tEKa = 8.04787
  lx_tEKb = 8.90539
  lx_tELa = 0.929682
  lx_tELb = 0.949838
  lx_tEMa = -1
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Zr': BEGIN 
  lx_tZ = 40.
  lx_tA = 91.22
  lx_trho = 6.52
; lines from this target
  lx_tEKa = 15.746
  lx_tEKb = 17.6678
  lx_tELa = 2.04236
  lx_tELb = 2.1244
  lx_tEMa = 0.170
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Nb': BEGIN 
  lx_tZ = 41.
  lx_tA = 92.9
  lx_trho = 8.57
; lines from this target
  lx_tEKa = 16.6151
  lx_tEKb = 18.6225
  lx_tELa = 2.16589
  lx_tELb = 2.2574
  lx_tEMa = 0.180
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Mo': BEGIN 
  lx_tZ = 42.
  lx_tA = 95.9
  lx_trho = 10.2
; lines from this target
  lx_tEKa = 17.4795
  lx_tEKb = 19.6085
  lx_tELa = 2.29319
  lx_tELb = 2.4
  lx_tEMa = 0.193
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Ag': BEGIN 
  lx_tZ = 47.
  lx_tA = 107.868
  lx_trho = 10.5
; lines from this target
  lx_tEKa = 22.1629
  lx_tEKb = 24.94
  lx_tELa = 2.9843
  lx_tELb = 3.1509
  lx_tEMa = 0.3
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'Sn': BEGIN 
  lx_tZ = 50.
  lx_tA = 118.71
  lx_trho = 7.28
; lines from this target
  lx_tEKa = 25.2713
  lx_tEKb = 28.4860
  lx_tELa = 3.44398
  lx_tELb = 3.6628
  lx_tEMa = 0.4
  lx_tEMb = -1
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

'W': BEGIN
  lx_tZ = 74.
  lx_tA = 183.9
  lx_trho = 19.35
; lines from this target
  lx_tEKa = 58.864
  lx_tEKb = 67.586
  lx_tELa = 8.396
  lx_tELb = 9.959
  lx_tEMa = 1.775
  lx_tEMb = 1.835
; line fluxes, -1 if not defines/calculated 
  lx_FlKa = -1
  lx_FlKb = -1
  lx_FlLa = -1
  lx_FlLb = -1
  lx_FlMa = -1
  lx_FlMb = -1
  END

ELSE: BEGIN
  print, ' labx_target: No information on target: ', lx_tName
  STOP
  END

ENDCASE

RETURN
END
