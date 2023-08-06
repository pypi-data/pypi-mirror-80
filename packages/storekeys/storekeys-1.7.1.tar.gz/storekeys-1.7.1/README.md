# storekeys <br>

**Simple package to store values at a single place** 

**Store Keys**<br><br>
Navigate to the folder you want to store the key file you whisth to rename, then type **storekeys** command in command prompt


    usage: storekeys [-h] [--delete] [--noprint] [--showkeys] fileName

    Store important keys and values together in a keys file.

    positional arguments:
    fileName        File Name of the kys file

    optional arguments:
    -h, --help      show this help message and exit
    --delete, -d    Set this flag to delete a key
    --noprint, -np  Set this flag to not print the keys after the operation
    --showkeys, -s  Set this flag to only print the keys

    
**Load Keys**<br>

    from storekeys import LoadKeys

    keys = LoadKeys('fileName').get_keys()

**Try:**
>pip3 install storekeys