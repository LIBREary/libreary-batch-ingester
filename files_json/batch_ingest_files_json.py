"""
Example script to ingest a bunch of files in a set of directories.

This script assumes it's only one level deep, but it could be easily modified 
    to not make that assumption

Each file has an optional JSON metadata file in the same directory as it which contains
    its metadata. This assumption could also be easily modified
"""
from libreary import Libreary
import json
import os

# Get Libreary object
la = Libreary("../config_dir")

# Go through directories
subdirs = [d for d in os.listdir(".") if os.path.isdir(d)]
for directory in subdirs:
    # Ignore second-level subdirs
    files = [f for f in os.listdir(directory) if not os.path.isdir(f)]
    for file in files:
        # We only want to deal with metadata files
        # If their corresponding data file has come up
        if file.split(".")[1] == "json":
                    continue
        
        # These fields are set in metadata always.
        metadata_schema = ["collection", "directory"]
        metadata = [
                    {"field": "collection", "value": "file_json"},
                    {"field": "directory", "value": directory}
                    ]
        raw_filename = file.split(".")[0]
        
        # JSON Metadata is optional
        try:
            extra_md = json.load(open(f"{directory}/{raw_filename}.json"))
            metadata_schema.extend(extra_md.keys())
            for key in extra_md.keys():
                metadata.append({"field": key, "value": extra_md[key]})

        except FileNotFoundError:
            pass

        """
        By here, metadata object looks like this:
        [
        {'field': 'collection', 'value': 'file_json'},
        {'field': 'directory', 'value': 'directory_1'},
        {'field': 'author', 'value': 'Mike Greenberg'},
        {'field': 'owner', 'value': 'ESPN, a Disney Company'}
        ]
        """

        # Now, we just ingest the file and metadata
        obj_id = la.ingest(file,
                         # Levels 
                         ["low"],
                         "Description",
                         metadata_schema=metadata_schema,
                         metadata=metadata)