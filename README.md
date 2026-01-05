# Reflectance of optical multilayer coatings
## How to use
<b>Step 1</b>: Save the python script into a directory of choice.

<b>Step 2</b>: Gather refractive index data of the involved materials. A good source for that is https://refractiveindex.info/

<b>Step 3</b> Save the refractive index data in the directory. This repository contains some random dummy data for the sake of example, to demonstrate the convention. CSV files are used, filenames are named like "n_SiO2.csv". Each row contains a datapoint "wavelenghth (nm); real refractive index;extinction coefficient", using ";" as separators

<code>wl;nr;k
400;1.2;0.1
500;1.3;0.2</code>
...

<b>Step 4</b> Open the python script and define the user inputs
<p align="center"><img  src="https://github.com/LukasMoer/reflectance/blob/main/coatings.png" width=400 align="center"></p>
<b>Step 5</b> Run the script
<p align="center"><img  src="https://github.com/LukasMoer/reflectance/blob/main/reflectance.png" width=400 align="center"></p>
## Theory
Calculation using the <b>transfer matrix method</b> according to

Pedrotti, F. L., Pedrotti, L. S., Bausch, W., & Schmidt, H. (2005). Optik für Ingenieure. In Springer eBooks. https://doi.org/10.1007/b139018 Pages  554-559

For each layer i (substrate and air not included) with refractive index $n_i$ and thickness $d_i$, there is a transfer matrix $M_i$

$$M_i = \left( \begin{array}{rr}
m_{00} & m_{01} \\
m_{10} & m_{11} \\
\end{array}\right) = \left( \begin{array}{rr}
cos \delta_i & j {{sin \delta_i} \over {\gamma_i}} \\
j \gamma_i sin \delta_i & cos \delta_i \\
\end{array}\right)$$

With the respective phase shift $\delta_i$:

$$\delta_i = {{2 \pi}\over{\lambda_0}}n_i d_i cos\theta_i$$

<ul>
<li>refractive index $n_i$, generally dependent on wavelength $n_i=n_i(\lambda_0)$</li>

<li>angle of incidence $\theta_i$ in the respective medium according to Snell's law of refraction. Is not the original angle of incidence $\theta_0$. Measured relative to the perpendicular.</li>
</ul>

And the $\gamma$  -parameter:

$$\gamma_i = {{n_i}\over {c_0}} cos\theta_i$$
<ul><li>c<sub>0</sub> speed of light in vacuum</li></ul>

The matrices of the layers are multiplied to get an overall transfer matrix.
$$M_{ges}=M_1 \cdot M_2 \cdot ... M_N$$

Their elements can be used to calculate the reflection coefficient $\rho$. Finally, the ambient and substrate media are also included here via their $\gamma$ parameters $\gamma_0$ and $\gamma_S$.

$$\rho = {{\gamma_0 m_{00} + \gamma_0\gamma_S m_{01} - m_{10}-\gamma_S m_{11}}\over{\gamma_0 m_{00} + \gamma_0\gamma_S m_{01} + m_{10}+\gamma_S m_{11}}}$$

Finally, we can obtain the reflectance R:

$$R=|\rho|^2$$
