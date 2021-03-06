

import numpy as np    
def make_blobs(n_blobs=3, n_points=100): 
    def make_blob(m=100, center=(0,0), span=10):
        while(True):
            with np.warnings.catch_warnings():
                np.warnings.filterwarnings("error")  # treat warning as errors
                try: 
                    Σ = np.random.randint(low=-span, high=span, size=(2,2))
                    Σ[1,0] = Σ[0,1]
                    mx = np.random.multivariate_normal(mean=center, cov=Σ, size=m)
                    b = np.unique(Σ).size <= 2
                    if b: continue
                    else: break
                except RuntimeWarning: continue
        return(mx)


    def get_center_and_radius_of_blob(mx):
        center = (mx.max(axis=0) + mx.min(axis=0))/2
        ix = ((mx - center)**2).sum(axis=1).argmax()
        max_point = mx[ix]
        radius = np.sqrt(((max_point - center)**2).sum())
        return(center,radius)
        
    
    def shift_blob(main_blob, other_blob):
        from math import pi as π, cos, sin
        from random import uniform
        
        center, radius = main_blob[:2] if isinstance(main_blob, (tuple,list)) else get_center_and_radius_of_blob(main_blob)
        center2, radius2 = get_center_and_radius_of_blob(other_blob)
        
        θ = uniform(0, 2*π)
        
        adjacent = (radius+radius2) * cos(θ)
        opposite = (radius+radius2) * sin(θ)
        
        x,y = np.add(center, [adjacent, opposite]) - center2
    
        other_blob += (x,y)
        return(other_blob)
    
    X = []
    y = sum(([label,]*n_points for label in range(n_blobs)),[])
      
        
    mx = make_blob(n_points)
    X.append(mx)
    center, radius = get_center_and_radius_of_blob(mx)
    
    for i in range(1, n_blobs):
        mx_new = shift_blob([center, radius], make_blob(n_points))
        X.append(mx_new)
    
    X = np.concatenate(X, axis=0)
    X += np.abs(X.min(axis=0))
    return(X, np.array(y, dtype='uint8'))


#=========================================================================================


def main():
    X,y = make_blobs(4)
    
    import matplotlib.pyplot as plt
    sp = plt.subplot()
    sp.scatter(*X.T, c=y)

if __name__=="__main__":main()



























