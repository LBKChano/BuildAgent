import os
import stat


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        outside_error = (
            f'Error: Cannot list "{directory}" as it is outside '
            "the permitted working directory"
        )

        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            return outside_error

        resolved_root = os.path.realpath(working_dir_abs)
        resolved_target = os.path.realpath(target_dir)
        if os.path.commonpath([resolved_root, resolved_target]) != resolved_root:
            return outside_error

        if not os.path.isdir(resolved_target):
            return f'Error: "{directory}" is not a directory'

        lines = []
        for name in os.listdir(resolved_target):
            item_path = os.path.join(resolved_target, name)
            info = os.stat(item_path, follow_symlinks=False)
            is_dir = stat.S_ISDIR(info.st_mode)
            lines.append(f"- {name}: file_size={info.st_size} bytes, is_dir={is_dir}")

        return "\n".join(lines)
    except (OSError, ValueError, TypeError) as exc:
        return f"Error: {exc}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory, including their sizes and whether they are directories.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory to list, relative to the working directory. Defaults to '.'.",
                },
            },
        },
    },
}
