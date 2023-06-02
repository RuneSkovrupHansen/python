import tempfile
import zipfile
import os


def check_zip_files(zip_path="example.zip"):

    required_files = ["file1.txt", "file2.txt", "file3.txt"]

    with tempfile.TemporaryDirectory() as td:

        with zipfile.ZipFile(zip_path, "r") as zip:

            zip.extractall(td)

            zip_files = [file for file in os.listdir(td) if os.path.isfile(os.path.join(td, file))]

            return all(file in zip_files for file in required_files)


def main():
    zip_ok = check_zip_files()

    if zip_ok:
        print("Zip contains all required files")
    else:
        print("Zip does not contain all required files")


if __name__ == "__main__":
    main()
