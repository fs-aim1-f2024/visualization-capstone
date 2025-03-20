from nicegui import ui
import pandas as pd
import pickle
import os

class AppState:
    def __init__(self):
        self.data = None
        self.is_data_loaded = False
        # Try to load existing state on initialization
        try:
            self.load_state()
        except:
            # If no saved state exists, load fresh data
            self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_csv("data/spotify-2023.csv", encoding="latin-1")
            self.is_data_loaded = True
            ui.notify("Data loaded successfully")
        except Exception as e:
            ui.notify(f"Error loading data: {str(e)}")

    def delete_state(self):
        self.data = None
        self.is_data_loaded = False
        if os.path.exists("state.pkl"):
            os.remove("state.pkl")

    def load_state(self):
        if os.path.exists("state.pkl"):
            with open("state.pkl", "rb") as f:
                loaded_state = pickle.load(f)
                self.data = loaded_state.data
                self.is_data_loaded = loaded_state.is_data_loaded
                
    def save_state(self):
        try:
            with open("state.pkl", "wb") as f:
                pickle.dump(self, f)
            ui.notify("State saved successfully")
        except Exception as e:
            ui.notify(f"Error saving state: {str(e)}")
    
    def preprocess_data(self):
        if self.data is not None:
            # Add your preprocessing steps here
            pass
            
app_state = AppState()

def paint_data_preparation():
    ui.label("Data Preparation")
    ui.button("Load Data", on_click=app_state.load_data) 
    ui.button("Clear State", on_click=app_state.delete_state)
