PRO source_spectrum
;
; Plots the spectrum of the source as configured
;

@labx_common
@b_on_w

; Calculate the spectrum - puts it in lx_tubespec,
;  units of phots/ (sec bin steradian)
labx_tubespec

; units of phots/ (sec bin steradian mA)
lx_tubespec = lx_tubespec/(lx_sI)

plot_oo, lx_es, lx_tubespec, psym=10, $
	xrange = [0.1,10.], yrange = [1.E8, 1.E14], $
        title = 'Source spectrum', $
	xtitle = 'Energy (keV, bin size = '+ $
		STRING(lx_estep*1000.0,FORMAT="(F6.2)")+' eV)', $
	ytitle = 'Flux  ( photons / sec bin steradian mA )'

; Use 1.0 mA for the current for the plot becasue it's in units
; of per mA and another current value would confuse.
save_sI = lx_sI
lx_sI = 1.0
notes = [1,1,0,0,0,0,0,0,0,0,0]
labx_annotate, notes, 0.15, 0.28
lx_sI = save_sI

RETURN
END
