============
FSC3D plugin
============

**ATTENTION: This plugin has been renamed from NYSBC to FSC3D.**

This plugin provide a wrapper around `3DFSC <https://github.com/nysbc/Anisotropy/>`_ program developed at Salk Institute and NYSBC.

+--------------+----------------+--------------------+
| prod: |prod| | devel: |devel| | support: |support| |
+--------------+----------------+--------------------+

.. |prod| image:: http://scipion-test.cnb.csic.es:9980/badges/fsc3d_prod.svg
.. |devel| image:: http://scipion-test.cnb.csic.es:9980/badges/fsc3d_devel.svg
.. |support| image:: http://scipion-test.cnb.csic.es:9980/badges/fsc3d_support.svg


Installation
-------------

You will need to use `3.0 <https://github.com/I2PC/scipion/releases/tag/V3.0.0>`_ version of Scipion to be able to run these protocols. To install the plugin, you have two options:

a) Stable version

.. code-block::

   scipion installp -p scipion-em-fsc3d

b) Developer's version

   * download repository

    .. code-block::

        git clone https://github.com/scipion-em/scipion-em-fsc3d.git

   * install

    .. code-block::

       scipion installp -p path_to_scipion-em-fsc3d --devel

FSC3D binaries will be installed automatically with the plugin at **software/em/fsc3D-3.0**, but you can also link an existing installation.

**Important:** you need to have conda (miniconda3 or anaconda3) pre-installed to use this program.

Configuration variables
-----------------------
*CONDA_ACTIVATION_CMD*: If undefined, it will rely on conda command being in the
PATH (not recommended), which can lead to execution problems mixing scipion
python with conda ones. One example of this could can be seen bellow but
depending on your conda version and shell you will need something different:
CONDA_ACTIVATION_CMD = eval "$(/extra/miniconda3/bin/conda shell.bash hook)"

*FSC3D_HOME* (default = software/em/fsc3D-3.0):
Path where the 3DFSC is installed.

*FSC3D_ACTIVATION_CMD* (default = conda activate 3DFSC):
Command to activate the 3DFSC environment.


Verifying
---------
To check the installation, simply run the following Scipion test:

``scipion test fsc3d.tests.test_protocols_3dfsc.Test3DFSC``

Supported versions
------------------

3.0

Protocols
----------
* resolution estimation

References
-----------

1.  Yong Zi Tan, Philip R Baldwin, Joseph H Davis, James R Williamson, Clinton S Potter, Bridget Carragher & Dmitry Lyumkis. Addressing preferred specimen orientation in single-particle cryo-EM through tilting. Nature Methods volume 14, pages 793–796 (2017).
