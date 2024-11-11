Future / to do
==============

- [ ] Document the code better. At least sensible docstrings for the
  major classes.

- [ ] Correct for shifts between channels. It is assumed that this has
  been performed by some other tool.

- [ ] Tear out the `assert` and replace it with a proper
  `sys.exit(-1)`. For example in places like this:

   .. code:: python

      assert Confirm.ask("Confirm settings and proceed?")

- [ ] When calculating the radial profiles it would be much more
  memory efficient to load-process-free one image at a time rather
  than loading everything into RAM.

- [ ] Place temporary files an a separate folder or at least offer a
  cleanup command to remove all files created by radiantkit.


Refactoring
-----------

- [ ] Remove some intermediate classes, for example `ImageBase`,
  `ParticleBase` and possible also `Particle`.

- [ ] Integrate the `RadialDistanceCalculator` directly into `Nucleus`?

- [ ] Rename `BoundingElement` to `BoundingBox` etc ...

- [ ] rename `ND2Reader2` to `rkND2reader` and `CziFile2` to `rkCziFile`.

- [ ] Merge `Series` and `ChannelList`

- [ ] rename `Series` to `FOV` (it is a multi channel FOV).

- [ ] consider placing the script in a separate package (some
  decoupling needed).
