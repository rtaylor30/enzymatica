#from enzymatica import *
import numpy as np
from itertools import takewhile

def write_test_data(filename,sigma,calib,initial_conditions,time,k,phi):
    """Generates a test data set from specified arguments"""
    #@Rob Work below can now (in principle), be accomplished by...
    turbiditysetup = TurbiditySetup('test data!',calib,sigma,initial_conditions,time)
    sim = Simulation(turbiditysetup,k,phi)
    Rho_exact = sim.turbidity_time_series()
    #rate_fun = partial(mm_rate,k)
    #Z = [reaction_time_series(rate_fun, z0, time) for z0 in Z0]
    #Rho_exact = [turbidity_from(z,partial(basic_susceptibility,phi,z[0,:]),calib) for z in Z]
    
    Rho_data = [rho+sigma*np.random.randn(*rho.shape) for rho in Rho_exact]
    with open(filename,'w') as f:
        f.write('>Test data generated assuming MM reaction\n')
        f.write('k_exact = '+str(k)+'\n phi_exact = ' + str(phi) + '\n\n')
        f.write('>Turbidity error (std)\n')
        f.write(str(sigma)+'\n\n')
        f.write('>Turbidity Calibration\n')
        f.write(str(calib[0])+' '+str(calib[1])+'\n\n') 
        f.write('>Initial Conditions (substrate concentration,enzyme concentration)\n')
        f.write(' '.join(str(s0) for s0 in S0)+'\n')
        f.write(' '.join(str(e0) for e0 in E0)+'\n\n')
        f.write('>Time series\n')
        for row in zip(time,*Rho_data):
            f.write(' '.join(str(x) for x in row)+'\n')
    print 'Test written to: '+filename

#sampling times, turbidity calibration and turbidity measurement error
N_max = 1000
T_end = 30
t_interval = .1
time = [t_interval*n for n in takewhile(lambda k: t_interval*k < T_end, range(N_max))]
calibration = (1.0,0.1)
sigma = .002

#initial conditions                                                                                               
S0 = [1.0, 1.0, 1.0, 1.0, 1.0]
E0 = [0.5, 1.0, 2.0, 4.0, 8.0]
Z0 = [[s0, e0, 0.0, 0.0] for s0,e0 in zip(S0,E0)]

#reaction rate constants and turbidity shape parameters
K = [(1.0,1.1,.2),(.5,2.1,.5)]
Phi = [(2,2),(5,1),(1,5)]
indexed_params = [((i+1)*(j+1),k,phi) for i,k in zip(range(len(K)),K) for j,phi in zip(range(len(Phi)),Phi)]
for index,k,phi in indexed_params:
    write_test_data('test_data'+str(index)+'.data',sigma,calibration,Z0,time,k,phi)
