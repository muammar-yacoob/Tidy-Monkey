# Tidy Monkey Tutorial Script

## Introduction (0:00-0:30)
Welcome to this quick tutorial on Tidy Monkey, the Blender addon that might just save your sanity when working with complex models. If you've ever spent hours fixing mesh issues or setting up exports, this addon is about to become your new best friend. Let's skip the fluff and jump straight into what matters.

## Installation (0:30-1:00)
First, download the addon from the GitHub releases page. In Blender, go to Edit > Preferences > Add-ons > Install, then select the TidyMonkey.zip file. Enable the checkbox, and you're ready to go. Press N in the 3D viewport to reveal the sidebar, and look for the Tidy Monkey tab.

## Object Mode Tools (1:00-3:30)

### Beautify (1:00-1:30)
Select one or more mesh objects and click "Beautify." This applies several mesh improvements in one go:
- Makes normals consistent
- Converts triangles to quads
- Dissolves unnecessary vertices
- Adds bevel and weighted normal modifiers
- Sets up auto-smooth
- For parent-child objects, transfers normals at the seams

The result? Clean topology without those weird shading artifacts that make your models look like they were made in 1997.

### Clear Materials (1:30-1:45)
Need to start fresh with materials? Select objects and click "Clear Materials." It removes all material assignments instantly. Sometimes your model needs a blank canvas—like giving it a haircut after a terrible dye job.

### Generate Actions (1:45-2:10)
For animators, this one's a gem. Click "Generate Actions" to convert animation strips into individual action data blocks. This makes animations easier to manage and reuse across different files or characters. Your animation workflow just went from "where is that keyframe?" to "oh, there it is."

### Clean Textures (2:10-2:25)
Blender files bloated with unused textures? One click on "Clean Textures" and they're gone. Your file size will thank you, and so will anyone you share your files with.

### Rename Bones (2:25-2:45)
For armatures, enter search text and replacement text, then click "Rename Bones." You can toggle case sensitivity too. Goodbye to manually renaming 200 bones because your naming convention changed halfway through.

### Export FBX/GLB (2:45-3:30)
Exporting for game engines or other software is now painless:
- Export multiple objects at once or each object separately
- FBX or GLB formats
- Automatic texture packing that includes only what you need
- Proper scale conversion
- Animation export options

No more going through the same 10-step process every time you need to export something. Even better, you won't forget to pack those textures and then wonder why your model looks like a purple checkerboard in Unity.

## Edit Mode Tools (3:30-4:45)

### Checker Edge (3:30-4:00)
In edit mode, select edges in a loop and click "Checker Edge." It selects alternating edges in your selection. With the dissolve option enabled, it'll remove those edges, creating a cleaner, lower-poly mesh. Perfect for game assets where you need to reduce polygon count without making your model look like it was hit by a car.

### Clean Verts (4:00-4:20)
This tool finds vertices with exactly two edge connections and dissolves them. These vertices don't affect the shape but add unnecessary complexity. Think of it as removing the middle managers from your mesh's organizational chart—nobody notices they're gone, but everything runs more efficiently.

### Fix Rotation (4:20-4:45)
Select faces, edges, or vertices and click "Fix Rotation" to align their rotation to world or local coordinates. Those misaligned UVs and texture issues you've been fighting? Consider them handled. It's like a chiropractor for your mesh.

## Real-World Workflow Example (4:45-5:45)
Let's see how these tools work together in a typical scenario:

1. Import a complex mesh from another program
2. Use "Beautify" to clean up the topology and get consistent shading
3. Use "Clean Verts" in edit mode to simplify geometry
4. Use "Checker Edge" to reduce edge loops in less important areas
5. Use "Fix Rotation" on any parts with awkward orientation
6. Finally, use the export function to get it into your game engine

What would normally take 30+ minutes and multiple steps is now done in about 2 minutes.

## Conclusion (5:45-6:00)
Tidy Monkey isn't trying to replace your modeling skills—it's giving you time to use those skills on things that actually matter. Less cleanup, more creativity. If you found this helpful, the links for the addon are in the description. Happy Blending!

---

## Call to Action
Don't forget to star the repository if you find this useful, and consider supporting the developer with a coffee if this addon saves you time. Links are in the description. 