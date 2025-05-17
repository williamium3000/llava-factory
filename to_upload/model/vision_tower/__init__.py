import os

import importlib
import os

def import_modules(models_dir, namespace):
    for file in os.listdir(models_dir):
        path = os.path.join(models_dir, file)
        if (
            not file.startswith("_")
            and not file.startswith(".")
            and file.endswith(".py")
        ):
            model_name = file[: file.find(".py")] if file.endswith(".py") else file
            importlib.import_module(namespace + "." + model_name)


VISION_TOWER_FACTORY = {}

def VisionTowerFactory(vision_tower_name):
    vision_tower_name = vision_tower_name.split(':')[0]
    model = None
    for name in VISION_TOWER_FACTORY.keys():
        if name.lower() in vision_tower_name.lower():
            model = VISION_TOWER_FACTORY[name]
    assert model, f"{vision_tower_name} is not registered"
    return model


def register_vision_tower(name):
    def register_vision_tower_cls(cls):
        if name in VISION_TOWER_FACTORY:
            return VISION_TOWER_FACTORY[name]
        VISION_TOWER_FACTORY[name] = cls
        return cls
    return register_vision_tower_cls


# automatically import any Python files in the models/ directory
models_dir = os.path.dirname(__file__)
import_modules(models_dir, "to_upload.model.vision_tower")
