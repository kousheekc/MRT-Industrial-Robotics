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

    return np.array([[x, y, z]]), links

def links2fig(links):
    lines = go.Scatter3d(
        x=links[:, 0],
        y=links[:, 1],
        z=links[:, 2],
        mode='lines',
        marker=dict(
            size=5,
            colorscale='Viridis',
            opacity=0.8
        )
    )
    return lines


point1, links1 = FKM_links(10, 5, -89, 0, 8)
point2, links2 = FKM_links(10, 5, -45, 20, 6)
point3, links3 = FKM_links(10, 5,   0, 40, 4)
point4, links4 = FKM_links(10, 5,  45, 60, 2)
point5, links5 = FKM_links(10, 5,  89, 80, 0)

points = np.vstack((point1, point2, point3, point4, point5))
links = np.vstack((links1,links2,links3,links4,links5))


points = go.Scatter3d(
    x=points[:, 0],
    y=points[:, 1],
    z=points[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        colorscale='Viridis',
        opacity=0.8
    )
)

lines1 = links2fig(links1)
lines2 = links2fig(links2)
lines3 = links2fig(links3)
lines4 = links2fig(links4)
lines5 = links2fig(links5)

fig = go.Figure(data=[points, lines1, lines2, lines3, lines4, lines5])

fig.show()





