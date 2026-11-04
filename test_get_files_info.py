from functions.get_files_info import get_files_info


if __name__ == "__main__":
    for directory, label in [
        (".", "current directory"),
        ("pkg", "'pkg' directory"),
        ("/bin", "'/bin' directory"),
        ("../", "'../' directory"),
    ]:
        print(f"Result for {label}:")
        result = get_files_info("calculator", directory)
        indent = "    " if result.startswith("Error:") else "  "
        for line in result.splitlines():
            print(indent + line)

