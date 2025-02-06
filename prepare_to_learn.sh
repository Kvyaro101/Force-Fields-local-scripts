#!/bin/bash

strn=$1
dynamics_folder="ryazantsev_m@login1.hpc.spbstu.ru:/home/ibsbnicigt/ryazantsev_m/Projects/001_001_force_fields/sub$strn/dynamics$strn"
opt_folder="ryazantsev_m@login1.hpc.spbstu.ru:/home/ibsbnicigt/ryazantsev_m/Projects/001_001_force_fields/sub$strn/optimisations$strn/ ."

# getting general files. Not edit them
cd "to_learn_$strn" ; basedir=$(pwd)
cp -r ../scripts .
unzip UNK*.zip; mv tmp/ libpargenfiles
mkdir to_learn
cp libpargenfiles/*.prm to_learn ; rm to_learn/*.Q.prm ; mv to_learn/*.prm to_learn/ff.par # took .par from libpargen

cp libpargenfiles/*.lib scripts/generatefilepramfiles/charges.txt
cp sub$strn.xyz scripts/generatefilepramfiles/struct.xyz # cp all files for read_graphs.py

# modified charges.txt for read_graphs
cd scripts/generatefilepramfiles ; sed -n '/\[atoms]/,\/\[bonds]/p' charges.txt | awk '/\[atoms]/ {f=1;next} /\[bonds]/ {f=0;next} f' >  temp.txt ; mv temp.txt charges.txt
awk '{print $4}' charges.txt > temp.txt ; mv temp.txt charges.txt

python3 read_graphs.py ; mv mol.pdb mol.psf ff.top ../../to_learn # run read_graphs.py and get .pdb, .pcf, .top from it

# creating dynamics input
cd ../../
scp -r -i ~/.ssh/id_rsa_polt  $opt_folder .
scp -r -i ~/.ssh/id_rsa_polt $dynamics_folder .
cd dynamics$strn

run_rrt () {
	cd $basedir/scripts/
	python3 read_reanet_traj.py
	cd -
}

dnum=0
for dir in */; do
	cd "$dir"
	cp output/* $basedir/scripts ; run_rrt
	echo $dnum
	mv $basedir/scripts/0 $basedir/to_learn/$dnum
	dnum=$((dnum+1))
	cd ..
done

# sort dynamics input so that $basedir/to_learn/0 conformer dynamics had the lowest 0-step energy
cd $basedir/to_learn
for dir in */; do
	cd $dir
	current_energy=$(grep "^0 " energy | awk '{print $NF}')
	echo "Current Energy: $current_energy, compare: $compare"
	if [[ -z "$compare" || $(echo "$compare > $current_energy" | bc -l) -eq 1 ]]; then
		echo $dir
		compare="$current_energy"
		if [[ "$dir" != "0/" ]]; then
			cd ../
			mv 0 temp_folder
			mv $dir 0
			mv temp_folder $dir
			cd $dir
		fi
	fi
	cd ..
done


cd $basedir/to_learn ; third_column_array=()

# edit general inputs
while IFS= read -r line; do
	
	if [[ "$line" == "AUTO ANGLES DIHE"* ]]; then
		break
	fi
	
	fields=($line)

	if [[ ${#fields[@]} -ge 3 ]]; then
		third_column_array+=("${fields[2]}")
	fi
done < ff.top

echo "Atoms:" ; cp ff.par temp.par

# in .par file adjusting atoms identifiers and changing WdW param strings
for pattern in "${third_column_array[@]}"; do
	echo "$pattern"
	element="${pattern%%[0-9]*}"
	number="${pattern##*[!0-9]}"
	if (($number < 10)); then
		sed -i "s/${element}80${number}/${element}${number}/g" temp.par
	elif (($number < 100)); then
		sed -i "s/${element}8${number}/${element}${number}/g" temp.par
	elif (($number < 110)); then
		sed -i "s/${element}50${number}/${element}${number}/g" temp.par
	else
		sed -i "s/${element}5${number}/${element}${number}/g" temp.par
	fi
done
sed -i "s/NONBONDED nbxmod 5 atom cdiel switch vatom vdistance vswitch -/NONBONDED  NBXMOD 5  GROUP SWITCH CDIEL -/g" temp.par
sed -i "s/cutnb 14.0 ctofnb 12.0 ctonnb 11.5 eps 1.0 e14fac 0.5  geom/     CUTNB 14.0  CTOFNB 12.0  CTONNB 10.0  EPS 1.0  E14FAC 0.83333333  WMIN 1.4/g" temp.par


mv temp.par ff.par

mkdir $basedir/to_learn/sub1; mv $basedir/to_learn/* $basedir/to_learn/sub1

