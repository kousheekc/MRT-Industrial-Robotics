import math
import numpy as np
import plotly.graph_objects as go

class Robot:
    def __init__(self, a, b):
        self.a = a
        self.b = b

        origin = go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode="markers+text",
            name="Origin",
            text=["Origin"],
            marker=dict(
                size=5
            )
        )

        self.fig = go.Figure(data=[origin])
        self.fig.update_layout(scene=dict(
                    xaxis=dict(range=[-30, 30], title='X (m)'),
                    yaxis=dict(range=[-30, 30], title='Y (m)'),
                    zaxis=dict(range=[-30, 30], title='Z (m)'),
                    aspectmode='cube'
                    )
                )
        
    def plot_title(self, my_title):
        self.fig.update_layout(title=my_title)


    def enveloppe(self, joint1_limits, joint2_limits, joint4_limits):
        poses = []
        for i in np.arange(joint1_limits[0], joint1_limits[1], joint1_limits[2]):
            for j in np.arange(joint2_limits[0], joint2_limits[1], joint2_limits[2]):
                for k in np.arange(joint4_limits[0], joint4_limits[1], joint4_limits[2]):
                    poses.append(self.FKM(i, j, k))

            print(i)
        poses = np.array(poses)  

        points = go.Scatter3d(
            x=poses[:, 0],
            y=poses[:, 1],
            z=poses[:, 2],
            mode='markers',
            name="Workspace",
            marker=dict(
                size=5,
                opacity=0.8
            )
        )

        self.fig.update_layout(
            annotations=[
                dict(
                    text=f"{joint1_limits[0]} < q1 < {joint1_limits[1]} <br> {joint2_limits[0]} < q2 < {joint2_limits[1]} <br> {joint4_limits[0]} < d4 < {joint4_limits[1]}",
                    xref="paper", 
                    yref="paper",
                    x=1.1,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=20
                    )
                )
            ]
        )

        self.fig.add_trace(points)

    
    def enveloppe_with_links(self, joint1_limits, joint2_limits, joint4_limits):
        poses = []
        for i in np.arange(joint1_limits[0], joint1_limits[1], joint1_limits[2]):
            for j in np.arange(joint2_limits[0], joint2_limits[1], joint2_limits[2]):
                for k in np.arange(joint4_limits[0], joint4_limits[1], joint4_limits[2]):
                    self.FKM_draw(i, j, k)

    def FKM(self, q1, q2, d4):
        x = -(self.a - (d4 + self.b) * math.sin(math.radians(q2))) * math.sin(math.radians(q1))
        y = (self.a - (d4 + self.b) * math.sin(math.radians(q2))) * math.cos(math.radians(q1))
        z = (d4 + self.b) * math.cos(math.radians(q2))
        return [x, y, z]
    
    def IKM(self, x, y, z):
        q1 = -math.atan2(x, y)
        q2 = math.atan2(x+self.a*math.sin(q1), z*math.sin(q1))
        d4 = z/math.cos(q2) - self.b
        return [math.degrees(q1), math.degrees(q2), d4]
    
    def FKM_draw(self, q1, q2, d4):
        pose = self.FKM(q1, q2, d4)
        links = np.zeros((4, 3))

        links[1][0] = -self.a * math.sin(math.radians(q1))
        links[1][1] = self.a * math.cos(math.radians(q1))
        
        links[2][0] = -(self.a+self.b*math.sin(math.radians(-q2))) * math.sin(math.radians(q1))
        links[2][1] = (self.a+self.b*math.sin(math.radians(-q2))) * math.cos(math.radians(q1))
        links[2][2] = self.b * math.cos(math.radians(q2))

        links[3][0] = -(self.a+(self.b+d4)*math.sin(math.radians(-q2))) * math.sin(math.radians(q1))
        links[3][1] = (self.a+(self.b+d4)*math.sin(math.radians(-q2))) * math.cos(math.radians(q1))
        links[3][2] = (self.b+d4) * math.cos(math.radians(q2))
 
        point = go.Scatter3d(
            x=[pose[0]],
            y=[pose[1]],
            z=[pose[2]],
            mode='markers',
            name="End Effector",
            marker=dict(
                color='black',
                size=2,
                opacity=0.8
            )
        )

        link1 = go.Scatter3d(
            x=links[:2, 0],
            y=links[:2, 1],
            z=links[:2, 2],
            mode='lines',
            name="Link1",
            line=dict(color='blue' if (0<=d4<=10) else 'red')
        )

        link2 = go.Scatter3d(
            x=links[1:3, 0],
            y=links[1:3, 1],
            z=links[1:3, 2],
            mode='lines',
            name="Link2",
            line=dict(color='orange' if (0<=d4<=10) else 'red')
        )

        link3 = go.Scatter3d(
            x=links[2:4, 0],
            y=links[2:4, 1],
            z=links[2:4, 2],
            mode='lines',
            name="Link3",
            line=dict(color='green' if (0<=d4<=10) else 'red')
        )

        self.fig.add_trace(point)
        self.fig.add_trace(link1)
        self.fig.add_trace(link2)
        self.fig.add_trace(link3)

        return [point, link1, link2, link3]

    def IKM_draw(self, x, y, z):
        joints = self.IKM(x, y, z)
        return self.FKM_draw(joints[0], joints[1], joints[2])

    def trajectory(self, points):
        trajectory = self.interpolate(points)

        first_frame_data = None
        trajectory_frames = []

        for point in trajectory:
            frame_data = self.IKM_draw(point[0], point[1], point[2])
            if first_frame_data == None:
                first_frame_data = frame_data
            trajectory_frames.append(go.Frame(data=frame_data))

        fig = go.Figure(
            data=first_frame_data,
            layout=go.Layout(
                scene=dict(
                    xaxis=dict(range=[-20, 20]),
                    yaxis=dict(range=[-20, 20]),
                    zaxis=dict(range=[-20, 20]),
                    aspectmode='cube'
                ),
                updatemenus=[dict(
                    type="buttons",
                    buttons=[dict(label="Play",
                                method="animate",
                                args=[None, {'frame': {'duration': 1}}])])]
            ),
            frames=trajectory_frames
        )

        trajectory = np.array(trajectory)
        traj = go.Scatter3d(
            x=trajectory[:, 0],
            y=trajectory[:, 1],
            z=trajectory[:, 2],
            mode='lines',
            name="Trajectory",
            line=dict(color='rgba(0, 0, 0, 0.5)')
        )

        origin = go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode="markers+text",
            name="Origin",
            text=["Origin"],
            marker=dict(
                size=5
            )
        )

        fig.add_trace(origin)
        fig.add_trace(traj)

        fig.show()

    def interpolate(self, points, resolution=5):
        interpolated_points = []

        for i in range(len(points)-1):

            point1 = np.array(points[i])
            point2 = np.array(points[i+1])

            for i in range(resolution):
                alpha = i / (resolution - 1)
                interpolated_point = (1 - alpha) * point1 + alpha * point2
                interpolated_points.append(interpolated_point)

        return interpolated_points
    
    def show(self):
        self.fig.show()