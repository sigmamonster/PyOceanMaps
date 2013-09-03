#! /usr/bin/python

# TO DO:
#   multilocation cases
#   at the moment duplicate cases are also calculated. 
#   i.e. upper and lower triangles of the distance matrix.
#   next step would be to get all combinations without duplicate

def haversine(location1, location2=None):  # calculates great circle distance
    __doc__ = """Returns the great circle distance of the given
    coordinates.
    
    INPUT:  location1 = ((lat1, lon1), ..., n(lat1, lon1))
           *location2 = ((lat2, lon2), ..., n(lat2, lon2))
           *if location2 is not given a square matrix of distances
             for location1 will be put out
    OUTPUT: distance in km
            (dist1  ...  ndist
              :            : 
             ndist1 ...  ndist)
            shape will depend on the input
    METHOD: a = sin(dLat / 2) * sin(dLat / 2) + 
                sin(dLon / 2) * sin(dLon / 2) * 
                cos(lat1) * cos(lat2)
            c = 2 * arctan2(sqrt(a), sqrt(1 - a))
            d = R * c
            
            where R is the earth's radius (6371 km)
            and d is the distance in km"""
    
    from itertools import product, combinations
    from pylab import   deg2rad, sin, cos, arctan2, \
                        meshgrid, sqrt, array, arange
    
    if location2: 
        location1 = array(location1, ndmin=2)
        location2 = array(location2, ndmin=2)
    elif location2 is None:
        location1 = array(location1, ndmin=2)
        location2 = location1.copy()
    
    # get all combinations using indicies
    ind1 = arange(location1.shape[0])
    ind2 = arange(location2.shape[0])
    ind  = array(list(product(ind1, ind2)))
    
    # using combination inds to get lats and lons
    lat1, lon1 = location1[ind[:,0]].T
    lat2, lon2 = location2[ind[:,1]].T
    
    # setting up variables for haversine
    R = 6371.
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)
    
    # haversine formula
    a = sin(dLat / 2) * sin(dLat / 2) + \
        sin(dLon / 2) * sin(dLon / 2) * \
        cos(lat1) * cos(lat2)
    c = 2 * arctan2(sqrt(a), sqrt(1 - a))
    d = R * c
    
    # reshape accodring to the input
    D = d.reshape(location1.shape[0], location2.shape[0])
    
    return D

def test1():
    """Tests the output of the function with two points using Joburg
    amd Cape Town as the points. """

    # Coords of the two locations 
    joburg = 26.204, 28.046
    capetn = 33.925, 18.424

    known_dist = 1261. # known dist between cities from internet
    hav_dist  = haversine(joburg, capetn) # get haversine output
    dist_diff = abs(known_dist - hav_dist)

    # Test whether known and haversine distance are within 50km
    if dist_diff > 50.:
        print "FAILED: Test 1 (1x1 point case)" 
    else:
        print "PASSED: Test 1 (1x1 point case)"

def test2(): # location1 = 1x1; location2 = 1xn
    # Cape Town will be location1
    capetn = (-33.925, 18.424) # Cape Town
    
    # African capilats will be location2
    # coordinates from Google
    afr_caps = ((-17.864, 31.030), # Harare
                ( 30.050, 31.233), # Cairo
                ( -4.325, 15.322), # Kinshasa
                (  8.484,-13.234)) # Freetown
    
    # http://distancecalculator.globefeed.com
    # distances are from Cape Town and are in km
    known_dists = ( 2186.6, # Harare
                    7239.0, # Cairo 
                    3305.4, # Kinshasa
                    5776.7) # Freetown
    
    hav_dists = haversine(capetn, afr_caps) # get haversine output
    dist_diff = abs(known_dists - hav_dists)
    
    # Test whether known and haversine distance are within 50km
    if prod(dist_diff < 50.): # if any are false whole list is false
        print "PASSED: Test 2 (1xn point case)" 
    else:
        print "FAILED: Test 2 (1xn point case)"

def test3(): # only location1 input
    afr_caps = ((-33.925, 18.424), # Cape Town
                (-26.204, 28.046), # Joburg
                (-17.864, 31.030), # Harare
                ( 30.050, 31.233), # Cairo
                ( -4.325, 15.322), # Kinshasa
                (  8.484,-13.234)) # Freetown
    
    # http://distancecalculator.globefeed.com
    # distances are from Cape Town and are in km
    known_dists = ( 1261.0, # Joburg
                    2186.6, # Harare
                    7239.0, # Cairo 
                    3305.4, # Kinshasa
                    5776.7) # Freetown
    
    hav_dists = haversine(afr_caps)
    dist_diff = abs(hav_dists[0,1:] - known_dists)
    
    # Test whether known and haversine distance are within 50km
    if prod(dist_diff < 50.): # if any are false whole list is false
        print "PASSED: Test 3 (nxn point case)" 
    else:
        print "FAILED: Test 3 (nxn point case)"
    
def test4(): # illegal input tests
    pass
if __name__ == "__main__":
    from pylab import prod

    test1()
    test2()
    test3()
