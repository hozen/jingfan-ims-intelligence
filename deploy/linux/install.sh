#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
cd "$repo_root"

if command -v python3 >/dev/null 2>&1; then
  python3 scripts/build_icp_poc.py
else
  echo "python3 not found; using the prebuilt customer/water-clay-poc snapshot" >&2
fi

docker compose -f deploy/linux/docker-compose.yml up -d --build
echo "Water Clay is running at http://127.0.0.1:8080"
echo "Health check: curl -fsS http://127.0.0.1:8080/healthz"

