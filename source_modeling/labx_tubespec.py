import numpy as np

from labx_target import labx_target
from source_spectrum import labx_tubeinuum, labx_tubelines

def labx_tubespec(spec):
    #PRO labx_tubespec, XRCF = xrcf
    #+
    # This routine calculates the energies (lx_es) and tube spectrum and
    # puts the spectrum in lx_tubespec
    #  units of phots/ (sec bin steradian)
    #-
    # 3/20/97 Modified to add KEYWORD XRCF in order to improve agreement
    # with XRCF...
    #               - add satellite lines to Al-K, Mg-K
    #               - broaden other lines: C-K, O-K, all L lines
    # 12/17/97 dd Broaden Be also.  Other changes to Mg, etc.
    # 4/16/99 dd Modify Nb lines to remove "2.03" HRMA-Area effect
    #            and add Nb at 1.902
    #            Modify Mo line: remove the "2.03" etc lines...
    #            Adjust Sn Ll line E...
    # 5/31/99 dd Adjust for agreement with HSI measured spectra...

    spec.es = np.arange(spec.emin, spec.emax + spec.estep/2., spec.estep)

    labx_target(spec)

    # Calculate the continuum using the bin spacing and the dE value
    spec.tubespec = labx_tubeinuum(spec, spec.es) * 1000.*(spec.es[1]-spec.es[0]) #eV
    # units of spec.tubespec are now photons/sec/steradian

    # catch an undefined spec.lines_off
    #if len(spec.lines_off) < 0:
    #if spec.lines_off != 1:
    #    spec.lines_off = 0

    if (spec.lines_off != 1):  #optionally turn off line emmision
        # Calculate the line intensities
        labx_tubelines(spec)

        # Put the lines in the spectrum
        line_es = np.array([spec.tEKa, spec.tEKb, spec.tELa, spec.tELb, spec.tEMa, spec.tEMb])
        line_fs = np.array([spec.FlKa, spec.FlKb, spec.FlLa, spec.FlLb, spec.FlMa, spec.FlMb])
        # and allow them to be broadened by specifying an E/dE_fwhm value,
        # -1 indicates "delta function"
        line_edes = -1. + 0.*line_es  # same size as line_es
        # These three arrays that define the lines are in common as
        # the variables spec.line_es, 'fs, 'edes.

        # Put these values into common spec container
        spec.line_es = line_es
        spec.line_fs = line_fs
        spec.line_edes = line_edes

        for il in range(0, len(line_es)):
        # Check for a non-zero flux
            if line_fs[il] > 0:
            # Check for line in es range
                if (line_es[il] > spec.es[0]) and (line_es[il] < spec.es[-2]):
                    # Go through the array and find where its flux goes:
                    for ie in range(0, len(spec.es)-1):
                        if(spec.es[ie] <= line_es[il]) and (spec.es[ie+1] > line_es[il]):
                            # here's where it goes, now blur it?
                            if line_edes[il] < 0.:
                                # no blur
                                spec.tubespec[ie] += line_fs[il]
                            else:
                                # blur it
                                # how many bins is sigma?
                                sigma_bins = ( (line_es[il]/(spec.es[1]-spec.es[0]))/line_edes[il] )/ 2.35
                                sig_bins = int(sigma_bins)
                                if sig_bins <= 0:
                                	sig_bins = 1
                                # go out to -/+ 4 sigma so use 4*sig_bins+1+4*sig_bins points total
                                array = float(np.arange(2*4*sig_bins+1))
                                sigs = (array-4.0*sig_bins) / float(sigma_bins)
                                gdist = np.exp( -1.0*(sigs)**2/2.)
                                # Normalize it and multiply by the flux
                                gdist = line_fs[il] * gdist/sum(gdist)
                                # and add it in in right place...
                                spec.tubespec[ie-4*sig_bins:ie+4*sig_bins] += gdist
                #end es check
            #end flux check
    #end lines off
