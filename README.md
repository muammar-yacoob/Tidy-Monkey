[//]: # (Constants)
[license-link]: ../../blob/main/LICENSE
[stars-link]: ../../stargazers
[youtube-link]: https://youtu.be/3g1JKg0-Wtc
[website-link]: https://spark-games.co.uk
[coffee-link]: https://buymeacoffee.com/spark88
[bug-link]: ../../issues
[release-link]: ../../releases
[object-tutorial-link]: https://youtu.be/3g1JKg0-Wtc
[fork-link]: ../../fork
[privacy-link]: ../../blob/main/PRIVACY.md

# Tidy Monkey

<div align="center">
  <img src="./res/logo.png" width="300" alt="Tidy Monkey Logo">

  <h3>Productivity Tools for Blender 3D Artists</h3>

  [![License](https://img.shields.io/badge/license-MIT-blue.svg)](../../blob/main/LICENSE)
  [![Issues](https://img.shields.io/badge/issues-report-red?logo=github)](../../issues)
  [![YouTube](https://img.shields.io/badge/YouTube-red?style=flat&logo=youtube)](https://youtu.be/3g1JKg0-Wtc)
  [![Website](https://img.shields.io/badge/website-visit-green)](https://spark-games.co.uk)
  [![Buy me a coffee](https://img.shields.io/badge/coffee-donate-yellow.svg)](https://buymeacoffee.com/spark88)
</div>

## Features

- Topology cleanup and editing tools
- Automated mesh decimation and simplification
- Parent-child normal transfers
- Export automation with texture packing
- Material and texture management

## Tool Functions

### Object Mode

- **Beautify**: Applies consistent normals, transforms tris to quads, adds bevel/weighted normal modifiers, and transfers normals data between parent-child objects.

- **Clear Materials**: Removes all unused material from selected objects.

- **Clean Textures**: Removes all unused image textures from the .blend file.

- **Generate Actions**: Converts animation strips to individual action data blocks.

- **Rename Bones**: Removes keywords like `mixamo` from bone names without breaking the animation.

- **Export FBX/GLB**: Packs materials, textures and generates actions. Currently only supports FBX & GLB formats.

### Edit Mode

- **Checker Edge**: Selects alternating edges in connected loops with dissolve option for topology decimation.

- **Clean Verts**: Identifies and dissolves vertices with exactly 2 edge connections.

- **Fix Rotation**: Aligns selected elements' rotation to world or local coordinate space.

## Installation

1. [Download latest release](../../releases)
2. Drag the `TidyMonkey.zip` file into Blender
3. Press `N` key to view the sidebar panel

<table>
<tr>
<td width="50%" valign="top">

### Object Mode
[![Object Mode Tutorial](./res/Object%20Mode.jpg)](https://youtu.be/3g1JKg0-Wtc)

</td>
<td width="50%" valign="top">

### Edit Mode
![Edit Mode Guide](./res/Edit%20Mode.jpg)

</td>
</tr>
</table>

## Support

- [⭐ Star the repo](../../stargazers) to support development
- [☕ Buy me a coffee](https://buymeacoffee.com/spark88) to fuel more tools
- [🔧 Contributions welcome](../../fork)
