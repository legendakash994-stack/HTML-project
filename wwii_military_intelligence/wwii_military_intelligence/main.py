from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

production = pd.read_csv(DATA / "military_production.csv")
battles = pd.read_csv(DATA / "selected_battle_casualties.csv")
equipment = pd.read_csv(DATA / "equipment_totals_1942_1944.csv")


def line():
    print("-" * 72)


def show_battle_analysis():
    print("\nSELECTED BATTLE CASUALTIES")
    line()
    df = battles.copy()
    df["known_casualties"] = df[["killed", "wounded"]].sum(axis=1, min_count=1)
    print(df[["battle", "theater", "killed", "wounded", "known_casualties"]]
          .sort_values("known_casualties", ascending=False)
          .to_string(index=False))
    print("\nHighest known casualty count in this selected dataset:")
    row = df.loc[df["known_casualties"].idxmax()]
    print(f"{row['battle']}: {int(row['known_casualties']):,}")
    print("Note: this is a selected dataset of reported US losses, not total losses on both sides.")


def show_production_analysis():
    print("\nTANK/SPG AND COMBAT AIRCRAFT PRODUCTION")
    line()
    pivot = production.pivot_table(
        index="country", columns="equipment",
        values="production_thousands", aggfunc="sum"
    )
    pivot["combined_category_totals"] = pivot.sum(axis=1, min_count=1)
    print(pivot.sort_values("tanks_spg", ascending=False).round(1).to_string())
    print("\nThe figures are in thousands. Missing values are not treated as zero.")
    print("1945 covers January-August in the source.")


def show_equipment_comparison():
    print("\nEQUIPMENT PRODUCTION COMPARISON: 1942-1944")
    line()
    df = equipment.copy()
    df["tanks_spg_units"] = df["tanks_spg_thousands"] * 1000
    df["aircraft_units"] = df["combat_aircraft_thousands"] * 1000
    print(df[["country", "alliance", "tanks_spg_units", "aircraft_units",
              "guns_thousands", "major_naval_vessels_units"]]
          .sort_values("tanks_spg_units", ascending=False)
          .to_string(index=False))
    print("\nAlliance totals (thousands for tanks, aircraft and guns):")
    print(df.groupby("alliance")[[
        "tanks_spg_thousands", "combat_aircraft_thousands", "guns_thousands"
    ]].sum().round(1).to_string())


def show_industry_analysis():
    print("\nWARTIME INDUSTRIAL OUTPUT SNAPSHOT")
    line()
    # Compare separate production categories. Do not add unlike units together.
    for category in ["tanks_spg", "combat_aircraft"]:
        df = production[production["equipment"] == category].copy()
        totals = df.groupby("country")["production_thousands"].sum(min_count=1)
        totals = totals.sort_values(ascending=False)
        print(f"\nTotal recorded {category.replace('_', ' ')} output (thousands):")
        print(totals.round(1).to_string())
        values = totals.dropna().to_numpy(dtype=float)
        print(f"Mean country total: {np.mean(values):,.2f} thousand")
        print(f"Standard deviation: {np.std(values):,.2f} thousand")
        print(f"Highest / lowest ratio: {values.max() / values.min():.2f}x")


def export_summary():
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    battle_copy = battles.copy()
    battle_copy["known_casualties"] = battle_copy[["killed", "wounded"]].sum(
        axis=1, min_count=1
    )
    battle_copy.to_csv(out / "battle_casualty_analysis.csv", index=False)

    production_summary = production.pivot_table(
        index="country", columns="equipment",
        values="production_thousands", aggfunc="sum"
    ).reset_index()
    production_summary.to_csv(out / "production_summary.csv", index=False)
    print(f"\nAnalysis CSV files exported to: {out}")


def menu():
    while True:
        print("\n" + "=" * 72)
        print("             WWII MILITARY DATA INTELLIGENCE")
        print("=" * 72)
        print("1. Analyze selected battle casualties")
        print("2. Compare tank and aircraft production")
        print("3. Compare military equipment output (1942-44)")
        print("4. Analyze industrial output using NumPy")
        print("5. Export analysis results to CSV")
        print("6. Run all analyses")
        print("0. Exit")
        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            show_battle_analysis()
        elif choice == "2":
            show_production_analysis()
        elif choice == "3":
            show_equipment_comparison()
        elif choice == "4":
            show_industry_analysis()
        elif choice == "5":
            export_summary()
        elif choice == "6":
            show_battle_analysis()
            show_production_analysis()
            show_equipment_comparison()
            show_industry_analysis()
            export_summary()
        elif choice == "0":
            print("Exiting project. Goodbye.")
            break
        else:
            print("Invalid choice. Enter a number from 0 to 6.")


if __name__ == "__main__":
    menu()
