from undaqTools import Daq
import numpy as np
import pandas as pd
import argparse
import os
import re
import datetime as dt

def main():

    parser = argparse.ArgumentParser(description='Get folder location to look for DAQ files')

    parser.add_argument('-dir', action="store", dest="dir_daq")
    parser.add_argument('-elemlist', action="store", dest="elemlist")

    results = parser.parse_args()

    current_directory = os.getcwd()
    target_directory = results.dir_daq # Replace with the folder that holds all the HDF5 files or the top level folder of where your HDF5 files are

    with open(results.elemlist) as fname:
        elemlist = fname.read().split('\n')
    
    for root, dirs, files in os.walk(os.path.join(current_directory, target_directory)):
        for fname in files:
            if fname.endswith('.daq'):
                try:
                    daq = Daq()
                    print("Trying to read {}".format(fname))
                    daq.read_daq(os.path.join(root,fname), process_dynobjs=False, interpolate_missing_frames=True)
                    #daq.write_hd5(os.path.join(root,fname + '.hdf5'))

                    # Daq Size
                    data_length = daq['CFS_Accelerator_Pedal_Position'].shape[1]

                    # Date Index
                    data_run_start = ''.join(re.findall(r'\d+', np.array2string(np.array(daq['RunInst']).flatten())))
                    data_run_start = dt.datetime.strptime(data_run_start, '%Y%m%d%H%M%S')
                    data_run_start = pd.date_range(pd.to_datetime(data_run_start), periods=data_length, freq='0.01667S')
                    
                    data_list = []
                    col_list = []
                    for elem in elemlist:
                        data = np.array(daq[elem]).T
                        num_col = data.shape[1]
                        data_list.append(data)
                        for i in range(num_col):
                            col_list.append(elem + '_' + str(i))

                    data = np.concatenate(data_list, axis=1)

                    df = pd.DataFrame(data=data, index=data_run_start, columns=col_list)
                    df.index.rename('timestamp', inplace=True)
                    df.to_csv(os.path.join(root,fname + '.csv'))

                except AssertionError:
                    print("Could not read {}".format(fname))

if __name__ == "__main__":
    main()
