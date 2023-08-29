import subprocess
import shlex
p=subprocess.Popen(['perl','start.pl','1','2'],stdout=subprocess.PIPE)
print(p.stdout.read())