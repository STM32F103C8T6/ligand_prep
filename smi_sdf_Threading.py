from openbabel import pybel
import concurrent.futures
import subprocess
import time
import os
from tqdm import tqdm

current_path = os.getcwd()
work_threading = 22


def smi_sdf(file):
    smi_file_path = file
    sdf_file_path = str(file.split('.')[0] + '.sdf')
    molecules = pybel.readfile('smi', smi_file_path)
    # print(sdf_file_path)
    # time.sleep(0.5)
    with pybel.Outputfile('sdf', sdf_file_path, overwrite=True) as sdf_output:
        for mol in molecules:
            print(mol)
            mol.make3D()
            sdf_output.write(mol)
            # init_numb = init_numb + 1


def get_file_list(path):
    file_list = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file)) and file.endswith('.smi')]
    return(file_list)


file_list = get_file_list(current_path)
start_time = time.time()

# with concurrent.futures.ThreadPoolExecutor(max_workers=work_threading) as executor:
#     executor.map(smi_sdf, file_list)

with concurrent.futures.ThreadPoolExecutor(max_workers=work_threading) as executor:
    with tqdm(total=len(file_list), desc='Processing files', unit='file') as progress_bar:
        list(tqdm(executor.map(smi_sdf, file_list), total=len(file_list), desc='Processing files', unit='file'))

end_time = time.time()

# print('total process molecular: ', str(init_numb))
print('total takes time :', str(end_time - start_time))

