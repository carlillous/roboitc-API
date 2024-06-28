import numpy as np


class DirectKinematics:

    def __init__(self):
        self.__dh_parameters = [
            {'theta': np.radians(0), 'd': 6.2, 'a': 0, 'alpha': np.radians(90)},
            {'theta': np.radians(0), 'd': 0, 'a': 12.3, 'alpha': np.radians(180)},
            {'theta': np.radians(180), 'd': 0, 'a': 0, 'alpha': np.radians(180)},
            {'theta': np.radians(0), 'd': 0, 'a': 12.8, 'alpha': np.radians(0)},
        ]
        self.positions = []

    def __dh_matrix(self, theta, d, a, alpha):
        return np.array([
            [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
            [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
            [0, np.sin(alpha), np.cos(alpha), d],
            [0, 0, 0, 1]
        ])

    def get_positions(self):
        return self.positions

    def calculate_position(self, joint_angles):
        self.positions.clear()
        base_height = 7.5  # altura de la base del coche en cm
        T = np.identity(4)  # Matriz identidad 4x4
        self.positions.append([T[0, 3], T[1, 3], T[2, 3] + base_height])
        self.__dh_parameters[0]['theta'] = np.radians(joint_angles[0])
        self.__dh_parameters[1]['theta'] = np.radians(joint_angles[1])
        self.__dh_parameters[3]['theta'] = np.radians(joint_angles[2])

        # Calcular la matriz de transformación total
        for param in self.__dh_parameters:
            theta = param['theta']
            d = param['d']
            a = param['a']
            alpha = param['alpha']
            T = np.dot(T, self.__dh_matrix(theta, d, a, alpha))
            self.positions.append([T[0, 3], T[1, 3], T[2, 3] + base_height])

        # La posición del efector final
        x, y, z = T[0, 3], T[1, 3], T[2, 3] + base_height

        return x, y, z
