=====================
Phenix scipion plugin
=====================

This plugin allows to use programs from the *PHENIX* software suite within the Scipion framework. **You need to install the Phenix suite before installing the plugin**, see section "Binary Files" for details.

Phenix is a software suite that allows model building of macromolecule structures obtained by X-ray crystallography, and that has been extended to other techniques like cryo-EM (see `Phenix home page <https://www.phenix-online.org/>`_ for details).

Current programs implemented:

  * dock in map
  * emringer
  * real space refine
  * molprobity
  * superpose pdbs
  * validation cryoem

===================
Install this plugin
===================

You will need to use `3.0.0 <https://github.com/I2PC/scipion/releases/tag/v3.0>`_ version of Scipion to run these protocols. To install the plugin, you have two options:

- **Stable version**  

.. code-block:: 

      scipion installp -p scipion-em-phenix
      
OR

  - through the plugin manager GUI by launching Scipion and following **Configuration** >> **Plugins**
      
- **Developer's version** 

1. Download repository: 

.. code-block::

            git clone https://github.com/scipion-em/scipion-em-phenix.git

2. Install:

.. code-block::

           scipion installp -p path_to_scipion-em-phenix --devel
 
 
- **Binary files** 

*PHENIX* binaries will *NOT* be installed automatically with the plugin. The independent installation of PHENIX software suite by the user is required before running the programs. Default installation path assumed is */usr/local/phenix-1.13-2998*; this path or any other of your preference has to be set in *PHENIX_HOME* in *scipion.conf* file. We recommend to install PHENIX version 1.13-2998.

  the plug-in also requires imagemagick package:  sudo apt-get install imagemagick

