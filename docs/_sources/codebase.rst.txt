Codebase
========

The code is in OOP style divided into two parts, `radiantkit` which
contain the core functionality and `radiantkit.scripts` which contain
the command line tools.

The main entry point can be found in `run.py` which is also called from `__main__.py`.

Class inheritance
-----------------

.. code::

   BinarizerSettings -> Binarizer
   BoundingElement
   ChannelList
   CziFile -> CziFile2
   Enum -> CenterType
   Enum -> DistanceType
   Enum -> LaminaDistanceType
   Enum -> MidsectionType
   Enum -> ProjectionType
   Enum -> RootType
   Enum -> SegmentationType
   Enum -> ShellType
   ImageBase -> Image -> ImageBinary
   ImageBase -> Image -> ImageBinary -> ParticleBase -> Particle -> Nucleus
   ImageBase -> Image -> ImageGrayScale
   ImageBase -> Image -> ImageLabeled
   MultiRange
   ND2Reader -> ND2Reader2
   NucleiList
   OutputDirectories -> Output
   OutputDirectories -> ReportBase
   OutputDirectories -> ReportMaker
   OutputReader
   ParticleFinder
   ProfileMultiConditionNorm
   ProfileSingleCondition
   RadialDistanceCalculator
   ReportPage
   SeriesList
   string.Template -> TIFFNameTemplate
   TIFFNameTemplateFields


The call stacks are somewhat deep and can be hard to understand

.. code::

   where
   /home/erikw/.local/bin/radiantkit(8)<module>()
   -> sys.exit(radiant())
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/run.py(74)radiant()
   -> args.run(args)
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/scripts/radial_population.py(380)run()
   -> profiles = series_list.get_radial_profiles(
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/series.py(582)get_radial_profiles()
   -> self.__prep_single_channel_profile(
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/series.py(506)__prep_single_channel_profile()
   -> channel_intensity_data = self.__retrieve_channel_intensity_at_distance(
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/series.py(469)__retrieve_channel_intensity_at_distance()
   -> s.init_particles_distances(rdc, reInit)
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/series.py(155)init_particles_distances()
   -> particle.init_distances(rdc, C)
   /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/particle.py(168)init_distances()
   -> distances = rdc.calc(self, C)
   > /home/erikw/.local/share/pipx/venvs/radiantkit/lib/python3.12/site-packages/radiantkit/distance.py(159)calc()
   -> return (contour_dist.pixels, center_dist.pixels)
