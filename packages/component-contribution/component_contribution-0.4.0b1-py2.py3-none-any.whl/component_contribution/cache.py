"""Handles downloading an caching of files from Zenodo."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import pathlib
import urllib
from io import BytesIO

import appdirs
import diskcache
import pyzenodo3


def get_cached_file(zenodo_doi: str, fname: str) -> BytesIO:
    """Get data from a file stored in Zenodo (or from cache, if available).

    Parameters
    ----------
    zenodo_doi : str
        the DOI of the Zenodo entry.
    fname : str
        the filename to fetch.

    Returns
    -------
    DataFrame
        the data contained in the file.

    """
    cache_directory = pathlib.Path(
        appdirs.user_cache_dir(appname="equilibrator")
    )
    with diskcache.Cache(cache_directory) as cache:
        if zenodo_doi not in cache:
            zen = pyzenodo3.Zenodo()
            rec = zen.find_record_by_doi(zenodo_doi)
            dataframe_dict = {}
            for file_dict in rec.data["files"]:
                _fname = file_dict["key"]
                _url = file_dict["links"]["self"]
                with urllib.request.urlopen(_url) as fp:
                    data = BytesIO(fp.read())
                dataframe_dict[_fname] = data
            cache.set(key=zenodo_doi, value=dataframe_dict)
        return cache[zenodo_doi][fname]
