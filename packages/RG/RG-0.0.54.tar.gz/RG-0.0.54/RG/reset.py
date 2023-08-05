# reset: resent Python console



def reset():
    '''
    
    Reset: resent Python console
    - clear console
    - delete variables
    - close windows
    reset(X)
    
    INPUT
    none
    
    OUTPUT
    none 
    
    '''
    
    
    # Clear console
    import os
    os.system('cls' if os.name=='nt' else 'clear')
    
    # Delete variables
    from IPython import get_ipython
    get_ipython().magic('reset -sf')
    
    # Close windows
    import matplotlib.pyplot as plt
    plt.close('all')
    
    return
