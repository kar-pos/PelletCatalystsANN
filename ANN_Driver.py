import torch
import numpy as np

# Reference inputs
ref_wood=[0.08, 48, 5.7, 0.017, 43.2, 8.65, 1.88679, 75.15, 627, 693, 258, 369, 66, 435, 18.5116, 1.77966, 0, 0, 0]
ref_straw=[0.58, 44, 6.2, 0.068, 41.3, 9.71, 2.83019, 71.42, 400, 476, 77.6, 322.4, 76, 398.4, 15.9694, 1.94444, 0, 0, 0]
ref_hemp=[4.9, 46, 6.8, 0.267, 42.7, 9.83, 7.61905, 66.16, 324, 362, 148, 176, 38, 214, 17.011, 1.875, 0, 0, 0]

# Change the value in square brackets to test other inputs
# You can select one of the predefined, or input your own of the same shape
selected_input=np.array([ref_wood])

#Loading ANN model and calculating outputs
model=torch.jit.load('ANN_model_deployed.pth')
output=model(torch.tensor(selected_input, dtype=torch.float32)).detach().numpy()

#Output formatting and printing
Names_list=['S_CO','S_NOx','S_CO2','S_O2','S_Dust','S_COCs','S_PAH','T_B','S_C_C','S_C_FA','F_cons']
Units_list=['[ppm]','[ppm]','[%]','[%]','[ppm]','[ug/30dm3]','[ug/30dm3]','[°C]','[%]','[%]','[kg/h]']
print('-'*50)
print(' Parameter',' ' * 6,'Unit',' ' * 14, 'Value')
print('-'*50)
for i in range(output.shape[1]):
    P_name=Names_list[i]
    P_unit=Units_list[i]
    P_value=output[0,i]
    print(" {: <17}{: <20}{: <10.5}".format(P_name, P_unit, P_value))
    # print('  {n:<14}{u:<12}{v:15.5}'.format(n =  P_name, u = P_unit, v = P_value))