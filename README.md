# Football Match Total Goals Predictor

A Poisson-based model for predicting total goals in English football matches across the Premier League, Championship, and League One, using Expected Goals (xG) data.

---

## Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Dependencies](#dependencies)

---

## Project Structure

```
bet365/
│
├── data/
│   └── match_data.csv          # Match data (required)
│
├── src/
│   ├── data_pipeline.py        # Data loading, cleaning, and model inputs
│   └── poisson_model.py        # Poisson model and projection functions
│
├── backtest.py                 # Backtest against unseen fixtures
├── main.py                     # Predict total goals for a single fixture
├── requirements.txt
└── README.md
```

---

## Installation

Requires Python 3.13.1.

```bash
pip install -r requirements.txt
```

Ensure `match_data.csv` is placed in the `data/` directory before running.

---

## Usage

### Predict a single fixture

Edit the fixture details in `main.py`:

```python
fixture = {
    'home_team': 'Arsenal',
    'away_team': 'Chelsea',
    'league_name': 'Premier League'
}
```

Then run:

```bash
python main.py
```

### Run the backtest

```bash
python backtest.py
```

Evaluates the model on fixtures after 2026-01-01, reporting MAE, RMSE, and distribution statistics.

---

## Dependencies

```
pandas
numpy
scipy
matplotlib
```
