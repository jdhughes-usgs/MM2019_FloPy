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

if sys.version_info >= (3, 3):
    from shutil import which
else:
    from distutils.spawn import find_executable as which

exes = {'python': 'python',
        'conda': 'conda',
        'pip': 'pip'}

if platform.system() in 'Windows':
    for key, value in exes.items():
        if not value.lower().endswith('.exe'):
            value += '.exe'
        exes[key] = which(value)

pythonpath = exes['python']
condacommand = exes['conda']
pipcommand = exes['pip']


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
    pip_list = ['https://github.com/modflowpy/pymake/zipball/master',
                'https://github.com/jtwhite79/pyemu/zipball/develop']
    conda_list = ['jupyter',
                  'pyshp',
                  'flopy',
                  'nose',
                  'scipy']

    # prepare the pip installs to run in a single command (after activating env)
    cmds = ['{} config --add channels conda-forge'.format(condacommand)]
    cmds.append('{} config --set ssl_verify false'.format(condacommand))
    cmds.append('{} update conda -y'.format(condacommand))
    for c in conda_list:
        cmds.append('{} install {} -y'.format(condacommand, c))
    cmds.append('{} info'.format(condacommand))
    # add pip installs
    cmds.append('{} -m pip install --trusted-host pypi.python.org --upgrade pip'.format(pythonpath))
    for p in pip_list:
        cmds.append('{} install --trusted-host codeload.github.com {}'.format(pipcommand, p))
    
    run_and_print(cmds)
    
    print('\nRunning tests of installed python packages in root installation...')
    print('    using python installed in "{}"'.format(pythonpath))
    cmds = [pythonpath + ' -m nose -v test_install.py']
    run_and_print(cmds)    

    return


if __name__ == "__main__":

    install_root = True
    
    # install packages to root environment
    if install_root:
        root_install()
