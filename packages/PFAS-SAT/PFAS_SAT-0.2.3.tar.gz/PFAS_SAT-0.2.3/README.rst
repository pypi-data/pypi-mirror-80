.. General

================================================================
Perfluoroalkyl Substances(PFAS) Systems Analysis Tool(SAT) 
================================================================

.. image:: https://img.shields.io/pypi/v/PFAS_SAT.svg
        :target: https://pypi.python.org/pypi/PFAS_SAT
        
.. image:: https://img.shields.io/pypi/pyversions/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: Supported Python Versions

.. image:: https://img.shields.io/pypi/l/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: License

.. image:: https://img.shields.io/pypi/format/PFAS_SAT.svg
    :target: https://pypi.org/project/PFAS_SAT/
    :alt: Format




Objectives
-----------

* The objective of this project was to develop a comprehensive systems analysis tool (SAT) to estimate PFAS release associated with management
  alternatives for a wide range of PFAS-containing wastes. 

Features
---------

* Through this project, we have established an analytical framework to rigorously describe alternatives for the management of individual PFAS-containing wastes,
  and to quantify interrelationships between individual PFAS-containing wastes and their treatment alternatives. 
* The SAT estimates PFAS release to a receiving medium (air, surface water, groundwater, soil) as well as the storage
  of PFAS in a process (e.g., landfill, injection well) or product (e.g., thermally reactivated carbon). 
* The SAT includes process models for multiple treatment and disposal alternatives to estimate PFAS release as a function of the mass, composition,
  and properties of the waste managed.  



.. Installation

Installation
------------
You should install `Python <https://www.python.org>`_ (3.7 or newer) and `Graphviz <https://graphviz.org>`_ before installing the PFAS_SAT.
We recommend to use `miniconda <https://docs.conda.io/en/latest/miniconda.html>`_ and create a new environment for the PFAS_SAT but it's not
required.
Here are PFAS_SAT dependencies: (These packages are available on `PyPI <https://pypi.org/>`_).

1. **PySide2**: Used for creating the user interface.
2. **stats-arrays**: Used for defining uncertainty distributions.
3. **plotly**: Used for plotting Sankey diagrams.
4. **matplotlib**: Used for data visualization.
5. **graphviz**: Used for plotting the Network.
6. **pandas**: Used for storing data in tables and manipulating them.	
7. **jupyter**: Used as a command-line interface.

**Here are the instructions to install PFAS_SAT with miniconda:**

1- Download and install miniconda from:  https://docs.conda.io/en/latest/miniconda.html

2- Update conda in a terminal window or anaconda prompt::

        conda update conda

3- Create a new environment for PFAS_SAT::

        conda create --name PFAS_SAT python=3.7 graphviz

4- Activate the environment (Windows users)::

        conda activate PFAS_SAT

Note: If you are using Linux or macOS::

        source activate PFAS_SAT
        
5- Install PFAS_SAT in the environment::

        pip install PFAS_SAT

6- Only for Windows user (If you are using Linux or macOS, go to the next step). Make sure that ``bin/`` subdirectory of Graphviz which contains
the layout commands for rendering graph descriptions (dot) is on your system path: On the command-line, ``dot -V`` should print the version
of your Graphviz.


7- Open python to run PFAS_SAT::

        python

8- Run PFAS_SAT in python::

        import PFAS_SAT import ps
        ps.PFAS_SAT()


.. endInstallation
