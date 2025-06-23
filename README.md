# EcoRoute: AI-Driven Sustainable Supply Chain Optimization

EcoRoute is a Streamlit-based prototype that simulates how a retail company (like Walmart) can:

- Predict inventory waste using AI
- Optimize delivery routes to reduce carbon emissions
- Assign sustainability scores based on logistics and product data

## Features

1. **Data Input:** Upload inventory and route CSV files
2. **Waste Prediction:** AI model predicts inventory waste and visualizes top waste products
3. **Route Carbon Scoring:** Calculates and compares carbon footprint for each delivery route
4. **Sustainability Scoring:** Computes a sustainability score for each route and visualizes with color indicators
5. **Dashboard:** Multi-page Streamlit app for easy navigation
6. **Optional:** Map visualization, tooltips, and downloadable reports

## Tech Stack

- Frontend: Streamlit
- Backend: Python
- ML: Scikit-learn (can swap for XGBoost)
- Mapping: Folium
- Data: Local CSV files (see `data/` folder)

## Folder Structure

```
EcoRoute/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   ├── inventory.csv
│   └── routes.csv
└── modules/
    ├── __init__.py
    ├── data_upload.py
    ├── waste_prediction.py
    ├── route_optimizer.py
    ├── sustainability_summary.py
    └── README.md
```

## Setup & Run

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the app:
   ```
   streamlit run app.py
   ```
3. Use the sidebar to navigate between pages.

## Data Format

- `inventory.csv`: product_id, category, stock, demand_forecast, shelf_life
- `routes.csv`: route_id, source, destination, distance_km, vehicle_type (EV or Diesel)

## Notes

- This is a prototype for demonstration and educational purposes.
- Replace dummy models and data with real ones for production use.
