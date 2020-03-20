# Files + JSON metadata configuration

In this scenario, which I believe is relatively frequently occurring, data is stored in a set of folders in a directory. Within each folder is a set of files, each of which optionally has an associated metadata JSON file. 

That looks something like this:

In the directory is:

- directory_1
	- file_1.pdf
	- file_1.json
	- file_2.pdf
	- file_2.json
	- file_3.pdf

- directory_2
	- file_1.pdf
	- file_1.json
	- file_2.pdf
	- file_2.json
	- file_3.pdf

In this case, we're going to use the metadata tag "collection" to refer to the fact that we're using the "files_json" strategy. We're going to use the metadata tag "directory" to remember which subdirectory each file came from.


