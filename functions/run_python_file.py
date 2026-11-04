import os
import subprocess
import sys


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        root = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(root, file_path))
        outside_error = (
            f'Error: Cannot execute "{file_path}" as it is outside '
            "the permitted working directory"
        )

        if os.path.commonpath([root, target]) != root:
            return outside_error

        resolved_root = os.path.realpath(root)
        resolved_target = os.path.realpath(target)
        if os.path.commonpath([resolved_root, resolved_target]) != resolved_root:
            return outside_error

        if not os.path.isfile(resolved_target):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = [sys.executable, resolved_target]
        if args is not None:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=resolved_root,
            capture_output=True,
            text=True,
            timeout=30,
        )

        output = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        if not result.stdout and not result.stderr:
            output.append("No output produced")
        else:
            if result.stdout:
                output.append(f"STDOUT:\n{result.stdout.rstrip(chr(10))}")
            if result.stderr:
                output.append(f"STDERR:\n{result.stderr.rstrip(chr(10))}")

        return "\n".join(output)
    except Exception as exc:
        return f"Error: executing Python file: {exc}"
schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python file with optional command-line arguments and returns its output.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to a .py file, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional command-line arguments, one string per argument.",
                },
            },
            "required": ["file_path"],
        },
    },
}
