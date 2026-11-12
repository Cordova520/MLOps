import os
import sys
import json
import argparse
import click



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

@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--sort", "-s", is_flag=True)
def main(path, sort):
    """
    Main function to read a JSON file and print its formatted content.

    Args:
        path (str): The path to the JSON file.
    """
    if not os.path.isfile(path):
        print(f"Error: The file '{path}' does not exist.")
        sys.exit(1)

    with open(path, 'r') as file:
        content = file.read()
        formatted_content = formatter(content, sort_keys=sort)
        print(formatted_content)

# print(sys.argv)
if __name__ == "__main__":
    main()