# WWII Military Data Intelligence

A beginner-to-intermediate Python data-analysis project using **Pandas and NumPy only**.
Matplotlib is intentionally not used. Results are displayed as terminal tables and exported as CSV files.

## Features
1. Analyze selected World War II battle casualty figures.
2. Compare annual tank/self-propelled gun and combat-aircraft production.
3. Compare equipment output among major powers for 1942-1944.
4. Use NumPy to calculate means, standard deviations, and output ratios.
5. Export analysis results into the `output/` folder.

## Project structure
```text
wwii_military_intelligence/
├── data/
│   ├── equipment_totals_1942_1944.csv
│   ├── military_production.csv
│   └── selected_battle_casualties.csv
├── output/                 # created when you export results
├── main.py
└── requirements.txt
```

## Setup (Windows / VS Code terminal)
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

If `python` does not work in your terminal, try `py main.py`.

## Data notes and limitations
- Production data comes from Mark Harrison, *The Economics of World War II: An Overview*, Table 1-6 and Table 1-7. Values in the annual production file are **thousands of items**, not individual units. The 1945 production figures are partial (through August for the great powers in Table 1-6).
- Selected battle casualties are figures reproduced in a Congressional Research Service report from Michael Clodfelter, *Warfare and Armed Conflicts*, vol. 2 (1991). They are **US losses / US-force figures**, not total casualties for both sides. The Midway entry has killed figures only in that table; missing wounded values remain blank, not zero.
- The equipment comparison dataset uses Harrison's 1942-1944 comparison table. Tanks/SPG, aircraft and guns are in thousands; major naval vessels are individual units.
- Historical casualty and production estimates differ among sources because definitions, time periods, equipment categories and reporting practices differ. Do not treat different datasets as perfectly interchangeable.
- The project uses production volume as a limited proxy for industrial capacity. It does not measure total national industrial output or economic productivity.

## Suggested challenges
- Add a filter that lets the user choose a year.
- Let the user compare two countries.
- Add a function that calculates each country's share of the selected equipment category.
- Add a search option for a battle name.
- Add validation for missing values and duplicate rows.

## Sources
1. Mark Harrison, “The Economics of World War II: An Overview,” Table 1-6 and Table 1-7 (1998):
   https://warwick.ac.uk/fac/soc/economics/staff/mharrison/public/ww2overview1998.pdf
2. Congressional Research Service, *American War and Military Operations Casualties: Lists and Statistics* (battle casualty table cites Michael Clodfelter, 1991):
   https://www.everycrsreport.com/files/20121115_RL32492_f79da945073a75ac56b6e82608bff811a60308f6.html
