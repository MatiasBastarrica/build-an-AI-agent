import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read file contents in a specified file path relative to the working directory, if the file is larger than a certain limit (MAX_CHARS) then only a certain amount of characters are read (MAX_CHARS)",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "desctiption": "File path to read file contents from, relative to the working directory (default is the working directory itself)"
                }
            },
            "required": ["file_path"]
        }
    } 
}

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        with open(target_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS) 
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string
    except Exception as err:
        return f"Error: {err}"

