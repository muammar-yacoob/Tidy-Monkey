from . import organize_panel
from . import origin_to_selected
from . import center_origins
from . import origin_to_bottom
from . import align
from . import fix_rotation
from . import apply_modifiers
from . import select_similar
from . import checker_edge
from . import select_bottom
from . import select_similar_mesh

classes = (
    *organize_panel.classes,
    *origin_to_selected.classes,
    *center_origins.classes,
    *origin_to_bottom.classes,
    *align.classes,
    *fix_rotation.classes,
    *apply_modifiers.classes,
    *select_similar.classes,
    *checker_edge.classes,
    *select_bottom.classes,
    *select_similar_mesh.classes,
) 