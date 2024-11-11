.. rst questions? https://www.sphinx-doc.org/en/master/index.html

radiantkit version |version|
============================

**Rad**\ ial **I**\ mage **An**\ alysis **T**\ ool\ **kit**
(RadIAnTkit or simply radiantkit) is a Python3.12+ package containing
tools for full-stack image analysis for YFISH images, such as used in
the GPSeq pipeline. This is a detached fork of the original, now
archived, repository at
`github.com/ggirelli/radiantkit
<https://github.com/ggirelli/radiantkit>`_.


Pipeline summary
----------------

-  **Convert** proprietary microscope formats CZI (Zeiss) and ND2
   (Nikon) to the TIFF format.

-  **Segment** nuclei in 2D or 3D.

- **Select** nuclei in G1-phase of the cell cycle, based on DNA
   staining and nuclear volume.

-  **Extract** segmented objects and **measure** their features (e.g.,
   volume, integral of intensity, shape descriptors).

-  Measure **radial patterns** as radial profiles (with different
   center definitions), and characterize them (e.g., peaks,
   inflection points, contrast).

- And finally, generate interactive reports.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   example.rst
   usage.rst
   install.rst
   changelog.rst
   codebase.rst
   todo.rst
