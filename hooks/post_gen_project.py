#!/usr/bin/env python
import warnings
import os
from os.path import split
import shutil
import urllib3
import zipfile

PROJECT_DIRECTORY = os.path.realpath(os.path.curdir)


def download_file(url, filename):
    """Download a file
    """
    try:
        http = urllib3.PoolManager()
        with open(filename, 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)
    except:
        warnings.warn("Could not download the manuscript template")
        return


def download_and_extract(url, filename):
    """Download and extract the manuscript template
    """
    try:
        http = urllib3.PoolManager()
        with open(filename, 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)

        with zipfile.ZipFile(filename, 'r') as zip_ref:
            fname_extract = os.path.join(
                os.path.split(filename)[0], 'template')
            zip_ref.extractall(fname_extract)
    except:
        warnings.warn("Could not download the manuscript template")
        return


def remove_file(filepath):
    os.remove(os.path.join(PROJECT_DIRECTORY, filepath))


def remove_dir(filepath):
    shutil.rmtree(os.path.join(PROJECT_DIRECTORY, filepath))


if __name__ == '__main__':

    if '{{ cookiecutter.manuscript }}' == 'n':
        shutil.rmtree(os.path.join(
            PROJECT_DIRECTORY, 'process', 'manuscript'))
        shutil.rmtree(os.path.join(
            PROJECT_DIRECTORY, 'manuscript'))
    else:
        if '{{ cookiecutter.manuscript }}' != 'Custom':
            if '{{ cookiecutter.manuscript }}' == 'JASA':
                filename = os.path.join(PROJECT_DIRECTORY, 'manuscript', 'JASA.zip')
                url = 'https://acousticalsociety.org/wp-content/uploads/2018/02/2021-05-v-JASA_LaTeXPackage_2.zip'

            elif '{{ cookiecutter.manuscript }}' == 'JASA-EL':
                filename = os.path.join(PROJECT_DIRECTORY, 'manuscript', 'JASA-EL.zip')
                url = 'https://acousticalsociety.org/wp-content/uploads/2018/02/2021-05-v-JASA-EL_LaTeXPackage-1.zip'

            download_and_extract(url, filename)
            remove_file(os.path.join('manuscript', 'manuscript.tex'))


    if '{{ cookiecutter.presentation }}' != 'y':
        shutil.rmtree(os.path.join(
            PROJECT_DIRECTORY, 'process', 'presentation'))
        shutil.rmtree(os.path.join(
            PROJECT_DIRECTORY, 'presentation'))

    if 'Not' in '{{ cookiecutter.code_license }}':
        remove_file('LICENSE')