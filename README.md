# Tripple ANN system for biomass combustion analysis
Artificial Neural Network system for determaining slected emission and engineering parameters of biomass combustion. The tool is designed to predict combustion properties returned by pre-trained Artificial Neural Network (ANN). Applied ANN utilizes branched three-path topology. The user can select one of the pre-defined feedstock data or provide own values. The networks can work on any non-negative data, however, it should be remembered that in the case of entering data very far from the area on which the networks were trained, it can lead to uncertain results.

![App GUI](Screenshot_GUI.png?raw=true "Title")
## Project description
The tool is intended to support renewable energy production from variouse plant biomass waste via catalytic combustion. It requires 19 input parameters describing biomass and catalyst properties. The output of the model consists of 11 features, including emission and engineering parameters of the system. To provide the best possible accuracy, the system consists of three multi-layer ANN networks combined in one topology.

## Files description
* [Release](https://github.com/kar-pos/PelletCatalystsANN/releases/tag/v1.0.0) version of App with full GUI (see screenshot above), recommended for most users.
* ANN_Driver.py - the file is general driver for the model in Python language. It includes theree examples of model input data, and lets the user specifies their own. It includes also simple data visualization script. Recommended for advanced users
* ANN_Driver_GUI.py - a variant of above script, with simple GUI based on CustomTkinter library.
* ANN_model_deployed.pth - this file holds deployed version of finall pre-trained ANN system. It is standallone package, and cannot be edited by the user. However, you can conveniently import this model into your projects using PyTorch library (or equivalent in non-python environments).