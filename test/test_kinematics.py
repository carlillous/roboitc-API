import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Función para calcular la matriz de transformación DH
def dh_transform(theta, d, a, alpha):
    return np.array([
        [np.cos(theta), -np.sin(theta) * np.cos(alpha), np.sin(theta) * np.sin(alpha), a * np.cos(theta)],
        [np.sin(theta), np.cos(theta) * np.cos(alpha), -np.cos(theta) * np.sin(alpha), a * np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])

# Parámetros DH dados

DH_params = [
    {'theta': np.radians(0), 'd': 6, 'a': 0, 'alpha': np.radians(90)},  # theta1 es variable
    {'theta': np.radians(0), 'd': 0, 'a': 13, 'alpha': np.radians(180)},  # theta2 es variable
    {'theta': np.radians(180), 'd': 0, 'a': 0, 'alpha': np.radians(180)},  # Junta intermedia fija
    {'theta': np.radians(0), 'd': 0, 'a': 8.5, 'alpha': np.radians(0)},  # theta3 = theta2
]


# Función para calcular todas las matrices de transformación con los valores de theta1, theta2 y theta3
def compute_transformations(theta1, theta2, theta3):
    # Asignar los valores de theta1, theta2 y theta3
    DH_params[0]['theta'] = np.radians(theta1)
    DH_params[1]['theta'] = np.radians(theta2)
    DH_params[3]['theta'] = np.radians(theta3)

    # Calcular las matrices de transformación DH
    T_matrices = [dh_transform(param['theta'], param['d'], param['a'], param['alpha']) for param in DH_params]

    # Multiplicar las matrices para obtener la posición y orientación final
    T = np.eye(4)
    positions = [T[:3, 3]]  # Lista de posiciones para visualización
    for T_i in T_matrices:
        T = np.dot(T, T_i)
        positions.append(T[:3, 3])

    return np.array(positions)

# Valores de ejemplo para theta1, theta2 y theta3
theta1 = 90 # en grados
theta2 = 90 # en grados
theta3 = 90 # en grados

# Calcular las posiciones
positions = compute_transformations(theta1, theta2, theta3)

# Ajustar la posición inicial debido a la base del coche
base_height = 7  # altura de la base del coche en cm
positions[:, 2] += base_height
print(positions)

# Visualizar el brazo robótico
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'bo-',linewidth=5)
ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='b')

x = np.linspace(-10.5, 10.5, 100)
z = np.linspace(0, 8.5, 100)
x, z = np.meshgrid(x, z)
y = np.full_like(x, 2)  # El valor constante de y
ax.plot_surface(x, y, z, alpha=0.5, color='red')


x = np.linspace(-10.5, 10.5, 100)
z = np.linspace(8.5, 12.5, 100)
x, z = np.meshgrid(x, z)
y = np.full_like(x, -10)  # El valor constante de y
ax.plot_surface(x, y, z, alpha=0.5, color='red')

x = np.linspace(-10.5, 10.5, 100)
y = np.linspace(2, -10, 100)
x, y = np.meshgrid(x, y)
z = np.full_like(x, 8.5)
ax.plot_surface(x, y, z, alpha=0.5, color='red')

x = np.linspace(-10.5, 10.5, 100)
y = np.linspace(-10, -21, 100)
x, y = np.meshgrid(x, y)
z = np.full_like(x, 12.5)
ax.plot_surface(x, y, z, alpha=0.5, color='red')
ax.set_xlabel('X (cm)')
ax.set_zlabel('Z (cm)')
ax.set_xlim([-30, 30])
ax.set_ylim([-30, 30])
ax.set_ylabel('Y (cm)')
ax.set_zlim([0, 30])



plt.title('Visualización del Brazo Robótico')
plt.show()
