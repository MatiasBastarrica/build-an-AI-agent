import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file_path = os.path.commonpath([working_dir_abs, target_file_path]) == working_dir_abs
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file_path]
        if args != None:
            command.extend(args)
        completed_process = subprocess.run(args=command, capture_output=True, text=True, timeout=30)
        output_str = ""
        if completed_process.returncode != 0:
            output_str += "Process exited with code X"
        if len(completed_process.stdout) == 0 and len(completed_process.stderr) == 0:
            output_str += "No output produced"
        output_str += f"STDOUT:\n{completed_process.stdout}\nSTDERR:\n{completed_process.stderr}"
        return output_str
    except Exception as err:
        return f"Error: executing Python file: {err}"
