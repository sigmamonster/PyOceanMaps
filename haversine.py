#! /usr/bin/python

# TO DO:
#   multilocation cases
#   1   if location2.shape is m,2 with m > 1 then haversine should
#       calculate the distance between location1 and each m in location2
#   2   if location1.shape == location2.shape and both are m,2 and m > 1
#       do a calculation for each pair of n
#   3   if  location1 is n,2 and location2 is not given, calculate the
#       distance for each pair to give an n,n output where diagonals = 0

def haversine(location1, location2=None):  # calculates great circle distance
    """Returns the great circle distance of the given
    coordinates.
    
    INPUT:  location1 = lat1, lon1
            location2 = lat2, lon2
    
    OUTPUT: distance in km
    
    METHOD: a = sin(dLat / 2) * sin(dLat / 2) + 
                sin(dLon / 2) * sin(dLon / 2) * 
                cos(lat1) * cos(lat2)
            c = 2 * arctan2(sqrt(a), sqrt(1 - a))
            d = R * c
            
            where R is the earth's radius (6371 km)
            and d is the distance in km"""
    from pylab import   deg2rad, sin, cos, arctan2, \
                        sqrt, plot, show, array
    
    location1 = array(location1)
    location2 = array(location2)
    
    if location2.ndim == 2:
        lat1, lon1 = location1
        lat2, lon2 = location2.T
    elif location2.ndim == 1:
        lat1, lon1 = location1
        lat2, lon2 = location2
    elif location2 is None:
        pass
        # future task
    
    R = 6371.
    dLat = deg2rad(lat2 - lat1)
    dLon = deg2rad(lon2 - lon1)
    lat1 = deg2rad(lat1)
    lat2 = deg2rad(lat2)

    a = sin(dLat / 2) * sin(dLat / 2) + \
        sin(dLon / 2) * sin(dLon / 2) * \
        cos(lat1) * cos(lat2)
    c = 2 * arctan2(sqrt(a), sqrt(1 - a))
    d = R * c
    return d

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

def test2():
    from pylab import prod
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

    
if __name__ == "__main__":

    test1()
    test2()
