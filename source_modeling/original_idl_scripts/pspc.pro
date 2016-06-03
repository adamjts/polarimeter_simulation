PRO pspc
; sets nominal values of the PSPC counter into COMMON
; 4/19/96 changed lx_tpoly to 7.5 microns for better agreement
; with PSPC Cu data...
@labx_common

lx_dname='PSPC'
lx_tBe=0.
;;lx_tpoly=8.5    ; Kapton
lx_tpoly=7.5    ; Kapton
lx_tAl=0.05	; 500A
lx_tvyns=0. ; ug/cm^2
lx_tmylar=0.0 ;um
lx_tdet=12.5  ; mm thick
lx_PAr=0.9  ; atm
lx_PKr=0.
lx_PXe=0.0
lx_mesh=0.0 ; % trans

lx_dde=TOTAL(labx_det_res(lx_es))/n_elements(lx_es)
; 4/20/95 Based on HX220p000.950214 data the X FWHM may be more like 0.8;
;         Ti data might indicate ~0.5 mm FWHM so call it 0.7 for now.
; lx_dpixel=0.3 ;mm
lx_dpixel=0.7 ;mm

RETURN
END
