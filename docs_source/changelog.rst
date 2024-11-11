Changelog
=========

..
    The format is based on `Keep a Changelog
    <http://keepachangelog.com/en/1.0.0/>`__ and this project adheres
    to `Semantic Versioning <http://semver.org/spec/v2.0.0.html>`__.

0.1.0
-----

This marks the first release in the new repository. The archived
parent can be found at `github.com/ggirelli/radiantkit
<https://github.com/ggirelli/radiantkit>`_

Added
~~~~~
- Added the option `--gaussian sigma` to `tiff_segment`. That will low
  pass filter images with a Gaussian kernel as a first step in the
  segmentation pipeline. Solves issues with noisy image.
- Added the option `--slice2d` to `radial_population` which will tell
  radiantkit to only extract intensities at the plane with the largest
  cross sectional area for each nuclei. Expected to be useful for
  nuclei grown and attached to coverslips.

Changed
~~~~~~~

- The binary name is `radiantkit`, not `radiant` any more.
- Runs with Python 3.12 and probably also 3.13 but probably not with
  older versions.
- Updated dependency list in ``pyproject.toml``.
- The documentation has been updated, although it is far from complete.
- Changes reflection API changes in pandas and scikit-image.
- Don’t care what the axes are called in the tif files, the first axis
  will be considered as the axial direction “Z”.
- Fixed: Correct titles in the settings screens (several had the same
  title, “Object extraction”).
- In `radial_population`: Files containing the word `mask` are not
  allowed to be used as regular images and will be silently
  ignored. This solves the issues that masks could be confused with
  normal images when the inreg was not properly configured.
- It is considered an error (previously a warning) if there is more
  than one image per channel for any FOV when loading images from a
  folder.

Removed
~~~~~~~
- Progressbars that were in the way for debugging (a few
  `rich.track`), can be enabled again in `util.py`

Regressions
~~~~~~~~~~~

-  Compression disabled when writing tif files (tifffile has changed the
   API).
- ``WARNING <tifffile.TiffWriter 'cjDAPI_007.mask.tif'> not writing       extratag 393``
