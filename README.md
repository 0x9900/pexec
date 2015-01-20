
pexec
=====

Execute task in parallel.

Usage:
------

```
Usage: pexec.py [options] [jobfile | -]

Execute all the command lines found in jobfile in parallel. Use '-' as
instead of jobfile to read all the commands from stdin.

Options:
  --version             show program's version number and exit
  -h, --help            show this help message and exit
  -n NB_PROCS, --nb-procs=NB_PROCS
                        Number of concurent processed to run in parallel by
                        default it is equal to the number of CPUs (2)
```

Note:
-----
  By default, the number of process that are run in parallel is equal
  to the number of CPU. Use the option --nb-procs to change that
  number.
