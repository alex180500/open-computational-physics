import pandas as pd
from PIL import Image
import streamlit as st

st.sidebar.write("""**Lennard Jonesium Phase Diagram**  
Image taken from [Wikipedia](https://en.wikipedia.org/wiki/Lennard-Jones_potential)""")

phase_diagram = Image.open('../molecular-dynamics/LJ_PhaseDiagram.png')
st.sidebar.image(phase_diagram)

temp = st.sidebar.select_slider('Input Temperature', [0.5, 1.0, 1.5, 2.0])
rho = st.sidebar.select_slider('Input Density', [0.1, 0.4, 0.7, 1.0])

folder = '../molecular-dynamics/data/' + \
    'T' + format(temp, '.1f').replace('.', '') + \
    '_r' + format(rho, '.1f').replace('.', '')

st.write(f"""
# Phase Diagram Explorer
Molecular Dynamics data visualizer *by Alessandro Romancino*  
https://github.com/alex180500/open-computational-physics  
## T = {temp:.1f} T\* &emsp; ρ = {rho:.1f} ρ\*
""")

st.write('##### Radial Distribution Function')
rdf_data = pd.read_csv(folder + '/rdf.txt', sep=' ', names=['x', 'rdf'], index_col=0)
st.line_chart(rdf_data)

st.write(f"""##### Pre-rendered Animation
Made with [VMD](https://www.ks.uiuc.edu/Research/vmd/)
""")
animation_data = open(folder + '/output.mp4', 'rb').read()
st.video(animation_data)