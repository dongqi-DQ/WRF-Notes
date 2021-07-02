#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 11:46:50 2020
Visulise WPS domains using metgrid
@author: dli84
"""
import numpy as np
import xarray as xr
import os
import matplotlib.pylab as plt
import netCDF4 as nc
from copy import copy
import cartopy.crs as ccrs
from cartopy.feature import NaturalEarthFeature
from cartopy.mpl.gridliner import LATITUDE_FORMATTER, LONGITUDE_FORMATTER
import cartopy.feature as cfeature
import cartopy.io.img_tiles as cimgt
import wrf
import matplotlib as mpl
import shapely.geometry as sgeom
wps_dir = '/home/dli84/Documents/WRF/metgrid_mask/'

def find_side(ls, side):
    """
    Given a shapely LineString which is assumed to be rectangular, return the
    line corresponding to a given side of the rectangle.
    
    """
    minx, miny, maxx, maxy = ls.bounds
    points = {'left': [(minx, miny), (minx, maxy)],
              'right': [(maxx, miny), (maxx, maxy)],
              'bottom': [(minx, miny), (maxx, miny)],
              'top': [(minx, maxy), (maxx, maxy)],}
    return sgeom.LineString(points[side])

def lambert_xticks(ax, ticks):
    """Draw ticks on the bottom x-axis of a Lambert Conformal projection."""
    te = lambda xy: xy[0]
    lc = lambda t, n, b: np.vstack((np.zeros(n) + t, np.linspace(b[2], b[3], n))).T
    xticks, xticklabels = _lambert_ticks(ax, ticks, 'bottom', lc, te)
    ax.xaxis.tick_bottom()
    ax.set_xticks(xticks)
    for idx, lon in enumerate(ticks):
        if lon >180:
            ticks[idx] = lon-360
    
    xticks, xticklabels = _lambert_ticks(ax, ticks, 'bottom', lc, te)
    ax.set_xticklabels([ax.xaxis.get_major_formatter()(xtick) for xtick in xticklabels])
    

def lambert_yticks(ax, ticks):
    """Draw ricks on the left y-axis of a Lamber Conformal projection."""
    te = lambda xy: xy[1]
    lc = lambda t, n, b: np.vstack((np.linspace(b[0], b[1], n), np.zeros(n) + t)).T
    yticks, yticklabels = _lambert_ticks(ax, ticks, 'left', lc, te)
    ax.yaxis.tick_left()
    ax.set_yticks(yticks)
    ax.set_yticklabels([ax.yaxis.get_major_formatter()(ytick) for ytick in yticklabels])

def _lambert_ticks(ax, ticks, tick_location, line_constructor, tick_extractor):
    """Get the tick locations and labels for an axis of a Lambert Conformal projection."""
    outline_patch = sgeom.LineString(ax.outline_patch.get_path().vertices.tolist())
    axis = find_side(outline_patch, tick_location)
    n_steps = 30
    extent = ax.get_extent(ccrs.PlateCarree())
    _ticks = []
    for t in ticks:
        xy = line_constructor(t, n_steps, extent)
        proj_xyz = ax.projection.transform_points(ccrs.Geodetic(), xy[:, 0], xy[:, 1])
        xyt = proj_xyz[..., :2]
        ls = sgeom.LineString(xyt.tolist())
        locs = axis.intersection(ls)
        if not locs:
            tick = [None]
        else:
            tick = tick_extractor(locs.xy)
        _ticks.append(tick[0])
    # Remove ticks that aren't visible:    
    ticklabels = copy(ticks)
    while True:
        try:
            index = _ticks.index(None)
        except ValueError:
            break
        _ticks.pop(index)
        ticklabels.pop(index)
    return _ticks, ticklabels


def get_plot_element(infile):
    with nc.Dataset(infile, 'r') as rootgroup:
        p = wrf.getvar(rootgroup, 'HGT_M')
        lats, lons = wrf.latlon_coords(p)
        cart_proj = wrf.get_cartopy(p)
        xlim = wrf.cartopy_xlim(p)
        ylim = wrf.cartopy_ylim(p)
        # xlim, ylim = bm(wrf.to_np(lons), wrf.to_np(lats))
    return cart_proj, (xlim, ylim)

ds = xr.open_dataset(wps_dir+'/met_em.d01.2019-07-28_2100.nc')


met_dict = {}    
for fname in sorted(os.listdir(wps_dir)):    
    if fname.find('met_em.d0')!=-1:
        idx = fname.find('d0')     
        # met_dict[fname[idx:idx+3]] = read_metgrid(wps_dir+fname)
        cart_proj, met_dict[fname[idx:idx+3]] = get_plot_element(fname)
    if fname.find('d01')!=-1:
        with nc.Dataset(fname, 'r') as wrf_d01:
            land = wrf.getvar(wrf_d01, 'LANDMASK')
            lats, lons = wrf.latlon_coords(land) 
            
fig = plt.figure(figsize=(10,8))


# stamen_terrain = cimgt.Stamen('terrain-background')
ax = plt.axes(projection=cart_proj)
# ax.stock_img()

# states = NaturalEarthFeature(category='cultural', scale='10m', facecolor='coral',
#                               name='admin_1_states_provinces_lines')
ax.coastlines('10m', linewidth=0.8)
# ax.add_feature(states, edgecolor='gray')
ax.add_feature(cfeature.LAND.with_scale('10m'), linewidth=0.5,facecolor='green')#'coral')
ax.add_feature(cfeature.OCEAN.with_scale('10m'),facecolor='deepskyblue')#'aqua')
# ax.add_image(stamen_terrain, 8,transform=ccrs.PlateCarree())


for name, (xlim, ylim) in met_dict.items():
    if name=='d02':
        ax.set_xlim([xlim[0]-(xlim[1]-xlim[0])/15, xlim[1]+(xlim[1]-xlim[0])/15])
        ax.set_ylim([ylim[0]-(ylim[1]-ylim[0])/15, ylim[1]+(ylim[1]-ylim[0])/15])
     
    ax.add_patch(mpl.patches.Rectangle((xlim[0], ylim[0]), xlim[1]-xlim[0], ylim[1]-ylim[0],
                  fill=None, lw=3, edgecolor='red', zorder=10))
    # ax.text(xlim[0]+(xlim[1]-xlim[0])*0.05, ylim[0]+(ylim[1]-ylim[0])*0.9, name,
    #         size=15, color='blue', zorder=10)

fig.canvas.draw()

xticks = [169,171,172,173,174,175]#[150, 160,  170,  180, 190, 200]
        
yticks = [-41,-42,-43,-44,-45,-46]# [-20, -30,-35,-40,-45,-50,-60]
ax.gridlines(xlocs=xticks, ylocs=yticks,linewidth=2, color='gray', alpha=0.5, linestyle='--')
# Label the end-points of the gridlines using the custom tick makers:
ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER) 
ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)

lambert_xticks(ax, xticks)
lambert_yticks(ax, yticks)
# ax.set_xticklabels([name for name in met_dict])


