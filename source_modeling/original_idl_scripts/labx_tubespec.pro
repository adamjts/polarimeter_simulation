PRO labx_tubespec, XRCF = xrcf
;+
; This routine calculates the energies (lx_es) and tube spectrum and
; puts the spectrum in lx_tubespec
;  units of phots/ (sec bin steradian)
;-
; 3/20/97 Modified to add KEYWORD XRCF in order to improve agreement
; with XRCF...
;               - add satellite lines to Al-K, Mg-K
;               - broaden other lines: C-K, O-K, all L lines
; 12/17/97 dd Broaden Be also.  Other changes to Mg, etc.
; 4/16/99 dd Modify Nb lines to remove "2.03" HRMA-Area effect
;            and add Nb at 1.902
;            Modify Mo line: remove the "2.03" etc lines...
;            Adjust Sn Ll line E...
; 5/31/99 dd Adjust for agreement with HSI measured spectra...
@labx_common

lx_es = lx_emin+lx_estep*INDGEN(1+(lx_emax-lx_emin)/lx_estep)

labx_target

; Calculate the continuum using the bin spacing and the dE value
lx_tubespec = labx_tubeinuum(lx_es) * 1000.*(lx_es(1)-lx_es(0)) ;eV

; catch an undefined lx_lines_off
if n_elements(lx_lines_off) LE 0 then lx_lines_off = 0

if (lx_lines_off NE 1) then begin  ;optionally turn off line emmision
; Calculate the line intensities
labx_tubelines

; Put the lines in the spectrum
line_es = [lx_tEKa, lx_tEKb, lx_tELa, lx_tELb, lx_tEMa, lx_tEMb]
line_fs = [lx_FlKa, lx_FlKb, lx_FlLa, lx_FlLb, lx_FlMa, lx_FlMb]
; and allow them to be broadened by specifying an E/dE_fwhm value,
; -1 indicates "delta function"
line_edes = -1. + 0.*line_es  ; same size as line_es
; These three arrays that define the lines are in common as
; the variables lx_line_es, 'fs, 'edes.


; For XRCF modeling make some changes
; including adding finite E/dE values...  -1 indicates narrow line
; default is no additional broadening...

if KEYWORD_SET(XRCF) then begin
  ; - - - - - - - - -
  ; Add other lines, modify line strength, etc.
  if lx_tname EQ 'Al' then begin
    ; Add satellites... from analysis of 970109/hsi108034.fits (Alx2)
    ; Energy and fluxes are fractions times K line values
    line_es = [line_es, 1.0062*line_es(0)]
    line_fs = [line_fs, 0.125*line_fs(0)]
    ; Reduce the Kbeta based on HSI data (D-HXH-FC-28.003)
    line_fs(1) = 0.4 * line_fs(1)
    line_edes = [line_edes, 1.*line_edes(0)]
    ; Add more continuum based on 'FC-1.011, '3D-2.001
    lx_tubespec = 1.5* lx_tubespec
  end
  if lx_tname EQ 'Be' then begin
    ; Increase the line strength based on D-LXH-3D-12.004, 970125/hsi110192
    line_fs = 8.75 * line_fs
  end
  if lx_tname EQ 'B' then begin
    ; add an extra component to better model shape D-LXH-3D-22.045
    line_es = [line_es, 0.965*line_es(0)]
    line_es(0) = 1.002 * line_es(0)
    line_fs = 6.0*[line_fs, 0.085*line_fs(0)]
    lx_tubespec = 50.0*lx_tubespec
    line_edes = [line_edes, line_edes(0)]
  end
  if lx_tname EQ 'C' then begin
    ; add anextra component to better model shape D-LXH-3D-11.047
    line_es = [line_es, 0.965*line_es(0)]
    line_es(0) = 1.002 * line_es(0)
    line_fs = 0.6*[line_fs, 0.085*line_fs(0)]
    lx_tubespec = 7.5*lx_tubespec
    line_edes = [line_edes, line_edes(0)]
  end
  if lx_tname EQ 'Cu' then begin
    ; Energy and flux is fraction times La line values
    ; reduce the Cu l-b line to agree with spectrum
    line_fs(3) = 0.75*line_fs(3)
    line_es = [line_es, 0.8698*line_es(2), 0.8698*line_es(3), $
			0.9797*line_es(2), 0.9797*0.8698*line_es(2)]
    line_fs = [line_fs, 0.095*line_fs(2), 0.095*line_fs(3), $
			0.01*line_fs(2), 0.01*line_fs(2)]
    line_edes = [line_edes, line_edes(2),line_edes(3), $
			line_edes(2), line_es(2)]
    ; increase La a bit
    line_fs(2) = 1.1*line_fs(2)
    ; reduce the continuum a bit
    lx_tubespec = 0.6*lx_tubespec
    ; Increase the K lines
    line_fs(0:1) = 2.0 * line_fs(0:1)
  end
  if lx_tname EQ 'Fe' then begin
    ; Add satellites...
    ; Energy and flux is fraction times La line values
    ; Change the L values
    line_fs(2) = 0.7*line_fs(2)
    line_fs(3) = 2.0*line_fs(3)
    line_es = [line_es, 0.8725*line_es(2), 0.8725*line_es(3), $
			0.9797*line_es(2), 0.9797*0.8725*line_es(2)]    
    line_fs = [line_fs, 0.950*line_fs(2), 1.2*0.950*line_fs(3), $
			1.2*0.16*line_fs(2), 1.2*0.16*0.950*line_fs(2)]
    line_fs(3) = 1.2*line_fs(3)
    line_edes = [line_edes, line_edes(2), line_edes(3), $
			line_edes(2), line_edes(2)]
    ; Adjust the continuum for Fe-L lines... 
    lx_tubespec = 1.0*lx_tubespec
    ; Increase Ka,b lines to continuum
    line_fs(0:1) = 2.0 * line_fs(0:1)
  end
  if lx_tname EQ 'Ni' then begin
    ; Add satellites...
    ; Energy and flux is fraction times La line values
    line_fs(2) = 1.0*line_fs(2)
    line_fs(3) = 0.8*line_fs(3)
    line_es = [line_es, 0.8725*line_es(2), 0.8725*line_es(3), $
			0.9797*line_es(2), 0.9797*0.8725*line_es(2)]    
    line_fs = [line_fs, 0.5*line_fs(2), 1.2*0.5*line_fs(3), $
			1.2*0.15*line_fs(2), 1.2*0.15*0.5*line_fs(2)]
    line_fs(3) = 1.0*line_fs(3)
    line_edes = [line_edes, line_edes(2), line_edes(3), $
			line_edes(2), line_edes(3)]
    ; Reduce continuum
    lx_tubespec = 0.7*lx_tubespec
  end
  if lx_tname EQ 'O' then begin
    ; Broaden the O-K line by also including a second line
    line_es = [line_es, 0.991*line_es(0)]
    line_fs = [line_fs, 0.3*line_fs(0)]
    line_edes = [line_edes, 1.*line_edes(0)]
  end
  if lx_tname EQ 'Ti' then begin
    ; Add the low-energy other line seen on all Ls:
    ; Energy and flux is fraction times La line values
    ; Adjust the Lb fluxes:
    line_fs(3) = 0.8*line_fs(3)
    line_es = [line_es, 0.8714*line_es(2), 0.8714*line_es(3), $
			0.005+0.9797*line_es(2), 0.9797*0.8714*line_es(2)]    
    line_fs = [line_fs, 0.9*line_fs(2), 0.9*line_fs(3), $
			0.2*line_fs(2), 0.7*line_fs(2)]
    line_edes = [line_edes, line_edes(2), line_edes(3), $
			line_edes(2), line_edes(3)]
    line_fs(2) = 0.95*line_fs(2)
    ;
    ; K-line set with E-HXH-3D-10.007:
    ; Adjust the Ka, Kb fluxes slightly
    line_fs(0) = 1.5 * line_fs(0)
    line_fs(1) = 0.8 * line_fs(1)
    ; Increase continuum
    lx_tubespec = 1.5*lx_tubespec
  end
  if lx_tname EQ 'SiO' then begin
    ; Broaden the O-K line by also including a second line
    ; and add a satellite line to the Si-K
    line_es = [line_es, 0.991*line_es(2), 1.0074*line_es(0)]
    line_fs = [line_fs, 0.3*line_fs(2), 0.1*line_fs(0)]
    line_edes = [line_edes, 1.*line_edes(2), line_edes(0)]
    ; and add a little Cu-L in for XRCF source!
    line_es(3) = 0.9297
    line_es(4) = 0.9498
    line_fs(3) = 0.65*line_fs(2)  ; relative to the O-K
    line_fs(4) = 0.33*line_fs(3)
    ; 12/29/97 dd Reduce the O line flux relative to continuum
    ; for XRCF... Based mostly on D-LXH-3D-11.042 .
    line_fs(2) = 0.5*line_fs(2)
    line_fs(6) = 0.5*line_fs(6)
    ; Adjust the Si-K lines w.r.t. continuum
    line_fs(0) = 1.0*0.26*line_fs(0)
    line_fs(1) = 1.1*0.2*line_fs(1)
    line_fs(7) = 1.0*0.25*line_fs(7)
    ; Adjust absolute continuum based on D-HXH-3D-11.037 (high V)
    ; and D-HXH-3D-11.043 (low V)
    if lx_sV GT 2.0 then begin
      lx_tubespec = lx_tubespec
    end else begin
      lx_tubespec = 9.5*lx_tubespec
    end
  end
  if lx_tname EQ 'Mg' then begin
    ; Add satellites... from analysis of 970116/hsi109003i2.fits
    ; (D-HXH-dF-16.003)
    ; Energy and fluxes are fractions times K line values
    line_es = [line_es, 1.0065*line_es(0)]
    line_fs = [line_fs, 1.1*0.086*line_fs(0)]
    line_es = [line_es, 1.0077*line_es(0)]
    line_fs = [line_fs, 1.1*0.062*line_fs(0)]
    line_es = [line_es, 1.01547*line_es(0)]
    line_fs = [line_fs, 0.024*line_fs(0)]
    ; Reduce the Kbeta based on HSI data (D-HXH-FC-28.003)
    line_fs(1) = 0.2 * line_fs(1)
    line_edes = [line_edes, 1.*line_edes(0), 1.*line_edes(0), 1.*line_edes(0)]
    line_fs = 0.3 * line_fs
    ; increase the Ka line
    line_fs(0) = 1.1*line_fs(0)
  end
  if lx_tname EQ 'Nb' then begin
    ; Energy and fluxes are fractions times L line values
    line_es = [line_es, 0.8781*line_es(2)]
    line_fs = [line_fs, 0.040*line_fs(2)]
    line_edes = [line_edes, line_edes(2)]
    line_fs(2) = 1.50*0.72*line_fs(2)
    line_fs(3) = 1.0*line_fs(3) ; 11.0
    ; Bring line and continuum up to agree better with HSI value
    line_fs = 2.0*line_fs
    lx_tubespec = 2.0* lx_tubespec
  end
  if lx_tname EQ 'Mo' then begin
    ; Energy and fluxes are fractions times L line values
;;    line_es = [line_es, 0.8853*line_es(2), 0.92455*line_es(2), $
;;			1.0728*line_es(2)]
;;    line_fs = [line_fs, 0.16*line_fs(2), 0.09*line_fs(2), $
;;			0.15*line_fs(2)]
    ; Add the Ll,
    line_es = [line_es,  0.87907*line_es(2), $
			1.0728*line_es(2)]
    line_fs = [line_fs,  0.05*line_fs(2), $
			0.7*0.15*line_fs(2)]
    line_fs(3) = 1.1*0.8 * line_fs(3)
    line_fs(2) = 1.1 * 1.05 * line_fs(2)
    line_edes = [line_edes, line_edes(2), line_edes(2)]
    ; reduce the continuum some
    lx_tubespec = 0.5 * lx_tubespec
  end
  if lx_tname EQ 'Ag' then begin
    line_es = [line_es, 0.8713*line_es(2), $
			1.01438*1.1059*line_es(2)]
    line_fs = [line_fs, 0.05*line_fs(2), $
			0.08*line_fs(2)]
    line_fs(2) = 0.80*line_fs(2)
    line_fs(3) = 0.6*line_fs(3)
    line_edes = [line_edes, line_edes(2), line_edes(2)]
    ; reduce the continuum some
    lx_tubespec = 0.5 * lx_tubespec
  end
  if lx_tname EQ 'Sn' then begin
    line_es = [line_es, 0.8841*line_es(2), $
			1.1339*line_es(2)]
    line_fs = [line_fs, 0.05*line_fs(2), $
			0.08*line_fs(2)]
    line_fs(2) = 1.15*0.9 * 0.58*line_fs(2)
    line_fs(3) = 1.15*0.7*0.58*line_fs(3)
    line_edes = [line_edes, line_edes(2), line_edes(2)]
    ; adjust the continuum some
    lx_tubespec = 1.5 * lx_tubespec
  end
  ; - - - - - - - - - - - 
  ; Add BROADENING to lines
  if lx_tname EQ 'Be' then begin
    ; value from hsi110192
    line_edes(0) = 12.
  end
  if lx_tname EQ 'B' then begin
    ; value from hsi110212
    line_edes(0) = 30.
    line_edes(6) = 25.
  end
  if lx_tname EQ 'C' then begin
    ; value from hsi109001i2, 108578i0
    line_edes(0) = 35.  ; 
    line_edes(6) = 25.  ; 
  end
  if lx_tname EQ 'Mg' then begin
    ; if "= -1" then E/dE ~ 3700.0 for given binning
    ; 980919: tried E/dE = 1200. but MARX simulation of
    ;         PSF/1D scan was too wide
    ; tried 2200, now try 1800: 9/29/98:
    line_edes(0) = 1800.  ; try to reduce as much as possible yet
                          ; keeping agreement w/XRCF data
  end
  if lx_tname EQ 'Cu' then begin
    ; value from hsi109525i0
    line_edes(2) = 150.
    line_edes(3) = 100.
    line_edes(6) = 150.
    line_edes(7) = 100.
    line_edes(8:9) = 25.
  end
  if lx_tname EQ 'Fe' then begin
    line_edes(2) = 120. ; 200
    line_edes(3) =  35. ; 200
    line_edes(6) = 120. ; 200
    line_edes(7) =  35.
    line_edes(8) =  20.
    line_edes(9) =  20.
  end
  if lx_tname EQ 'Mo' then begin
    ; E/dE ~300 for Mo Llines from
    ; XRCF 970125/hsi110154i0.fits
    line_edes(2:3) = 300.
    ; use same for the M line
    line_edes(4) = 300.
    line_edes(6) = 150.
    line_edes(7) = 40.
  end
  if lx_tname EQ 'Ag' then begin
    line_edes(2:3) = 300.
    ; use same for the M line
    line_edes(4) = 300.
    line_edes(6:7) = 150.
  end
  if lx_tname EQ 'Sn' then begin
    line_edes(2:3) = 300.
    ; use same for the M line
    line_edes(4) = 300.
    line_edes(6) = 150.
    line_edes(7) = 300.
  end
  if lx_tname EQ 'Nb' then begin
    line_edes(2:3) = 300.
    line_edes(6) = 300.
    ; use same for the M line
    line_edes(4) = 300.
  end
  if lx_tname EQ 'Ni' then begin
    line_edes(2) = 200.
    line_edes(3) =  35.
    line_edes(6) = 200.
    line_edes(7) =  35.
    line_edes(8) =  25.
    line_edes(9) =  25.
  end
  if lx_tname EQ 'O' then begin
    line_edes(0) = 120.
    line_edes(6) = 120.
  end
  if lx_tname EQ 'SiO' then begin
    line_edes(2) = 120.  ; O-K
    line_edes(3) = 150.  ; Cu-L contamination
    line_edes(4) = 100.  ; Cu-L contamination
    line_edes(6) = 120.  ; O-K
  end
  if lx_tname EQ 'Ti' then begin
    line_edes(2) = 120.
    line_edes(3) =  50.
    line_edes(6) = 120.
    line_edes(7) =  50.
    line_edes(8) =  40.
    line_edes(9) =  20.
  end
  print, 'labx_tubespec: line_es: ',line_es
  print, 'labx_tubespec: line_edes: ',line_edes
  print, 'labx_tubespec: line_fs: ',line_fs

end  ; of XRCF additions

; Put these values into common
lx_line_es = line_es
lx_line_fs = line_fs
lx_line_edes = line_edes

for il = 0, n_elements(line_es)-1 do begin
; Check for a non-zero flux
  if line_fs(il) GT 0 then begin
  ; Check for line in es range
    if (line_es(il) GT lx_es(0)) AND $
		(line_es(il) LT lx_es(n_elements(lx_es)-2)) $
      		then begin
      ; Go through the array and find where its flux goes:
      for ie = 0, n_elements(lx_es)-2 do begin
        if(lx_es(ie) LE line_es(il)) AND (lx_es(ie+1) GT line_es(il)) $
		then begin
          ; here's where it goes, now blur it?
          if line_edes(il) LT 0. then begin
            ; no blur
            lx_tubespec(ie) = lx_tubespec(ie)+line_fs(il)
          end else begin
            ; blur it
            ; how many bins is sigma?
            sigma_bins = ( (line_es(il)/(lx_es(1)-lx_es(0)))/line_edes(il) )/ 2.35
            sig_bins = FIX(sigma_bins)
            if sig_bins LE 0 then sig_bins = 1
            ; go out to -/+ 4 sigma so use 4*sig_bins+1+4*sig_bins points total
            sigs = (FLOAT(indgen(2*4*sig_bins+1))-4.0*sig_bins) / $
			FLOAT(sigma_bins)
            gdist = EXP( -1.0*(sigs)^2/2.)
            ; Normalize it and multiply by the flux
            gdist = line_fs(il) * gdist/TOTAL(gdist)
            ; and add it in in right place...
            lx_tubespec(ie-4*sig_bins:ie+4*sig_bins) = $
		lx_tubespec(ie-4*sig_bins:ie+4*sig_bins) + gdist
          end
        end
      end
    end ; es check
  end ;flux check
end
end ; lines off

RETURN
END
