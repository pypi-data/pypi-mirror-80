# coding: utf-8

# SICOR is a freely available, platform-independent software designed to process hyperspectral remote sensing data,
# and particularly developed to handle data from the EnMAP sensor.

# This file contains the package setup tools.

# Copyright (C) 2018  Niklas Bohn (GFZ, <nbohn@gfz-potsdam.de>),
# German Research Centre for Geosciences (GFZ, <https://www.gfz-potsdam.de>)

# This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
# funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
# Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later
# version.

# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along with this program.
# If not, see <https://www.gnu.org/licenses/>.


from setuptools import setup, find_packages
from importlib import util
import warnings
import urllib.request
import os
import pkgutil
import gdown
import json
from jsmin import jsmin

requirements_save_to_install_with_setuptools = [
    "scikit-image", "glymur", "pyprind", "geopandas",
    "dicttoxml", "tables", "pandas", "xlrd", "psutil", "sympy", "pyproj",
    "cerberus", "scipy", "tqdm", "dill", "shapely", "geoarray", "mpld3",
    "jsmin", "iso8601", "pint", "matplotlib", "sphinx-argparse", "numpy",
    "pillow", "pylint", "mypy", "pycodestyle", "pydocstyle", "flake8",
    "sphinx", "arosics", "numba", "netCDF4", "pyrsr"]

other_requirements = {  # dict of "[needed import]: [proposed command for install]
    "gdal": "conda install -c conda-forge gdal",
    "tables": "conda install -c conda-forge pytables",
    "h5py": "conda install -c conda-forge h5py",
    "numba": "conda install -c conda-forge numba",
    "llvmlite": "conda install -c conda-forge llvmlite",
    "pyfftw": "conda install -c conda-forge pyfftw",
    "sklearn": "conda install -c conda-forge scikit-learn"
}

with open("README.rst") as readme_file:
    readme = readme_file.read()

version = {}
with open("sicor/version.py", encoding="utf-8") as version_file:
    exec(version_file.read(), version)

requirements = requirements_save_to_install_with_setuptools

setup_requirements = ["setuptools-git"]

test_requirements = requirements + ["coverage", "mock"]

# test for packages that do not install well with pip
not_installed = {}
for needed_import, propossed_install_command in other_requirements.items():
    is_installed = util.find_spec(needed_import)
    if is_installed is None:
        not_installed[needed_import] = propossed_install_command
if len(not_installed) > 0:
    raise ImportError((
        "Could not find the following packages (please use different installer, e.g. conda).\n" +
        "\n".join(["missing: '{missing_import}', install, e.g. by: '{command}'".format(
            missing_import=missing_import, command=command) for missing_import, command in not_installed.items()])
    ))

setup(
    authors="Niklas Bohn, Daniel Scheffler, Maximilian Brell, André Hollstein, René Preusker",
    author_email="nbohn@gfz-potsdam.de",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8"
    ],
    description="Sensor Independent Atmospheric Correction",
    data_files=[
        ("data", [
            # "sicor/sensors/S2MSI/GranuleInfo/data/S2_tile_data_lite.json",
            "sicor/sensors/S2MSI/data/S2A_SNR_model.xlsx",
            "sicor/AC/data/k_liquid_water_ice.xlsx",
            "sicor/AC/data/newkur_EnMAP.dat",
            "sicor/AC/data/solar_irradiances_400_2500_1.dill"
        ])],
    keywords=["SICOR", "EnMAP", "EnMAP-Box", "hyperspectral", "remote sensing", "satellite", "atmospheric correction"],
    include_package_data=True,
    install_requires=requirements,
    license="GNU General Public License v3 (GPLv3)",
    long_description=readme,
    long_description_content_type="text/x-rst",
    name="sicor",
    package_dir={"sicor": "sicor"},
    package_data={"sicor": ["AC/data/*"]},
    packages=find_packages(exclude=["tests*", "examples"]),
    scripts=[
        "bin/sicor_ac.py",
        "bin/sicor_ecmwf.py",
        "bin/sicor_ac_EnMAP.py"
    ],
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url="https://gitext.gfz-potsdam.de/EnMAP/sicor",
    version=version["__version__"],
    zip_safe=False
)

# download EnMAP AC LUT
fname = "https://gitext.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
path_LUT_default = os.path.join(path_sicorlib, "AC", "data", "EnMAP_LUT_MOD5_formatted_1nm")
if os.path.exists(path_LUT_default):
    pass
else:
    urllib.request.urlretrieve(fname, path_LUT_default)

# download additional tables for multispectral mode
# MOMO LUT
fname = "https://drive.google.com/uc?export=download&id=1-__e8dMlJMC_Lbt5q9-LwS-L5wghKYnn"
path_MOMO_LUT_default = os.path.join(
    path_sicorlib, "tables", "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5")
if os.path.exists(path_MOMO_LUT_default):
    pass
else:
    gdown.download(fname, path_MOMO_LUT_default, quiet=False)
# S2 Cloud Mask
fname = "https://drive.google.com/uc?export=download&id=1PHmX24B_LkbGRgfntQbYc8NWlSkdIX-M"
path_cl_mask_default = os.path.join(
    path_sicorlib, "tables", "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5")
if os.path.exists(path_cl_mask_default):
    pass
else:
    gdown.download(fname, path_cl_mask_default, quiet=False)
# Novelty Detector
fname = "https://drive.google.com/uc?export=download&id=1k0m5fJCBiJbVAoPQPfN0iqn3LnI3UVvu"
path_nov_det_default = os.path.join(
    path_sicorlib, "tables", "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl")
if os.path.exists(path_nov_det_default):
    pass
else:
    gdown.download(fname, path_nov_det_default, quiet=False)


def json_to_python(dd):
    if type(dd) is dict:
        return {json_to_python(k): json_to_python(v) for k, v in dd.items()}
    elif type(dd) is list:
        return [json_to_python(v) for v in dd]
    else:
        if dd == "None":
            return None
        if dd == "slice(None, None, None)":
            return slice(None)
        if dd == "10.0":
            return 10.0
        if dd in ["10.0", "20.0", "60.0"]:
            return float(dd)
        if dd == "true":
            return True
        if dd == "false":
            return False
        else:
            return dd


def python_to_json(dd):
    if type(dd) is dict:
        return {python_to_json(k): python_to_json(v) for k, v in dd.items()}
    elif type(dd) is list:
        return [python_to_json(v) for v in dd]
    else:
        if dd is None:
            return "None"
        if dd == slice(None):
            return "slice(None, None, None)"

        if dd is True:
            return "true"
        if dd is False:
            return "false"
        else:
            return dd


def get_options(target):
    if os.path.isfile(target):
        with open(target, "r") as fl:
            options = json_to_python(json.loads(jsmin(fl.read())))
        return options
    else:
        raise FileNotFoundError("target:%s is not a valid file path" % target)


sicor_tables = [path_MOMO_LUT_default, path_cl_mask_default, path_nov_det_default]
sicor_tables_fn = {os.path.basename(fn) for fn in sicor_tables}
sicor_table_path = os.path.join(path_sicorlib, "tables")

for sensor in ["s2", "l8"]:

    settings = os.path.join(path_sicorlib, "options", "{sensor}_options.json".format(sensor=sensor))
    opts = get_options(settings)

    def update_opts(opt):
        if isinstance(opt, dict):
            return {k: update_opts(v) for k, v in opt.items()}
        elif isinstance(opt, str):
            for fn in sicor_tables_fn:
                if fn in opt:
                    return os.path.join(sicor_table_path, fn)
            return opt
        else:
            return opt

    new_opts = update_opts(opts)

    opts_fn = os.path.join(path_sicorlib, "options", "sicor_{sensor}_user_options.json".format(sensor=sensor))

    print("Export user options to: %s" % opts_fn)
    with open(opts_fn, "w") as fl:
        json.dump(python_to_json(new_opts), fl, indent=4)

# check for pygrib
if not util.find_spec('pygrib'):
    warnings.warn('You need to install pygrib manually (use pip install pygrib) if you are using Linux'
                  'and want to download ECMWF data in grib file format. For Windows this package is not available')
