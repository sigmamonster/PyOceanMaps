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
    from pylab import deg2rad, sin, cos, arctan2, sqrt, plot, show

    lat1, lon1 = location1
    lat2, lon2 = location2

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
    if not dist_diff < 50.:
        print "FAILED: Test 1 (1x1 point case)" 
    else:
        print "PASSED: Test 1 (1x1 point case)"

if __name__ == "__main__":

    test1()
