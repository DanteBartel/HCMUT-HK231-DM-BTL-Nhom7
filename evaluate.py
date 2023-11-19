def evaluate(result, gt):
    t, f = 0,0
    for res in result:
        if res in gt:
            t += 1
        else:
            f += 1
    """ Return: 3 values respectively
    1. percentage of true predictions over all predictions
    2. percentage of false predictions over all predictions
    3. percentage of true predictions over ground truth
    """
    return round(float(t/len(result)),4), round(float(f/len(result)),4), round(float(t/len(gt)),4)