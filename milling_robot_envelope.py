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

def workspace(a, b, joints):
    poses = []
    for i in np.arange(joints[0].min, joints[0].max, joints[0].step):
        for j in np.arange(joints[1].min, joints[1].max, joints[1].step):
            for k in np.arange(joints[2].min, joints[2].max, joints[2].step):
                poses.append(FKM(a, b, i, j, k) + [0])

        print(i)
    poses.append([0,0,0,1])
    return np.array(poses)

joints = [joint(-90, 90, 10), joint(-90, 0, 10), joint(0, 10, 1)]

poses = workspace(10, 5, joints)
print(poses)

points = go.Scatter3d(
    x=poses[:, 0],
    y=poses[:, 1],
    z=poses[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=poses[:, 3],
        colorscale='Viridis',
        opacity=0.8
    )
)

lines = np.array([
    [0,0,0],
    [0,10,0],
    [0,10,5]
])

points = go.Scatter3d(
    x=poses[:, 0],
    y=poses[:, 1],
    z=poses[:, 2],
    mode='markers',
    marker=dict(
        size=5,
        color=poses[:, 3],
        colorscale='Viridis',
        opacity=0.8
    )
)

lines = go.Scatter3d(
    x=lines[:, 0],
    y=lines[:, 1],
    z=lines[:, 2],
    mode='lines',
    marker=dict(
        size=5,
        colorscale='Viridis',
        opacity=0.8
    )
)

fig = go.Figure(data=[points, lines])

fig.show()





