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


CONNECTOR_FACTORY = {}

def ConnectorFactory(connector_name):
    model = None
    for name in CONNECTOR_FACTORY.keys():
        if name.lower() in connector_name.lower():
            model = CONNECTOR_FACTORY[name]
    assert model, f"{connector_name} is not registered"
    return model


def register_connector(name):
    def register_connector_cls(cls):
        if name in CONNECTOR_FACTORY:
            return CONNECTOR_FACTORY[name]
        CONNECTOR_FACTORY[name] = cls
        return cls
    return register_connector_cls


# automatically import any Python files in the models/ directory
models_dir = os.path.dirname(__file__)
import_modules(models_dir, "to_upload.model.connector")
