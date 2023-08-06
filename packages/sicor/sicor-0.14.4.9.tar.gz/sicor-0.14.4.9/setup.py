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
from os.path import isfile
import pkgutil
from pkg_resources import resource_filename, Requirement, DistributionNotFound
from glob import glob
import shutil
import requests
import hashlib
import sys
import json
from jsmin import jsmin
from cerberus import Validator

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

# download AC LUT
fname = "https://gitext.gfz-potsdam.de/EnMAP/sicor/-/raw/master/sicor/AC/data/EnMAP_LUT_MOD5_formatted_1nm"
path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
path_LUT_default = os.path.join(path_sicorlib, 'AC', 'data', 'EnMAP_LUT_MOD5_formatted_1nm')
urllib.request.urlretrieve(fname, path_LUT_default)

# download additional tables for multispectral mode
tables_origins = []
try:
    pp = resource_filename(Requirement.parse('sicor'), "data")
    if os.path.isdir(pp):
        tables_origins += [pp]
except DistributionNotFound:
    pass
tables_origins += list(set(sys.path))

sicor_downloads = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        ("google_drive", "0B2ygRjmN4hzNcC15Z2pPS2tQdTg"),
    "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        ("google_drive", "0B2ygRjmN4hzNRzhKZ3Z2V2FsWHM"),
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        ("google_drive", "0B2ygRjmN4hzNSHN2RG1lY0M4RW8")
}

sicor_downloads_optional = {
    "ch4": {
        "fn": "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5",
        "dn": ("google_drive", "0B2ygRjmN4hzNNEVmX29ROHhJTGc",)},
    "hyperspectral_sample": {
        "fn": "hyperspectral_sample.hdf5",
        "dn": ("google_drive", "0B2ygRjmN4hzNemk2OWtOQ3k4Rkk")},
    "s2_manual_classification": {
        "fn": "20170523_s2_manual_classification_data.h5",
        "dn": ("google_drive", "0B2ygRjmN4hzNXy0tckl3UkROSjg")
    },
}

file_checksums = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        "b6d5189a694f25fe20f1ad664d465bcc",
    "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        "aaf6da6c4a4286500407c04e0feb043a",
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        "d2e14b204ac7ee486a946a1c3bded467",
    "linear_atm_functions_ncwv_4_npre_2_ncoz_2_ntmp_1_nch4_4_wvl_350.0_2550.0_1.00_pca.h5":
        "07bac6ff6cb6f927cffaeed297f94a54",
    "hyperspectral_sample.hdf5":
        "1ac7a3759a8ca1ae31a01832f5b7a418",
    "20170523_s2_manual_classification_data.h5":
        "d0a7b0c13b02d6da0ce60ac6ca9d29a2"
}


def verify_table(fn: str):
    def md5(fname):
        hash_md5 = hashlib.md5()
        with open(fname, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    if os.path.basename(fn) in file_checksums:
        md5sum_is = md5(fn)
        md5sum_should = file_checksums[os.path.basename(fn)]
        if md5sum_should != md5sum_is:
            raise ValueError("Md5Sum of file: {fn} is: {md5sum_is}, but should be: {md5sum_should}".format(
                fn=fn, md5sum_is=md5sum_is, md5sum_should=md5sum_should))


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


def _processing_dict():
    return {"Exception": None,
            "interface": {"args": (), "kwargs": {}},
            "Exception_type": "",
            "clear_fraction": None,
            "status": 1,
            "tIO": 0.0,
            "tRT": 0.0,
            "uncertainties": {}
            }


class SicorrValidator(Validator):
    def _validate_existing_path(self, existing_path, value):
        if existing_path is True and os.path.isdir(value) is False:
            warnings.warn("Path '%s' should exist." % value)


sicor_enmap_schema = {
    "EnMAP": {
        "type": "dict",
        "schema": {
            "FO_settings": {
                "type": "dict",
                "schema": {
                    "aot": {
                        "type": "float",
                        "required": True
                    }
                }
            },
            "Retrieval": {
                "type": "dict",
                "schema": {
                    "fn_LUT": {
                        "type": "string",
                        "required": True,
                        "existing_path": True
                    },
                    "fast": {
                        "type": "boolean",
                        "required": True
                    },
                    "ice": {
                        "type": "boolean",
                        "required": True
                    },
                    "cpu": {
                        "type": "integer",
                        "required": True
                    },
                    "disable_progressbars": {
                        "type": "boolean",
                        "required": True
                    },
                    "segmentation": {
                        "type": "boolean",
                        "required": True
                    },
                    "n_pca": {
                        "type": "integer",
                        "required": True
                    },
                    "segs": {
                        "type": "integer",
                        "required": True
                    }
                }
            }
        }
    }
}


def get_options(target, validation=True):
    if isfile(target):
        with open(target, "r") as fl:
            options = json_to_python(json.loads(jsmin(fl.read())))
            options["processing"] = _processing_dict()

        if validation is True:
            vv = SicorrValidator(allow_unknown=True, schema=sicor_enmap_schema)
            if vv.validate(document=options) is False:
                raise ValueError("Options is malformed: %s" % str(vv.errors))

        return options
    else:
        raise FileNotFoundError("target:%s is not a valid file path" % target)


def get_tables(sicor_table_path=None, sensor="s2", style="link", optional_downloads=None, export_options_to=None):
    path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
    if sensor == "s2":
        settings = os.path.join(path_sicorlib, 'options', 's2_options.json')
    else:
        settings = os.path.join(path_sicorlib, 'options', 'l8_options.json')
    opts = get_options(settings)
    sicor_tables = set([op['atm_tables_fn'] for scat_type, op in opts["RTFO"].items()] +
                       [opts['cld_mask']["persistence_file"], opts['cld_mask']["novelty_detector"]])
    sicor_tables_fn = {os.path.basename(fn) for fn in sicor_tables}

    if optional_downloads is not None:
        for opt_dn in optional_downloads:
            try:
                fn = str(sicor_downloads_optional[opt_dn]["fn"])
            except KeyError:
                print("Optional download: %s is not available" % opt_dn)
                raise

            sicor_tables_fn.update({fn})
            sicor_downloads[fn] = sicor_downloads_optional[opt_dn]["dn"]

    tables_origins.append(sicor_table_path)

    for fn in sicor_tables:
        print("Needed are: %s" % os.path.basename(fn))
    for fn in tables_origins:
        print("Looking in: %s" % fn)

    fn_table_paths = {}
    for fn_table in sicor_tables_fn:
        if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
            for table_path in tables_origins:
                if os.path.isdir(table_path):
                    glb = glob(os.path.join(table_path, "**", fn_table), recursive=True)
                    if len(list(glb)) > 0:
                        if style == "link":
                            if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
                                os.symlink(glb[0], os.path.join(sicor_table_path, fn_table))
                                print("Make link file: %s" % glb[0])
                                fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
                        elif style == "copy":
                            if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
                                print("Copy file: %s" % glb[0])
                                shutil.copy(glb[0], sicor_table_path)
                                fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
        else:
            print("Table %s is already available in %s." % (fn_table, sicor_table_path))
            fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)

        if os.path.exists(os.path.join(sicor_table_path, fn_table)) is False:
            print("File: %s not found locally, try to download." % fn_table)
            try:
                download_type, download = sicor_downloads[fn_table]
                if download_type == "google_drive":
                    print("Downloading %s from google drive: %s" % (fn_table, download))
                    download_file_from_google_drive(download, os.path.join(sicor_table_path, fn_table))
                    fn_table_paths[fn_table] = os.path.join(sicor_table_path, fn_table)
                else:
                    raise ValueError("Download type: %s is not implemented" % download_type)

            except KeyError:
                print("Table %s not available for download." % fn_table)
                raise ValueError("Table: %s unable to retrieve -> giving up." % fn_table)

    print("Verify tables:")
    for fn_table, fn in fn_table_paths.items():
        print(fn_table, fn)
        verify_table(fn)

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

    if export_options_to is None:
        path_sicorlib = os.path.dirname(pkgutil.get_loader("sicor").path)
        path_opts_default = os.path.join(path_sicorlib, 'options')
        opts_fn = os.path.join(path_opts_default, "sicor_{sensor}_user_options.json".format(sensor=sensor))
    else:
        os.makedirs(os.path.dirname(export_options_to), exist_ok=True)
        opts_fn = export_options_to

    print("Export user options to: %s" % opts_fn)
    with open(opts_fn, "w") as fl:
        json.dump(python_to_json(new_opts), fl, indent=4)


def download_file_from_google_drive(gid, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': gid}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': gid, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


path_tables_default = os.path.join(path_sicorlib, 'tables')
get_tables(sicor_table_path=path_tables_default, sensor="s2")
get_tables(sicor_table_path=path_tables_default, sensor="l8")

# check for pygrib
if not util.find_spec('pygrib'):
    warnings.warn('You need to install pygrib manually (use pip install pygrib) if you are using Linux'
                  'and want to download ECMWF data in grib file format. For Windows this package is not available')
