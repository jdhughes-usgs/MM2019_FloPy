import os
import platform
import sys
import shutil

try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
import platform
from subprocess import Popen, PIPE, STDOUT

pythonpath = os.path.join('..', 'Miniconda3', 'python')
scriptpath = os.path.join('..', 'Miniconda3', 'Scripts')
kernelpath = os.path.join('..', 'Miniconda3', 'share', 'jupyter',
                          'kernels', 'python3')
condacommand = os.path.join(scriptpath, 'conda')
pipcommand = os.path.join(scriptpath, 'pip')

exeloc = {'Windows': 'python',
          'Darwin': 'python'}


# simple function to print a message to STDOUT
def printmsg(msg):
    print(msg)
    return


def run_and_print(cmds):
    for cmd in cmds:
        print(' {}'.format(cmd))
        cmd_list = cmd.split()
        p = Popen(cmd_list, stdout=PIPE, stderr=STDOUT)
        while True:
            line = p.stdout.readline()
            c = line.decode('utf-8')
            if c != '':
                c = c.rstrip('\r\n')
                print('{}'.format(c))
            else:
                break
    return


def root_install():
    pip_list = []
    conda_list = ['jupyter',
                  'scipy',
                  'pyshp',
                  'nose',
                  'pandas',
                  'flopy']

    # prepare the pip installs to run in a single command (after activating env)
    cmds = ['{} config --add channels conda-forge'.format(condacommand)]
    cmds.append('{} config --set ssl_verify false'.format(condacommand))
    cmds.append('{} update conda -y'.format(condacommand))
    cmds.append('{} update -y --all'.format(condacommand))
    for c in conda_list:
        cmds.append('{} install {} -y'.format(condacommand, c))
    cmds.append('{} info'.format(condacommand))
    # add pip installs
    cmds.append('{} -m pip install --upgrade pip'.format(pythonpath))
    for p in pip_list:
        cmds.append('{} install {}'.format(pipcommand, p))
    
    run_and_print(cmds)
    
    print('\nRunning tests of installed python packages in root installation...')
    print('    using python installed in "{}"'.format(pythonpath))
    cmds = [pythonpath + ' -m nose -v test_root_install.py']
    run_and_print(cmds)    

    return


def fix_jupyter_kernel():
    """
    The latest version of miniconda (10/5/2018) has a problem where python
    cannot be found when a notebook starts.  It turns out the problem is
    that the path to python is incorrect in a kernel file called
    kernel.json.  This function corrects the kernel.json file to point to
    the correct location.  The problem is only on windows.
    """
    import json
    print('Kernel path is: {}'.format(kernelpath))
    if not os.path.isdir(kernelpath):
        print('Error. Kernel path not found: {}'.format(kernelpath))

    kerneljson = os.path.join(kernelpath, 'kernel.json')
    print('Checking: {}'.format(kerneljson))
    if not os.path.isfile(kerneljson):
        print('Error.  Kernel json file not found: {}'.format(kerneljson))
        kerneljson = None

    pythonexe = None
    if kerneljson is not None:
        with open(kerneljson) as data_file:
            jsondata = json.load(data_file)
        pythonexe = jsondata['argv'][0]
        print('Kernel python exe is: {}'.format(pythonexe))

    if pythonexe is not None:
        if not os.path.isfile(pythonexe):
            s = pythonexe
            if pythonexe.endswith('bin/python'):
                s = s.replace('bin/python', 'python')
                print('Attempting to find: {}'.format(s + '.exe'))
                if os.path.isfile(s + '.exe'):
                    pythonexe = s
                    os.rename(kerneljson, kerneljson + '.bak')
                    jsondata['argv'][0] = pythonexe
                    with open(kerneljson, 'w') as outfile:
                        json.dump(jsondata, outfile, indent=1)
                else:
                    print('Error. Could not reset kernel python exe.')

    print('Done checking kernel path.')


if __name__ == "__main__":

    install_root = True
    fix_jupyter = True
    
    # install packages to root environment
    if install_root:
        root_install()

    # fix the jupyter kernel location
    if fix_jupyter:
        fix_jupyter_kernel()
