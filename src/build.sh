#!/usr/bin/env bash
set -euo pipefail

echo "Building application..."

if [[ ! -f build/config.txt ]]; then
    echo "Build configuration is missing"
    exit 1
fi

mkdir -p build/output

cat > build/output/application.txt <<'EOF'
CI/CD security demonstration application

This artifact represents the output of a normal build.
EOF

echo "Build completed successfully."
