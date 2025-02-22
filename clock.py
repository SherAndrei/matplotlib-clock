import numpy as np
import matplotlib.pyplot as plt

def rotate(v, alpha):
    assert v.shape == (2, 1)
    rotation_matrix = np.array([
        [np.cos(alpha),  np.sin(alpha)],
        [-np.sin(alpha), np.cos(alpha)]
      ])
    return np.matmul(rotation_matrix, v)


def column_vector(l):
    return np.vstack(l)

class Arrow:
    def __init__(self, other: np.array) -> None:
        self.__raw = other

    def value(self) -> np.array:
        return self.__raw

    def length(self) -> float:
        return np.sqrt(np.matmul(self.value().T, self.value()).item())

class HourArrow(Arrow):
    @staticmethod
    def angular_velocity() -> float:
        return np.pi / 12 / 60

class MinuteArrow(Arrow):
    @staticmethod
    def angular_velocity() -> float:
        return np.pi / 30

hour_arrow = HourArrow(column_vector([0, 0.4]))
minute_arrow = MinuteArrow(column_vector([0, 1]))

fig, ax = plt.subplots(figsize=(8,8))

fig.canvas.manager.set_window_title('Clock')

def display_clock():
    plt.cla()
    ax.axis('off')
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])

    def display_hours():
        for hour in range(1, 13):
            angle = hour * np.pi / 6
            coords = np.array([np.sin(angle), np.cos(angle)])
            plt.text(*coords, str(hour), horizontalalignment='center', verticalalignment='center')

    def display_minutes():
        for minute in range(60):
            if minute % 5 == 0:
                continue
            angle = minute * np.pi / 30
            xcoord = np.sin(angle)
            ycoord = np.cos(angle)
            scale = 0.98
            plt.plot([scale * xcoord, xcoord], [scale * ycoord, ycoord], '-k')

    def do_display_arrow(target):
        plt.quiver(*target.value(), angles='xy', scale_units='xy', scale=1)

    display_hours()
    display_minutes()
    do_display_arrow(hour_arrow)
    do_display_arrow(minute_arrow)
    plt.draw()

def do_rotate(target, explicit_direction):
    direction = 1 if explicit_direction == 'right' else -1
    return rotate(target.value(), direction * target.angular_velocity())

def on_key_press(event):
    global hour_arrow
    global minute_arrow
    if event.key == 'right' or event.key == 'left':
      hour_arrow = HourArrow(do_rotate(hour_arrow, event.key))
      minute_arrow = MinuteArrow(do_rotate(minute_arrow, event.key))
    display_clock()

fig.canvas.mpl_connect('key_press_event', on_key_press)

display_clock()
plt.show()
