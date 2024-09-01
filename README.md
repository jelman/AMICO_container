Forked from https://github.com/TIGRLab/AMICO_container for use on VETSA project.

# Docker container for AMICO

A docker container implementing the "linear framework for Accelerated Microstructure Imaging via Convex Optimization (AMICO)". Original implementation [here](https://github.com/daducci/AMICO).


# Usage:

`docker run --rm -v <study directory>:/input jaelman/amico /input <subject ID>`


# Optional arguments

`--bvals <bvals file>` - Path to the bvals file. Interpreted relative to the study folder.

`--bvecs <bvecs file>` - Path to the bvecs file. Interpreted relative to the study folder.

`--scheme_file <scheme file>` - Path to the scheme file. If the file doesn't exist, it will be created from bvals and bvecs.

`--dwi_file <dwi file>` - Name of the DWI file. Interpreted relative to the subject folder.

`--mask_file <mask file>` - Name of the mask file. Interpreted relative to the subject folder.

`--delimiter <delimiter>` - Delimiter to be used for bvals and bvecs files. Defaults to whitespace.

`--parallel_diff <diff value>` - Set alternative intrinsic parallel diffusivity value. Defaults to 1.7e-3.

`--threads <number of threads>` - Number of threads to use. Defaults to 1.

`--compute_rmse` - Compute the root mean square error between the predicted and the measured signal. Defaults to False.

`--compute_nrmse` - Compute the normalized root mean square error between the predicted and the measured signal. Defaults to False.

`--save_modulated` - Save the modulated NDI and ODI maps for tissue-weighted means described in Parker, Christopher S. et al. 2021. Defaults to False.

`--help` - Show help message and exit.




