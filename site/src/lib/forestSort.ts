// Chronological ordering for Forest entries. A grove's period is
// "<year>-<season>" (e.g. "2026-spring"), which doesn't sort correctly
// next to sapling periods ("2026-05") by string comparison alone — this
// gives every entry a comparable YYYY-MM-ish key so a season's grove lands
// right after that season's last sapling, not after the following season's.
const SEASON_END_MONTH: Record<string, string> = {
  spring: "05",
  summer: "08",
  autumn: "11",
  winter: "02",
};

export function forestSortKey(entry: { data: { type: string; period: string; season: string } }): string {
  const { type, period, season } = entry.data;
  if (type === "sapling") return period;
  const [year] = period.split("-");
  // "z" sorts after any two-digit month, so the grove lands after that
  // season's last sapling but still before the next season's first one.
  return `${year}-${SEASON_END_MONTH[season]}z`;
}

export function sortForestEntries<T extends { data: { type: string; period: string; season: string } }>(
  entries: T[]
): T[] {
  return [...entries].sort((a, b) => forestSortKey(a).localeCompare(forestSortKey(b)));
}
