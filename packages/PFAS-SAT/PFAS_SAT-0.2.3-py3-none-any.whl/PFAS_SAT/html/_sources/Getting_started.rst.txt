.. toctree::
   :maxdepth: 3
   :hidden:


****************
Getting Started
****************

To open the PFAS_SAT, do the following steps:

1- Open the conda command prompt.

2- Activate the environment::

        conda activate PFAS_SAT

3- Open python to run PFAS_SAT::

        python

4- Run PFAS_SAT in python::

        import PFAS_SAT as ps
        ps.PFAS_SAT()


PFAS SAT
#########

Here is the PFAS_SAT start screen (:numref:`Start_fig`). The user interface includes the following tabs:

1. `Start`
2. `Waste Material Properties` tab: Shows the default data for waste materials, and you can edit, import, or export the data through this tab.
3. `Process Models` tab: Shows the process models and type of waste materials that each can treat.
4. `Process Models` Input Data tab: Shows the default input data for process models, and you can edit, import, or export the data through this tab.
5. `Define System` tab: In this tab, you can create a scenario and define which processes are used to treat the waste material.
6. `Flow Analysis` tab: This tab shows the Sankey diagram and data for PFAS flows in the treatment system.
7. `Monte Carlo Simulation` tab: In this tab, you can define/change uncertainty distributions for the input data and perform a Monte Carlo simulation.
8. `Sensitivity Analysis` tab: In this tab, you can perform sensitivity analysis on your system and study the effect of input parameters on the PFAS fate.


You can create a new project by clicking on the `Start New Project` button [9].

.. figure:: /Images/Start.png
	:alt: alternate text
	:align: left
	:name: Start_fig
	
	Start tab


Create new project
###################

Waste Materials Tab
********************

The first step of creating a new project is to check the default data for the waste material that you want to simulate. If you have the data for waste material (e.g., PFAS concentration), 
you can update the default data in the `Waste Material Properties` tab. :numref:`WM_fig` shows how you can edit, import, or export data for waste materials. If you have data in `csv` format,
you can import it by using the `Browse` [1] and `Import` [2] Buttons.

.. note:: If you are importing data, the data should be in the `csv` format and have the same column names as the default data files. 
		  We suggest to copy our data files and edit them to keep the structure.


.. Warning:: Some of the waste materials like `Contaminated Water`,  `Contaminated Soil`, etc. are too case dependent and the user should only create a scenario with them
			 if he/she has the data for PFAS concentration.

You can change the waste material via drop-down list [3] and its help button [4] displays more information about the sources of waste material and potential treatment options.
You can see the uncertainty distributions for data by checking the checkbox [5]. The `Uncertainty Distribution Help` button [6] shows you how to read the distributions. You can change
the data in the table [7] and don't forget to click the `Update` button [9] otherwise your changes will be lost. You can remove all the uncertainty distribution by the `Clear Uncertainty` button [8].
`Export` button [9] lets you export the data in 'csv' format and then you can import your data file next time that you want to use `PFAS_SAT`. When you are done with data for waste materials, you can
go to the next tab by clicking on the `Define Process Models` button [11].


.. figure:: /Images/WM.png
	:alt: alternate text
	:align: left
	:name: WM_fig
	
	Waste Materials tab





Process Models Tab
********************

The :numref:`PM_fig` shows the `Process Models` tab. You can select the process model by the drop-down list [1] and see the waste materials that the selected process can treat/accept. The help button [2] displays
more information about how we modeled the process. You can import your input data (`csv` file) for the process models by the `Browse` button [3] and don't forget to check the `User Defined` radio button
if you are importing data. You can change the types of waste that each process model accept and click the `Update` button [6] to save them. You can go to the next tab by clicking on the 
`Check Process Models Input Data` button [7].



.. figure:: /Images/PM.png
	:alt: alternate text
	:align: left
	:name: PM_fig
   
	Process Models tab





Process Models Input Data Tab
*******************************

You should check the input data for the process models, especially the operational input data that are case dependent (e.g.,  Windrow height or width in the composting process). This tab is similar to
`Waste Materials Tab`_ (:numref:`WM_fig`) and you can edit, import, or export the data.

.. Warning:: If you are changing the input data for process models, check the minimum and maximum range. The model doesn't check that your data is valid. Wrong data can
			 results in wrong results or produce an error.

.. Warning:: Don't change the name or unit of the parameters unless you are also updating the code.

.. note:: You can develop new process models for the technologies that are included in the current version of PFAS_SAT or revise current models. See `Develop New Process Models`_.


.. figure:: /Images/PMInput.png
	:alt: alternate text
	:align: left
	:name: PM_Input_fig
   
	Process Models Input Data tab


	
Define System Tab
******************

:numref:`SYS_fig` shows the `Define System` tab. In this tab, you should select the starting waste material [1] and it's mass flow [2] that you want to simulate and click the `Setup Scenario`
button. `Treatment Processes` frame [5] will show all the potential processes that can be used to handle the starting waste material and the residuals/products from the downstream processes.
If some of these processes don't exist in your region/state, deselect them so they won't be used in the treatment network.


.. Warning:: The treatment network should include at least one process for the staring material and each of the products/residuals produced in the downstream processes. The pop-up warnings will help
			 you add the required processes.
			 
			 .. image:: /Images/SYS_Error2.png
			 	:alt: alternate text
				:align: center


After selecting the treatment options [5], click on the `Create Network` button [6] to create the `Treatment Network Parameters` table [7]. In the table, you should allocate the starting
materials and other products/residuals to the treatment processes and then click on the `Update Network` button [8]. After updating the network parameters, you will see the network graph [9].


Now you have a complete scenario, and you can do further analysis include Flow Analysis, Monte Carlo simulation, or Sensitivity analysis on your scenario.


.. Warning:: You should check and define the allocation of waste materials to treatment processes in `Treatment Network Parameters`. The sum of the fractions (allocations) for
			 each waste/product should be 1 otherwise, you will get the following pop-up error that tells you which of the allocations are wrong.
			 
			 .. image:: /Images/SYS_Error1.png
				:alt: alternate text
				:align: center
  



.. figure:: /Images/SYS.png
	:alt: alternate text
	:align: left
	:name: SYS_fig
   
	Define System tab



Flow Analysis
##############

All the data for PFAS flows in the treatment network are added to the PFAS Inventory which can be seen in the `Flow Analysis` tab (:numref:`FA_fig` [2]). The currently included
endpoints are air, water, soil, landfill storage, reactivated activated carbon, destroyed/mineralized PFAS, and injection well. The row indexes for the Inventory are:

#. **Flow name**: Name of the flow in the process models.
#. **Source**: The process that produces the flow.
#. **Target**: The process that treats/receives the flow.
#. **Unit**: Unit for the PFAS flows.
#. **PFAS**: In the current version, 10 types of PFAS are tracked through the system.

.. note:: When you are doing the flow analysis, `PFAS_SAT` will show a pop-up window that displays the error in the PFAS balance. As some of the flows are loop (e.g., 
		  Sending the landfill leachate to WWT produces WWT solids that will be dumped in the landfill and result in landfill leachate generation, which was the starting material),
		  PFAS_SAT is using the **Cut-off** approach to break the loop when the PFAS flows are less than Cut-off. So small errors in PFAS mass balance (< 5%) are acceptable. You can change
		  the Cut-off from the ``menu/tools/Options``.
		  
		  .. image:: /Images/FA_popup.png
			:alt: alternate text
			:align: center 		  



.. note:: The Sankey is interactive, and you can change the view, export ``png``, or see the labels for flow. Check the toolbar for Sankey Diagram. The source file of the Sankey 
		  diagram is also saved in ``html`` format in the directory that you opened the `PFAS_SAT`.

		  .. image:: /Images/FA_Sankey.png
			:alt: alternate text
			:align: center
  

.. figure:: /Images/FA.png
	:alt: alternate text
	:align: left
	:name: FA_fig

	Flow Analysis tab 




Monte Carlo Simulation
#######################

You can define the uncertainty distributions for the input data and then run the Monte Carlo simulation to study the effect of uncertainty/variability in the input data.  
:numref:`MC_fig` [2] shows the `Monte Carlo Simulation` tab. Changing and updating the data is similar to the `Waste Materials Tab`_ and `Process Models Input Data Tab`_.
You should enter the number of simulations in the spin box [8] and click the `Run` button. The progress bar [9] will show you the progress and when the simulation is done,
you can save the results in ``csv`` format or analyze the results to find the distributions or correlations by clicking on the `Show Results` button [10]. 



.. figure:: /Images/MC.png
	:alt: alternate text
	:align: left
	:name: MC_fig

	Monte Carlo Simulation tab



Monte Carlo Simulation Results
*******************************

Results from the Monte Carlo simulation will be shown in a new window when the simulation is done. You can view the results from the Monte Carlo simulation in the 
Data tab (:numref:`MC_Data_fig`), plot the results based on the inputs (:numref:`MC_Plot_fig`), plot the distributions (:numref:`MC_Plot2_fig`) and calculate
the correlations between the results and input data (:numref:`MC_Cor_fig`) to find the most important parameters.


.. figure:: /Images/MCData.png
	:alt: alternate text
	:align: left
	:name: MC_Data_fig

	Monte Carlo Simulation Results Table

Select the parameter for the x-axis [1] and y-axis [2] from the drop-down lists and then click the `Update` button to see the plot [4]. You can plot scatter and hexbin [3].
Use the toolbar [5] to change the view, export, or edit the plot.

.. figure:: /Images/MCPlot1.png
	:alt: alternate text
	:align: left
	:name: MC_Plot_fig
	
	Plot Monte Carlo Simulation Results


Select the output from the drop-down list [1] and then click the `Update` button [3] to see the distribution plot [4]. You can plot a histogram, box plot, or density
plot [2]. Use the toolbar [5] to change the view, export, or edit the plot.

.. figure:: /Images/MCPlot2.png
	:alt: alternate text
	:align: left
	:name: MC_Plot2_fig
	
	Plot Distributions of Monte Carlo Simulation Results

Select the endpoint from the drop-down list [1] and then click the `Update` button to see the correlation plot [2]. Use the toolbar [3] to change the view, export or edit the plot. 

.. figure:: /Images/MCCor.png
	:alt: alternate text
	:align: left
	:name: MC_Cor_fig
	
	Monte Carlo Simulation Results (Correlation data tab)


Sensitivity Analysis
#####################

You can perform parametric sensitivity analysis in the `Sensitivity Analysis` tab (:numref:`SA_fig`) and export the results or plot them (:numref:`SA_Plot_fig`).
'Model', 'Category' and 'Parameter' drop-down lists [1-3] will help you to choose a parameter for your analysis and then you can see more info in the `Parameter Information` screen[4]
which will guide you to choose a realistic range for your analysis. Increase the number of steps, if your parameter has a non-linear effect. You can track the sum of the all
PFAS types include in SAT or select only one type (e.g., PFOA) [6].    

.. figure:: /Images/SA.png
	:alt: alternate text
	:align: left
	:name: SA_fig

	Sensitivity Analysis tab


Select the parameter for the x-axis [1] and y-axis [2] from the drop-down lists and then click the `Update` button to see the plot [3].
Use the toolbar [4] to change the view, export, or edit the plot.


.. figure:: /Images/SAPlot.png
   :alt: alternate text
   :align: left
   :name: SA_Plot_fig
   
   Plot Sensitivity Analysis Results
 
 
 
Uncertainty Distribution
##########################

Tha `stats_arrays <https://stats-arrays.readthedocs.io/en/latest/index.html#>`_ package is used to define uncertain input parameters for the
process models and waste materials. The table below shows the main uncertainty distributions that are currently used


======================= ===================== =========================== ============================= ================= ============= ===============
Name                    ``uncertainty_type``  ``loc``                     ``scale``                     ``shape``         ``minimum``   ``maximum``
======================= ===================== =========================== ============================= ================= ============= ===============
Undefined               0                     **static value**                                                                                           
No uncertainty          1                     **static value**                                                                                           
Lognoraml               2                     :math:`\boldsymbol{\mu}`    :math:`\boldsymbol{\sigma}`                     *Lower bound* *Upper bound*  
Normal                  3                     :math:`\boldsymbol{\mu}`    :math:`\boldsymbol{\sigma}`                     *Lower bound* *Upper bound*  
Uniform                 4                                                                                                 *Minimum*     *Maximum*      
Triangular              5                     **mode**                                                                    *Minimum*     *Maximum*      
Discrete Uniform        7                     **mode**                                                                    *Minimum*     *upper bound*    
======================= ===================== =========================== ============================= ================= ============= ===============

Guideline to define uncertainty
*******************************

1. **Normal distributions (ID = 3)**: When there is sufficient published data.
2. **Triangular distribution (ID = 5)**: When values are based on expert opinions with a reasonable value for the mode.
3. **Uniform Distribution (ID=4)**: When only the range is known without preference for mode.
4. **Lognormal distributions (ID=2)**:  When only one value is available or there is significant data and the value must be non-negative.
5. **Discrete Uniform (ID=7)**: For True/False (0,1) parameters.(min=0,max=2).


.. note:: In **Normal distribution**, if the mean is too close to lower or upper bound (mostly for parameters that are fractions), 
		  use the triangular distribution.

.. note:: In **Lognormal distribution**, if the parameter is related to the emission factors, sigma should be in the range of
		  0.04 to 0.09 based on the quality of the data.  

.. seealso:: For more information about distributions check `stats_arrays <https://stats-arrays.readthedocs.io/en/latest/index.html#>`_ website.



Develop New Process Models
###########################

