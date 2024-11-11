Example usage
=============

This section gives a brief presentation of the steps together with
examples of actual command line usage. It ends with a complete script
that could be used to process a dataset with only a few
modifications. The next :ref:`section, details, <ch_details>` shows all command line
options and contain in depth descriptions of some of the steps.

Extract images as tiff files from nd2
-------------------------------------


.. code:: shell

          radiantkit nd2_to_tiff CJ_20240702_CJ052_SLIDE012.nd2


Segment nuclei
--------------

Please check the command line options with

.. code:: shell

          radiantkit tiff_segment --help

In this case we let radiantkit know the name of the channel containing
the nuclei, ask to apply a mild low pass filter and allows it to use 8
threads. Please note that options like `--only-focus` produce 2D
images and that is not supported in the downstreams analysis at the moment.

.. code:: shell

          radiantkit tiff_segment --gaussian 2 CJ_20240702_CJ052_SLIDE012 --inreg "cjDAPI.*\.tif" --threads 8

The result is that we get a `tiff_segment.log.txt` file in the folder
`CJ_20240702_CJ052_SLIDE012` as well as a binary mask, `file.mask.tif`
for each `file.tif`.

Processing 8 image of size [41, 1608, 1608] using 8 threads used less
than 32 GB of RAM and took about 3 minutes.

Extract radial profiles
-----------------------

.. code:: shell

          radiantkit measure_objects CJ_20240702_CJ052_SLIDE012 cjDAPI


This will create a
`CJ_20240702_CJ052_SLIDE012/objects/nuclear_features.tsv` which
contains some measurements of the nuclei. Though that it would produce a a `radiant.pkl`
which contain the radial profiles ?

What is a particle?

Select nuclei
-------------

.. code:: shell

          radiantkit select_nuclei CJ_20240702_CJ052_SLIDE012 cjDAPI

This does not work at the moment.

Generate a report
-----------------


Example script
--------------

Given a folder structure like this:

.. code::

   ├── CJ_20240702_CJ052_SLIDE007
   ├── CJ_20240702_CJ052_SLIDE008
   ├── CJ_20240702_CJ052_SLIDE009
   ├── CJ_20240702_CJ052_SLIDE010
   ├── CJ_20240702_CJ052_SLIDE011
   └── CJ_20240702_CJ052_SLIDE012

The following script would process all images and generate a report:

.. literalinclude:: example_script.sh.txt
   :language: bash
