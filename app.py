from flask import Flask, request, render_template
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.json
        mass = float(data['mass'])
        
        # Calculate trajectory based on mass
        trajectory = calculate_trajectory(mass)

        return json.dumps({'trajectory': trajectory})
    except Exception as e:
        return json.dumps({'error': str(e)})

def calculate_trajectory(mass, distance=1e9, light_path_length=2e9):
    """
    Calculate the trajectory of light near a massive object.
    
    :param mass: Mass of the object in kilograms.
    :param distance: Closest approach of light to the object in meters. Default is 1 billion meters.
    :param light_path_length: Total length of the light path to visualize in meters. Default is 2 billion meters.
    :return: A list of points representing the light path.
    """
    G = 6.67430e-11  # Gravitational constant in m^3 kg^-1 s^-2
    c = 2.99792458e8  # Speed of light in m/s

    # Calculate deflection angle (in radians)
    alpha = (4 * G * mass) / (c**2 * distance)

    # Assuming a straight line path initially and then bending at the point of closest approach
    # Dividing the path into two segments: before and after the closest approach
    half_path_length = light_path_length / 2
    num_points = 100  # Number of points to calculate for the path
    trajectory = []

    for i in range(num_points):
        if i < num_points / 2:
            # Before closest approach - straight line
            x = i * (half_path_length / num_points)
            y = 0
        else:
            # After closest approach - apply deflection
            x = i * (half_path_length / num_points)
            # Simple linear approximation of deflection for visualization
            y = (x - half_path_length) * alpha

        trajectory.append((x, y))

    return trajectory

if __name__ == '__main__':
    app.run(debug=True)
