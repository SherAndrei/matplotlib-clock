from typing import Tuple

import datetime
import numpy as np
import matplotlib.pyplot as plt

def rotate(v: np.ndarray, alpha: float) -> np.ndarray:
    """Rotate a 2D vector by a given angle."""
    assert v.shape == (2, 1)
    rotation_matrix = np.array([
        [np.cos(alpha),  np.sin(alpha)],
        [-np.sin(alpha), np.cos(alpha)]
      ])
    return np.matmul(rotation_matrix, v)

def column_vector(l: Tuple[float, float]) -> np.ndarray:
    """Convert a list or tuple to a column vector."""
    return np.vstack(l)

class Arrow:
    """Base class for clock arrows."""
    def __init__(self, length: float, angle: float):
        self.vector = rotate(column_vector([0, length]), angle)

    @property
    def value(self) -> np.ndarray:
        """Get the current vector representation of the arrow."""
        return self.vector

    @staticmethod
    def angular_velocity() -> float:
        """Get the angular velocity of the arrow."""
        raise NotImplementedError


class HourArrow(Arrow):
    """Class representing the hour arrow."""
    @staticmethod
    def angular_velocity() -> float:
        return np.pi / 6 / 60

class MinuteArrow(Arrow):
    """Class representing the minute arrow."""
    @staticmethod
    def angular_velocity() -> float:
        return np.pi / 30

class Clock:
    """Class representing a clock."""

    def __init__(self):
        now = datetime.datetime.now()
        self.hour_arrow = HourArrow(0.4, now.hour * np.pi / 6 + now.minute * HourArrow.angular_velocity())
        self.minute_arrow = MinuteArrow(0.6, now.minute * MinuteArrow.angular_velocity())
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.canvas.manager.set_window_title('Clock')
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def display_clock(self):
        """Display the clock with hour and minute arrows."""
        self.ax.clear()
        self.ax.axis('off')
        self.ax.set_xlim([-1, 1])
        self.ax.set_ylim([-1, 1])

        self.ax.add_patch(plt.Circle((0, 0), 1, edgecolor='black', facecolor='none'))

        for hour in range(1, 13):
            angle = hour * np.pi / 6
            scale = 0.94
            coords = np.array([scale * np.sin(angle), scale * np.cos(angle)])
            self.ax.text(*coords, str(hour), fontsize=14, horizontalalignment='center', verticalalignment='center')

        for minute in range(60):
            if minute % 5 == 0:
                continue
            angle = minute * np.pi / 30
            xcoord = np.sin(angle)
            ycoord = np.cos(angle)
            scale = 0.98
            self.ax.plot([scale * xcoord, xcoord], [scale * ycoord, ycoord], '-k')

        self.ax.quiver(*self.hour_arrow.value, angles='xy', scale_units='xy', scale=1, color='blue')
        self.ax.quiver(*self.minute_arrow.value, angles='xy', scale_units='xy', scale=1, color='red')

        plt.draw()

    def on_key_press(self, event):
        """Handle key press events to rotate arrows."""
        if event.key in ('right', 'left'):
            direction = 1 if event.key == 'right' else -1
            self.hour_arrow.vector = rotate(self.hour_arrow.value, direction * self.hour_arrow.angular_velocity())
            self.minute_arrow.vector = rotate(self.minute_arrow.value, direction * self.minute_arrow.angular_velocity())
            self.display_clock()

if __name__ == "__main__":
    clock = Clock()
    clock.display_clock()
    plt.show()
