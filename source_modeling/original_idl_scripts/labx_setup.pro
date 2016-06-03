PRO labx_setup

@labx_common

; Setup the target and operating voltages if not already
if n_elements(lx_tName) EQ 0 then lx_tName = 'Cr'
labx_target

; Setup source operating parameters
if n_elements(lx_sV) EQ 0 then lx_sV = 10.		; kV
if n_elements(lx_sI) EQ 0 then lx_sI = 0.1		; mA
if n_elements(lx_sAngle) EQ 0 then lx_sAngle = 45.	; deg.
if n_elements(lx_sH) EQ 0 then lx_sH = 0.5		; mm
if n_elements(lx_sW) EQ 0 then lx_sW = 0.5		; mm
if n_elements(lx_lines_off) EQ 0 then lx_lines_off = 0  ; use lines normaly

; Setup energies for the continuum, etc.
if n_elements(lx_emax) EQ 0 then lx_emax = 10.0		; keV
if n_elements(lx_emin) EQ 0 then lx_emin = 0.10		; keV
if n_elements(lx_estep) EQ 0 then lx_estep = 0.010	; keV
if n_elements(lx_es) EQ 0 then $
	lx_es = lx_emin+lx_estep*INDGEN(1+(lx_emax-lx_emin)/lx_estep)

; Setup detector parameters
pspc
if n_elements(lx_dname) EQ 0 then lx_dname = 'PSPC'
if n_elements(lx_dblur) EQ 0 then lx_dde = 0.220	; keV
if n_elements(lx_dres) EQ 0 then lx_dpixel = 0.200	; mm
if n_elements(lx_time) EQ 0 then lx_time = 60.		;sec
; For flow counter:
pspc
if n_elements(lx_tBe) EQ 0 then lx_tBe = 0.0		; microns
if n_elements(lx_tpoly) EQ 0 then lx_tpoly = 0.7	; microns
if n_elements(lx_tAl) EQ 0 then lx_tAl = 0.1		; microns
if n_elements(lx_tvyns) EQ 0 then lx_tvyns = 0.		; ug/cm^2
if n_elements(lx_mesh) EQ 0 then lx_mesh = 0.		; ug/cm^2
if n_elements(lx_tdet) EQ 0 then lx_tdet = 12.5		; mm
if n_elements(lx_PAr) EQ 0 then lx_PAr = 1.0		; atm
if n_elements(lx_PKr) EQ 0 then lx_PKr = 0.0		; atm
if n_elements(lx_PXe) EQ 0 then lx_PXe = 0.0		; atm

; Setup Slit system parameters
if n_elements(lx_Dgd) EQ 0 then lx_Dgd = 8613.8		; mm
IF n_elements(lx_Dog) EQ 0 THEN lx_Dog =  203.          ; mm
IF n_elements(lx_Dso) EQ 0 THEN lx_Dso = 8789.0		; mm
if n_elements(lx_slitW) EQ 0 then lx_slitW = 0.2	; mm
if n_elements(lx_slitH) EQ 0 then lx_slitH = 4.*3.94	; mm

; Setup grating parameters
heg
if n_elements(lx_gp) EQ 0 then lx_gp = 4000.		; A
if n_elements(lx_gm) EQ 0 then lx_gm = 1		; 
if n_elements(lx_gmat) EQ 0 then lx_gmat = 'Au'		; 
if n_elements(lx_gthk) EQ 0 then lx_gthk = 5000.	; A
if n_elements(lx_gline) EQ 0 then lx_gline = 1800.	; A
if n_elements(lx_gdpp) EQ 0 then lx_gdpp = 2.5E-4	; dp/p value
if n_elements(lx_gpoly) EQ 0 then lx_gpoly = 0.5	; um
if n_elements(lx_gplating) EQ 0 then lx_gplating = 1.0	; relative thkness
if n_elements(lx_gtilt) EQ 0 then lx_gtilt = 0.0	; grating tilt
if n_elements(lx_gshape) EQ 0 then lx_gshape = tilt_set_shape(10)

; Setup Hettrick parameters
if n_elements(lx_htrslit) EQ 0 then lx_htrslit = 30.	; microns
if n_elements(lx_htrres) EQ 0 then labx_hettr_res

; Setup Optic parameters
if n_elements(lx_oangle) EQ 0 then lx_oangle = 0.5	; degrees
if n_elements(lx_olength) EQ 0 then BEGIN		; mm
    lx_olength = lx_slitW/TAN(lx_oangle*!DTOR)
  END
if n_elements(lx_ob) EQ 0 then lx_ob = 1.0		; arc sec rms 1-D
if n_elements(lx_oeffic) EQ 0 then lx_oeffic = 0.7	; refl effic.

RETURN
END


