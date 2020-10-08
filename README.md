# Subscribe & Symlink for Illumina
Listen for messages indicating the arrival of a new illumina run. When a new run arrives, create
symbolic links (aka. 'symlinks') from .fastq.gz files in the run to a specific directory.

## Usage
```
usage: subscribe_and_symlink.py [-h] [--port PORT] [--topic TOPIC]
                                [--experiment_name_regex EXPERIMENT_NAME_REGEX]
                                [--symlink_directory SYMLINK_DIRECTORY]
                                [--public_key PUBLIC_KEY] [--private_key PRIVATE_KEY]

optional arguments:
  -h, --help            show this help message and exit
  --port PORT
  --topic TOPIC
  --experiment_name_regex EXPERIMENT_NAME_REGEX
  --symlink_directory SYMLINK_DIRECTORY
  --public_key PUBLIC_KEY
  --private_key PRIVATE_KEY
```