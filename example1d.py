import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator


## 1d example
# camera is at origin and looks right
# objects have position, importance, transparency

## Formulas
# extinction \mu(x) = \alpha_x
# optical_depth \tau(d_i) = \sum_j^i - \ln(1-\alpha_j)
#               = - \ln (\prod_j^i (1 - \alpha_j))
#               = - \ln (T)
# transmittance T = \exp -(\int_0^t \mu(x) dt)   -> gives me wrong result
#               T = \exp (-\tau(d_i))
#               T = \prod_j^i (1 - \alpha_j)
class Object:
    def __init__(self, position, importance, transparency):
        self.position = position
        self.importance = importance
        self.transparency = transparency

def calculate_extinction(objects, domain, detail):
    x = np.linspace(domain[0], domain[1], detail)
    y = np.zeros(shape=detail)
    for element in objects:
        idx = (np.abs(x - element.position)).argmin()
        y[idx] = element.transparency
    return x, y

# maybe use pos mask + ordered alpha values to calculate this instead
def calculate_transmittance(objects, domain, detail):
    x = np.linspace(domain[0], domain[1], detail)
    y = np.ones(shape=detail)
    for element in objects:
        idx = (np.abs(x - element.position)).argmin()
        y[idx] -= element.transparency
    y = np.cumprod(y)
    return x, y

#def calculate_transmittance_optical(optical_depth):
#    transmittance = np.exp(-optical_depth[1])
#    return optical_depth[0], transmittance

#def calculate_transmittance_wrong(extinction):
#    integral = np.cumsum(extinction[1])
#    transmittance = np.exp(-integral)
#    return extinction[0], transmittance

def calculate_optical_depth(objects, domain, detail):
    x = np.linspace(domain[0], domain[1], detail)
    y = np.zeros(shape=detail)
    for element in objects:
        idx = (np.abs(x - element.position)).argmin()
        y[idx] = -np.log(1 - element.transparency)
    y = np.cumsum(y)
    return x, y

def plot_extinction_transmittance_optical_depth(extinction, transmittance, optical_depth):
    fig, axs = plt.subplots(3)
    axs[0].step(extinction[0], extinction[1], where='mid')
    axs[0].set_title("Extinction")
    axs[1].step(transmittance[0], transmittance[1], where='mid')
    axs[1].set_title("Transmittance")
    axs[2].step(optical_depth[0], optical_depth[1], where='mid')
    axs[2].set_title("Optical depth")
    fig.tight_layout()
    plt.show()

# function per fragment
def energy_function_gun17(index, objects, p, q, l, r):
    object_i = objects[index]
    alpha_i = object_i.transparency
    importance_i = object_i.importance

    t1 = p / 2 * (alpha_i - 1) ** 2
    t2 = 0
    for obj in objects[index+1:]: # look at occluded objects
        t2 += (alpha_i * (1 - importance_i) ** l * obj.importance) ** 2
    t2 = t2 * q / 2

    t3 = 0
    for obj in objects[:index]: # look at objects before us
        t3 += (alpha_i * (1 - importance_i) ** l * obj.importance) ** 2
    t3 = t3 * r / 2
        
    energy = t1 + t2 + t3
    return energy

# function per fragment
def energy_function_gun17_array(index, objects, p, q, l, r, detail):
    importance_i = objects[index].importance
    alpha = np.linspace(0, 1, detail)
    t1 = p / 2 * (alpha - 1) ** 2
    t2 = 0
    for obj in objects[index+1:]: # look at occluded objects
        t2 += (alpha * (1 - importance_i) ** l * obj.importance) ** 2
    t2 = t2 * q / 2
    t3 = 0
    for obj in objects[:index]: # look at objects before us
        t3 += (alpha * (1 - importance_i) ** l * obj.importance) ** 2
    t3 = t3 * r / 2
    energy = t1 + t2 + t3
    return alpha, energy

def plot_object_energy(objects, p, q, l, r, detail):
    plots = len(objects)
    fig, axs = plt.subplots(plots)
    for index in range(plots):
        energy = energy_function_gun17_array(index, objects, p, q, l, r, detail)
        min_idx = energy[1].argmin()
        axs[index].plot(energy[0], energy[1])
        axs[index].plot(energy[0][min_idx], energy[1][min_idx], 'ro')
        annotation = r'$\alpha_{min}$ = %.2f' % energy[0][min_idx]
        axs[index].annotate(annotation, (energy[0][min_idx], energy[1][min_idx]), textcoords="offset points", xytext=(0,10), ha='center')
        axs[index].set_title(f"Energy of Object {index} with importance: {objects[index].importance}")
        axs[index].set_xlabel("Transparency")
        axs[index].set_ylabel("Energy")
    fig.tight_layout()
    plt.show()

# maybe work with a position mask for the object -> n-hot vector -> avoid redundant calculation
# position doesnt matter -> order does
DOMAIN = 0, 4
DETAIL = 100
objects = [
    Object(position=1, importance=0.2, transparency=0.5),
    Object(position=2, importance=0.5, transparency=0.5),
    #Object(position=3, importance=0.2, transparency=0.5),
]
extinction = calculate_extinction(objects, DOMAIN, DETAIL)
transmittance = calculate_transmittance(objects, DOMAIN, DETAIL)
optical_depth = calculate_optical_depth(objects, DOMAIN, DETAIL)
#plot_extinction_transmittance_optical_depth(extinction, transmittance, optical_depth)


P = 1
Q = 50
LAMBDA = 3
R = 100
#plot_object_energy(objects, P, Q, LAMBDA, R, DETAIL)


fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# idea make transmitance energy function -> vector field function 
# -> input vector of transparencies
# -> output vector of transmittance * importance
# -> optimization -> find longest arrow in the field

# Make data.
X = np.linspace(0, 1, DETAIL)
Y = np.linspace(0, 1, DETAIL)
X, Y = np.meshgrid(X, Y)

Z = np.zeros(shape=(DETAIL, DETAIL))

i1 = 0.2
i2 = 1
for x in range(DETAIL):
    for y in range(DETAIL):
        Z[y][x] = (1 - X[y][x]) * (1 - Y[y][x])  * i2

min_z = Z.argmin()
min_val = Z.min()
max_val = Z.max()



# Plot the surface.
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)

# Customize the z axis.
#ax.set_zlim(-0.5, 0.5)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()