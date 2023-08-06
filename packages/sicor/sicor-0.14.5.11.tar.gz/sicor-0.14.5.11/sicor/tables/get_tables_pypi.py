import os
import json
import requests
import hashlib

from ..options import python_to_json
from .. import get_options
from .. import options

tables_origins = []

sicor_downloads = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        ("google_drive", "0B2ygRjmN4hzNcC15Z2pPS2tQdTg"),
    # "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        # ("google_drive", "0B2ygRjmN4hzNRzhKZ3Z2V2FsWHM"),
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        ("google_drive", "0B2ygRjmN4hzNSHN2RG1lY0M4RW8")
}

file_checksums = {
    "cld_mask_S2_classi_20170412_v20170412_11:43:14.h5":
        "b6d5189a694f25fe20f1ad664d465bcc",
    # "linear_atm_functions_ncwv_5_npre_4_ncoz_2_ntmp_2_wvl_350.0_2550.0_1.00_pca.h5":
        # "aaf6da6c4a4286500407c04e0feb043a",
    "noclear_novelty_detector_channel2_difference9_0_index10_1_channel12_index1_8.retrain.pkl":
        "d2e14b204ac7ee486a946a1c3bded467"
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


def get_tables_pypi(sicor_path=None, sicor_table_path=None, sensor="s2"):

    settings = os.path.join(sicor_path, "options", "{sensor}_options.json".format(sensor=sensor))
    opts = get_options(settings)
    sicor_tables = ([opts['cld_mask']["persistence_file"], opts['cld_mask']["novelty_detector"]])
    sicor_tables_fn = {os.path.basename(fn) for fn in sicor_tables}

    tables_origins.append(sicor_table_path)

    fn_table_paths = {}
    for fn_table in sicor_tables_fn:
        if os.path.exists(os.path.join(sicor_table_path, fn_table)):
            print("%s is already available. Skipping download." % fn_table)
            pass
        else:
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
        """
        if opt_v is string which contains a path to a sicor table, update path to the current sicor_table_path,
        if not return the string. If opt_v is dict, then recurse into key, value pairs and apply update_opts
        :param opt:
        :return:
        """
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

    opts_fn = os.path.join(sicor_path, "options", "sicor_{sensor}_user_options.json".format(sensor=sensor))

    print("Export user options to: %s" % opts_fn)
    with open(opts_fn, "w") as fl:
        json.dump(python_to_json(new_opts), fl, indent=4)


def download_file_from_google_drive(gid, destination):
    """Download from gdrive using public id (gid)."""
    def get_confirm_token(response):
        """Get token from gdrive."""
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value
        return None

    def save_response_content(response, destination):
        """Get response from gdrive to file system."""
        CHUNK_SIZE = 32768
        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params={'id': gid}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': gid, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)
