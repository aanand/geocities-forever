import sys

while True:
    line = sys.stdin.readline()

    if not line:
        break

    line = line.decode('utf-8', 'replace')
    sys.stdout.write(line.encode('ascii', 'xmlcharrefreplace'))