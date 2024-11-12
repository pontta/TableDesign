from flask import Flask, request, render_template
from scipy.optimize import fsolve
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

def equations(vars, A, B):
    x, y = vars
    a = 3
    eq1 = x/y - (B - y)/(A - x)
    eq2 = (2*a)**2 - (x**2 + y**2)

    return [eq1, eq2]

def intersection_lines(vars, Ax, Ay, k, Bx, By, l):
    x, y = vars
    eq1 = y - Ay - k * (x - Ax)
    eq2 = y - By - l * (x - Bx)
    
    return [eq1, eq2]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        A = float(request.form['A'])
        B = float(request.form['B'])
        initial_guess = [1, 1]
        solution1 = fsolve(lambda vars: equations(vars, A, B), initial_guess)
        x_sol = solution1[0]
        y_sol = solution1[1]
        k = np.divide(x_sol,y_sol)

        # Calculate angle alpha in degrees
        alpha = np.arctan2(x_sol, y_sol) * (180 / np.pi)  # Convert radians to degrees
    
        # Find intersection point of diagonal and x-axis (y=0)
        initial_guess = [-3,0]
        solution2 = fsolve(lambda vars: intersection_lines(vars, x_sol/2, y_sol/2, k, 0, 0, 0), initial_guess) 
        x1_sol = solution2[0]
        y1_sol = solution2[1]

        # Plot the rectangle and the points
        fig, ax = plt.subplots()
        ax.plot([0, A, A, 0, 0], [0, 0, B, B, 0], '-k')  # Rectangle
        ax.plot([x1_sol, A-x1_sol], [y1_sol, B-y1_sol], '-k', linewidth=1)  # Diagonal segment
        ax.plot([0,x_sol],[y_sol,0], ':k')

        ax.plot(x_sol/2, y_sol/2, 'ob')  # Intersection point
        ax.plot(A/2, B/2, 'or')  # Center point
        ax.plot(0, y_sol, 'ok')
        ax.plot(x_sol, 0, 'ok')

        # Annotate points
        ax.text(x_sol/2 + 0.5, y_sol/2 + 0.5, f'({x_sol/2:.2f}, {y_sol/2:.2f})', fontsize=12)
        ax.text(A/2 + 0.5, B/2 + 0.5, f'({A/2:.2f}, {B/2:.2f})', fontsize=12)
        
        ax.set_aspect('equal')
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Rectangle and Intersection Point')
        
        # Save plot to a string in base64 format
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        
        return render_template('index.html', x1 = x1_sol, y1 = y1_sol, x=x_sol, y=y_sol, alpha=alpha, A=A, B=B, plot_url=plot_url)
    return render_template('index.html', x=None, y=None, alpha=None)

if __name__ == '__main__':
    app.run(debug=False)
