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


LLM_FACTORY = {}

def LLMFactory(model_name_or_path):
    model, tokenizer_and_post_load = None, None
    for name in LLM_FACTORY.keys():
        if name in model_name_or_path.lower():
            model, tokenizer_and_post_load = LLM_FACTORY[name]()
    assert model, f"{model_name_or_path} is not registered"
    return model, tokenizer_and_post_load


def register_llm(name):
    def register_llm_cls(cls):
        if name in LLM_FACTORY:
            return LLM_FACTORY[name]
        LLM_FACTORY[name] = cls
        return cls
    return register_llm_cls


# automatically import any Python files in the models/ directory
models_dir = os.path.dirname(__file__)
import_modules(models_dir, "to_upload.model.llm")
