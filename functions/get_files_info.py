import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        dir_contents = os.listdir(target_dir)
        contents_str = ""
        for content_name in dir_contents:
            content_path = "/".join([target_dir, content_name])
            size = os.path.getsize(content_path)
            is_dir = os.path.isdir(content_path)
            contents_str += f"- {content_name}: file_size={size}, is_dir={is_dir}\n"
        return contents_str
    except Exception as err:
        return f"Error: {err}"

