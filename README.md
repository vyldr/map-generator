# Map Generator

This program creates random maps to be used in Manic Miners.  It is available as a Python script or a Windows executable.

## How to use

Simply run either the exe or the Python script and the map will automatically be created and saved as `Untitled.dat`.

> `python map-generator.py`

or

> `map-generator.exe`

The program will also display the parameters used to create that map.  If the file name is already taken, a number will be appended so the first map is not overwritten.

### Custom Parameters

You can choose custom parameters with command line arguments.  Here are some examples.

To create a 48 * 48 map:
> `map-generator.exe -size 48`

To choose the level name and file name:
> `map-generator.exe -name 'Cool Level Name'`

To choose the biome:
> `map-generator.exe -biome lava`

To hide lots of crystals in most walls:
> `map-generator.exe -crystalDensity 1.0`

To cover most of the ground with slimy slug holes:
> `map-generator.exe -slugDensity 0.7`

To make the ground very uneven:
> `map-generator.exe -terrain 50`

To create a level similar to "Lake of Fire"
> `map-generator.exe -wallDensity 0.3 -solidDensity 0.2 -biome lava -terrain 20 -floodLevel 0.55 -flowDensity 0.005 -name 'Puddle of Spicy Rock'`

### List of parameters
| Parameter | Range of values | Default | Description |
|-|-|-|-|
| `length` | 4+ | 64 | How long to make the map
| `width` | 4+ | 64 | How wide to make the map
| `size` | 4+ | 64 | Overrides both length and width
| `solidDensity` | 0.0 - <1.0 | random | How much solid rock to generate
| `wallDensity` | 0.0 - <1.0 | random | How much other rock to generate
| `oreDensity` | 0.0 - 1.0 | random | How common ore is
| `crystalDensity` | 0.0 - 1.0 | random | How common energy crystals are
| `oreSeamDensity` | 0.0 - 1.0 | random | How common ore seams are
| `crystalSeamDensity` | 0.0 - 1.0 | random | How common energy crystal seams are
| `rechargeSeamDensity` | 0.0 - 1.0 | random | How common recharge seams are
| `floodLevel` | 0.0 - <1.0 | random | The height to be flooded with water or lava
| `floodType` | water or lava | random | Whether to flood with water or lava
| `flowDensity` | 0.0 - <1.0 | random | How common erosion sources are
| `flowInterval` | 1+ | random | How slow erosion spreads
| `preFlow` | 1+ | random | How much erosion should spread before the level starts
| `landslideDensity` | 0.0 - <1.0 | random | How common landslide sources are
| `landslideInterval` | 1+ | random | How long between landslides
| `monsterDensity` | 0.0 - 1.0 | random | How common monster sources are
| `monsterInterval` | 1+ | random | How long between monster attacks
| `slugDensity` | 0.0 - <1.0 | random | How common slimy slug holes are
| `terrain` | 1+ | random | How much the height of the terrain varies vertically
| `smoothness` | 1+ | 16 | How smoothly the terrain slopes
| `oxygen` | 1+ | Based on `size` | How much oxygen to start with
| `biome` | rock, lava, ice | random | Which biome to use
| `stats` | true or false | true | Whether to show the statistics
| `save` | true or false | true | Whether to save the file
| `name` | 'level name' | 'Untitled' | What to name the file
| `show` | true or false | false | Whether to show the map, does not work on Windows

## Notes

- Some parameters, such as `wallDensity` or `floodLevel` can limit the number of ground tiles, which can make it impossible to set a starting point if their values are too high.  This will force the program to keep trying to create a level and eventually give up.
- Setting the `length` and `width` parameters to different values will create a non-square map.  The map will still generate fine, but Manic Miners will not like it.
- The objectives and challenges are often less interesting than those of maps created by people.  Feel free to edit the maps to add more interesting challenges.