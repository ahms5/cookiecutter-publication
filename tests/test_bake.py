from contextlib import contextmanager
import shlex
import os
import subprocess
import yaml
import datetime
from cookiecutter.utils import rmtree


import importlib


@contextmanager
def inside_dir(dirpath):
    """
    Execute code from inside the given directory
    :param dirpath: String, path of the directory the command is being run.
    """
    old_path = os.getcwd()
    try:
        os.chdir(dirpath)
        yield
    finally:
        os.chdir(old_path)


@contextmanager
def bake_in_temp_dir(cookies, *args, **kwargs):
    """
    Delete the temporal directory that is created when executing the tests
    :param cookies: pytest_cookies.Cookies,
        cookie to be baked and its temporal files will be removed
    """
    result = cookies.bake(*args, **kwargs)
    try:
        yield result
    finally:
        pass
        # rmtree(str(result.project_path))


def run_inside_dir(command, dirpath):
    """
    Run a command from inside a given directory, returning the exit status
    :param command: Command that will be executed
    :param dirpath: String, path of the directory the command is being run.
    """
    with inside_dir(dirpath):
        return subprocess.check_call(shlex.split(command))


def check_output_inside_dir(command, dirpath):
    "Run a command from inside a given directory, returning the command output"
    with inside_dir(dirpath):
        return subprocess.check_output(shlex.split(command))


def test_year_compute_in_license_file(cookies):
    with bake_in_temp_dir(cookies) as result:

        license_file_path = open(os.path.join(
            result.project_path, 'LICENSE'), 'r')
        now = datetime.datetime.now()
        assert str(now.year) in license_file_path.read()


def test_manuscript(cookies):
    with bake_in_temp_dir(cookies) as result:
        assert os.path.exists(os.path.join(result.project_path, 'manuscript'))

        run_inside_dir(
            'pdflatex manuscript.tex', os.path.join(result.project_path, 'manuscript'))
        assert os.path.exists(
            os.path.join(result.project_path, 'manuscript', 'manuscript.pdf'))


def test_wo_manuscript(cookies):
    extra = {"manuscript": "n"}
    with bake_in_temp_dir(cookies, extra_context=extra) as result:
        assert os.path.exists(os.path.join(result.project_path, 'manuscript')) is False


def test_conda_environ(cookies):
    with bake_in_temp_dir(cookies) as result:
        fname = os.path.join(result.project_path, 'environment.yml')
        with open(fname, 'r') as stream:
            decoded = yaml.safe_load(stream)
            assert decoded['name'] == result.context['publication_slug']
            assert 'python=' + result.context['python_version'] in decoded['dependencies']
            assert decoded['prefix'] == './env/' + result.context['publication_slug']


def test_download_templates(cookies):
    extra = {'manuscript': 'JASA'}
    with bake_in_temp_dir(
            cookies,
            extra_context=extra) as result:

        assert os.path.exists(
            os.path.join(result.project_path, 'manuscript', 'JASA.zip'))