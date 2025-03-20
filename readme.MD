# Group 5 - Spotify Data Visualization Dashboard

## Project Overview
This project is a data visualization dashboard for Spotify music data, featuring machine learning analysis and interactive visualizations. The dashboard allows users to explore various aspects of Spotify tracks including release years, streams, playlist presence, and musical characteristics.

## Data Source
- Dataset: `spotify-2023.csv`
- Location: `data/spotify-2023.csv`
- Description: Contains Spotify track data including release years, streams, playlist presence, and various musical characteristics

## Project Structure
```
visualization-capstone/
├── data/                   # Data directory
│   └── spotify-2023.csv    # Main dataset
├── latex/                  # LaTeX directory
│   └── report.tex          # LaTeX report / presentation
├── src/                    # Source code directory
│   ├── main.py            # Main application entry point
│   └── charts/            # Chart modules directory
│       ├── chart1.py      # Distribution of Released Year
│       ├── chart2.py      # Year vs Streams Analysis
│       ├── chart3.py      # Streams by Playlist Presence
│       ├── chart4.py      # Streams Trend Over Time
│       ├── chart5.py      # Correlation Matrix Heatmap
│       ├── chart6.py      # Streams by Artist Count
│       ├── chart7.py      # Streams by Key
│       └── chart8.py      # Danceability vs Valence
├── requirement.txt        # Project dependencies
└── readme.MD             # Project documentation
```

## Features
1. **Data Preprocessing Tab**
   - Load sample data or upload custom CSV
   - Interactive data filtering
   - Filter reset functionality

2. **Visualization Tabs**
   - Distribution of Released Year
   - Relationship between Released Year and Streams
   - Distribution of Streams by Playlist Presence
   - Streams Trend Over Time
   - Correlation Matrix Heatmap
   - Distribution of Streams by Artist Count
   - Distribution of Streams by Key
   - Danceability vs. Valence Scatter Plot

## Dependencies
- nicegui: UI framework
- pandas: Data manipulation
- pathlib: File path handling
- Additional dependencies listed in `requirement.txt`

## Setup and Running
1. Install dependencies:
   ```bash
   pip install -r requirement.txt
   ```
2. Run the application:
   ```bash
   python src/main.py
   ```
3. Open your browser and navigate to the provided local URL

## Usage
1. Start by loading data using either the "Load Sample Data" button or uploading a custom CSV file
2. Use the filters in the Data Preprocessing tab to filter the data
3. Navigate through different visualization tabs to explore various aspects of the data
4. Each visualization includes machine learning analysis and interactive features

## Contributing
This project is developed by Group 5 for the Data Visualization course.
