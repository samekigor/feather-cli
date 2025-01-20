import os
import sys
import json
from jinja2 import Template, Environment, FileSystemLoader


def get_generated_commands_structs_path() -> str:
    try:
        return sys.argv[1]
    except IndexError:
        raise ValueError("Generated commands structs path is not provided")

def get_command_config_path(env_var_name: str) -> str:
    command_config_path: str = os.getenv(env_var_name)

    if command_config_path is None:
        raise ValueError(f"{env_var_name} is not set")
    
    return command_config_path

from jinja2 import Template

def generate_command_structs(commands_config: dict, template: Template, destiny_path:str) -> None:
    for command_name, command_config in commands_config.items():
        filled_template = template.render(command_config)                 
        dir_file_path = os.path.join(destiny_path, f"{command_name}")
        try:
            os.makedirs(dir_file_path)
        except FileExistsError:
            print(f"Directory {dir_file_path} already exists")
        file_path = os.path.join(dir_file_path, f"{command_config['command_name']}.go")
        with open(file_path, "w") as command_file:
            command_file.write(filled_template)


# def generate_command_structs(commands_config: dict, template: Template, destiny_path:str) -> None:
#     for command_name, command_config in commands_config.items():
#         filled_template = template.render(command_config)                 
#         dir_file_path = os.path.join(destiny_path, f"{command_name}")
#         print(dir_file_path)
#         try:
#             os.makedirs(dir_file_path)
#         except FileExistsError:
#             print(f"Directory {dir_file_path} already exists")
        
#         file_path = os.path.join(dir_file_path, f"{command_name}.go")
#         with open(file_path, "w") as command_file:
#             command_file.write(filled_template)

def main():
    
    template_path = get_command_config_path("FEATHER_COMMANDS_STRUCTURE_TEMPLATE_FILE_PATH")
    command_config_path = get_command_config_path("FEATHER_COMMANDS_CONFIG_FILE_PATH")
    destiny_path = get_generated_commands_structs_path()
    with open(command_config_path, "r") as f:
        commands_config = json.load(f)

    with open(template_path, "r") as file:
        template_content = file.read()
        template = Template(template_content)
       
    
    print(len(commands_config))

    generate_command_structs(commands_config, template, destiny_path)


if __name__ == "__main__":
    main()