#!/usr/bin/env python3


import igraph
import matplotlib.pyplot as plt
import numpy as np
import argparse as arg
import powerlaw as pl
import lmfit as lmf


fig, subplot = plt.subplots(ncols=1, nrows=1)

argparser = arg.ArgumentParser(description='')
argparser.add_argument('file', help='graph file')

args = argparser.parse_args()

g = igraph.read(args.file)

degrees = g.indegree()


fit = pl.Fit(degrees, discrete=True)
KMIN = fit.find_xmin()

degrees = KMIN+degrees
num_vertices = len(degrees)
max_degree = np.max(degrees)

#################################################################
#        Logaritmic binning
#################################################################

# Extension de los histogramas a todos los grados entre 0 y max_degree
all_degrees = np.arange(0, max_degree+1)
all_degrees_hist = np.zeros_like(all_degrees, dtype=float)


nbins = None           # Numero de bins pasado por argumentos
if nbins is None:                  # si no
    nbins = np.sqrt(max_degree)             # tomar nbins = sqrt(kmax)

# creamos una escala logaritmica para los bins
log_bins = np.unique(np.ceil(np.logspace(0, np.log10(max_degree), nbins)))


hist, bins = np.histogram(degrees, bins=log_bins, density=True)
centers = .5*(bins[:-1]+bins[1:])
centers = centers[hist > 0]
hist = hist[hist > 0]

print(hist)
print(centers)

keff = centers
subplot.plot(keff, hist, 'ko-')

model = lmf.models.PowerLawModel()
params = model.guess(hist, x=keff)
model.set_param_hint('exponent',value=-0.01/16.)
result = model.fit(hist, params, x=keff)
print(result.fit_report())

kmin, kmax = (np.min(keff), np.max(keff))
print(keff)
print(kmin, kmax)
k = np.linspace(kmin,kmax,100)
fit = result.params['amplitude']*np.power(k, (0.001 - 0.06)/(106.2-9.8))  # result.params['exponent'])
fit = result.best_fit

#subplot.plot(keff,fit,'--')

# subplot.plot(centers, res.alpha*centers )

# subplot.plot(log_bin_centers, log_hist, 'o', label='data')
# sns.distplot(grados, kde=False, ax=subplot, norm_hist=True, bins=bins)

print('k_sat',KMIN)


subplot.set_xlabel('$k+k_{sat}$')
subplot.set_ylabel("$p(k)=(k+k_{sat})^{-\\alpha}$")

subplot.grid(b=True)
subplot.set_xscale('log')
subplot.set_yscale('log')


filename = args.file.split('/')[-1]
plt.savefig('degree_distribution.png')
plt.show()
