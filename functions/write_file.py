import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        root = os.path.abspath(working_directory)
        target = os.path.normpath(os.path.join(root, file_path))
        outside_error = (
            f'Error: Cannot write to "{file_path}" as it is outside '
            "the permitted working directory"
        )

        if os.path.commonpath([root, target]) != root:
            return outside_error

        # Resolve symlinks before creating directories or writing the file.
        resolved_root = os.path.realpath(root)
        resolved_target = os.path.realpath(target)
        if os.path.commonpath([resolved_root, resolved_target]) != resolved_root:
            return outside_error

        if os.path.isdir(resolved_target):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(resolved_target), exist_ok=True)

        with open(resolved_target, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except (OSError, ValueError, TypeError) as exc:
        return f"Error: {exc}"
schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Creates a file or overwrites its contents with the supplied text.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The complete text to write to the file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

