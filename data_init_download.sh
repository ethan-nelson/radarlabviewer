#!/bin/bash
# Note: these files are fairly substantial (750 MB - 1.25 GB a piece), so be wary of bandwidth and disk space

# Base data directory
mkdir -p data

# Download data
curl "https://lecuyer.aos.wisc.edu/radarlabviewerdata/MLAT-a-A-2009-04-10-030000-g2.h5" -o "data/MLAT-a-A-2009-04-10-030000-g2.h5"
curl "https://lecuyer.aos.wisc.edu/radarlabviewerdata/quickbeam_w-MLAT-a-A-2009-04-10-030000-g2.h5" -o "data/quickbeam_w-MLAT-a-A-2009-04-10-030000-g2.h5"
curl "https://lecuyer.aos.wisc.edu/radarlabviewerdata/quickbeam_ka-MLAT-a-A-2009-04-10-030000-g2.h5" -o "data/quickbeam_ka-MLAT-a-A-2009-04-10-030000-g2.h5"
curl "https://lecuyer.aos.wisc.edu/radarlabviewerdata/quickbeam_ku-MLAT-a-A-2009-04-10-030000-g2.h5" -o "data/quickbeam_ku-MLAT-a-A-2009-04-10-030000-g2.h5"
curl "https://lecuyer.aos.wisc.edu/radarlabviewerdata/quickbeam_s-MLAT-a-A-2009-04-10-030000-g2.h5" -o "data/quickbeam_s-MLAT-a-A-2009-04-10-030000-g2.h5"
