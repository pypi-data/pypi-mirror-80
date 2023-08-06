import subprocess

import dualitee

VERSION = '0.0.0'


def run(args, *, env=None, timeout=None, check=False, capture_output=False, quiet=False):
    if isinstance(args, list):
        command_string = " ".join(args)
    else:
        command_string = args

    if capture_output:
        if quiet:
            return subprocess.run(
                command_string, env=env, shell=True, executable='bash',
                timeout=timeout, check=check, capture_output=True, text=True)

        return dualitee.run(
            command_string, env=env, shell=True, executable='bash',
            timeout=timeout, check=check)

    if quiet:
        return subprocess.run(
            command_string, env=env, shell=True, executable='bash',
            timeout=timeout, check=check, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return subprocess.run(
        command_string, env=env, shell=True, executable='bash',
        timeout=timeout, check=check, text=True)
