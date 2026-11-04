import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        root = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(root, file_path))
        outside_error = (
            f'Error: Cannot read "{file_path}" as it is outside '
            "the permitted working directory"
        )

        if os.path.commonpath([root, target]) != root:
            return outside_error

        # Resolve symlinks and check that the file is still inside the root.
        resolved_root = os.path.realpath(root)
        resolved_target = os.path.realpath(target)
        if os.path.commonpath([resolved_root, resolved_target]) != resolved_root:
            return outside_error

        if not os.path.isfile(resolved_target):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(resolved_target, encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content
    except (OSError, ValueError, TypeError) as exc:
        return f"Error: {exc}"
schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the contents of a file, up to the configured character limit.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}
