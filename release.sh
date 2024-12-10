#!/bin/bash -ex

version=$1
changes=$(git log $(git describe --tags --abbrev=0)..HEAD --no-merges --format="- %s")

echo "__version__ = '${version}'" > cmdqueue/version.py
osc vc -m "Version ${version}\n${changes}" queue.changes
vi queue.changes
git commit cmdqueue/version.py queue.changes -m "Version ${version}"
git tag "v${version}"
read -p "Push now? "
git push
git push --tags
gh release create "v${version}"  --generate-notes

read -p "Update RPM? "
cd ~/devel/obs/utilities/queue
osc up
sed -i -e "s/^\(Version: *\)[^ ]*$/\1${version}/" queue.spec
osc vc -m "Version ${version}\n${changes}"
vi queue.changes
osc rm queue-*.tar.gz
osc service mr download_files
osc add queue-*.tar.gz
osc st
osc diff

read -p "Submit RPM? "
osc ci
#osc sr
