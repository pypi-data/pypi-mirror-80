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

from pyworkflow.utils import exists, magentaStr
from pyworkflow.tests import BaseTest, DataSet, setupTestProject
from pwem.protocols import ProtImportVolumes, ProtImportMask

from fsc3d.protocols import Prot3DFSC


class Test3DFSCBase(BaseTest):
    @classmethod
    def setData(cls, dataProject='resmap'):
        cls.dataset = DataSet.getDataSet(dataProject)
        cls.map3D = cls.dataset.getFile('betagal')
        cls.half1 = cls.dataset.getFile('betagal_half1')
        cls.half2 = cls.dataset.getFile('betagal_half2')
        cls.mask = cls.dataset.getFile('betagal_mask')

    @classmethod
    def runImportVolumes(cls, pattern, samplingRate):
        """ Run an Import volumes protocol. """
        cls.protImport = cls.newProtocol(ProtImportVolumes,
                                         filesPath=pattern,
                                         samplingRate=samplingRate)
        cls.launchProtocol(cls.protImport)
        return cls.protImport

    @classmethod
    def runImportMask(cls, pattern, samplingRate):
        """ Run an Import volumes protocol. """
        cls.protImport = cls.newProtocol(ProtImportMask,
                                         maskPath=pattern,
                                         samplingRate=samplingRate)
        cls.launchProtocol(cls.protImport)
        return cls.protImport


class Test3DFSC(Test3DFSCBase):
    @classmethod
    def setUpClass(cls):
        setupTestProject(cls)
        Test3DFSCBase.setData()
        print(magentaStr("\n==> Importing data - volume:"))
        cls.protImportVol = cls.runImportVolumes(cls.map3D, 3.54)
        print(magentaStr("\n==> Importing data - volume half 1:"))
        cls.protImportHalf1 = cls.runImportVolumes(cls.half1, 3.54)
        print(magentaStr("\n==> Importing data - volume half 2:"))
        cls.protImportHalf2 = cls.runImportVolumes(cls.half2, 3.54)
        print(magentaStr("\n==> Importing data - mask:"))
        cls.protImportMask = cls.runImportMask(cls.mask, 3.54)

    def test_3DFSC1(self):
        print(magentaStr("\n==> Testing fsc3d - no mask:"))
        protFsc = self.newProtocol(Prot3DFSC,
                                   inputVolume=self.protImportVol.outputVolume,
                                   volumeHalf1=self.protImportHalf1.outputVolume,
                                   volumeHalf2=self.protImportHalf2.outputVolume)
        self.launchProtocol(protFsc)
        protFsc._initialize()
        self.assertTrue(exists(protFsc._getFileName('out_vol3DFSC')), "3D FSC has failed")

    def test_3DFSC2(self):
        print(magentaStr("\n==> Testing fsc3d - with mask:"))
        protFsc = self.newProtocol(Prot3DFSC,
                                   inputVolume=self.protImportVol.outputVolume,
                                   volumeHalf1=self.protImportHalf1.outputVolume,
                                   volumeHalf2=self.protImportHalf2.outputVolume,
                                   maskVolume=self.protImportMask.outputMask,
                                   applyMask=True)
        self.launchProtocol(protFsc)
        protFsc._initialize()
        self.assertTrue(exists(protFsc._getFileName('out_vol3DFSC')), "3D FSC (with mask) has failed")
