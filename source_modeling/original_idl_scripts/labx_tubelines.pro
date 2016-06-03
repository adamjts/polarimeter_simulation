PRO labx_tubelines
;
; This procedure calculates the intensity of the lines from a source
; based on the continuum value and the line-to-continuum ratio.
; The line fluxes (phots/sec steradian) are left in the common
; variables lx_FlKa, etc.
;
; 4/15/93 - dd
;

@labx_common

if(lx_tEKa GT 0.) then $
lx_FlKa = labx_linetoc(lx_tEKa,'Ka')*labx_tubeinuum(lx_tEKa)
if(lx_tEKb GT 0.) then $
lx_FlKb = labx_linetoc(lx_tEKb,'Kb')*labx_tubeinuum(lx_tEKb)
if(lx_tELa GT 0.) then $
lx_FlLa = labx_linetoc(lx_tELa,'La')*labx_tubeinuum(lx_tELa)
if(lx_tELb GT 0.) then $
lx_FlLb = labx_linetoc(lx_tELb,'Lb')*labx_tubeinuum(lx_tELb)
if(lx_tEMa GT 0.) then $
lx_FlMa = labx_linetoc(lx_tEMa,'Ma')*labx_tubeinuum(lx_tEMa)
if(lx_tEMb GT 0.) then $
lx_FlMb = labx_linetoc(lx_tEMb,'Mb')*labx_tubeinuum(lx_tEMb)

RETURN
END
