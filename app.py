import streamlit as st

from multiapp import MultiApp
from apps import (
	exoplanet,
	gravity_wave,
	sun
)


st.set_page_config(layout="wide")

app = MultiApp()
app.add_app('太陽系外行星', exoplanet.app)
app.add_app('重力波', gravity_wave.app)
app.add_app('太陽', sun.app)
app.run()
