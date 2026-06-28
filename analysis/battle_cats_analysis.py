"""
Battle Cats Game Analysis
=========================
Analysis framework for Battle Cats unit data.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------------------
# Data Structure
# ---------------------------------------------------------------------------

@dataclass
class BattleCatUnit:
    """Represents a single Battle Cats unit with core stats."""
    name: str
    unit_id: int
    category: str                  # e.g. "Normal", "Special", "Rare", "Super Rare", "Uber Rare"
    hp: int                        # Hit points
    attack_power: int              # Single hit damage
    attack_speed: float            # Attack cycle in frames (30f = 1s)
    movement_speed: int            # Movement speed
    range_: int                    # Attack range
    cost: int                      # Cat food / energy cost
    recharge_time: float           # Recharge time in seconds
    area_attack: bool = False      # True if area attack
    knockback_count: int = 0       # Number of knockbacks
    special_ability: Optional[str] = None  # e.g. "Strong vs Red", "Freeze"


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_unit_csv(filepath: str) -> pd.DataFrame:
    """
    Load unit stats from a CSV file.

    Expected columns: name, unit_id, category, hp, attack_power,
                      attack_speed, movement_speed, range, cost,
                      recharge_time, area_attack, knockback_count,
                      special_ability
    """
    df = pd.read_csv(filepath)
    return df


def load_units_from_dict(records: list[dict]) -> pd.DataFrame:
    """Create a DataFrame directly from a list of unit stat dicts."""
    return pd.DataFrame(records)


def sample_data() -> pd.DataFrame:
    """Return a small sample dataset for quick testing."""
    records = [
        dict(name="Cat", unit_id=0, category="Normal", hp=250, attack_power=20,
             attack_speed=2.0, movement_speed=10, range_=140, cost=75,
             recharge_time=2.0, area_attack=False, knockback_count=3),
        dict(name="Tank Cat", unit_id=1, category="Normal", hp=1000, attack_power=70,
             attack_speed=4.13, movement_speed=10, range_=140, cost=150,
             recharge_time=4.0, area_attack=False, knockback_count=3),
        dict(name="Axe Cat", unit_id=2, category="Normal", hp=300, attack_power=200,
             attack_speed=3.0, movement_speed=14, range_=150, cost=150,
             recharge_time=4.0, area_attack=False, knockback_count=1),
        dict(name="Gross Cat", unit_id=3, category="Normal", hp=350, attack_power=100,
             attack_speed=3.0, movement_speed=18, range_=190, cost=225,
             recharge_time=5.0, area_attack=True, knockback_count=1),
        dict(name="Cow Cat", unit_id=4, category="Normal", hp=400, attack_power=110,
             attack_speed=2.2, movement_speed=32, range_=140, cost=300,
             recharge_time=8.0, area_attack=False, knockback_count=2),
    ]
    return pd.DataFrame(records)


# ---------------------------------------------------------------------------
# Feature Engineering
# ---------------------------------------------------------------------------

def compute_dps(df: pd.DataFrame) -> pd.DataFrame:
    """Add a DPS (damage per second) column."""
    df = df.copy()
    df["dps"] = df["attack_power"] / df["attack_speed"]
    return df


def compute_strength_score(df: pd.DataFrame,
                            hp_weight: float = 0.3,
                            dps_weight: float = 0.5,
                            range_weight: float = 0.2) -> pd.DataFrame:
    """
    Compute a simple normalised strength score.

    Score = hp_weight * norm(hp)
          + dps_weight * norm(dps)
          + range_weight * norm(range)

    All weights should sum to 1.0.
    """
    df = compute_dps(df)
    df = df.copy()

    def _norm(series: pd.Series) -> pd.Series:
        mn, mx = series.min(), series.max()
        if mx == mn:
            return pd.Series(np.zeros(len(series)), index=series.index)
        return (series - mn) / (mx - mn)

    df["score"] = (
        hp_weight    * _norm(df["hp"])
        + dps_weight * _norm(df["dps"])
        + range_weight * _norm(df["range_"])
    )
    return df


# ---------------------------------------------------------------------------
# Basic Visualisation
# ---------------------------------------------------------------------------

def plot_strength_scores(df: pd.DataFrame, top_n: int = 20) -> None:
    """Bar chart of top-N units by strength score."""
    if "score" not in df.columns:
        df = compute_strength_score(df)
    top = df.nlargest(top_n, "score")
    plt.figure(figsize=(10, 6))
    sns.barplot(data=top, x="score", y="name", palette="viridis")
    plt.title(f"Top {top_n} Units by Strength Score")
    plt.xlabel("Score")
    plt.ylabel("Unit")
    plt.tight_layout()
    plt.show()


def plot_hp_vs_dps(df: pd.DataFrame) -> None:
    """Scatter plot of HP vs DPS coloured by category."""
    if "dps" not in df.columns:
        df = compute_dps(df)
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="hp", y="dps", hue="category", s=80, alpha=0.8)
    plt.title("HP vs DPS by Category")
    plt.xlabel("HP")
    plt.ylabel("DPS")
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Entry Point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    df = sample_data()
    df = compute_strength_score(df)
    print(df[["name", "hp", "dps", "score"]].sort_values("score", ascending=False))
    plot_strength_scores(df, top_n=5)
    plot_hp_vs_dps(df)
