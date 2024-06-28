import requests
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import kinematics


def plot_robot_arm():
    url = "http://192.168.100.34:80/servo/angles"  # URL del endpoint
    response = requests.get(url)  # Realizar la solicitud GET

    if response.status_code == 200:  # Verificar si la solicitud fue exitosa
        data = response.json()  # Obtener los datos en formato JSON
        angles = data['angles']  # Extraer la lista de ángulos
    else:
        st.error(f"Error al obtener los ángulos del servo: {response.status_code}")
        return None

    print(angles)
    movement = kinematics.DirectKinematics()
    movement.calculate_position(angles[1:4])
    positions = movement.get_positions()

    positions = np.array(positions)
    print(positions)
    # Visualizar el brazo robótico
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = np.linspace(-12, 12, 100)
    z = np.linspace(0, 8.5, 100)
    x, z = np.meshgrid(x, z)
    y = np.full_like(x, 4)  # El valor constante de y
    ax.plot_surface(x, y, z, alpha=0.25, color='grey')

    x = np.linspace(-4, 4, 100)
    z = np.linspace(8.5, 12.5, 100)
    x, z = np.meshgrid(x, z)
    y = np.full_like(x, -10)  # El valor constante de y
    ax.plot_surface(x, y, z, alpha=0.25, color='grey')

    x = np.linspace(-12, 12, 100)
    y = np.linspace(4, -10, 100)
    x, y = np.meshgrid(x, y)
    z = np.full_like(x, 8.5)
    ax.plot_surface(x, y, z, alpha=0.25, color='grey')

    x = np.linspace(-4, 4, 100)
    y = np.linspace(-10, -21, 100)
    x, y = np.meshgrid(x, y)
    z = np.full_like(x, 12.5)
    ax.plot_surface(x, y, z, alpha=0.25, color='grey')

    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], 'bo-', linewidth=3)
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='yellow')

    for i, (x, y, z) in enumerate(positions):
        ax.text(x, y, z, f'({x:.1f}, {y:.1f}, {z:.1f})', color='red',size=7)

    ax.set_xlabel('X (cm)')
    ax.set_zlabel('Z (cm)')
    ax.set_xlim([-30, 30])
    ax.set_ylim([-20, 40])
    ax.set_ylabel('Y (cm)')
    ax.set_zlim([0, 30])

    plt.title('Visualización del Brazo Robótico')

    st.pyplot(fig)


def main():
    st.title('Visualizador del Brazo Robótico')
    st.text('Presiona el botón para visualizar el brazo robótico')

    if st.button('Mostrar Brazo'):
        plot_robot_arm()


if __name__ == '__main__':
    main()
