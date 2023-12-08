def color_aqi (x) :
    if x == "moderate" :
        return [255, 253, 55]
    elif x == "good":
        return [0, 128, 0]
    elif x == "unhealthy":
        return [255, 140, 0]
    else:
        return [255, 0, 0]