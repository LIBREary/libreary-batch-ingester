"""
Example script to ingest a bunch of files in a set of directories.

This script assumes it's only one level deep, but it could be easily modified 
    to not make that assumption

Each file has optional EXIF metadata attached to it.
"""
from libreary import Libreary
import json
import os
import exiftool


# Get Libreary object
la = Libreary("../run_dir/config")

# Go through directories
subdirs = [d for d in os.listdir(".") if os.path.isdir(d)]
for directory in subdirs:
    # Ignore second-level subdirs
    files = [f for f in os.listdir(directory) if not os.path.isdir(f)]
    for file in files:
        # These fields are set in metadata always.
        metadata_schema = ["collection"]
        metadata = [
                    {"field": "collection", "value": "exif"},
                    ]
        raw_filename = file.split(".")[0]
        
        # EXIF Metadata is optional
        try:
            with exiftool.ExifTool() as et:
                extra_md = et.get_metadata_batch(file)[0]
                metadata_schema.extend(extra_md.keys())
                for key in extra_md.keys():
                    metadata.append({"field": key, "value": extra_md[key]})

        except Exception:
            pass

        """
        By here, metadata object looks like this:
        [
        {'field': 'collection', 'value': 'exif'},
        {'field': 'directory', 'value': 'directory_1'},
        {'field': 'author', 'value': 'Mike Greenberg'},
        {'field': 'owner', 'value': 'ESPN, a Disney Company'}
        ]
        
        metadata_schema object is:
        
        ['collection', 'directory', 'author', 'owner']
        """

        # Now, we just ingest the file and metadata
        obj_id = la.ingest(file,
                         # Levels 
                         ["low"],
                         "Description",
                         metadata_schema=metadata_schema,
                         metadata=metadata)
