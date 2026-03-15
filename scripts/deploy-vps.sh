#!/bin/bash
# Deploy script for VPS (Ubuntu). Run as root: sudo bash scripts/deploy-vps.sh
# Avoids nested-quote issues by using a heredoc for the angraweb user block.

set -e

# ---- Block 1: run as user angraweb (git pull, migrate, collectstatic) ----
sudo -u angraweb bash -lc 'bash -s' << 'ANGRAWEB_BLOCK'
cd /srv/angraweb || exit 1

git config --global --add safe.directory /srv/angraweb
git merge --abort 2>/dev/null || true
git fetch origin
git reset --hard origin/main
git pull --ff-only || exit 1

if ! grep -q 'hero-section' /srv/angraweb/static/css/style.css 2>/dev/null; then
  echo "ERROR: static/css/style.css on server has no hero-section — git pull did not get latest code."
  exit 1
fi

set -a
source /etc/angraweb/angraweb.env
set +a
source /srv/angraweb/venv/bin/activate

python manage.py migrate --noinput || exit 1

echo "[Deploy] Clearing static cache and re-collecting..."
python manage.py collectstatic --noinput --clear || exit 1

echo $(date +%s) > static_version.txt
echo "[Deploy] static_version.txt updated."
ANGRAWEB_BLOCK

# ---- Block 2: run as root (env update, rsync, restart) ----
ENVFILE=/etc/angraweb/angraweb.env
if [ -f "$ENVFILE" ]; then
  NEW_VER=$(date +%s)
  if grep -q '^STATIC_VERSION=' "$ENVFILE" 2>/dev/null; then
    sudo sed -i "s/^STATIC_VERSION=.*/STATIC_VERSION=$NEW_VER/" "$ENVFILE"
  else
    echo "STATIC_VERSION=$NEW_VER" | sudo tee -a "$ENVFILE" >/dev/null
  fi
fi

PROJECT_ROOT=/srv/angraweb
NGINX_STATIC=/var/www/angraweb/staticfiles
if [ -d "$NGINX_STATIC" ] && [ "$(readlink -f "$PROJECT_ROOT/staticfiles" 2>/dev/null)" != "$(readlink -f "$NGINX_STATIC" 2>/dev/null)" ]; then
  echo "Syncing staticfiles to Nginx path..."
  sudo rsync -a --delete "$PROJECT_ROOT/staticfiles/" "$NGINX_STATIC/"
fi

if [ -d /var/cache/nginx ] 2>/dev/null; then
  echo "Purging Nginx cache..."
  sudo rm -rf /var/cache/nginx/* 2>/dev/null || true
fi

sudo systemctl restart angraweb
sudo systemctl restart nginx

echo ""
echo "=== Deploy done. Health check ==="
curl -sI https://angraweb.com 2>/dev/null | head -n 5
echo ""
echo "To close without losing output, press Enter."
read -p "Press Enter to finish..."
