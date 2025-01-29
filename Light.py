import numpy as np

class Light:
    def __init__(self, position, intensity=1.0, color=(1, 1, 1)):
        """
        Tworzy nowe źródło światła.

        :param position: Pozycja światła (numpy array)
        :param intensity: Intensywność światła (float)
        :param color: Kolor światła (tuple r,g,b)
        """
        self.position = np.array(position)
        self.intensity = intensity
        self.color = np.array(color)
