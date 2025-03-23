import os

class TowerModel:
    directory: str
    name: str
    level: int
    is_evolution: bool

    def __init__(self, directory: str, name: str, level: int, is_evolution: bool):
        self.directory = directory
        self.name = name
        self.level = level
        self.is_evolution = is_evolution

    def __str__(self):
        if self.is_evolution:
            return f"{self.name} (Evolution)"
        else:
            return f"{self.name} {self.level} (Level)"
                                                                
    def generate_gltf(self):
        blend_path = f"./{self.directory}/{self.find_blend_file()}"

        os.makedirs("./output", exist_ok=True)

        if self.is_evolution:
            output_name = f"./output/{self.name}.gltf"
        else:
            output_name = f"./output/{self.name}_{self.level}.gltf"
        
        os.system(f"blender -b {blend_path} --python-expr \"import bpy; bpy.ops.wm.open_mainfile(filepath='{blend_path}'); \
for obj in bpy.data.objects: \
    if obj.type == 'MESH': \
        for mod in obj.modifiers: \
            if mod.type == 'MIRROR': \
                bpy.context.view_layer.objects.active = obj; \
                bpy.ops.object.modifier_apply(modifier=mod.name); \
bpy.ops.export_scene.gltf(filepath='{output_name}', export_animations=False)\"")
    
    def find_blend_file(self):
        blend_files = [f for f in os.listdir(self.directory) if f.endswith(".blend")]
        if len(blend_files) == 0:
            raise Exception(f"No .blend file found in {self.directory}")
        
        return blend_files[0]


towers_paths = os.listdir("Towers")
towers_paths.remove("All")

towers: list[TowerModel] = []

for tower in towers_paths:
    tower_files = os.listdir(f"Towers/{tower}")

    level_paths = [f for f in tower_files if f.startswith("Level")]
    evolution_paths = [f for f in tower_files if f not in level_paths]

    for path in level_paths:
        level = int(path.split("Level")[1]) - 1
        model = TowerModel(f"Towers/{tower}/{path}", tower, level, False)
        towers.append(model)

    for path in evolution_paths:
        model = TowerModel(f"Towers/{tower}/{path}", path, -1, True)
        towers.append(model)

print([str(tower) for tower in towers])

os.makedirs("./output", exist_ok=True)

for tower in towers:
    print(f"Generating {tower}")
    tower.generate_gltf()