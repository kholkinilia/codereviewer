#! /usr/bin/env bash

zip_url="https://zenodo.org/record/6900648/files/Comment_Generation.zip?download=1"

destination_folder="dataset"

curl -L -o "$destination_folder/Comment_Generation.zip" "$zip_url"

unzip -q "$destination_folder/Comment_Generation.zip" -d "$destination_folder"
