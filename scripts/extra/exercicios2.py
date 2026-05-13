from math import pi, sqrt

u0 = 12.5664e-7
e0 = 8.8542e-12

f = 5e6

eR = 2
sigma = 2e-3
u = u0
e = e0 * eR

alpha = 2*pi*f * sqrt((e*u/2)*(sqrt(1+(sigma/(2*pi*f*e))**2)-1))
print(f'alpha = {alpha:.2f} Np/m')
beta = 2*pi*f * sqrt((e*u/2)*(sqrt(1+(sigma/(2*pi*f*e))**2)+1))
print(f'beta = {beta:.2f} rad/m')