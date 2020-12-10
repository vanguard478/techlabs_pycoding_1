Background Information:

In order to gain information about the impact of the reaction temperature and gas mixture on
the performance of the Solid Oxide Electrolysis Cell (SOEC), I/V measurements were conducted. The obtained data can be
used to determine the open circuit voltage (OCV) and the area specific resistance (ASR). The
latter is equal to the slope of the I/V curve at a desired current density. In this work, the ASR
was calculated for 0.1 A cm-2. Furthermore, the current density I_{1.4 V} at our chosen maximum of
1.4 V can be obtained, which gives insight into the performance of the cell. This maximum
voltage was chosen, in order to keep degradation and aging effects which might occur at higher
voltages, as low as possible.

Data:
- The high temeperature electrolysis was conducted in two different gas mixtures. The  first mixture contains 80% CO2 and 20% CO.
The second mixture contains 50% CO2 and 50% CO. 

- The current density at given potential were measured for both mixtures in a temperature range
between 700 and 900 °C

- The area of the cell is: 0.785 cm^2

Your Task:
- Calculate the current density: current density= current/cell_area
- Plot the IV curves for each mixture as shown in the example picture: y_axis: potential, x_axis: Current density
 -> plot the I/V curves of 50-50 CO2-CO in a separate plot then the 11 I/V curves of 80-20 CO2-CO 
 (so you should have 2 plots, one for 50-50 and the second for 80-20)
- Determine the Open Circuit Voltage (OCV): this is the potential, where the current is 0 (where the IV curve intersects with the y-axis )
- Determine the Area Specific Resistance (ARS): Calculate the slopes at 100mA
- determine the current density at 1.4 V
- write all values in a results txt (or csv) file (for this part: check if a resulst.txt file exists. if not, then create one)
your results file should have following columns:

CO2/%	CO/%	T/°C	OCV/V	ASR/ohm cm^2	J_1.4V/A cm^2



