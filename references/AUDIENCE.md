# Audience Priority Presets

Pass `--audience <type>` with any mode to prioritize rules for the reader (`leadership`
| `peers` | `xfn`; matching is case-insensitive). Read this file only when an audience
flag is provided. Without one, every applicable rule has equal priority and the changes
table omits the Priority column.

| Audience | P0 Rules |
| :--- | :--- |
| leadership | 1-3: TL;DR, ask, so-what; 5: baselines; 7: recommendation; 25-26: acronyms and jargon |
| peers | 16-19: precision and data; 6: trade-offs |
| xfn | 1-3: TL;DR, ask, so-what; 7: recommendation; 8: toy examples; 25-26: acronyms and jargon |

Rules listed for the audience are **P0**; every other applicable rule is **P1**.
Audience priority changes severity only; no rules are skipped.

`scripts/render_output.py` stamps the Priority cell from the same preset (its
`AUDIENCE_P0` constant); this table and that constant must stay in sync.
