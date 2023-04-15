import subprocess
import sys
import pandas as pd
import os
import  torch
import utils

data = pd.DataFrame({'a':[1,2,3], 'b':[4,5,6]})

date = sys.argv[1]
mnt_dir = '/mnt/data'

directory_name = os.path.join(mnt_dir,date,"harvest_data")
print(f"LAYING DOWN DIR: {directory_name}")
if not os.path.exists(directory_name):
    print('GOTTA MAKE THE PATH')
    os.makedirs(directory_name)

data_file = os.path.join(directory_name,'some_good_data.csv')
data.to_csv(data_file,index = False)

new_data = pd.read_csv(data_file)
print('the new data that was reloaded')
print(new_data)


print(f"I GOT THE DATE: {date}")
utils.hello('sydney!')
output = subprocess.run(['ls', '-latrs', mnt_dir], capture_output=True, text=True)

print(output.stdout)