#!/usr/bin/env python3

import hashlib
import json
import sys

digest_freq = {}
fqdns = set()
hashfile = open("hashes.txt", "w")
skipped = 0

for line in sys.stdin:
    fqdn = line.split()[0]
    if fqdn in fqdns:
        # Skip entries we've already seen
        skipped += 1
        continue

    fqdns.add(fqdn)
    m = hashlib.new("sha1", bytes(fqdn, "utf-8"), usedforsecurity=False)
    digest = m.hexdigest()
    hashfile.write("{} {}\n".format(digest, fqdn))

    if not digest[:2] in digest_freq:
        digest_freq[digest[:2]] = 0
    digest_freq[digest[:2]] += 1

hashfile.flush()
hashfile.close()

print("Skipped {} duplicates.".format(skipped))

with open("hash_freq.json", "w") as f:
    json.dump(digest_freq, f, indent=2, sort_keys=True)
    f.flush()
