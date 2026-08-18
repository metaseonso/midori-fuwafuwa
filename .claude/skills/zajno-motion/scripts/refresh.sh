#!/usr/bin/env bash
# refresh.sh — Quarterly refresh of Zajno motion data.
#
# What it does:
#   1. Fetches motion.zajno.com
#   2. Extracts current Lottie asset URLs from the HTML
#   3. Diffs against ~/.cache/zajno-motion/manifest.json
#   4. Downloads new/changed files into ~/.cache/zajno-motion/lotties/
#   5. Re-runs the parser → updates empirical-output.json
#   6. Writes a diff summary to ~/.cache/zajno-motion/last-diff.md
#      (Claude reads this on next zajno-motion skill activation and
#       writes a memory entry if non-empty)
#
# Designed to be safe to run any number of times. Idempotent.
# No-ops if nothing has changed.

set -euo pipefail

SKILL_DIR="$HOME/.claude/skills/zajno-motion"
CACHE_DIR="$HOME/.cache/zajno-motion"
LOTTIE_DIR="$CACHE_DIR/lotties"
SOURCE_DIR="$CACHE_DIR/source"
MANIFEST="$CACHE_DIR/manifest.json"
DIFF_FILE="$CACHE_DIR/last-diff.md"
TAKEDOWN_FLAG="$CACHE_DIR/takedown-detected.md"
EMPIRICAL_JSON="$SKILL_DIR/assets/empirical-output.json"
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

mkdir -p "$LOTTIE_DIR" "$SOURCE_DIR"

log() { printf '[refresh %s] %s\n' "$(date '+%H:%M:%S')" "$*" >&2; }

# ─── 1. Fetch HTML (with takedown detection) ───────────────────────────
log "Fetching motion.zajno.com…"
HTTP_STATUS=$(curl -sL -o "$TMP_DIR/index.html" -w "%{http_code}" \
  -A "Mozilla/5.0" https://motion.zajno.com)

if [[ "$HTTP_STATUS" != "200" ]] || [[ ! -s "$TMP_DIR/index.html" ]]; then
  log "TAKEDOWN DETECTED: HTTP $HTTP_STATUS or empty body. Cache left untouched."
  cat > "$TAKEDOWN_FLAG" <<EOF
# motion.zajno.com unreachable — $(date '+%Y-%m-%d %H:%M:%S')

- HTTP status: $HTTP_STATUS
- Body size:   $(wc -c < "$TMP_DIR/index.html" | tr -d ' ') bytes

Cache content (lotties/, source/, manifest.json) preserved from last
successful refresh. The skill remains fully functional with archived data.

Claude: on next zajno-motion activation, record this in memory as
"zajno-motion site unreachable on YYYY-MM-DD" (type: project), then
clear this file.
EOF
  exit 0
fi

# ─── 2. Extract Lottie URLs ────────────────────────────────────────────
grep -oE 'https://cdn\.prod\.website-files\.com/[^"]*\.json' "$TMP_DIR/index.html" \
  | sort -u > "$TMP_DIR/urls_raw.txt"
N_RAW=$(wc -l < "$TMP_DIR/urls_raw.txt" | tr -d ' ')

# Deduplicate: case-insensitive filename collisions on APFS would cause
# sequential overwrites and false "changed" diffs. Keep the URL with the
# highest hex-hash prefix (= the newer Webflow upload) per filename.
while read -r url; do
  fname=$(basename "$url" | sed 's/^[^_]*_//' | tr '[:upper:]' '[:lower:]')
  printf '%s|%s\n' "$fname" "$url"
done < "$TMP_DIR/urls_raw.txt" \
  | sort -t'|' -k1,1 -k2,2r \
  | awk -F'|' '!seen[$1]++ {print $2}' > "$TMP_DIR/urls.txt"

N_REMOTE=$(wc -l < "$TMP_DIR/urls.txt" | tr -d ' ')
log "Remote URLs: $N_RAW raw → $N_REMOTE unique after case-collision dedup"

if [[ "$N_REMOTE" -eq 0 ]]; then
  log "WARNING: zero Lottie URLs found — site structure may have changed. Aborting."
  exit 1
fi

# ─── 2b. Archive page source (HTML + custom JS) for posterity ──────────
log "Archiving page source…"
cp "$TMP_DIR/index.html" "$SOURCE_DIR/index.html"
SCRIPT_URL=$(grep -oE 'https://cdn\.zajno\.com/dev/motion/script[^"]*\.js' \
  "$TMP_DIR/index.html" | head -1 || true)
if [[ -n "$SCRIPT_URL" ]]; then
  SCRIPT_FNAME=$(basename "$SCRIPT_URL")
  curl -sL "$SCRIPT_URL" -o "$SOURCE_DIR/$SCRIPT_FNAME"
  log "Archived $SCRIPT_FNAME ($(wc -c < "$SOURCE_DIR/$SCRIPT_FNAME" | tr -d ' ') bytes)"
fi

# ─── 3. Diff against manifest ──────────────────────────────────────────
NEW_FILES=()
CHANGED_FILES=()
UNCHANGED_FILES=()

while read -r url; do
  fname=$(basename "$url" | sed 's/^[^_]*_//' | tr '[:upper:]' '[:lower:]')
  remote_path="$TMP_DIR/$fname"

  # Download fresh copy to tmp (cheap — files are small)
  curl -sL "$url" -o "$remote_path"
  new_hash=$(shasum -a 256 "$remote_path" | awk '{print $1}')

  # Compare to manifest
  if [[ -f "$MANIFEST" ]]; then
    old_hash=$(python3 -c "import json,sys;m=json.load(open('$MANIFEST'));print(m['files'].get('$fname',{}).get('sha256',''))" 2>/dev/null || echo "")
  else
    old_hash=""
  fi

  if [[ -z "$old_hash" ]]; then
    NEW_FILES+=("$fname")
    mv "$remote_path" "$LOTTIE_DIR/$fname"
  elif [[ "$old_hash" != "$new_hash" ]]; then
    CHANGED_FILES+=("$fname")
    mv "$remote_path" "$LOTTIE_DIR/$fname"
  else
    UNCHANGED_FILES+=("$fname")
  fi
done < "$TMP_DIR/urls.txt"

log "New:       ${#NEW_FILES[@]}"
log "Changed:   ${#CHANGED_FILES[@]}"
log "Unchanged: ${#UNCHANGED_FILES[@]}"

# ─── 4. Update manifest ────────────────────────────────────────────────
python3 << PYEOF
import json, hashlib
from pathlib import Path
from datetime import date

cache    = Path("$CACHE_DIR")
lotties  = Path("$LOTTIE_DIR")
manifest_path = cache / "manifest.json"
manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {
    "schema_version": 1,
    "source": "https://motion.zajno.com",
    "source_cdn": "https://cdn.prod.website-files.com/6384fe1e68c38ac8097a7e47/",
    "files": {},
}
today = str(date.today())
manifest["last_refreshed"] = today + "T" + __import__("datetime").datetime.now().isoformat(timespec="seconds")[11:]

# Update entries for all files currently in cache
for f in sorted(lotties.glob("*.json")):
    data = f.read_bytes()
    h = hashlib.sha256(data).hexdigest()
    entry = manifest["files"].get(f.name, {"first_seen": today})
    if entry.get("sha256") != h:
        entry["last_changed"] = today
    entry["size_bytes"] = len(data)
    entry["sha256"] = h
    manifest["files"][f.name] = entry

manifest_path.write_text(json.dumps(manifest, indent=2))
print(f"Manifest updated: {len(manifest['files'])} files tracked")
PYEOF

# ─── 5. Re-run parser ──────────────────────────────────────────────────
log "Re-running parser…"
# Snapshot old output for diffing
if [[ -f "$EMPIRICAL_JSON" ]]; then
  cp "$EMPIRICAL_JSON" "$TMP_DIR/empirical-old.json"
fi
python3 "$SKILL_DIR/assets/parse_lotties.py" > "$EMPIRICAL_JSON"

# ─── 6. Compute semantic diff, write to last-diff.md ───────────────────
python3 << PYEOF
import json
from pathlib import Path

old = Path("$TMP_DIR/empirical-old.json")
new = Path("$EMPIRICAL_JSON")
diff_path = Path("$DIFF_FILE")

new_data = json.loads(new.read_text())
file_changes = {
    "new":       ${#NEW_FILES[@]},
    "changed":   ${#CHANGED_FILES[@]},
    "removed":   0,
    "unchanged": ${#UNCHANGED_FILES[@]},
}

if not old.exists():
    diff_path.write_text("")  # first run, no diff
    print("First-run baseline, no diff")
    raise SystemExit

old_data = json.loads(old.read_text())

# Quick numeric comparisons
def top_color(d): return d["top_colors"][0]["hex"] if d.get("top_colors") else None
def median_dur(d): return d.get("duration_histogram", {}).get("median_s")
def top_easing(d):
    eas = d.get("top_easings", [])
    return (eas[1] if len(eas) > 1 else eas[0]) if eas else None  # skip auto-bezier default

lines = []
if file_changes["new"] or file_changes["changed"]:
    lines.append(f"# Zajno motion refresh — {__import__('datetime').date.today()}")
    lines.append("")
    lines.append(f"- Files new: {file_changes['new']}, changed: {file_changes['changed']}, unchanged: {file_changes['unchanged']}")

    if top_color(old_data) != top_color(new_data):
        lines.append(f"- **Dominant color changed**: {top_color(old_data)} → {top_color(new_data)}")
    if median_dur(old_data) != median_dur(new_data):
        lines.append(f"- **Median duration changed**: {median_dur(old_data)}s → {median_dur(new_data)}s")
    if top_easing(old_data) != top_easing(new_data):
        lines.append(f"- **Top intentional easing changed**: {top_easing(old_data)} → {top_easing(new_data)}")

    lines.append("")
    lines.append("Claude: after using the zajno-motion skill, write a memory entry summarizing")
    lines.append("this delta, then clear this file (truncate to empty).")

diff_path.write_text("\n".join(lines))
if lines:
    print("Diff written:")
    print("\n".join(lines))
else:
    print("No material changes")
PYEOF

log "Done."
