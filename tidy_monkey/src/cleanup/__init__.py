from . import cleanup_panel
from . import fix_normals
from . import clear_materials
from . import generate_actions
from . import clean_textures
from . import rename_bones
from . import rename_vertex_groups
from . import clean_verts

classes = (
    *cleanup_panel.classes,
    *fix_normals.classes,
    *clear_materials.classes,
    *generate_actions.classes,
    *clean_textures.classes,
    *rename_bones.classes,
    *rename_vertex_groups.classes,
    *clean_verts.classes,
)

def register():
    rename_bones.register()

def unregister():
    rename_bones.unregister() 