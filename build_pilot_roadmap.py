from datetime import date
from pathlib import Path

# ============================================================
# 1. Timeline settings
# ============================================================

START = date(2026, 1, 1)
END = date(2035, 1, 1)

BIRTHDAY_MONTH = 8
BIRTHDAY_DAY = 24
BIRTH_YEAR = 2003

ROW_H = 58
LEFT_W = 260

tasks = [
    ("Pre-course prep", "📋", "prep", date(2026, 5, 22), date(2026, 12, 31)),
    ("ATPL theory", "🎓", "ifa", date(2027, 1, 1), date(2027, 12, 31)),
    ("Flight phase", "✈️", "ifa", date(2028, 1, 1), date(2028, 12, 31)),
    ("Licences + MCC", "📜", "ifa", date(2029, 1, 1), date(2029, 4, 30)),
    ("Airline applications", "💼", "transition", date(2029, 4, 1), date(2029, 12, 31)),
    ("Type rating", "🕹️", "entry", date(2029, 10, 1), date(2030, 5, 31)),
    ("Line training", "🛫", "entry", date(2030, 5, 1), date(2030, 12, 31)),
    ("Junior FO", "👨‍✈️", "fo", date(2031, 1, 1), date(2032, 12, 31)),
    ("Experienced FO", "⭐", "fo", date(2033, 1, 1), date(2034, 12, 31)),
]

# Rows:
# 0 = age row
# 1..9 = tasks
# 10 = year row
N_ROWS = 1 + len(tasks) + 1
CHART_H = N_ROWS * ROW_H

def pct(d: date) -> float:
    total = (END - START).days
    val = (d - START).days
    return max(0, min(100, val / total * 100))

def clamp_date(d: date) -> date:
    return max(START, min(END, d))

def band_style(start: date, end: date) -> str:
    start = clamp_date(start)
    end = clamp_date(end)
    left = pct(start)
    width = pct(end) - pct(start)
    return f"left:{left:.4f}%; width:{width:.4f}%;"

# ============================================================
# 2. Generate age bands
# ============================================================

age_bands = []
for age in range(22, 32):
    start = date(BIRTH_YEAR + age, BIRTHDAY_MONTH, BIRTHDAY_DAY)
    end = date(BIRTH_YEAR + age + 1, BIRTHDAY_MONTH, BIRTHDAY_DAY)

    visible_start = max(start, START)
    visible_end = min(end, END)

    if visible_start < visible_end:
        age_bands.append(
            f'<div class="age-band" style="{band_style(visible_start, visible_end)}"><span>{age}</span></div>'
        )

# ============================================================
# 3. Generate year bands
# ============================================================

year_bands = []
year_grid_lines = []

for year in range(2026, 2035):
    ys = date(year, 1, 1)
    ye = date(year + 1, 1, 1)
    year_bands.append(
        f'<div class="year-band" style="{band_style(ys, ye)}"><span>{year}</span></div>'
    )
    year_grid_lines.append(
        f'<div class="year-grid-line" style="left:{pct(ys):.4f}%;"></div>'
    )

# right boundary at 2035
year_grid_lines.append(
    f'<div class="year-grid-line" style="left:{pct(date(2035, 1, 1)):.4f}%;"></div>'
)

# ============================================================
# 4. Generate rows and bars
# ============================================================

label_rows = []
plot_rows = []

# Age label
label_rows.append('<div class="age-row-label"><span class="icon prep">🎂</span>Age</div>')

# Age row
plot_rows.append(f'<div class="plot-row age-bg" style="top:{0 * ROW_H}px;"></div>')

# Task labels and plot rows
for i, (name, icon, cls, start, end) in enumerate(tasks, start=1):
    label_rows.append(f'<div class="row-label"><span class="icon {cls}">{icon}</span>{name}</div>')
    plot_rows.append(f'<div class="plot-row" style="top:{i * ROW_H}px;"></div>')

# Year row
year_row_index = N_ROWS - 1
label_rows.append('<div class="year-row-label"><span class="icon prep">📅</span>Year</div>')
plot_rows.append(f'<div class="plot-row year-bg" style="top:{year_row_index * ROW_H}px;"></div>')

bars = []
for i, (name, icon, cls, start, end) in enumerate(tasks, start=1):
    top = i * ROW_H + 12
    bars.append(
        f'<div class="bar {cls}" style="top:{top}px; {band_style(start, end)}"></div>'
    )

# ============================================================
# 5. Career milestone callouts
# ============================================================

def row_center(row_index: int) -> int:
    return row_index * ROW_H + ROW_H // 2

# Milestone area starts below chart. Use negative top offsets to point back into chart.
milestones = [
    {
        "title": "Start IFA",
        "date_label": "Jan 2027",
        "icon": "🚀",
        "date": date(2027, 1, 1),
        "row": 2,  # ATPL theory
        "card_top": 26,
        "card_shift": 0,
    },
    {
        "title": "Course<br/>completion",
        "date_label": "Spring 2029",
        "icon": "📜",
        "date": date(2029, 4, 30),
        "row": 4,  # Licences + MCC
        "card_top": 26,
        "card_shift": 1.5,
    },
    {
        "title": "Airline entry",
        "date_label": "Around 2030",
        "icon": "👨‍✈️",
        "date": date(2030, 6, 1),
        "row": 7,  # Line training
        "card_top": 104,
        "card_shift": 1.2,
    },
]

milestone_html = []
for m in milestones:
    x = pct(m["date"])
    target_y = row_center(m["row"])
    top = target_y - CHART_H
    line_top = top + 4
    card_x = x + m["card_shift"]

    # Dot points to the exact target row/bar inside the chart.
    # Connector line only appears below the chart, so it does not pollute the vertical year grid.
    connector_height = max(0, m["card_top"] - 2)

    milestone_html.append(f'''
    <div class="callout-dot" style="left:{x:.4f}%; top:{top}px;"></div>
    <div class="callout-line" style="left:{x:.4f}%; top:0px; height:{connector_height}px;"></div>
    <div class="milestone-card" style="left:{card_x:.4f}%; top:{m["card_top"]}px;">
      <div class="m-icon">{m["icon"]}</div>
      <div>
        <div class="m-title">{m["title"]}</div>
        <div class="m-date">{m["date_label"]}</div>
      </div>
    </div>
''')

# ============================================================
# 6. HTML
# ============================================================

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Pilot Career Roadmap</title>

<style>
  :root {{
    color-scheme: light;

    --navy: #0b1f44;
    --text: #102033;
    --muted: #64748b;
    --grid: #e5eaf2;
    --border: #d8dee8;
    --page-bg: #ffffff;
    --card-bg: rgba(255, 255, 255, 0.95);
    --plot-bg: #ffffff;
    --label-bg: rgba(248, 250, 252, 0.72);
    --age-row-bg: rgba(219, 234, 254, 0.70);
    --year-row-bg: rgba(226, 232, 240, 0.82);
    --note-bg-top: #ffffff;
    --note-bg-bottom: #f8fafc;
    --shadow: rgba(15, 23, 42, 0.07);

    --prep: #718096;
    --ifa: #2563eb;
    --transition: #f59e0b;
    --entry: #16a34a;
    --fo: #7c3aed;

    --page-width: clamp(1080px, 90vw, 1740px);
    --left-col: clamp(220px, 15vw, 275px);
  }}

  body.dark {{
    color-scheme: dark;

    --navy: #e5efff;
    --text: #e5e7eb;
    --muted: #aab6c8;
    --grid: rgba(148, 163, 184, 0.20);
    --border: rgba(148, 163, 184, 0.28);
    --page-bg: #08111f;
    --card-bg: rgba(15, 23, 42, 0.94);
    --plot-bg: #0b1220;
    --label-bg: rgba(15, 23, 42, 0.86);
    --age-row-bg: rgba(30, 64, 175, 0.22);
    --year-row-bg: rgba(51, 65, 85, 0.42);
    --note-bg-top: #111827;
    --note-bg-bottom: #0b1220;
    --shadow: rgba(0, 0, 0, 0.30);

    --prep: #94a3b8;
    --ifa: #3b82f6;
    --transition: #f59e0b;
    --entry: #22c55e;
    --fo: #8b5cf6;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    margin: 0;
    background: #ffffff;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    color: var(--text);
    overflow-x: auto;
  }}

  .page {{
    width: var(--page-width);
    margin: 0 auto;
    padding: clamp(20px, 2vw, 30px) clamp(18px, 2vw, 32px) clamp(28px, 3vw, 42px);
    background:
      radial-gradient(circle at top, rgba(37, 99, 235, 0.05), transparent 34%),
      #ffffff;
  }}

  .title-row {{
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 28px;
    margin-bottom: 2px;
  }}

  .wing {{
    width: 82px;
    height: 28px;
    position: relative;
  }}

  .wing::before,
  .wing::after {{
    content: "";
    position: absolute;
    right: 0;
    height: 6px;
    background: var(--navy);
    border-radius: 999px;
  }}

  .wing.left::before,
  .wing.right::before {{
    width: 82px;
    top: 0;
  }}

  .wing.left::after,
  .wing.right::after {{
    width: 58px;
    top: 11px;
  }}

  .wing.left span,
  .wing.right span {{
    position: absolute;
    right: 0;
    top: 22px;
    width: 34px;
    height: 6px;
    background: var(--navy);
    border-radius: 999px;
  }}

  .wing.right {{
    transform: scaleX(-1);
  }}

  h1 {{
    margin: 0;
    font-size: clamp(29px, 2.45vw, 44px);
    line-height: 1.05;
    color: var(--navy);
    letter-spacing: -0.8px;
    font-weight: 800;
  }}

  .subtitle {{
    text-align: center;
    font-size: clamp(15px, 1.2vw, 21px);
    color: var(--muted);
    margin-bottom: 22px;
  }}

  .legend {{
    display: flex;
    justify-content: center;
    gap: clamp(18px, 2.4vw, 46px);
    align-items: center;
    margin-bottom: 24px;
    font-size: 17px;
  }}

  .legend-item {{
    display: flex;
    align-items: center;
    gap: 12px;
  }}

  .swatch {{
    width: 22px;
    height: 22px;
    border-radius: 6px;
    box-shadow: 0 6px 14px rgba(15, 23, 42, 0.15);
  }}

  .marker-legend {{
    display: flex;
    justify-content: center;
    gap: 28px;
    align-items: center;
    margin-top: -12px;
    margin-bottom: 18px;
    font-size: 13px;
    font-weight: 700;
    color: var(--muted);
  }}

  .marker-legend-item {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .marker-swatch {{
    width: 18px;
    height: 3px;
    border-radius: 999px;
    display: inline-block;
  }}

  .marker-swatch.red {{
    background: rgba(220, 38, 38, 0.78);
  }}

  .marker-swatch.gold {{
    background: rgba(245, 158, 11, 0.86);
  }}

  .theme-toggle {{
    position: fixed;
    top: 18px;
    right: 22px;
    z-index: 100;
    width: 84px;
    height: 40px;
    border: 1px solid var(--border);
    background: var(--card-bg);
    color: var(--text);
    border-radius: 999px;
    padding: 0;
    display: grid;
    grid-template-columns: 1fr 1fr;
    align-items: center;
    cursor: pointer;
    box-shadow: 0 10px 24px var(--shadow);
    backdrop-filter: blur(10px);
    overflow: hidden;
  }}

  .theme-toggle:hover {{
    transform: translateY(-1px);
  }}

  .theme-option {{
    position: relative;
    z-index: 2;
    display: grid;
    place-items: center;
    height: 100%;
    font-size: 16px;
    transition:
      opacity 160ms ease,
      transform 160ms ease;
  }}

  .theme-knob {{
    position: absolute;
    z-index: 1;
    top: 4px;
    left: 4px;
    width: 36px;
    height: 30px;
    border-radius: 999px;
    background: #ffffff;
    box-shadow:
      0 6px 14px rgba(15, 23, 42, 0.22),
      inset 0 1px 0 rgba(255, 255, 255, 0.85);
    transition:
      transform 180ms ease,
      background 180ms ease;
  }}

  body.dark .theme-knob {{
    transform: translateX(40px);
    background: #1e293b;
    box-shadow:
      0 6px 14px rgba(0, 0, 0, 0.38),
      inset 0 1px 0 rgba(255, 255, 255, 0.08);
  }}

  body.dark .light-option {{
    opacity: 0.42;
    transform: scale(0.92);
  }}

  body:not(.dark) .dark-option {{
    opacity: 0.42;
    transform: scale(0.92);
  }}


  .chart-card {{
    border: 1px solid var(--border);
    border-radius: 16px;
    overflow: hidden;
    background: var(--card-bg);
    box-shadow:
      0 16px 38px var(--shadow),
      inset 0 1px 0 rgba(255,255,255,0.9);
  }}

  .chart {{
    position: relative;
    height: {CHART_H}px;
    display: grid;
    grid-template-columns: {LEFT_W}px 1fr;
  }}

  .labels {{
    border-right: 1px solid var(--border);
    background: var(--label-bg);
  }}

  .row-label,
  .age-row-label,
  .year-row-label {{
    height: {ROW_H}px;
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 0 18px;
    border-bottom: 1px solid var(--grid);
    font-size: clamp(13.5px, 0.95vw, 15.5px);
    font-weight: 650;
    white-space: nowrap;
  }}

  .age-row-label {{
    font-weight: 800;
    color: var(--navy);
    background: var(--age-row-bg);
  }}

  .year-row-label {{
    font-weight: 800;
    color: var(--navy);
    background: var(--year-row-bg);
  }}

  .icon {{
    width: 39px;
    height: 39px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    color: white;
    font-size: 21px;
    box-shadow: 0 8px 16px rgba(15, 23, 42, 0.16);
    flex: 0 0 auto;
  }}

  .plot {{
    position: relative;
    background: #ffffff;
  }}

  .plot-row {{
    position: absolute;
    left: 0;
    right: 0;
    height: {ROW_H}px;
    border-bottom: 1px solid var(--grid);
  }}

  .year-grid-line {{
    position: absolute;
    top: {ROW_H}px;
    bottom: {ROW_H}px;
    width: 0;
    border-left: 1px solid rgba(100, 116, 139, 0.24);
    z-index: 2;
    pointer-events: none;
  }}

  .plot-row:nth-child(odd) {{
    background: rgba(248, 250, 252, 0.50);
  }}

  .age-bg {{
    background: linear-gradient(90deg, rgba(219, 234, 254, 0.72), rgba(239, 246, 255, 0.82)) !important;
  }}

  .year-bg {{
    background: linear-gradient(90deg, rgba(226, 232, 240, 0.82), rgba(248, 250, 252, 0.88)) !important;
  }}

  .age-band,
  .year-band {{
    position: absolute;
    top: 0;
    height: {ROW_H}px;
    display: grid;
    place-items: center;
    border-right: 1px solid rgba(148, 163, 184, 0.42);
    font-size: 14px;
    font-weight: 850;
    color: var(--navy);
    letter-spacing: 0.2px;
    z-index: 3;
  }}

  .year-band {{
    top: {(N_ROWS - 1) * ROW_H}px;
  }}

  .age-band:nth-child(odd) {{
    background: rgba(219, 234, 254, 0.58);
  }}

  .age-band:nth-child(even) {{
    background: rgba(191, 219, 254, 0.34);
  }}

  .year-band:nth-child(odd) {{
    background: rgba(241, 245, 249, 0.90);
  }}

  .year-band:nth-child(even) {{
    background: rgba(226, 232, 240, 0.62);
  }}

  .age-band span,
  .year-band span {{
    display: inline-grid;
    place-items: center;
    min-width: 38px;
    height: 26px;
    padding: 0 10px;
    border-radius: 999px;
    color: white;
    box-shadow: 0 7px 16px rgba(15, 23, 42, 0.12);
  }}

  .age-band span {{
    background: rgba(30, 64, 175, 0.92);
  }}

  .year-band span {{
    min-width: 62px;
    background: rgba(51, 65, 85, 0.92);
  }}

  .income-marker {{
    position: absolute;
    top: 0;
    bottom: 0;
    width: 22px;
    transform: translateX(-50%);
    z-index: 19;
    pointer-events: none;
  }}

  .income-marker::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 15px;
    height: 11px;
    transform: translateX(-50%);
    background: rgba(245, 158, 11, 0.88);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
  }}

  .income-marker::after {{
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 2px;
    transform: translateX(-50%);
    background: rgba(245, 158, 11, 0.78);
  }}

  .today-marker {{
    position: absolute;
    top: 0;
    bottom: 0;
    width: 20px;
    transform: translateX(-50%);
    z-index: 20;
    pointer-events: none;
  }}

  .today-marker::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 13px;
    height: 9px;
    transform: translateX(-50%);
    background: rgba(220, 38, 38, 0.76);
    clip-path: polygon(0 0, 100% 0, 50% 100%);
  }}

  .today-marker::after {{
    content: "";
    position: absolute;
    top: 0;
    bottom: 0;
    left: 50%;
    width: 1.5px;
    transform: translateX(-50%);
    background: rgba(220, 38, 38, 0.68);
  }}

  .bar {{
    position: absolute;
    z-index: 4;
    height: 34px;
    border-radius: 9px;
    box-shadow:
      0 10px 18px rgba(15, 23, 42, 0.16),
      inset 0 1px 0 rgba(255,255,255,0.32);
  }}

  .bar::after {{
    content: "";
    position: absolute;
    inset: 0;
    border-radius: 9px;
    background: linear-gradient(180deg, rgba(255,255,255,0.22), rgba(255,255,255,0));
    pointer-events: none;
  }}

  .milestones {{
    position: relative;
    height: 160px;
    margin-left: {LEFT_W}px;
  }}

  .callout-line {{
    position: absolute;
    width: 1.5px;
    border-left: 1.5px dashed rgba(15, 31, 68, 0.26);
    z-index: 5;
  }}

  .callout-dot {{
    position: absolute;
    width: 10px;
    height: 10px;
    transform: translate(-4.25px, -4.25px);
    border-radius: 999px;
    background: var(--navy);
    box-shadow: 0 0 0 4px rgba(11, 31, 68, 0.08);
    z-index: 6;
  }}

  .milestone-card {{
    position: absolute;
    transform: translateX(-50%);
    min-width: 132px;
    padding: 13px 14px;
    border-radius: 12px;
    background: #ffffff;
    border: 1px solid var(--border);
    box-shadow: 0 12px 25px rgba(15, 23, 42, 0.11);
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .milestone-card .m-icon {{
    font-size: 25px;
    color: var(--navy);
  }}

  .milestone-card .m-title {{
    font-size: 13px;
    font-weight: 800;
    color: var(--navy);
    line-height: 1.15;
  }}

  .milestone-card .m-date {{
    font-size: 11px;
    color: var(--muted);
    margin-top: 3px;
    white-space: nowrap;
  }}

  .note {{
    margin: 20px auto 0;
    width: min(1220px, calc(100% - 120px));
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 26px;
    display: flex;
    align-items: center;
    gap: 18px;
    background: linear-gradient(180deg, var(--note-bg-top), var(--note-bg-bottom));
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
    font-size: 15px;
    color: var(--muted);
    line-height: 1.45;
  }}

  .note-icon {{
    width: 38px;
    height: 38px;
    border-radius: 999px;
    background: #2563eb;
    color: white;
    display: grid;
    place-items: center;
    font-size: 23px;
    font-weight: 800;
    flex: 0 0 auto;
  }}

  .small {{
    font-weight: 700;
    color: var(--navy);
  }}

  .prep {{ background: var(--prep); }}
  .ifa {{ background: var(--ifa); }}
  .transition {{ background: var(--transition); }}
  .entry {{ background: var(--entry); }}
  .fo {{ background: var(--fo); }}


  /* ============================================================
     Dark mode overrides
     ============================================================ */

  body.dark {{
    background: #07111f;
    color: #e5e7eb;
  }}

  body.dark .page {{
    background:
      radial-gradient(circle at top, rgba(59, 130, 246, 0.13), transparent 34%),
      #07111f;
  }}

  body.dark h1 {{
    color: #eaf2ff;
  }}

  body.dark .subtitle {{
    color: #b8c4d8;
  }}

  body.dark .wing::before,
  body.dark .wing::after,
  body.dark .wing span {{
    background: #dbeafe;
  }}

  body.dark .legend,
  body.dark .legend-item,
  body.dark .marker-legend,
  body.dark .marker-legend-item {{
    color: #dbeafe;
  }}

  body.dark .chart-card {{
    background: #0b1220;
    border-color: rgba(148, 163, 184, 0.32);
    box-shadow:
      0 18px 44px rgba(0, 0, 0, 0.36),
      inset 0 1px 0 rgba(255,255,255,0.04);
  }}

  body.dark .labels {{
    background: #101827;
    border-right-color: rgba(148, 163, 184, 0.28);
  }}

  body.dark .plot {{
    background: #0b1220;
  }}

  body.dark .row-label {{
    color: #e5e7eb;
    border-bottom-color: rgba(148, 163, 184, 0.20);
  }}

  body.dark .age-row-label,
  body.dark .year-row-label {{
    color: #eaf2ff;
    background: #172033;
    border-bottom-color: rgba(148, 163, 184, 0.24);
  }}

  body.dark .plot-row {{
    border-bottom-color: rgba(148, 163, 184, 0.18);
  }}

  body.dark .plot-row:nth-child(odd) {{
    background: rgba(15, 23, 42, 0.40);
  }}

  body.dark .age-bg {{
    background: linear-gradient(90deg, rgba(30, 64, 175, 0.24), rgba(30, 58, 138, 0.16)) !important;
  }}

  body.dark .year-bg {{
    background: linear-gradient(90deg, rgba(51, 65, 85, 0.58), rgba(30, 41, 59, 0.58)) !important;
  }}

  body.dark .age-band:nth-child(odd) {{
    background: rgba(30, 64, 175, 0.24);
  }}

  body.dark .age-band:nth-child(even) {{
    background: rgba(37, 99, 235, 0.16);
  }}

  body.dark .year-band:nth-child(odd) {{
    background: rgba(51, 65, 85, 0.54);
  }}

  body.dark .year-band:nth-child(even) {{
    background: rgba(30, 41, 59, 0.62);
  }}

  body.dark .age-band,
  body.dark .year-band {{
    border-right-color: rgba(148, 163, 184, 0.26);
  }}

  body.dark .age-band span {{
    background: #3b82f6;
    color: #ffffff;
  }}

  body.dark .year-band span {{
    background: #475569;
    color: #ffffff;
  }}

  body.dark .year-grid-line {{
    border-left-color: rgba(148, 163, 184, 0.22);
  }}

  body.dark .milestone-card {{
    background: #111827;
    border-color: rgba(148, 163, 184, 0.28);
    box-shadow: 0 12px 25px rgba(0, 0, 0, 0.32);
  }}

  body.dark .milestone-card .m-title {{
    color: #eaf2ff;
  }}

  body.dark .milestone-card .m-date {{
    color: #aab6c8;
  }}

  body.dark .milestone-card .m-icon {{
    color: #eaf2ff;
  }}

  body.dark .callout-line {{
    border-left-color: rgba(203, 213, 225, 0.28);
  }}

  body.dark .callout-dot {{
    background: #dbeafe;
    box-shadow: 0 0 0 4px rgba(219, 234, 254, 0.08);
  }}

  body.dark .note {{
    background: linear-gradient(180deg, #111827, #0b1220);
    border-color: rgba(148, 163, 184, 0.28);
    color: #cbd5e1;
    box-shadow: 0 14px 32px rgba(0, 0, 0, 0.28);
  }}

  body.dark .note .small {{
    color: #eaf2ff;
  }}

  body.dark .theme-toggle {{
    background: #111827;
    color: #eaf2ff;
    border-color: rgba(148, 163, 184, 0.32);
  }}

</style>
</head>

<body>
<button id="theme-toggle" class="theme-toggle" type="button" aria-label="Toggle theme">
  <span class="theme-option light-option">☀️</span>
  <span class="theme-option dark-option">🌙</span>
  <span class="theme-knob"></span>
</button>

<div class="page">
  <div class="title-row">
    <div class="wing left"><span></span></div>
    <h1>Pilot Career Roadmap</h1>
    <div class="wing right"><span></span></div>
  </div>

  <div class="subtitle">IFA start: January 2027 | Base-case path to experienced First Officer by end-2034</div>

  <div class="legend">
    <div class="legend-item"><span class="swatch prep"></span>Preparation</div>
    <div class="legend-item"><span class="swatch ifa"></span>IFA Training</div>
    <div class="legend-item"><span class="swatch transition"></span>Transition</div>
    <div class="legend-item"><span class="swatch entry"></span>Airline Entry</div>
    <div class="legend-item"><span class="swatch fo"></span>FO Development</div>
  </div>

  <div class="marker-legend">
    <div class="marker-legend-item"><span class="marker-swatch red"></span>Today</div>
    <div class="marker-legend-item"><span class="marker-swatch gold"></span>Expected first paid airline phase</div>
  </div>

  <div class="chart-card">
    <div class="chart">
      <div class="labels">
        {chr(10).join(label_rows)}
      </div>

      <div class="plot">
        <!-- Only vertical grid lines: calendar year boundaries -->
        {chr(10).join(year_grid_lines)}

        {chr(10).join(plot_rows)}

        <!-- Age bands, calculated from 24 August birthdays -->
        {chr(10).join(age_bands)}

        <!-- Task bars -->
        {chr(10).join(bars)}

        <!-- Year bands, calculated from calendar years -->
        {chr(10).join(year_bands)}

        <!-- Dynamic today marker -->
        <div id="today-marker" class="today-marker"></div>

        <!-- First paid airline phase marker -->
        <div id="income-marker" class="income-marker"></div>
      </div>
    </div>
  </div>

  <div class="milestones">
    {chr(10).join(milestone_html)}
  </div>

  <div class="note">
    <div class="note-icon">i</div>
    <div>
      <span class="small">Base-case assumption:</span>
      IFA training completed around 2029, followed by airline selection, type rating, line training and First Officer consolidation.
      Buffers account for weather, exams, aircraft availability, licence paperwork and hiring-market timing.
    </div>
  </div>
</div>

<script>
  (function () {{
    const body = document.body;
    const toggle = document.getElementById("theme-toggle");
    const icon = document.getElementById("theme-toggle-icon");
    const text = document.getElementById("theme-toggle-text");

    function applyTheme(theme) {{
      const isDark = theme === "dark";
      body.classList.toggle("dark", isDark);
        if (icon) icon.textContent = isDark ? "☀️" : "🌙";
      localStorage.setItem("pilot-roadmap-theme", theme);
    }}

    const savedTheme = localStorage.getItem("pilot-roadmap-theme");
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

    if (toggle) {{
      toggle.addEventListener("click", function () {{
        applyTheme(body.classList.contains("dark") ? "light" : "dark");
      }});
    }}

    const start = new Date("2026-01-01T00:00:00");
    const end = new Date("2035-01-01T00:00:00");
    const totalMs = end.getTime() - start.getTime();

    const marker = document.getElementById("today-marker");
    if (marker) {{
      const now = new Date();

      if (now < start || now > end) {{
        marker.style.display = "none";
      }} else {{
        const elapsedMs = now.getTime() - start.getTime();
        const position = Math.max(0, Math.min(100, (elapsedMs / totalMs) * 100));
        marker.style.left = position.toFixed(4) + "%";
      }}
    }}

    const incomeMarker = document.getElementById("income-marker");
    if (incomeMarker) {{
      const incomeDate = new Date("2030-06-01T00:00:00");
      const incomeElapsedMs = incomeDate.getTime() - start.getTime();
      const incomePosition = Math.max(0, Math.min(100, (incomeElapsedMs / totalMs) * 100));
      incomeMarker.style.left = incomePosition.toFixed(4) + "%";
    }}
  }})();
</script>
</body>
</html>
'''

Path("pilot_roadmap.html").write_text(html)
print("Created pilot_roadmap.html")
