# command_handlers/command_registry.py

import importlib
import os

# Initialize the command registry with "common" commands
command_registry = {}

# Dynamically load all command handlers in the command_handlers directory
command_handlers_dir = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(command_handlers_dir):
    if filename.endswith(".py") and not filename.startswith("_"):
        module_name = filename[:-3]  # Remove the ".py" extension
        module = importlib.import_module(f"command_handlers.{module_name}")
        handler_function = getattr(module, f"run_{module_name}_command", None)
        if handler_function:
            command_registry[module_name] = handler_function

# Ensure "common" commands are always available
if "common" not in command_registry:
    common_module = importlib.import_module("command_handlers.common")
    command_registry["common"] = getattr(common_module, "run_common_command")