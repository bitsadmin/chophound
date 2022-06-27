# ChopHound
Some scripts for dealing with any challenges that might arise when importing (large) JSON datasets into BloodHound. The blog which discusses these scripts can be found at [https://blog.bitsadmin.com/blog/dealing-with-large-bloodhound-datasets](https://blog.bitsadmin.com/blog/dealing-with-large-bloodhound-datasets).

## Scripts
| Name | Description |
| ---- | ----------- |
| chophound.ps1 | PowerShell implementation of ingesting a large BloodHound JSON file and splitting it into smaller chunks. Note that if the file you are trying to split is too large (or your PC's memory is too small), this script will fail with an out of memory exception. |
| chophound.py | Python implementation of the .ps1 script which has support for splitting large JSON files into smaller chunks. |
| replace.py | Little script to replace non-ASCII characters in the file provided with a question mark ('?') in order to avoid possible encoding errors. Note that when running this script against a file with a Byte-Order Mark at the beginning, those bytes will also simply be replaced by question marks and you will need to manually remove those bytes with a hex editor like [HxD](https://mh-nexus.de/en/hxd/) |
