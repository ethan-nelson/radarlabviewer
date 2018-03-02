# -*- coding: utf-8 -*-
# MIT License (c) 2015 Ethan Nelson 

def read(filename, *args):
    """
    A QuickBeam reader.

    Input
    -----
    filename: a QuickBeam file

    Optional arguments
    ------------------
    *args: include only these variables

    Output
    ------
    ref: dictionary of values

    """
    import numpy as np
    import struct

    ref = {}

    if filename[-3:] == '.gz':
        import gzip
        file = gzip.open(filename, 'rb')
    else:
        file = open(filename, 'rb')
    
    ref['filename'] = file.read(200)
    ref['title'] = file.read(100)
    ref['sensor'] = file.read(20)
    ref['freq'] = struct.unpack( "f", file.read(4) )[0]
    ref['year'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['month'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['day'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['hour'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['minute'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['second'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['nx'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['ny'] = struct.unpack( "hxx", file.read(4) )[0]
    ref['deltax'] = struct.unpack( "f", file.read(4) )[0]
    ref['deltay'] = struct.unpack( "f", file.read(4) )[0]
    ref['nhgt'] = struct.unpack( "hxx", file.read(4) )[0]
    
    grid1d = ref['nhgt']
    grid2d = ref['ny'] * ref['nx']
    grid3d = ref['nhgt'] * ref['ny'] * ref['nx']

    shape1d = [ ref['nhgt'] ]
    shape2d = [ ref['ny'], ref['nx'] ]
    shape3d = [ ref['nhgt'], ref['ny'], ref['nx'] ]

    pos = 0

    if args and 'hgt' not in args:
        pos += 4*grid1d
    else:
        file.seek(pos,1)
        ref['hgt'] = np.reshape( \
                struct.unpack( str(grid1d)+"f", file.read(4*grid1d) ), \
                shape1d )
        pos = 0

    if args and 'lat' not in args:
        pos += 4*grid2d
    else:
        file.seek(pos,1)
        ref['lat'] = np.reshape( \
                struct.unpack( str(grid2d)+"f", file.read(4*grid2d) ), \
                shape2d )
        pos = 0

    if args and 'lon' not in args:
        pos += 4*grid2d
    else:
        file.seek(pos,1)
        ref['lon'] = np.reshape( \
                struct.unpack( str(grid2d)+"f", file.read(4*grid2d) ), \
                shape2d )
        pos = 0

    if args and 'sfcrain' not in args:
        pos += 4*grid2d
    else:
        file.seek(pos,1)
        ref['sfcrain'] = np.reshape( \
                struct.unpack( str(grid2d)+"f", file.read(4*grid2d) ), \
                shape2d )
        pos = 0

    if args and 'tempk' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['tempk'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    if args and 'Z_eff' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['Z_eff'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    if args and 'Z_ray' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['Z_ray'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    if args and 'h_atten' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['h_atten'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    if args and 'g_atten' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['g_atten'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    if args and 'Z_cor' not in args:
        pos += 4*grid3d
    else:
        file.seek(pos,1)
        ref['Z_cor'] = np.reshape( \
                struct.unpack( str(grid3d)+"f", file.read(4*grid3d) ), \
                shape3d )
        pos = 0

    file.close()

    if args:
        return {key: ref[key] for key in ref if key in args}
    else:
        return ref
