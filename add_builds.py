#
# Copyright (C) 2023, lifehackerhansol
# SPDX-License-Identifier: Apache-2.0
#

#
# Helper script to add file names for check-update script
# argv[1] = file name of release
#

import json
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {sys.argv[0]} <ROM file name>")
        sys.exit(1)

    project, version, date, romtype, device = sys.argv[1].split('-')
    device = device.split('.')[0]

    with open('builds.json', 'r') as f:
        builds = json.load(f)

    builds["builds"][device] = sys.argv[1]

    with open('builds.json', 'w') as f:
        json.dump(builds, f, indent=2)
