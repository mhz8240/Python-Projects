# NFL Game Predictions Model (End-to-End Pipeline)

This repo contains an end-to-end pipeline (implemented in a single Jupyter notebook) that builds game-level features from historical NFL data, trains a model to predict outcomes, and generates weekly predictions.

## Results (Recent Seasons)
- **W/L record over Last Two Seasons:** `389-180-1` (**68.4%**)
- **ATS over Last Two Seasons (vs Vegas spread):** `305-257-8` (**54.3%**)
- 2024 recap deck: *https://docs.google.com/presentation/d/1znbKBgFQ_QQXw_xm91W1x_s_f14T21s4me7ceHXXfXg/edit?usp=sharing*
- 2025 recap deck: *https://docs.google.com/presentation/d/1V8nD894wQmctfSbW4x1LnBecPViLVMpCaN5Pzcu_H24/edit?usp=sharing*

---



---

## Table of Contents
- [How the Model Works](#how-the-model-works)
- [Pipeline: Step-by-Step](#pipeline-step-by-step)
- [Train / Predict Workflow](#train--predict-workflow)
- [Evaluation](#evaluation)
- [Areas for Improvement And Growth](#areas-for-improvement-and-growth)
- [Disclaimer](#disclaimer)

---

## How the Model Works
At prediction time, the model is answering a question like:

> “Given everything we know about Team A and Team B up to Week *k-1*, what should we expect to happen in Week *k*?”

Key design decisions:
1. **Game-level representation:** Construct a feature vector that corresponds to each NFL game.
2. **Team features aggregated from historical data:** we summarize team performance into numeric features.
3. **Time-aware feature generation:** features for a game in Week `k` only use information up to Week `k-1` (no future leakage).
4. **Regression framing:** we predict a continuous outcome (e.g., expected margin / expected points proxy), then derive winner / spread implications from that.

---

## Pipeline: Step-by-Step

### 1) Load & prepare raw data
**Purpose:** Pull all required tables (play-by-play, season, etc.) and make them consistent.

**What happens here:**
- unify team abbreviations
- filter extraneous records (QB spikes, plays nullified by penalty, etc.)
- confirm seasons/weeks loaded correctly
- remove duplicates and validate game keys

---

### 2) Build team-level feature tables
**Purpose:** Convert raw events into team strength signals.

This pipeline generally uses multiple feature “views” of a team:

#### A) Prior-season (baseline) features
These describe a team entering a season.
Examples:
- offensive/defensive efficiency summaries
- scoring and allowed scoring summaries
- pass/run tendencies
- explosiveness/turnover tendencies

**Why it matters:** early-season predictions are unstable without historical context.

---

#### B) Rolling window (“recent form”) features
These capture short-term momentum and recent changes.
Examples:
- last `N` weeks scoring / allowed scoring
- recent efficiency proxies
- volatility and trend signals

**Leakage rule:** for Week `k`, rolling features use only games through Week `k-1`.

---

#### C) Season-to-date features
These describe the full season performance so far.
Examples:
- season-to-date scoring/efficiency summaries
- cumulative or average team stats through Week `k-1`

---

#### D) Delta features (change vs prior season)
These measure directional change rather than absolute level:
- `delta = this_season_to_date - last_season_baseline`

**Why it helps:** teams change significantly year to year (QB, coaching, scheme, roster).

---

### 3) Construct a single feature vector per game
**Purpose:** Merge the two teams into one numeric vector representing the matchup.

A standard approach is:
- join away-team features onto each game
- join home-team features onto each game
- concatenate in a stable order

**Critical requirement:**  
The ordering of concatenation must be identical in:
- training set creation
- validation set creation
- prediction-time feature creation

---

### 4) Define the learning target (what the model predicts)
We are predicting away_score and home_score:

After predicting scores, we derive:
- predicted winner
- predicted spread implication (compare predicted margin vs Vegas line)

---

### 5) Train the model
**Purpose:** learn the mapping from `X` (features) to `y` (outcome).

Typical training steps:
1. assemble training games across seasons
2. standardize features
3. define and fit MLPRegressor
4. record training metrics and sanity checks
5. incorporate monte-carlo averaging since neural network training can be sensitive to random initialization and optimization noise.

### 6) Validation and Early Stopping (Preventing Overfitting)

When training the neural network regressor (`MLPRegressor`), the data is automatically split into:
- a **training subset** used to update model weights, and
- a **validation subset** (a holdout fraction of the training data) used only to **monitor generalization**.

I set:
- `early_stopping=True`
- `validation_fraction=0.15`

So, **15% of the training set is held out internally** as a validation set during training.

**What early stopping monitors:**
For `MLPRegressor`, early stopping monitors the **validation score** (the model’s `.score()`), which is **R²**. Training stops when the validation R² **stops improving** for `n_iter_no_change` consecutive epochs:
- `n_iter_no_change=40`

**Why early stopping matters**:
- preventing over-training and overfitting
- choosing a stopping point that generalizes better



### 7) Generate weekly predictions
**Purpose:** apply the feature pipeline to the upcoming slate.

Prediction-time flow:
1. determine the current week `k`
2. compute team features using data through Week `k-1`
3. build game feature vectors for Week `k`
4. run the trained model(s)
5. output predictions + derived picks

---


## Train / Predict Workflow

### Training workflow
1. select training seasons / weeks
2. build features per game
3. train the model
4. evaluate on a held-out or walk-forward set
5. save the model or keep it in-memory for immediate prediction

### Prediction workflow
1. identify upcoming slate (Week `k`)
2. build features using data through Week `k-1`
3. generate predictions
4. export results

---

## Evaluation
Evaluation lenses:
- **Straight-up accuracy** (did the pick win?)
- **Against the spread (ATS)** accuracy (if Vegas lines are available)
- Regression error metrics:
  - mean absolute error (MAE)
  - root mean squared error (RMSE)
  - coefficient of determination (R^2)

---



## Areas for Improvement and Growth
- [ ] Walk-forward validation instead of random splits
- [ ] Add injury / starting-QB signals (only if source is reliable and consistent)
- [ ] Calibrate a confidence or uncertain proxy.

---

## Disclaimer
This project is for educational and analytical purposes only. Predictions should not be interpreted as guarantees or financial advice.
