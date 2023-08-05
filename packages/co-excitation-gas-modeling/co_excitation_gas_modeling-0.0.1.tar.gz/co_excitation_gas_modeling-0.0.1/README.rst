##########################
co-excitation-gas-modeling
##########################

********************************************************************************************************************************
A Python Package for Galaxy Mean Molecular Gas Density and Gas Kinetic Temperature Estimation Using Carbon Monoxide Line Ratio.
********************************************************************************************************************************




A simple introduction:
======================

This Python package provides functions to estimate a galaxy's cold molecular gas mean density and kinetic temperature using Carbon Monoxide (CO) molecular line flux density ratio.

The motivation is that the galaxies emit CO spectral lines, and different transition of CO lines have different strength. The line ratio is affected by the cold molecular gas density and kinetic temperature. At global galaxy scales, the observed line ratio can probe the mean molecular gas density and temperature to some extent. Based on the work of Liu et al. (2020) who compiled the CO J=5-4 / J=2-1 (R52) line ratios in a sample of galaxies from local Universe to high redshift, a density probability distribution function (PDF) gas modeling has been studied and found promising in linking observed galaxy CO line ratios to physical cold molecular gas mean density and kinetic temperature. The highlight of this work is that it uses a density PDF to simulate the gas density distribution in a galaxy, thus provide more realistic CO excitation than single-state gas large velocity gradient radiative transfer modeling. See `Leroy et al. (2017) <https://ui.adsabs.harvard.edu/abs/2017ApJ...835..217L/abstract>` for a similar density-PDF gas modeling work. 
This code is thus based on the Liu et al. (2020) model grid and can convert an input CO line ratio to a fitting range of cold molecular gas density and kinetic temperature. 




A simple usage:
===============

To input a CO J=5-4/J=2-1 line ratio (in Jy km s-1 units), and output cold molecular gas mean density (<nH2>) and kinetic temperature (Tkin) ranges:

.. code-block:: python

    import co_excitation_gas_modeling as coexc
    coexc.help()
    fit_result = coexc.fit_line_ratio(z=4.755, R72=0.86/0.09, e_R72=0.01).help()
    print(fit_result)
    print(fit_result['lg_nH2'])
    print(fit_result['T_kin'])




Future work:
================

A future work will be conducted to fit CO spectral line energy distribution. 



Acknowledgement:
================






