# -*- coding: utf-8 -*-
# (c) 2015 MIT License Ethan Nelson
# * This code generates plots for the radar lab viewer at https://github.com/ethan-nelson/radarlabviewer/.
# * Two functions are defined to help with consistent plotting, then data are loaded and sent to plotting.
# * Note that the images directory structure should be created and the data files downloaded prior
#   to running this (see repo for scripts).
import matplotlib as mpl
import matplotlib.pyplot as plt
import netCDF4 as n
import numpy as np
import quickbeam


def plot_cross_section(x, y, data, crange, prange, cmap, title, figname, plot=None):
    """
    Plot a cross section of data, either along a lat, lon, or height.
    In addition, the data may be artifically degraded to simulate a
    sensor with lower resolution. 

    Inputs:
    x - x coordinate
    y - y coordinate
    data - data to plot
    crange - range of colormap to use
    prange - range of values to actually plot
    cmap - colormap
    title - title to print
    figname - figure file name
    plot - type of plot
    """
    if plot not in ['lat','lon','hgt']:
        raise Exception('Must specify whether this plot is across longitude (lon), latitude (lat), or height (hgt)')

    if plot == 'hgt':
        plt.figure(figsize=(10,7))
        xtitle = 'Longitude'
        ytitle = 'Latitude'
        xlims = [np.nanmin(x),np.nanmax(x)]
        ylims = [np.nanmin(y),np.nanmax(y)]
    else:
        plt.figure(figsize=(14,7))
        if plot == 'lon':
            xtitle = 'Latitude'
            xlims = [35,45]
        else:
            xtitle = 'Longitude'
            xlims = [-100,-80]
        ytitle = 'Height'
        ylims = [0,20]

    # We mask or saturate data outside our range (important for different MDRs)
    temp = np.copy(data)
    temp[temp < crange[0]] = np.nan
    temp[temp > crange[1]] = crange[1]
    plt.pcolormesh(x, y, temp, vmin=prange[0], vmax=prange[1], cmap=cmap)
    plt.title(title, fontsize=20)
    plt.xlim(xlims)
    plt.ylim(ylims)
    plt.xlabel(xtitle, fontsize=18)
    plt.ylabel(ytitle, fontsize=18)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    # Save png version for web
    plt.tight_layout()
    plt.savefig('images/' + figname + '.png')
    plt.close()
    #if GENERATE_PUBLICATION_QUALITY == True:
    #    if 'tif' in fig.canvas.get_supported_filetypes():
    #        plt.savefig('figures/' + figname + '.tiff', format='tif', dpi=300)
    #    elif 'eps' in fig.canvas.get_supported_filetypes():
    #        plt.savefig('figures/' + figname + '.eps', format='eps', dpi=300)


def plot_colorbar(colormap, vmin, vmax, pmin, label, figname, log=False, big=False):
    """
    Plot a colorbar separately. Data may be degraded, so
    the plot takes into consideration the range of values
    to label as well as the range of values to color.

    Inputs
    colormap - colormap object
    vmin - minimum value to color
    vmax - maximum value to color
    pmin - minimum value to plot
    label - label to print on plot
    figname - filename
    log - boolean for whether to plot on log scale
    big - boolean for whether to magnify text
    """
    if vmin == pmin:
        plot_cmap = plt.get_cmap(colormap)
    else:
        if colormap == 'rainbow':
            cbcall = mpl.cm.rainbow
        elif colormap == 'jet':
            cbcall = mpl.cm.jet
        else:
            raise Exception('Given colormap does not match a defined call function in plot_colorbar')
        cmap_start = int(float(vmin-pmin) / float(vmax-pmin) * 256)
        lower_cmap = np.ones([cmap_start, 4])
        upper_cmap = cbcall(range(cmap_start, 256))
        combined_cmap = np.vstack((lower_cmap, upper_cmap))
        plot_cmap = mpl.colors.ListedColormap(combined_cmap, '', 256)

    fig=plt.figure(figsize=(2,8))
    ax = fig.add_axes([0.05, 0.025, 0.3, 0.95])
    norm = mpl.colors.Normalize(vmin=pmin, vmax=vmax)
    if log == True:
        cb = mpl.colorbar.ColorbarBase(ax, cmap=plot_cmap, norm=norm, orientation='vertical', ticks=range(-2,3))
        cb.ax.set_yticklabels(['10$^{-2}\!$', '10$^{-1}\!$', '10$^{0}\!$', '10$^{1}\!$', '10$^{2}\!$'])
    else:
        cb = mpl.colorbar.ColorbarBase(ax, cmap=plot_cmap, norm=norm, orientation='vertical')
    if big == True:
        labelsize=30
        ticksize=26
    else:
        labelsize=18
        ticksize=14
    cb.set_label(label, fontsize=labelsize)
    cb.ax.tick_params(labelsize=ticksize)
    plt.savefig('images/%s.png' % figname, transparent=True)
    plt.close()


# Define arrays and dictionaries of information as well as file names
basedir = 'data/quickbeam_%s-MLAT-a-A-2009-04-10-030000-g2.h5'
frequencies = ['S','Ku','Ka','W']
frequency_values = {'Ku': '13','Ka': '35','W': '94','S': '3'}
reflectivities = ['Z_cor','Z_eff']

range_current = {'Ku': [18, 50], 'Ka': [12, 50], 'W': [-30, 50], 'S': [0, 50]}
range_future = {'Ku': [0, 50], 'Ka': [0, 50], 'W': [-30, 50], 'S': [0, 50]}
range_ref = [-30, 50]
range_model = {'ice': [1E-4, 2], 'liquid': [1E-4, 2], 'tempk': [28, 90], 'pcprate': [0.01, 100]}
model_title = {'ice': 'Ice Water Content', 'liquid': 'Liquid Water Content', 'tempk': 'Temperature', 'pcprate': 'Rainfall'}
model_title_cb = {'ice': 'Ice Water Content [g/kg]', 'liquid': 'Liquid Water Content [g/kg]', 'tempk': 'Temperature [F]', 'pcprate': 'Rainfall [mm/hr]'}

lon_sections = [229, 302, 361, 434, 507, 580]
lon_sections = range(220,580)
lon_sections = [329, 363, 406, 469, 522, 567]

lat_sections = [313, 346, 395, 461, 524, 562]
lat_sections = range(300,580)
lat_sections = [313, 330, 414, 464, 536, 579]

hgt_sections = [1.5, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12]

model_read_variables = ['pcprate','rain','cloud','snow','hail','aggregates','graupel','pristine','ue','ve','lon','lat','z_coords','tempk','topo']
model_variables = ['pcprate','lat','lon','ue','ve','z_coords','tempk','topo']
model_plot_variables = ['liquid','ice']

# Read in model data
model_file = 'data/MLAT-a-A-2009-04-10-030000-g2.h5'
model_file = n.Dataset(model_file, 'r')
model_read_data = {variable: np.squeeze(model_file[variable][:]) for variable in model_read_variables}
model_data = {variable: model_read_data[variable] for variable in model_variables}
model_data['ice'] = np.nansum([model_read_data[variable] for variable in ['snow','hail','aggregates','graupel','pristine']], axis=0)
model_data['liquid'] = np.nansum([model_read_data[variable] for variable in ['rain','cloud']], axis=0)
model_data['heights'] = np.zeros(np.shape(model_data['ice']))
for i in range(np.shape(model_data['heights'])[0]):
    model_data['heights'][i,:,:] = model_data['topo'] + model_data['z_coords'][i]
model_data['heights'] /= 1000.0
temp = np.zeros(np.shape(model_data['ice']))
for i in range(np.shape(model_data['heights'])[0]):
    temp[i,:,:] = model_data['lat']
model_data['lat'] = temp
temp = np.zeros(np.shape(model_data['ice']))
for i in range(np.shape(model_data['heights'])[0]):
    temp[i,:,:] = model_data['lon']
model_data['lon'] = temp
model_data['tempk'] = (model_data['tempk'] - 273.15) * 1.8 + 32.0

cmap = plt.get_cmap('jet')
cmap.set_under('w')

# Plot radar cross sections for each frequency
for ifreq,frequency in enumerate(frequencies):
    reftitle = '%s %s GHz Reflectivity' % (frequency, frequency_values[frequency])
    refctitle = 'Reflectivity [dBZ]'
    radar_data = quickbeam.read(basedir % frequency.lower(), 'Z_cor', 'Z_eff', 'lon', 'lat', 'hgt')

    for iref,ref in enumerate(reflectivities):
        for isec,section in enumerate(lon_sections):
            plot_cross_section(model_data['lat'][:,:,section], model_data['heights'][:,:,section], radar_data[ref][:,:,section], range_current[frequency], range_ref, cmap, reftitle, 'h/lon/%i/%i-%i' % (isec,ifreq+1,iref), 'lon')
            plot_cross_section(model_data['lat'][:,:,section], model_data['heights'][:,:,section], radar_data[ref][:,:,section], range_future[frequency], range_ref, cmap, reftitle, 'l/lon/%i/%i-%i' % (isec,ifreq+1,iref),  'lon')

        for isec,section in enumerate(lat_sections):
            plot_cross_section(model_data['lon'][:,section,:], model_data['heights'][:,section,:], radar_data[ref][:,section,:], range_current[frequency], range_ref, cmap, reftitle, 'h/lat/%i/%i-%i' % (isec,ifreq+1,iref), 'lat')
            plot_cross_section(model_data['lon'][:,section,:], model_data['heights'][:,section,:], radar_data[ref][:,section,:], range_future[frequency], range_ref, cmap, reftitle, 'l/lat/%i/%i-%i' % (isec,ifreq+1,iref), 'lat')

        for isec,section in enumerate(hgt_sections):
            shapes = np.shape(radar_data['lon'])
            temp = np.zeros(shapes)
            # We find nearest point to a given geometric height level
            for i in range(shapes[0]):
                for j in range(shapes[1]):
                    lev = np.argmin([np.abs(section - x) for x in model_data['heights'][:,i,j]])
                    temp[i,j] = radar_data[ref][lev,i,j]
            plot_cross_section(radar_data['lon'], radar_data['lat'], temp, range_current[frequency], range_ref, cmap, reftitle, 'h/vert/%i/%i-%i' % (isec,ifreq+1,iref), 'hgt')
            plot_cross_section(radar_data['lon'], radar_data['lat'], temp, range_future[frequency], range_ref, cmap, reftitle, 'l/vert/%i/%i-%i' % (isec,ifreq+1,iref), 'hgt')

    plot_colorbar('jet', range_current[frequency][0], range_current[frequency][1], -30, 'Reflectivity [dBZ]', 'h/leg/%i' % (ifreq+1), big=True)
    plot_colorbar('jet', range_future[frequency][0], range_future[frequency][1], -30, 'Reflectivity [dBZ]', 'l/leg/%i' % (ifreq+1), big=True)

# Plot model cross sections
for variable in model_plot_variables:
    for isec,section in enumerate(lon_sections):
        plot_cross_section(model_data['lat'][:,:,section], model_data['heights'][:,:,section], model_data[variable][:,:,section], range_model[variable], range_model[variable], cmap, model_title[variable], 'lon/%i/%s' % (isec, variable), 'lon')

    for isec,section in enumerate(lat_sections):
        plot_cross_section(model_data['lon'][:,section,:], model_data['heights'][:,section,:], model_data[variable][:,section,:], range_model[variable], range_model[variable], cmap, model_title[variable], 'lat/%i/%s' % (isec, variable), 'lat')

    for isec,section in enumerate(hgt_sections):
        shapes = np.shape(radar_data['lon'])
        temp = np.zeros(shapes)
        # We find nearest point to a given geometric height level
        for i in range(shapes[0]):
            for j in range(shapes[1]):
                lev = np.argmin([np.abs(section - x) for x in model_data['heights'][:,i,j]])
                temp[i,j] = model_data[variable][lev,i,j]
        plot_cross_section(model_data['lon'][0,:,:], model_data['lat'][0,:,:], temp, range_model[variable], range_model[variable], cmap, model_title[variable], 'vert/%i/%s' % (isec, variable), 'hgt')

    plot_colorbar('jet', range_model[variable][0], range_model[variable][1], range_model[variable][0], model_title_cb[variable], 'leg/%s' % variable, big=True)

# Write out orbits for map
f = open('coords.js', 'w')
f.write('var lonarray = [\n')
for isec,section in enumerate(lon_sections):
    f.write('[\n')
    points_in = [(y,x) for x,y in zip(model_data['lon'][0,:,section], model_data['lat'][0,:,section]) if y >= 35.0 and y <= 45.0]
    for points in points_in[::50]:
        f.write('    [ %2.2E , %2.2E ],\n' % points)
    f.write(']')
    f.write(',\n') if isec != len(lat_sections)-1 else f.write('\n')
f.write('];\nvar latarray = [\n')
for isec,section in enumerate(lat_sections):
    f.write('[\n')
    points_in = [(y,x) for x,y in zip(model_data['lon'][0,section,:], model_data['lat'][0,section,:]) if x >= -100.0 and x <= -80.0]
    for points in points_in[::50]:
        f.write('    [ %2.2E, %2.2E ],\n' % points)
    f.write(']')
    f.write(',\n') if isec != len(lat_sections)-1 else f.write('\n')
f.write('];')
f.close()

# Plot maps with their colorbars
# Note these *must* take up the _whole_ file space to project them better onto the slippy map
mapxlim = [np.nanmin(model_data['lon'][0,:,:]), np.nanmax(model_data['lon'][0,:,:])]
mapylim = [np.nanmin(model_data['lat'][0,:,:]), np.nanmax(model_data['lat'][0,:,:])]
fig = plt.figure()
ax = plt.axes([0,0,1,1])
plt.quiver(model_data['lon'][0,::50,::50], model_data['lat'][0,::50,::50], model_data['ue'][0,::50,::50], model_data['ve'][0,::50,::50])
plt.xlim(mapxlim)
plt.ylim(mapylim)
plt.gca().get_xaxis().set_visible(False)
plt.gca().get_yaxis().set_visible(False)
plt.gca().axis('off')
plt.savefig('images/swind.png', transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

fig = plt.figure()
ax = plt.axes([0,0,1,1])
plt.pcolor(model_data['lon'][0,:,:], model_data['lat'][0,:,:], model_data['tempk'][0,:,:], vmin=28, vmax=90)
plt.xlim(mapxlim)
plt.ylim(mapylim)
plt.gca().get_xaxis().set_visible(False)
plt.gca().get_yaxis().set_visible(False)
plt.gca().axis('off')
plt.savefig('images/stemp.png', transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

plot_colorbar('jet', 28, 90, 28, 'Temperature [F]', 'tlegend', big=True)

cmap = plt.get_cmap('winter')
cmap.set_under('w', alpha=0.0)

fig = plt.figure()
ax = plt.axes([0,0,1,1])
plt.pcolor(model_data['lon'][0,:,:], model_data['lat'][0,:,:], np.log10(model_data['pcprate']), vmin=-2, vmax=2, cmap=cmap)
plt.xlim(mapxlim)
plt.ylim(mapylim)
plt.gca().get_xaxis().set_visible(False)
plt.gca().get_yaxis().set_visible(False)
plt.gca().axis('off')
plt.savefig('images/rr.png', transparent=True, bbox_inches='tight', pad_inches=0)
plt.close()

plot_colorbar('winter', -2, 2, -2, 'Rain Rate [mm/hr]', 'rlegend', log=True, big=True)
