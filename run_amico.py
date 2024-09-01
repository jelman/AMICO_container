#!/usr/bin/env python
"""
Run the default AMICO process
"""

import argparse
import os
import amico

BASEDIR = '/input'


def main():
    study_folder = os.path.join(BASEDIR, args.study)
    if not os.path.isdir(study_folder):
        raise RuntimeError('Folder:{} not found'.format(study_folder))

    subject_folder = os.path.join(study_folder, args.subject)
    if not os.path.isdir(subject_folder):
        raise RuntimeError('Folder:{} not found'.format(subject_folder))

    bvals_file = os.path.join(study_folder, args.bvals)
    bvecs_file = os.path.join(study_folder, args.bvecs)

    scheme_file = args.scheme_file

    if scheme_file and not os.path.isfile(scheme_file):
        if not os.path.isdir(bvals_file) and scheme_file:
            raise RuntimeError('BVals file:{} not found'.format(bvals_file))

        if not os.path.isdir(bvecs_file) and scheme_file:
            raise RuntimeError('BVecs file:{} not found'.format(bvecs_file))

    dwi_file = os.path.join(subject_folder, args.dwi_file)
    if not os.path.isfile(dwi_file):
        raise RuntimeError('DWI file:{} not found'.format(dwi_file))

    mask_file = os.path.join(subject_folder, args.mask_file)
    if not os.path.isfile(mask_file):
        raise RuntimeError('Mask file:{} not found'.format(mask_file))
    
    dPar = args.parallel_diff
    nb_threads = args.threads
    rmse = args.compute_rmse
    nrmse = args.compute_nrmse
    save_modulated = args.save_modulated

    # start processing here
    amico.core.setup()
    ae = amico.Evaluation(study_folder, subject_folder)
    delimiter = args.delimiter

    if not scheme_file:
        scheme_file = amico.util.fsl2scheme(bvals_file, bvecs_file, delimiter=delimiter)
    if not os.path.isfile(scheme_file):
        scheme_file = amico.util.fsl2scheme(bvals_file, bvecs_file, scheme_file, delimiter=delimiter)

    ae.load_data(dwi_filename=dwi_file,
                 scheme_filename=scheme_file,
                 mask_filename=mask_file)

    # Set model to NODDI
    ae.set_model("NODDI")
    
    # Set parallel diffusivity
    if dPar:
        ae.model.set(dPar)

    # Generate kernels
    ae.generate_kernels()
    
    # Set number of threads
    ae.set_config('nthreads', nb_threads)
    
    # Set configuration options
    ae.set_config('doComputeRMSE', rmse)
    ae.set_config('doComputeNRMSE', nrmse)
    ae.set_config('doSaveModulatedMaps', save_modulated)

    # Load kernels and fit the model
    ae.load_kernels()
    ae.fit()
    if dPar:
        ae.save_results( path_suffix=f'_dPar={dPar:.2e}' )
    else:
        ae.save_results()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('study', nargs='?',
                        help="Path to the folder containing all subjects."
                        "Interpreted relative to /input",
                        default="/input")
    parser.add_argument('subject', nargs='?',
                        help="Path to the subject folder."
                        "Interpreted relative to study folder")
    parser.add_argument("--bvals", nargs='?',
                        help="Path to the bvals file."
                        "Interpreted relative to the study folder",
                        default='merged.bval')
    parser.add_argument("--bvecs", nargs='?',
                        help="Path to the bvecs file."
                        "Interpreted relative to the study folder",
                        default='merged.bvec')
    parser.add_argument("--scheme_file", nargs='?',
                        help="Path to the scheme file."
                        "If file doesn't exist it will be created from bvals"
                        " and bvecs",
                        default=None)
    parser.add_argument("--dwi_file", nargs='?',
                        help="Name of the DWI file."
                        " Interpreted relative to subject folder",
                        default='dwi_brain.nii.gz')
    parser.add_argument("--mask_file", nargs='?',
                        help="Name of the mask file."
                        " Interpreted relative to subject folder",
                        default="dwi_brain_mask.nii.gz")
    parser.add_argument("--parallel_diff", nargs='?',
                        help="Set alternative intrinsic parallel diffusivity value."
                        "  NODDI default is 1.7e-3",
                        default=None)
    parser.add_argument("--delimiter",
                        help="Delimiter to be used for bvals and bvecs files")
    parser.add_argument("--threads", nargs='?', 
                        help="Number of threads to use for parallel processing",
                        default=1)
    parser.add_argument("--compute_rmse", action='store_true', 
                        help="Compute the root mean square error between the predicted and the measured signal.", 
                        default=False)
    parser.add_argument("--compute_nrmse", action='store_true', 
                    help="Compute the normalized root mean square error between the predicted and the measured signal.", 
                    default=False)
    parser.add_argument("--save_modulated", action='store_true', 
                    help="Save the modulated NDI and ODI maps for tissue-weighted means described in Parker, Christopher S. et al. 2021.", 
                    default=False)
    args = parser.parse_args()
    main()
