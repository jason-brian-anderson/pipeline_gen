import  torch

print('HARVEST SOME DATA>>>>>>>>>>>>>>>>>>>>>>>>>>>')

import subprocess

mnt_dir = '/mnt/data'

output = subprocess.run(['ls', '-latrs', mnt_dir], capture_output=True, text=True)

print(output.stdout)