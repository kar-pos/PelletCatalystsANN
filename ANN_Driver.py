import torch
import numpy as np
import pandas as pd

#%%SET INPUT HERE
feed='wood' #wood/straw/hemp/custom, for custom see .xls file
catalyst_amount=0 # Catalyst amount in g/m2
catalyst_type=0 #Catalyst type, 0 for none, 1 for Pt, 2 for TiO2, 3 for CuO, 4 for MnO2
catalyst_adblue=0 #1 if yes, 0 if no addition of AdBlue to feedstock

#%% Model run script
#Loading model
model=torch.jit.load('ANN_model_deployed.pth');

#Reference feedstocks
ref_wood=[0.08, 48, 5.7, 0.017, 43.2, 8.65, 1.88679, 75.15, 627, 693, 258, 369, 66, 435, 18.5116, 1.77966]
ref_straw=[0.58, 44, 6.2, 0.068, 41.3, 9.71, 2.83019, 71.42, 400, 476, 77.6, 322.4, 76, 398.4, 15.9694, 1.94444]
ref_hemp=[4.9, 46, 6.8, 0.267, 42.7, 9.83, 7.61905, 66.16, 324, 362, 148, 176, 38, 214, 17.011, 1.875]

#Feedstock selection
feed='custom'
if feed == 'wood':
    input_array=np.append(ref_wood, [catalyst_amount,catalyst_adblue,catalyst_type])
elif feed == 'straw':
    input_array=np.append(ref_wood, [catalyst_amount,catalyst_adblue,catalyst_type])
elif feed == 'hemp':
    input_array=np.append(ref_wood, [catalyst_amount,catalyst_adblue,catalyst_type])
else:
    feedstock = pd.read_excel('Custom_feedstock.xlsx',skiprows = 1)
    feedstock = feedstock.to_numpy(dtype=float)
    input_array=np.append(feedstock, [catalyst_amount,catalyst_adblue,catalyst_type])

model_out=model(torch.tensor(input_array.reshape(1, -1), dtype=torch.float32)).detach().numpy()

#Printing results
s = f"""
{'-'*30}
#Modeled output parameters
{'-'*30}
# CO: {np.array([model_out[0,0]])[0]:.2f} [ppm]
# NOx: {np.array([model_out[0,1]])[0]:.1f} [ppm]
# CO2: {np.array([model_out[0,2]])[0]:.2f} [%]
# O2: {np.array([model_out[0,3]])[0]:.3f} [%]
# Dust: {np.array([model_out[0,4]])[0]:.5f} [g/m3]
# VOCs: {np.array([model_out[0,5]])[0]:.2f} [ug/30dm3]
# PAH: {np.array([model_out[0,6]])[0]:.4f} [ug/30dm3]
# T: {np.array([model_out[0,7]])[0]:.1f} [°C]
# Sc_c: {np.array([model_out[0,8]])[0]:.2f} [%]
# Sc_fa: {np.array([model_out[0,9]])[0]:.2f} [%]
# F: {np.array([model_out[0,10]])[0]:.2f} [kg/h]
{'-'*30}
"""
print(s)