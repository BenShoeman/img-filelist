# -*- coding: utf8 -*-

import os
import subprocess
import sys

from direcs_files import *

def main(argv):
    if len(argv) not in [2, 3]:
        print("Usage: python3 {} <images directory> <optional: plain/html>".format(argv[0]))
        sys.exit(1)
    if len(argv) == 3:
        print_type = DirectoryHTMLText if argv[2].lower() == "html" else DirectoryPlainText
    else:
        print_type = DirectoryPlainText
    imgs_dir = argv[1]

    for img_dir in sorted(os.listdir(imgs_dir)):
        # If file doesn't follow the standard, try the "data" folder
        img_file = os.path.join(imgs_dir, img_dir, img_dir + ".img")
        if not os.path.isfile(img_file):
            img_file = os.path.join(imgs_dir, img_dir, "data", img_dir + ".img")
        # Get directory info from fls command
        fls_process = subprocess.Popen(["fls", "-Dpur", img_file], stdout=subprocess.PIPE)
        output, err = fls_process.communicate()

        if err is not None or "Error" in output.decode():
            print("Error reading image", img_dir, end=":\n")
            print(output.decode())
            continue

        floppy_tree = Directory(img_dir, treeprint=print_type)
        if len(output.decode()) > 0:
            # Get the directory information from the fls output
            for line in output.decode().split("\n"):
                # Ignore blank lines and ones with system info directories like $OrphanFiles
                if len(line.strip()) > 0 and "V/V" not in line:
                    dir_name = line.split(':')[1].strip()
                    floppy_tree.add_directory(dir_name)
            
            # Now get file info from fls
            fls_process = subprocess.Popen(["fls", "-Fpur", img_file], stdout=subprocess.PIPE)
            output, err = fls_process.communicate()
            for line in output.decode().split("\n"):
                # Ignore blank lines and ones with system info files like $MBR
                if len(line.strip()) > 0 and "v/v" not in line:
                    file_name = line.split(':')[1].strip()
                    floppy_tree.add_file(file_name)
        else:
            # Treat it as an HFS file system
            
            # Extract files from HFS image in temporary directory
            if not os.path.exists("/tmp/getimgfiles"):
                try:
                    os.makedirs("/tmp/getimgfiles")
                except FileExistsError:
                    subprocess.run(["rm", "-r", "/tmp/getimgfiles"])
                    os.makedirs("/tmp/getimgfiles")
            subprocess.run(["/usr/share/hfsexplorer/bin/unhfs", "-o", "/tmp/getimgfiles", img_file])

            # Get directory info using find
            find_process = subprocess.Popen(["find", "/tmp/getimgfiles", "-type", "d"], stdout=subprocess.PIPE)
            output, err = find_process.communicate()
            for line in output.decode().split("\n"):
                # Remove /tmp/getimgfiles from each line
                line = line.replace("/tmp/getimgfiles", "").strip()
                # Ignore blank lines
                if len(line) > 0:
                    floppy_tree.add_directory(line[1:]) # Ignore first slash
            
            # Then get file info
            find_process = subprocess.Popen(["find", "/tmp/getimgfiles", "-type", "f"], stdout=subprocess.PIPE)
            output, err = find_process.communicate()
            for line in output.decode().split("\n"):
                # Remove /tmp/getimgfiles from each line
                line = line.replace("/tmp/getimgfiles", "").strip()
                # Ignore blank lines
                if len(line) > 0:
                    floppy_tree.add_file(line[1:]) # Ignore first slash
            
            # Now clean up
            subprocess.run(["rm", "-r", "/tmp/getimgfiles"])
        
        # Create text file in that directory with the file list info, plus some
        # text that describes where the data comes from
        txt_file = os.path.join(imgs_dir, img_dir, img_dir + ".txt")
        with open(txt_file, "w") as f:
            # Add description text here when I get it
            f.write(floppy_tree.get_tree_text())

if __name__ == "__main__":
    main(sys.argv)