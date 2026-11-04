from config import MAX_CHARS
from functions.get_file_content import get_file_content


if __name__ == "__main__":
    result = get_file_content("calculator", "lorem.txt")
    marker = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    truncated = result.endswith(marker) and len(result) == MAX_CHARS + len(marker)

    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {truncated}")

    for file_path in (
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",
        "pkg/does_not_exist.py",
    ):
        print(f"\nResult for {file_path}:")
        print(get_file_content("calculator", file_path))
