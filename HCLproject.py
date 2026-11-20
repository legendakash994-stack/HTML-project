from pathlib import Path
import numpy as np
import pandas as pd

# Getting the project directory
ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

# Loading datasets
production = pd.read_csv(DATA / "military_production.csv")
battles = pd.read_csv(DATA / "selected_battle_casualties.csv")
equipment = pd.read_csv(DATA / "equipment_totals_1942_1944.csv")


# Function to create separators
def line():
    print("-" * 72)


# 1. BATTLE CASUALTY ANALYSIS
def show_battle_analysis():

    print("\nSELECTED BATTLE CASUALTIES")
    line()

    df = battles.copy()

    # Calculate known casualties
    df["known_casualties"] = df[
        ["killed", "wounded"]
    ].sum(axis=1, min_count=1)

    print(
        df[
            ["battle", "theater", "killed",
             "wounded", "known_casualties"]
        ]
        .sort_values(
            "known_casualties",
            ascending=False
        )
        .to_string(index=False)
    )

    # Find battle with highest recorded casualties
    row = df.loc[df["known_casualties"].idxmax()]

    print("\nHighest recorded casualties:")
    print(
        f"{row['battle']}: "
        f"{int(row['known_casualties']):,}"
    )

    print("\nNote: Figures represent selected US losses,")
    print("not total casualties on both sides.")


# 2. TANK AND AIRCRAFT PRODUCTION
def show_production_analysis():

    print("\nTANK AND AIRCRAFT PRODUCTION")
    line()

    pivot = production.pivot_table(
        index="country",
        columns="equipment",
        values="production_thousands",
        aggfunc="sum"
    )

    pivot["combined_category_totals"] = pivot.sum(
        axis=1,
        min_count=1
    )

    print(
        pivot.sort_values(
            "tanks_spg",
            ascending=False
        ).round(1).to_string()
    )

    print("\nProduction figures are in thousands.")
    print("1945 figures cover January to August.")


# 3. MILITARY EQUIPMENT COMPARISON
def show_equipment_comparison():

    print("\nMILITARY EQUIPMENT COMPARISON")
    line()

    df = equipment.copy()

    # Convert thousands into individual units
    df["tanks_spg_units"] = (
        df["tanks_spg_thousands"] * 1000
    )

    df["aircraft_units"] = (
        df["combat_aircraft_thousands"] * 1000
    )

    print(
        df[
            [
                "country",
                "alliance",
                "tanks_spg_units",
                "aircraft_units",
                "guns_thousands",
                "major_naval_vessels_units"
            ]
        ]
        .sort_values(
            "tanks_spg_units",
            ascending=False
        )
        .to_string(index=False)
    )

    # Compare Axis and Allied production
    print("\nALLIED VS AXIS PRODUCTION")

    alliance_totals = df.groupby("alliance")[
        [
            "tanks_spg_thousands",
            "combat_aircraft_thousands",
            "guns_thousands"
        ]
    ].sum()

    print(alliance_totals)


# 4. INDUSTRIAL OUTPUT ANALYSIS
def show_industry_analysis():

    print("\nINDUSTRIAL OUTPUT ANALYSIS")
    line()

    categories = [
        "tanks_spg",
        "combat_aircraft"
    ]

    for category in categories:

        df = production[
            production["equipment"] == category
        ]

        # Calculate total production per country
        totals = df.groupby("country")[
            "production_thousands"
        ].sum(min_count=1)

        totals = totals.sort_values(
            ascending=False
        )

        print(f"\n{category.upper()} PRODUCTION")

        print(totals.round(1))

        # Convert Pandas Series into NumPy array
        values = totals.dropna().to_numpy(
            dtype=float
        )

        # Statistical calculations
        average = np.mean(values)

        standard_deviation = np.std(values)

        highest = np.max(values)

        lowest = np.min(values)

        print("\nSTATISTICS")

        print(f"Average production: {average:.2f}")

        print(
            f"Standard deviation: "
            f"{standard_deviation:.2f}"
        )

        print(f"Highest production: {highest:.2f}")

        print(f"Lowest production: {lowest:.2f}")

        print(
            f"Highest/Lowest ratio: "
            f"{highest / lowest:.2f}x"
        )


# 5. EXPORT RESULTS
def export_summary():

    output = ROOT / "output"

    output.mkdir(exist_ok=True)

    # Export battle analysis
    battle_copy = battles.copy()

    battle_copy["known_casualties"] = (
        battle_copy[
            ["killed", "wounded"]
        ].sum(axis=1, min_count=1)
    )

    battle_copy.to_csv(
        output / "battle_casualty_analysis.csv",
        index=False
    )

    # Export production summary
    production_summary = production.pivot_table(
        index="country",
        columns="equipment",
        values="production_thousands",
        aggfunc="sum"
    )

    production_summary.to_csv(
        output / "production_summary.csv"
    )

    print("\nAnalysis exported successfully!")

    print(f"Location: {output}")


# MAIN MENU
def menu():

    while True:

        print("\n" + "=" * 60)

        print("       WWII MILITARY DATA INTELLIGENCE")

        print("=" * 60)

        print("1. Analyze battle casualties")

        print("2. Compare tank and aircraft production")

        print("3. Compare military equipment")

        print("4. Analyze industrial output")

        print("5. Export analysis results")

        print("6. Run all analyses")

        print("0. Exit")

        choice = input("\nChoose an option: ")

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

            print("Exiting project. Goodbye!")

            break

        else:

            print("Invalid choice. Try again.")


# PROGRAM EXECUTION
if __name__ == "__main__":

    menu()