# Tripple ANN system for biomass combustion analysis
Artificial Neural Network system for determaining slected emission and engineering parameters of biomass combustion

## Project description
The tool is intended to support renewable energy production from variouse plant biomass waste via catalytic combustion. It requires 19 input parameters describing biomass and catalyst properties. The output of the model consists of 11 features, including emission and engineering parameters of the system. To provide the best possible accuracy, the system consists of three multi-layer ANN networks combined in one topology.

## Files description
* ANN_Driver.py - the file is general driver for the model. It includes theree examples of model input data, and lets the user specifies their own. It includes also simple data visualization script.
* ANN_model_deployed.pth - this file holds deployed version of finall pre-trained ANN system. It is standallone package, and cannot be edited by the user.