#!/bin/bash

# Cleans (if necessary) and sort the files from the runs to the specific folders
# namelist is simplified

for i in  $(ls);
do
    if [ -d $i ];
    then
	echo cleaning $i
	cd $i
	rm *restart* run_nemo* slope* slurm* time.step xios_server.exe *output* nemo *~ *.xml *.txt *.log layout.dat namelist*
	cd ..
    fi
done

cd ..

echo ""
echo starting to link files

md (){
    echo $1
    rm -r $1
    mkdir $1
    cd $1
}

md domcfg_1_file
ln -s ../runs/EXP_1_proc/domain_cfg_out.nc .
cd ..

md domcfg_mesh_mask
ln -s ../runs/EXP_4_procs/domain_cfg_out* .
ln -s ../runs/EXP_4_procs/mesh_mask* .
cd ..

md domcfg_multi_files
ln -s ../runs/EXP_4_procs/domain_cfg_out* .
cd ..

md mesh_mask_multi_files
ln -s ../runs/EXP_4_procs/mesh_mask* .
cd ..

md nemo
for i in T U V W;
do
    ln -s ../runs/EXP_1_proc/BASIN_1d_00010101_00010103_grid_${i}.nc BASIN_grid_${i}.nc
done
cd ..

md open_and_merge
for i in T U V W;
do
    ln -s ../runs/EXP_1_proc/BASIN_1d_00010101_00010103_grid_${i}.nc BASIN_grid_${i}.nc
done
ln -s ../runs/EXP_1_proc/domain_cfg_out.nc .
cd ..

md surface_fields
ln -s ../runs/EXP_1_proc/BASIN_1d_00010101_00010103_surface_grid_T.nc BASIN_surface_grid_T.nc
cd ..

echo DONE
