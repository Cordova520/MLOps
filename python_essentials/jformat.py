import os
import sys
import json
import argparse

def formatter(string, sort_keys=True, indent=4):
    """
    Formats a JSON string for better readability.

    Args:
        string (str): The JSON string to format.
        sort_keys (bool): Whether to sort the keys in the output. Default is True.
        indent (int): The number of spaces to use for indentation. Default is 4.

    Returns:
        str: The formatted JSON string.
    """
    loaded_json = json.loads(string)
    return json.dumps(loaded_json, sort_keys=sort_keys, indent=indent)

def main(path, no_sort):
    """
    Main function to read a JSON file and print its formatted content.

    Args:
        path (str): The path to the JSON file.
    """
    if not os.path.isfile(path):
        print(f"Error: The file '{path}' does not exist.")
        sys.exit(1)
    if no_sort:
        sort_keys = False
    else:
        sort_keys = True

    with open(path, 'r') as file:
        content = file.read()
        formatted_content = formatter(content)
        print(formatted_content)

# print(sys.argv)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format a JSON file for better readability.")
    parser.add_argument("--sort", action="store_true", help="Set the sorting")
    # parser.add_argument("path", type=str, help="The path to the JSON file to format.")
    args = parser.parse_args()
    print(args.sort)
    # main(sys.argv[-1], no_sort=False)