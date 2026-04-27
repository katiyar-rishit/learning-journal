import subprocess

result = subprocess.run(["ls", "-l", ".."])

output = result.stdout
