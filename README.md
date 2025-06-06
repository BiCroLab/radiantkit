# Radiantkit 
Radiantkit is a Python package containing tools for full-stack
image analysis YFISH images.

This repository is a fork of the archived
[ggirelli/radiantkit](https://github.com/ggirelli/radiantkit) with the
aim to keep the code up to date with current Python versions.      

The [CHANGELOG](https://bicrolab.github.io/radiantkit/changelog.html) will
describe any changes to the original repository.

_If you want to get in touch, please open an [issue
ticket](https://github.com/BiCroLab/radiantkit/issues)_.
***

## Installation instructions
#### :arrow_forward: For full and detailed installation instructions and usage read the full documentation [here](https://bicrolab.github.io/radiantkit/).

### For use with SLURM + conda env
1. Clone the repository:   
```
git clone https://github.com/BiCroLab/radiantkit.git
```

2. Create a conda env from yaml file provided ([radiant-kit-env.yml](radiant-kit-env.yml)):   
```
conda env create -f radiant-kit-env.yml
```   

3. Ensure your images are saved all together in .nd2 format in a single directory.

4. Modify the [radiantK_SLURM_jobscript.sh](./radiantK_SLURM_jobscript.sh) to include correct parameters for your imaging data.

5. Submit the job to SLURM:   
```
sbatch radiantK_SLURM_jobscript.sh
```

## Frequently Asked Questions (FAQ)

#### Q. What file formats does this pipeline accept?
We currently support:
- `.nd2`: first step is to convert to .tif (see [radiantK_SLURM_jobscript.sh](./radiantK_SLURM_jobscript.sh)).
- `.tif` / `.tiff`: recommended (channel-separated)

#### Q. What kind of fluorescent imaging techniques is this software compatible with?
- Confocal
- Spinning disk confocal
- Widefield (if first deconvolved e.g. using [deconwolf](https://github.com/elgw/deconwolf))

#### Q. Should I use 2D or 3D segmentation?
This depends on the application and cell-type. In general we would recommend using 2D segmentation if working with nuclei that are not round/uniformly shaped.


