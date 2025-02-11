#!/bin/bash

strn=$1
export strn
script_folder="/mnt/d/py/Science/from_txt_to_xlsx/"
data_folder="ryazantsev_m@login1.hpc.spbstu.ru:/home/ibsbnicigt/ryazantsev_m/Projects/001_001_force_fields/sub$strn/scans_$strn/scans_result$strn/"

cd to_learn_$strn ; mkdir plot$strn ; cd plot$strn

scp -r -i ~/.ssh/id_rsa_polt $data_folder/qm_e.txt qm_e.txt
scp -r -i ~/.ssh/id_rsa_polt $data_folder/mm_e.txt mm_e.txt

python3 $script_folder/ff_to_xlsx.py

mv ff_scan.xlsx ff_scan$strn.xlsx
mv qm_e.txt qm_e_$strn.txt ; mv mm_e.txt mm_e_$strn.txt

cd .. ; cd ..

