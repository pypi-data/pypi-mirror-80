import os.path

import numpy as np

from .utils import create_dir


def nii_modify(nii, fimout="", outpath="", fcomment="", voxel_range=[]):
    """
    Modify the NIfTI image given either as a file path or a dictionary,
    obtained by nimpa.getnii(file_path).
    """
    if isinstance(nii, str) and os.path.isfile(nii):
        dctnii = nii.getnii(nii, output="all")
        fnii = nii
    if isinstance(nii, dict) and "im" in nii:
        dctnii = nii
        if "fim" in dctnii:
            fnii = dctnii["fim"]

    # ---------------------------------------------------------------------------
    # > output path
    if outpath == "" and fimout != "" and "/" in fimout:
        opth = os.path.dirname(fimout)
        if opth == "" and isinstance(fnii, str) and os.path.isfile(fnii):
            opth = os.path.dirname(nii)
        fimout = os.path.basename(fimout)

    elif outpath == "" and isinstance(fnii, str) and os.path.isfile(fnii):
        opth = os.path.dirname(fnii)
    else:
        opth = outpath
    create_dir(opth)

    # > output floating and affine file names
    if fimout == "":

        if fcomment == "":
            fcomment += "_nimpa-modified"

        fout = os.path.join(
            opth, os.path.basename(fnii).split(".nii")[0] + fcomment + ".nii.gz"
        )
    else:
        fout = os.path.join(opth, fimout.split(".")[0] + ".nii.gz")
    # ---------------------------------------------------------------------------

    # > reduce the max value to 255
    if voxel_range and len(voxel_range) == 1:
        im = voxel_range[0] * dctnii["im"] / np.max(dctnii["im"])
    elif voxel_range and len(voxel_range) == 2:
        # > normalise into range 0-1
        im = (dctnii["im"] - np.min(dctnii["im"])) / np.ptp(dctnii["im"])
        # > convert to voxel_range
        im = voxel_range[0] + im * (voxel_range[1] - voxel_range[0])
    else:
        return None

    # > output file name for the extra reference image
    nii.array2nii(
        im,
        dctnii["affine"],
        fout,
        trnsp=(
            dctnii["transpose"].index(0),
            dctnii["transpose"].index(1),
            dctnii["transpose"].index(2),
        ),
        flip=dctnii["flip"],
    )

    return {"fim": fout, "im": im, "affine": dctnii["affine"]}
