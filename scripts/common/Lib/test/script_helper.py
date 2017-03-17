# Embedded file name: scripts/common/Lib/test/script_helper.py
import sys
import os
import re
import os.path
import tempfile
import subprocess
import py_compile
import contextlib
import shutil
import zipfile
from test.test_support import strip_python_stderr

def _assert_python(expected_success, *args, **env_vars):
    cmd_line = [sys.executable]
    if not env_vars:
        cmd_line.append('-E')
    cmd_line.extend(args)
    env = os.environ.copy()
    env.update(env_vars)
    p = subprocess.Popen(cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    try:
        out, err = p.communicate()
    finally:
        subprocess._cleanup()
        p.stdout.close()
        p.stderr.close()

    rc = p.returncode
    err = strip_python_stderr(err)
    if rc and expected_success or not rc and not expected_success:
        raise AssertionError('Process return code is %d, stderr follows:\n%s' % (rc, err.decode('ascii', 'ignore')))
    return (rc, out, err)


def assert_python_ok(*args, **env_vars):
    """
    Assert that running the interpreter with `args` and optional environment
    variables `env_vars` is ok and return a (return code, stdout, stderr) tuple.
    """
    return _assert_python(True, *args, **env_vars)


def assert_python_failure(*args, **env_vars):
    """
    Assert that running the interpreter with `args` and optional environment
    variables `env_vars` fails and return a (return code, stdout, stderr) tuple.
    """
    return _assert_python(False, *args, **env_vars)


def python_exit_code(*args):
    cmd_line = [sys.executable, '-E']
    cmd_line.extend(args)
    with open(os.devnull, 'w') as devnull:
        return subprocess.call(cmd_line, stdout=devnull, stderr=subprocess.STDOUT)


def spawn_python(*args, **kwargs):
    cmd_line = [sys.executable, '-E']
    cmd_line.extend(args)
    return subprocess.Popen(cmd_line, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kwargs)


def kill_python(p):
    p.stdin.close()
    data = p.stdout.read()
    p.stdout.close()
    p.wait()
    subprocess._cleanup()
    return data


def run_python(*args, **kwargs):
    p = spawn_python(*args, **kwargs)
    stdout_data = kill_python(p)
    return (p.wait(), stdout_data)


@contextlib.contextmanager
def temp_dir():
    dirname = tempfile.mkdtemp()
    dirname = os.path.realpath(dirname)
    try:
        yield dirname
    finally:
        shutil.rmtree(dirname)


def make_script(script_dir, script_basename, source):
    script_filename = script_basename + os.extsep + 'py'
    script_name = os.path.join(script_dir, script_filename)
    script_file = open(script_name, 'w')
    script_file.write(source)
    script_file.close()
    return script_name


def compile_script(script_name):
    py_compile.compile(script_name, doraise=True)
    compiled_name = script_name + 'c'
    return compiled_name


def make_zip_script(zip_dir, zip_basename, script_name, name_in_zip = None):
    zip_filename = zip_basename + os.extsep + 'zip'
    zip_name = os.path.join(zip_dir, zip_filename)
    zip_file = zipfile.ZipFile(zip_name, 'w')
    if name_in_zip is None:
        name_in_zip = os.path.basename(script_name)
    zip_file.write(script_name, name_in_zip)
    zip_file.close()
    return (zip_name, os.path.join(zip_name, name_in_zip))


def make_pkg(pkg_dir):
    os.mkdir(pkg_dir)
    make_script(pkg_dir, '__init__', '')


def make_zip_pkg(zip_dir, zip_basename, pkg_name, script_basename, source, depth = 1, compiled = False):
    unlink = []
    init_name = make_script(zip_dir, '__init__', '')
    unlink.append(init_name)
    init_basename = os.path.basename(init_name)
    script_name = make_script(zip_dir, script_basename, source)
    unlink.append(script_name)
    if compiled:
        init_name = compile_script(init_name)
        script_name = compile_script(script_name)
        unlink.extend((init_name, script_name))
    pkg_names = [ os.sep.join([pkg_name] * i) for i in range(1, depth + 1) ]
    script_name_in_zip = os.path.join(pkg_names[-1], os.path.basename(script_name))
    zip_filename = zip_basename + os.extsep + 'zip'
    zip_name = os.path.join(zip_dir, zip_filename)
    zip_file = zipfile.ZipFile(zip_name, 'w')
    for name in pkg_names:
        init_name_in_zip = os.path.join(name, init_basename)
        zip_file.write(init_name, init_name_in_zip)

    zip_file.write(script_name, script_name_in_zip)
    zip_file.close()
    for name in unlink:
        os.unlink(name)

    return (zip_name, os.path.join(zip_name, script_name_in_zip))