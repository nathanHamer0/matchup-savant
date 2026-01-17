# Matchup Savant

An interactive baseball batter–pitcher matchup calculator inspired by Baseball Savant.

## Functionality

Matchup Savant evaluates batter–pitcher matchups using:

- Per-pitch-type run value (RV/100)
- Per-pitch-type usage frequencies
- Per-zone run value (RV/100)
- Per-zone frequencies

It outputs:

- A frequency-weighted composite run value matchup score
- Per-pitch-type frequency-weighted run value scores and associated visualizations
- Per-zone frequency-weighted run value scores and associated visualizations

## Motivation

I wanted to combine:

- Baseball sabermetrics
- Data visualization

## Tech stack

- HTML
- CSS
- JavaScript
- Python
- FastAPI
- pandas

## Challenges

- Using Panda library and interacting with .CSVs
- Working with CSS grids and positioning

## Live demo

- https://matchup-savant.onrender.com/

**Notes:**

- The first load may take 30-60 seconds as the free tier render service spins up from sleep.
- Due to not-yet-optimized code, matchup loads may take 5-10 seconds per load.

## Project Structure

backend/
├── main.py
├── data_loader.py
├── matchup.py
├── name_utils.py
├── static/
├──── index.html
├──── style.css
├──── app.js
├── data/
├──── ...
scripts/
├── validate_matchup.py
...

## Future improvements

- Improve UI, at graphics specifically
  - Re-implement legend as an expandable and portable side-bar
- Optimize matchup load speeds
- Implementing handedness splits
- Handling missing data for small-sample players in terms of UI representation
- Caching player data
