#!/usr/bin/env bash
# install-cron.sh — Install the quarterly refresh launchd job.
#
# Usage:
#   bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh         # install
#   bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh status  # check
#   bash ~/.claude/skills/zajno-motion/scripts/install-cron.sh remove  # uninstall

set -euo pipefail

LABEL="com.zajno-motion-refresh"
PLIST_SRC="$HOME/.claude/skills/zajno-motion/scripts/com.zajno-motion-refresh.plist"
PLIST_DST="$HOME/Library/LaunchAgents/$LABEL.plist"

cmd="${1:-install}"

case "$cmd" in
  install)
    # Materialize the plist with the user's actual $HOME path
    mkdir -p "$(dirname "$PLIST_DST")" "$HOME/.cache/zajno-motion"
    sed "s|HOME_PLACEHOLDER|$HOME|g" "$PLIST_SRC" > "$PLIST_DST"

    # Unload first in case an old version is loaded
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true

    # Load
    launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"

    echo "Installed $LABEL"
    echo ""
    echo "Will run quarterly: Jan 1, Apr 1, Jul 1, Oct 1 at 09:13 local."
    echo "Logs:   ~/.cache/zajno-motion/refresh.log"
    echo "Status: bash $0 status"
    echo "Remove: bash $0 remove"
    ;;

  status)
    if launchctl print "gui/$(id -u)/$LABEL" 2>/dev/null | grep -q "$LABEL"; then
      echo "INSTALLED — $LABEL"
      echo ""
      launchctl print "gui/$(id -u)/$LABEL" | grep -E '(state|last exit|next fire|path)' || true
    else
      echo "NOT installed."
    fi
    ;;

  remove)
    launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
    rm -f "$PLIST_DST"
    echo "Removed $LABEL"
    ;;

  run-now)
    # Trigger an immediate run without waiting for the cron
    launchctl kickstart -k "gui/$(id -u)/$LABEL"
    echo "Kicked the job — check ~/.cache/zajno-motion/refresh.log in a few seconds."
    ;;

  *)
    echo "Usage: $0 {install|status|remove|run-now}"
    exit 1
    ;;
esac
