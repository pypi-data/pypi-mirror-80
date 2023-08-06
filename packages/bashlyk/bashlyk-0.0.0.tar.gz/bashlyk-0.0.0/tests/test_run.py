import subprocess

import pytest

import bashlyk


def test_run(capfd):
    process = bashlyk.run('echo $SHELL')

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout is None
    assert process.stderr is None

    assert process.returncode == 0

    assert 'bash' in stdout_sys
    assert stderr_sys == ''


def test_run_capture_output(capfd):
    process = bashlyk.run('echo $SHELL', capture_output=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert 'bash' in process.stdout
    assert process.stderr == ''

    assert process.returncode == 0

    assert 'bash' in stdout_sys
    assert stderr_sys == ''


def test_run_quiet(capfd):
    process = bashlyk.run('echo $SHELL', quiet=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout is None
    assert process.stderr is None

    assert process.returncode == 0

    assert stdout_sys == ''
    assert stderr_sys == ''


def test_run_capture_output_and_quiet(capfd):
    process = bashlyk.run('echo $SHELL', capture_output=True, quiet=True)

    stdout_sys, stderr_sys = capfd.readouterr()

    assert 'bash' in process.stdout
    assert process.stderr == ''

    assert process.returncode == 0

    assert stdout_sys == ''
    assert stderr_sys == ''


def test_run_timeout():
    with pytest.raises(subprocess.TimeoutExpired):
        bashlyk.run(['sleep', '9999'], timeout=0.001)


def test_run_env(capfd):
    process = bashlyk.run('echo $VAR', env={'VAR': 'variable'})

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout is None
    assert process.stderr is None

    assert process.returncode == 0

    assert stdout_sys.rstrip() == 'variable'
    assert stderr_sys == ''


def test_run_stderr(capfd):
    process = bashlyk.run('echo error >&2')

    stdout_sys, stderr_sys = capfd.readouterr()

    assert process.stdout is None
    assert process.stderr is None

    assert process.returncode == 0

    assert stdout_sys == ''
    assert stderr_sys.rstrip() == 'error'


def test_run_check():
    with pytest.raises(subprocess.CalledProcessError):
        bashlyk.run('exit 1', check=True)
