# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.

import matplotlib.pyplot as plt

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
st.text('Fixed width text')
col1, col2 = st.columns(2)
col1.write("This is column 1")
col2.write("This is column 2")


import numpy as np
import matplotlib.pyplot as plt


data = {
    'bigrams': ['ever seen',
                'ive seen',
                'special effects',
                'even though',
                'one best',
                'low budget',
                'looks like',
                'year old',
                'waste time',
                'first time',
                'see movie',
                'im sure',
                'good movie'],

    'frequency': [41212, 4215,4119,
                  4106, 3184,  35151, 3214,
                  3123, 13014, 2185,
                  2813,2813, 27112],

    'color': ['#5A69AF', '#579E65', '#F9C784', '#FC944A',
              '#F24C00', '#00B825', '#FC944A', '#EF4026',
              'goldenrod','green', '#F9C784', '#FC944A',
              'coral']
}

bubble_chart = BubbleChart(area=data['frequency'],
                           bubble_spacing=0.1)
bubble_chart.collapse()



fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))
fig.set_size_inches(9, 13, forward=True)
bubble_chart.plot(
    ax, data['bigrams'], data['color'])
ax.axis("off")
ax.relim()
ax.autoscale_view()
plt.show()