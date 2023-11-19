import importlib.util
import os

from omegaconf import OmegaConf


def simple_parse_args_string(args_string):
    """
    Parses something like
        args1=val1,arg2=val2
    Into a dictionary
    """
    args_string = args_string.strip()
    if not args_string:
        return {}
    arg_list = args_string.split(",")
    args_dict = OmegaConf.to_object(OmegaConf.from_dotlist(arg_list))
    return args_dict


def import_function_from_path(filepath: str, func_name: str):
    module_name = os.path.basename(filepath).rstrip(".py")

    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    function = getattr(module, func_name, None)
    if function is None:
        raise ImportError(f"Function {func_name} not found in {filepath}")

    return function
