#!/usr/bin/env bash
set -euo pipefail

# VI (Zenodo extract) and VII (cloth) folders on Desktop
VI_DIR="bcqm_vi_spacetime"
VII_DIR="bcqm_vii_cloth"

OUT_DIR="provenance"
mkdir -p "$OUT_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"
REPORT="$OUT_DIR/vi_vs_vii_hash_report_${STAMP}.txt"

# Core file list (relative to the package root)
FILES=(
  "__init__.py"
  "cli.py"
  "runner.py"
  "engine_vglue.py"
  "event_graph.py"
  "config_schema.py"
  "io.py"
  "selection.py"
  "kernels_v_ancestor.py"
  "metrics_v_ancestor.py"
  "state_v_ancestor.py"
  "analysis/build_fingerprint.py"
  "analysis/selftest_runner.py"
  "pipelines/run_selftest.sh"
)

sha256() {
  local f="$1"
  if command -v shasum >/dev/null 2>&1; then
    shasum -a 256 "$f" | awk '{print $1}'
  else
    openssl dgst -sha256 "$f" | awk '{print $2}'
  fi
}

echo "BCQM VI → VII lineage hash check"            >  "$REPORT"
echo "Timestamp: $STAMP"                          >> "$REPORT"
echo "VI dir : $VI_DIR"                           >> "$REPORT"
echo "VII dir: $VII_DIR"                          >> "$REPORT"
echo ""                                           >> "$REPORT"

if [[ ! -d "$VI_DIR" ]]; then
  echo "ERROR: VI folder not found: $VI_DIR" | tee -a "$REPORT"
  exit 1
fi
if [[ ! -d "$VII_DIR" ]]; then
  echo "ERROR: VII folder not found: $VII_DIR" | tee -a "$REPORT"
  exit 1
fi

match=0; diff=0; miss_vi=0; miss_vii=0

printf "%-8s  %-12s  %-12s  %s\n" "STATUS" "VI_SHA256" "VII_SHA256" "REL_PATH" >> "$REPORT"
printf "%-8s  %-12s  %-12s  %s\n" "------" "--------" "--------" "--------"   >> "$REPORT"

for rel in "${FILES[@]}"; do
  f_vi="$VI_DIR/$rel"
  f_vii="$VII_DIR/$rel"

  if [[ ! -f "$f_vi" ]]; then
    printf "%-8s  %-12s  %-12s  %s\n" "MISS_VI" "-" "-" "$rel" >> "$REPORT"
    ((miss_vi+=1))
    continue
  fi
  if [[ ! -f "$f_vii" ]]; then
    printf "%-8s  %-12s  %-12s  %s\n" "MISS_VII" "-" "-" "$rel" >> "$REPORT"
    ((miss_vii+=1))
    continue
  fi

  h_vi="$(sha256 "$f_vi")"
  h_vii="$(sha256 "$f_vii")"

  if [[ "$h_vi" == "$h_vii" ]]; then
    printf "%-8s  %-12s  %-12s  %s\n" "MATCH" "${h_vi:0:12}" "${h_vii:0:12}" "$rel" >> "$REPORT"
    ((match+=1))
  else
    printf "%-8s  %-12s  %-12s  %s\n" "DIFF"  "${h_vi:0:12}" "${h_vii:0:12}" "$rel" >> "$REPORT"
    ((diff+=1))
  fi
done

echo "" >> "$REPORT"
echo "Summary:" >> "$REPORT"
echo "  MATCH   : $match" >> "$REPORT"
echo "  DIFF    : $diff" >> "$REPORT"
echo "  MISS_VI : $miss_vi" >> "$REPORT"
echo "  MISS_VII: $miss_vii" >> "$REPORT"
echo "" >> "$REPORT"
echo "NOTE: Differences can be expected if you renamed package/import strings, pruned modules, or changed metadata; this report proves identity only for files that MATCH exactly." >> "$REPORT"

echo "Wrote: $REPORT"
