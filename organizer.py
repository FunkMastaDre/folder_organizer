import os
import json
import shutil


def main():
    # get the current directory this file is in, then get the parent
    path = os.getcwd()
    parent = os.path.dirname(path)

    # Create new log file. Overwrite it if it already exists.
    log = "log.txt"
    log_file = open(log, 'w')
    log_file.close()

    # load categories file. Error out if it does not exist.
    if not os.path.exists(f"{path}/categories.json"):
        exit_message(1)
        return 1

    with open("categories.json") as file:
        data = json.load(file)

    # Go through every file in the directory
    with os.scandir(parent) as directory:
        for file in directory:

            # Make sure the entry is actually a file, not a folder
            if not file.is_file():
                log_message = (f"Ignored {file.name} folder")
                print(log_message)
                with open(log, 'a') as file:
                    file.write(str(log_message) + '\n')
                continue

            # Debug: Ignore .gitignore or devcontainer.json for github codespaces.
            if file.name == ".gitignore" or file.name == ".devcontainer.json":
                log_message = (f"Ignored {file.name}")
                print(log_message)
                with open(log, 'a') as file:
                    file.write(str(log_message) + '\n')
                continue

            # Check the file extension and sort it into a category.
            category = get_extension(file, data)

            # Make a destination directory for the category if the directory isn't already available.
            destination = (f"{parent}/{category}")
            if not os.path.exists(destination):
                try:
                    os.mkdir(destination)
                except FileExistsError or FileNotFoundError:
                    exit_message(2)
                    return 2

            # Move file to new directory.
            source = (f"{parent}/{file.name}")
            destination = (f"{destination}/{file.name}")
            shutil.move(source, destination)
            log_message = (f"Moved {file.name} to {category}")
            print(log_message)

            # Write to log file. Error out if it does not exist.
            if not os.path.exists(f"{path}/{log}"):
                exit_message(3)
                return 3

            with open(log, 'a') as file:
                file.write(str(log_message) + '\n')

    exit_message(0)
    return 0

# Gets the file extension of a file. Sorts through the json dictionary and returns the key.


def get_extension(file, data):
    # Go through json file to see the category the file is in.
    # File extension list from https://github.com/dyne/file-extension-list?tab=readme-ov-file
    extension = os.path.splitext(file)[1].lstrip(".")
    for key in data:
        if extension in data[key]:
            return key
    # Return "misc" if not found in json file. This will create a misc category if needed.
    else:
        return "misc"

# Function for any exit messages. Displays once program is over if program has completed, or there are any errors.


def exit_message(code):

    # Success message
    if code == 0:
        print("Success! All possible files have been sorted! :)")
        print("Everything moved has been documented in log.txt.")
        input("Press the Enter key to exit")
        return

    # If categories.json does not exist
    if code == 1:
        print("Error: categories.json file does not exist. If it was deleted, please redownload the program.")
        input("Press the Enter key to exit")
        return

    # If unable to create a new directory
    if code == 2:
        print("Error: Issue creating new directory. Please try again.")
        input("Press the Enter key to exit")
        return

    # If somehow, the log.txt file is deleted while the program is running
    if code == 3:
        print("Error: log.txt does not exist. Was it somehow deleted while the program was running? Please try again to generate a new one.")
        input("Press the Enter key to exit")
        return


main()
