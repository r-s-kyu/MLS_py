import numpy as np


def screeming(pq, data_L2gpValue, data_Status, data_L2gpPrecision, data_Quality, data_Convergence, prs):
    if pq == "O3":
        # Status Flag: Only use profiles for which the Status field is an even number.
        data_L2gpValue[data_Status % 2 == 1] = np.nan
        # Precision: Only use values for which the estimated precision is a positive number.
        data_L2gpValue[data_L2gpPrecision <= 0] = np.nan
        # Quality : Only profiles with a value of the Quality greater than 1.0 should be used in scientific studies.
        data_L2gpValue[(data_Quality <= 1.0)] = np.nan
        # Convergence Threshold: < 1.03
        data_L2gpValue[data_Convergence >= 1.03] = np.nan
        # # Useful Range: 261-0.001 hPa
        data_L2gpValue[:, (prs > 262.) | (prs < 0.00099)] = np.nan

    elif pq == "Temperature" or pq == "GPH":
        # Pressure range: 261–0.00046 hPa.
        data_L2gpValue[:, (prs > 262.) | (prs < 0.00045)] = np.nan
        data_L2gpValue[data_L2gpPrecision <= 0] = np.nan
        data_L2gpValue[data_Status % 2 == 1] = np.nan
        # Only use Quality > 0.2 at 83 hPa <= prs and  Quality > 0.9 at 100 hPa >= prs

        data_cut1 =np.copy(data_L2gpValue)[:,( prs <= 84.)]
        data_cut2 =np.copy(data_L2gpValue)[:,( prs >= 99.)]
        data_cut1[(data_Quality <= 0.2)] = np.nan
        data_cut2[(data_Quality <= 0.9)] = np.nan
        data_L2gpValue[:,( prs <= 84.)] = data_cut1
        data_L2gpValue[:,( prs >= 99.)] = data_cut2
        
        data_L2gpValue[data_Convergence >= 1.03] = np.nan

    elif pq == "H2O":
        # Pressure range: 316–0.001 hPa.
        data_L2gpValue[:, (prs > 317) | (prs < 0.00099)] = np.nan
        data_L2gpValue[data_L2gpPrecision <= 0] = np.nan
        data_L2gpValue[data_Status % 2 == 1] = np.nan
        data_L2gpValue[(data_Quality <= 0.7)] = np.nan
        data_L2gpValue[data_Convergence >= 2.0] = np.nan

    return data_L2gpValue
