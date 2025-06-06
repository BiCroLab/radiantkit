#!/bin/bash
#SBATCH --job-name=job_name
#SBATCH --mail-type=ALL
#SBATCH --mail-user=user.name@fht.org
#SBATCH --output=%j_%x.out
#SBATCH --error=%j_%x.err
#SBATCH --partition=cpuq
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=100GB
#SBATCH --time=0-23:00:00

# Exit immediately if a command exits with a non-zero status:
set -e

source /home/user.name/miniconda3/bin/activate radiantkit

##############################################################
#             Settings to be adjust to you images:
##############################################################
dx=65 # pixel size (nm)
dy=65
dz=500 # axial direction
nucprefix='375' # Prefix of the files containing the nuclei staining
nthread=8 # Number of concurrent threads to use
dir=/{path_to_directory_containing.nd2}/
##############################################################

# Convert nd2 to tiff
radiantkit nd2_to_tiff ${dir} 

# # Per folder processing
process_cond() {
    # Automatic 3D segmentation
    radiantkit tiff_segment ${1} \
               --threads ${nthread} \
               --gaussian 2 \
               --inreg "${nucprefix}.*\.tif" \
               -y

    # Measure properties of the segmented objects
    radiantkit measure_objects ${1} ${nucprefix} \
               --threads ${nthread} \
               --aspect ${dz} ${dy} ${dx} \
               -y

    # Select G1 nuclei
    # Needs at least 6 nuclei
    radiantkit select_nuclei ${1} ${nucprefix} \
               --k-sigma 2 --threads ${nthread} \
               -y

    # Measure radial profiles for all segmented nuclei
    radiantkit radial_population ${1} ${nucprefix} \
               --aspect ${dz} ${dy} ${dx} \
               --mask-suffix mask_selected \
               --threads ${nthread}  -y \
               --slice2d
}

# Process each folder / condition
for slideDir in ${dir}/*/
do
echo "$slideDir being processed"
process_cond ${slideDir}
done
 

# Make a report (radiant.report.html)using all conditions that can be found in subfolders:
# Need to be inside the main folder containing nd2 files and folders:
cd ${dir}
radiantkit report .
