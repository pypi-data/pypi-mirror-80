#!/usr/bin/env python
import argparse
import logging
import glob
import os
import pickle
import sys
from time import sleep

import numpy as np

from ..utils.misc import get_settings, write_hdf5_movie

LOGGER_FORMAT = (
    "%(relativeCreated)12d [%(filename)s:%(funcName)20s():%(lineno)s]"
    "[%(process)d] %(message)s"
)

DEFAULT_MCORR_SETTINGS = {
    "fr": 10,  # movie frame rate
    "decay_time": 0.4,  # length of a typical transient in second
    "pw_rigid": False,  # flag for performing piecewise-rigid motion correction
    "max_shifts": (5, 5),  # maximum allowed rigid shift
    "gSig_filt": (3, 3),  # size of high pass spatial filtering, used in 1p data
    "strides": (48, 48),
    "overlaps": (24, 24),
    "max_deviation_rigid": (
        3
    ),  # maximum deviation allowed for patch with respect to rigid shifts
    "border_nan": "copy",  # replicate values along the boundaries
}

DEFAULT_CNMF_PARAMETERS = {
    "method_init": "corr_pnr",  # use this for 1 photon
    "K": None,  # upper bound on number of components per patch, in general None
    "gSig": (3, 3),  # gaussian width of a 2D gaussian kernel
    "gSiz": (13, 13),  # average diameter of a neuron, in general 4*gSig+1
    "merge_thr": 0.7,  # merging threshold, max correlation allowed
    "p": 1,  # order of the autoregressive system
    "tsub": 2,  # downsampling factor in time for initialization
    "ssub": 1,  # downsampling factor in space for initialization,
    "rf": 40,  # half-size of the patches in pixels
    "stride": 20,  # amount of overlap between the patches in pixels
    "only_init": True,  # set it to True to run CNMF-E
    "nb": 0,  # number of background components (rank) if positive
    "nb_patch": 0,  # number of background components (rank) per patch if gnb>0
    "method_deconvolution": "oasis",  # could use 'cvxpy' alternatively
    "low_rank_background": None,
    "update_background_components": True,
    # sometimes setting to False improve the results
    "min_corr": 0.8,  # min peak value from correlation image
    "min_pnr": 10,  # min peak to noise ration from PNR image
    "normalize_init": False,  # just leave as is
    "center_psf": True,  # leave as is for 1 photon
    "ssub_B": 2,  # additional downsampling factor in space for background
    "ring_size_factor": 1.4,  # radius of ring is gSiz*ring_size_factor,
    "del_duplicates": True,
    "border_pix": 0,
}

DEFAULT_QC_PARAMETERS = {
    "min_SNR": 2.5,  # adaptive way to set threshold on the transient size
    "rval_thr": 0.85,
    "use_cnn": False,
}


def parse_args():
    parser = argparse.ArgumentParser(description="Suite2p parameters")
    parser.add_argument("--file", default=[], type=str, help="options")
    parser.add_argument("--ncpus", default=1, type=int, help="options")
    parser.add_argument("--motion_corr", action="store_true")
    parser.add_argument("--mc_settings", default="", type=str, help="options")
    parser.add_argument("--cnmf_settings", default="", type=str, help="options")
    parser.add_argument("--qc_settings", default="", type=str, help="options")
    parser.add_argument("--output", default="", type=str, help="options")
    args = parser.parse_args()

    file_path = args.file
    n_cpus = args.ncpus
    motion_correct = args.motion_corr
    mc_settings = args.mc_settings
    cnmf_settings = args.cnmf_settings
    qc_settings = args.qc_settings
    output_dir = args.output

    return (
        file_path,
        n_cpus,
        motion_correct,
        mc_settings,
        cnmf_settings,
        qc_settings,
        output_dir,
    )


def run(
    file_path,
    n_cpus,
    motion_correct: bool = True,
    quality_control: bool = False,
    mc_settings: dict = {},
    cnmf_settings: dict = {},
    qc_settings: dict = {},
    output_directory: str = "",
):
    mkl = os.environ.get("MKL_NUM_THREADS")
    blas = os.environ.get("OPENBLAS_NUM_THREADS")
    vec = os.environ.get("VECLIB_MAXIMUM_THREADS")
    print(f"MKL: {mkl}")
    print(f"blas: {blas}")
    print(f"vec: {vec}")

    # we import the pipeline upon running so they aren't required for all installs
    import caiman as cm
    from caiman.source_extraction.cnmf import params as params
    from caiman.source_extraction import cnmf

    # print the directory caiman is imported from
    caiman_path = os.path.abspath(cm.__file__)
    print(f"caiman path: {caiman_path}")
    sys.stdout.flush()

    # setup the logger
    logger_file = os.path.join(output_directory, "caiman.log")
    logging.basicConfig(
        format=LOGGER_FORMAT, filename=logger_file, filemode="w", level=logging.DEBUG,
    )

    # load and update the pipeline settings
    mc_parameters = DEFAULT_MCORR_SETTINGS
    for k, v in mc_settings.items():
        mc_parameters[k] = v
    cnmf_parameters = DEFAULT_CNMF_PARAMETERS
    for k, v in cnmf_settings.items():
        cnmf_parameters[k] = v
    qc_parameters = DEFAULT_QC_PARAMETERS
    for k, v in qc_settings.items():
        qc_parameters[k] = v
    opts = params.CNMFParams(params_dict=mc_parameters)
    opts.change_params(params_dict=cnmf_parameters)
    opts.change_params(params_dict=qc_parameters)

    # get the filenames
    if os.path.isfile(file_path):
        print(file_path)
        fnames = [file_path]
    else:
        file_pattern = os.path.join(file_path, "*.tif*")
        fnames = glob.glob(file_pattern)
    print(fnames)
    opts.set("data", {"fnames": fnames})

    if n_cpus > 1:
        print("starting server")
        # start the server
        n_proc = np.max([(n_cpus - 1), 1])
        c, dview, n_processes = cm.cluster.setup_cluster(
            backend="local", n_processes=n_proc, single_thread=False
        )
        print(n_processes)
        sleep(30)
    else:
        print("multiprocessing disabled")
        dview = None
        n_processes = 1

    print("starting analysis")
    print(f"perform motion correction: {motion_correct}")
    print(f"perform qc: {quality_control}")
    sys.stdout.flush()
    cnm = cnmf.CNMF(n_processes, params=opts, dview=dview)
    cnm_results = cnm.fit_file(
        motion_correct=motion_correct, include_eval=quality_control
    )

    print("evaluate components")
    sys.stdout.flush()
    Yr, dims, T = cm.load_memmap(cnm_results.mmap_file)
    images = Yr.T.reshape((T,) + dims, order="F")
    cnm_results.estimates.evaluate_components(images, cnm.params, dview=dview)
    print("Number of total components: ", len(cnm_results.estimates.C))
    print("Number of accepted components: ", len(cnm_results.estimates.idx_components))

    # save the results object
    print("saving results")
    cnm_results.save(cnm_results.mmap_file[:-4] + "hdf5")

    # if motion correction was performed, save the file
    # we save as hdf5 for better reading performance
    # downstream
    if motion_correct:
        print("saving motion corrected file")
        filename_base = os.path.splitext(cnm_results.mmap_file)[0]
        mcorr_fname = filename_base + "_mcorr.hdf5"
        dataset_name = cnm_results.params.data["var_name_hdf5"]
        fnames = cnm_results.params.data["fnames"]
        memmap_files = []
        for f in fnames:
            if isinstance(f, bytes):
                f = f.decode()
            base_file = os.path.splitext(f)[0]
            if cnm_results.params.motion["pw_rigid"]:
                memmap_pattern = base_file + "*_els_*"
            else:
                memmap_pattern = base_file + "*_rig_*"
            memmap_files += glob.glob(memmap_pattern)
        write_hdf5_movie(
            movie_name=mcorr_fname,
            memmap_files=memmap_files,
            frame_shape=cnm_results.dims,
            dataset_name=dataset_name,
        )

    # save the parameters in the same dir as the results
    final_params = cnm.params.to_dict()
    path_base = os.path.dirname(cnm_results.mmap_file)
    params_file = os.path.join(path_base, "all_caiman_parameters.pkl")
    with open(params_file, "wb") as fp:
        pickle.dump(final_params, fp)

    print("stopping server")
    cm.stop_server(dview=dview)


def main():
    (
        file_path,
        n_cpus,
        motion_correct,
        mc_settings_path,
        cnmf_settings_path,
        qc_settings_path,
        output_dir,
    ) = parse_args()

    mc_settings = get_settings(mc_settings_path)
    cnmf_settings = get_settings(cnmf_settings_path)
    qc_settings = get_settings(qc_settings_path)

    # run the pipeline
    run(
        file_path=file_path,
        n_cpus=n_cpus,
        motion_correct=motion_correct,
        mc_settings=mc_settings,
        cnmf_settings=cnmf_settings,
        qc_settings=qc_settings,
        output_directory=output_dir,
    )
