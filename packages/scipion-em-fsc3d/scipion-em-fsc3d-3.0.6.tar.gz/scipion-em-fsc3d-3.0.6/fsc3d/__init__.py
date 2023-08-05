# **************************************************************************
# *
# * Authors:     Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk)
# *
# * MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

import os

import pwem
from pyworkflow import Config
from pyworkflow.utils import Environ

from .constants import *

_logo = "salk_logo.jpg"
_references = ['tan2017']
_url = "https://github.com/scipion-em/scipion-em-fsc3d"


class Plugin(pwem.Plugin):
    _homeVar = FSC3D_HOME
    _pathVars = [FSC3D_HOME]
    _supportedVersions = V3_0
    _condaActivationCmd = None

    @classmethod
    def _defineVariables(cls):
        cls._defineEmVar(FSC3D_HOME, 'fsc3D-3.0')
        cls._defineVar(FSC3D_ACTIVATION_CMD, 'conda activate 3DFSC')

    @classmethod
    def getEnviron(cls):
        """ Setup the environment variables needed to launch 3DFSC. """
        environ = Environ(os.environ)
        if 'PYTHONPATH' in environ:
            # this is required for python virtual env to work
            del environ['PYTHONPATH']
        environ.update({'PATH': cls.getHome('ThreeDFSC')},
                       position=Environ.BEGIN)

        return environ

    @classmethod
    def getFSCEnvActivation(cls):
        activation = cls.getVar(FSC3D_ACTIVATION_CMD)
        scipionHome = Config.SCIPION_HOME + os.path.sep

        return activation.replace(scipionHome, "", 1)

    @classmethod
    def runProgram(cls, protocol, args, cwd=None):
        """ Return the program binary that will be used. """
        cmd = '%s %s && ' % (cls.getCondaActivationCmd(),
                             cls.getFSCEnvActivation())
        cmd += cls.getHome('ThreeDFSC', 'ThreeDFSC_Start.py')
        protocol.runJob(cmd, args, env=cls.getEnviron(), cwd=cwd)

    @classmethod
    def defineBinaries(cls, env):
        # try to get CONDA activation command
        condaActivationCmd = cls.getCondaActivationCmd()
        neededProgs = []
        if not condaActivationCmd:
            neededProgs = ['conda']

        condaActivationCmd += 'conda env create -f environment.yml &&'
        fsc_commands = [(condaActivationCmd + 'touch IS_INSTALLED',
                         'IS_INSTALLED')]

        envPath = os.environ.get('PATH', "")
        # keep path since conda likely in there
        installEnvVars = {'PATH': envPath} if envPath else None

        env.addPackage('fsc3D', version='3.0',
                       url='https://github.com/azazellochg/fsc3D/archive/3.0.tar.gz',
                       commands=fsc_commands,
                       neededProgs=neededProgs,
                       default=True,
                       vars=installEnvVars)
