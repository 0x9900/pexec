#!/usr/bin/python
#

from optparse import OptionParser
from multiprocessing import Pool, cpu_count
from subprocess import Popen, PIPE
import select
import sys
import os
import errno

__doc__ = """Execute all the command lines found in jobfile in parallel.
Use '-' as instead of jobfile to read all the commands from stdin."""

DEFAULT_PROCESSES = cpu_count()

class MyPopen(Popen):
  def print_outputs(self):
    read_set = []
    stdout = None # Return
    stderr = None # Return

    if self.stdout:
      read_set.append(self.stdout)
    if self.stderr:
      read_set.append(self.stderr)

    while read_set:
      try:
        rlist, wlist, xlist = select.select(read_set, [], [])
      except select.error, e:
        if e.args[0] == errno.EINTR:
          continue
        raise

      if self.stdout in rlist:
        data = os.read(self.stdout.fileno(), 1024)
        if data == "":
          self.stdout.close()
          read_set.remove(self.stdout)
        else:
          sys.stdout.write(data)
          sys.stdout.flush()

      if self.stderr in rlist:
        data = os.read(self.stderr.fileno(), 1024)
        if data == "":
          self.stderr.close()
          read_set.remove(self.stderr)
        else:
          sys.stderr.write(data)
          sys.stderr.flush()
    self.wait()


def get_work(fd):
  for line in fd:
    line = line.strip()
    if not line or line.startswith('#'):
      continue
    yield line


def _run_process(work):
  cmdline = work
  try:
    p = MyPopen(cmdline, shell=True, stdin=PIPE, stdout=PIPE)
    p.print_outputs()
  except OSError as e:
    print >>sys.stderr, "process execution failed:", e
    return 0
  except KeyboardInterrupt:
    return "KeyboardException"
  return p.returncode


def run_pexec(jobfd, nbprocs):
  stderr = sys.stderr
  pool = Pool(processes=nbprocs)
  work = get_work(jobfd)
  try:
    for retcode in pool.map(_run_process, work):
      if retcode < 0:
        print >>stderr, "process terminated by signal", -retcode
      elif retcode > 0:
        print >>stderr, "process terminated with return code", retcode
    pool.close()
    pool.join()
  except KeyboardInterrupt:
    print "CTRL-C Pressed"
    pool.terminate()


def main():
  parser = OptionParser(usage="%prog [options] jobfile|-",
                        description=__doc__, version='%prog version 0.1')
  parser.add_option("-n", "--nb-procs", dest="nb_procs", type="int",
                    default=DEFAULT_PROCESSES,
                    help=("By default the number of concurent processes to "
                          "run is equal to the number of CPUs "
                          "(Default: %default)")
                    )

  (opts, spillover) = parser.parse_args()

  if len(spillover) != 1:
    parser.error('Invalid arguments.')

  if opts.nb_procs < 2:
    parser.error("There is no point of using that program if you are not "
                 "running anything in parallel.")

  if spillover[0] == '-':
    jobfd = sys.stdin
  else:
    try:
      jobfd = open(spillover[0])
    except IOError:
      parser.error("Job file '%s' open error" % spillover[0])

  run_pexec(jobfd, opts.nb_procs)

if __name__ == "__main__":
  main()
