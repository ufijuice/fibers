"""Illustrative planning assumptions, not a forecast or valuation opinion.

Run with Python 3; writes scenarios and investor-return sensitivities beside
this file. USD throughout. Years run from financing close. No customer demand,
vendor quotes, or founder cash compensation has been independently confirmed.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASP = [5000, 5000, 4500, 4000, 3500, 3200, 3000]
COGS = [4000, 4000, 3000, 2200, 1575, 1376, 1200]
SCENARIOS = {
    "delayed": {
        "units": [0, 0, 30, 150, 500, 1500, 3500],
        "opex_m": [.35, .65, .90, 1.20, 1.80, 2.60, 3.80],
        "capex_m": [.10, .10, .15, .20, .25, .30, .40],
    },
    "base": {
        "units": [0, 20, 150, 750, 2500, 6500, 12000],
        "opex_m": [.35, .85, 1.60, 2.80, 4.50, 7.00, 10.00],
        "capex_m": [.10, .15, .25, .40, .60, .80, 1.00],
    },
    "upside": {
        "units": [0, 40, 300, 1800, 7000, 18000, 35000],
        "opex_m": [.35, 1.20, 2.20, 4.20, 8.00, 15.00, 24.00],
        "capex_m": [.10, .20, .40, .70, 1.20, 2.00, 3.00],
    },
}


def write_scenarios():
    rows = []
    for scenario, assumptions in SCENARIOS.items():
        cumulative_cash = 0
        peak_deficit = 0
        previous_wc = 0
        for i, units in enumerate(assumptions["units"]):
            revenue = units * ASP[i]
            cost = units * COGS[i]
            gp = revenue - cost
            opex = round(assumptions["opex_m"][i] * 1_000_000)
            capex = round(assumptions["capex_m"][i] * 1_000_000)
            # Simplified net working capital, not a detailed inventory model.
            wc = round(.20 * revenue)
            cash = gp - opex - capex - (wc - previous_wc)
            cumulative_cash += cash
            peak_deficit = max(peak_deficit, -cumulative_cash)
            previous_wc = wc
            rows.append({
                "scenario": scenario, "year": i + 1, "units": units,
                "asp_usd": ASP[i], "cogs_per_unit_usd": COGS[i],
                "revenue_usd": revenue, "gross_profit_usd": gp,
                "gross_margin_pct": round(100 * gp / revenue, 2) if revenue else "",
                "cash_opex_usd": opex, "capex_usd": capex,
                "net_working_capital_usd": wc, "cash_flow_before_financing_usd": cash,
                "cumulative_cash_flow_usd": cumulative_cash,
                "peak_external_capital_needed_usd": peak_deficit,
            })
    path = ROOT / "projection_scenarios.csv"
    with path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for scenario in SCENARIOS:
        selected = [r for r in rows if r["scenario"] == scenario]
        print(scenario, "Y5 revenue", selected[4]["revenue_usd"],
              "Y7 revenue", selected[6]["revenue_usd"],
              "peak capital", selected[-1]["peak_external_capital_needed_usd"])


def write_returns():
    investment = 750_000
    rows = []
    for post_money_cap in [6_000_000, 8_000_000, 10_000_000]:
        for retained_fraction in [.4, .6, .8]:
            ownership = investment / post_money_cap * retained_fraction
            for exit_equity_value in [30_000_000, 50_000_000, 100_000_000,
                                      200_000_000, 300_000_000, 500_000_000,
                                      1_000_000_000]:
                proceeds = ownership * exit_equity_value
                rows.append({
                    "investment_usd": investment,
                    "post_money_safe_cap_usd": post_money_cap,
                    "fraction_of_initial_ownership_retained": retained_fraction,
                    "ownership_at_exit_pct": round(100 * ownership, 4),
                    "exit_equity_value_usd": exit_equity_value,
                    "gross_proceeds_usd": round(proceeds),
                    "gross_multiple_on_investment": round(proceeds / investment, 4),
                    "illustrative_7_year_gross_irr_pct": round(
                        100 * ((proceeds / investment) ** (1 / 7) - 1), 4),
                })
    with (ROOT / "investor_returns.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_preseed_budget():
    # Scheduled core spend: $450k in months 1-12, $185k in months 13-15.
    # The $115k contingency remains cash unless a risk actually materializes.
    fabrication = {3: 15000, 4: 25000, 5: 35000, 9: 15000,
                   11: 28000, 13: 32000, 14: 50000, 15: 20000}
    categories = {"people_usd": 250000, "lab_test_usd": 100000,
                  "operations_ip_usd": 65000}
    rows = []
    cash = 750000
    for month in range(1, 16):
        # Differences of rounded cumulative allocations avoid rounding drift.
        row = {"month": month}
        for name, total in categories.items():
            row[name] = round(total * month / 15) - round(total * (month - 1) / 15)
        row["fabrication_packaging_usd"] = fabrication.get(month, 0)
        row["scheduled_spend_usd"] = sum(row[n] for n in categories) + row["fabrication_packaging_usd"]
        cash -= row["scheduled_spend_usd"]
        row["closing_cash_usd"] = cash
        row["contingency_reserve_usd"] = 115000
        row["cash_above_reserve_usd"] = cash - 115000
        rows.append(row)
    assert sum(r["scheduled_spend_usd"] for r in rows) == 635000
    assert sum(r["scheduled_spend_usd"] for r in rows[:12]) == 450000
    assert rows[-1]["closing_cash_usd"] == 115000
    with (ROOT / "preseed_monthly_budget.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print("15-month scheduled spend", 635000, "remaining contingency", cash)


if __name__ == "__main__":
    write_scenarios()
    write_returns()
    write_preseed_budget()
