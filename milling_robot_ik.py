import math
import numpy as np
import plotly.graph_objects as go

class joint:
    def __init__(self, min, max, step):
        self.min = min
        self.max = max
        self.step = step

def FKM(a, b, q1, q2, d4):
    x = -(a - (d4 + b) * math.sin(math.radians(q2))) * math.sin(math.radians(q1))
    y = (a - (d4 + b) * math.sin(math.radians(q2))) * math.cos(math.radians(q1))
    z = (d4 + b) * math.cos(math.radians(q2))
    return [x, y, z]

def FKM_links(a, b, q1, q2, d4):
    x = -(a - (d4 + b) * math.sin(math.radians(q2))) * math.sin(math.radians(q1))
    y = (a - (d4 + b) * math.sin(math.radians(q2))) * math.cos(math.radians(q1))
    z = (d4 + b) * math.cos(math.radians(q2))
    links = np.zeros((4, 3))
    links[1][0] = -a * math.sin(math.radians(q1))
    links[1][1] = a * math.cos(math.radians(q1))
    
    links[2][0] = -(a+b*math.sin(math.radians(-q2))) * math.sin(math.radians(q1))
    links[2][1] = (a+b*math.sin(math.radians(-q2))) * math.cos(math.radians(q1))
    links[2][2] = b * math.cos(math.radians(q2))

    links[3][0] = -(a+(b+d4)*math.sin(math.radians(-q2))) * math.sin(math.radians(q1))
    links[3][1] = (a+(b+d4)*math.sin(math.radians(-q2))) * math.cos(math.radians(q1))
    links[3][2] = (b+d4) * math.cos(math.radians(q2))

    link1 = go.Scatter3d(
        x=links[:2, 0],
        y=links[:2, 1],
        z=links[:2, 2],
        mode='lines',
        line=dict(color='blue')
    )

    link2 = go.Scatter3d(
        x=links[1:3, 0],
        y=links[1:3, 1],
        z=links[1:3, 2],
        mode='lines',
        line=dict(color='red')
    )

    link3 = go.Scatter3d(
        x=links[2:4, 0],
        y=links[2:4, 1],
        z=links[2:4, 2],
        mode='lines',
        line=dict(color='green')
    )

    return np.array([[x, y, z]]), [link1, link2, link3]


point, links = FKM_links(10, 5, -89, 0, 8)

points = go.Scatter3d(
    x=point[:, 0],
    y=point[:, 1],
    z=point[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        colorscale='Viridis',
        opacity=0.8
    )
)

fig = go.Figure(data=[points] + links)

fig.show()





