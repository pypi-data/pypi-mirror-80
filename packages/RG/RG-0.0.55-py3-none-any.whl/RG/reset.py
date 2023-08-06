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
    
    # A good start, but causes problem when printing subsequent results
    #import os
    #os.system('cls' if os.name=='nt' else 'clear')
    
    # Workaround
    print('\n'*100)
    
    
    # Delete variables
    from IPython import get_ipython
    get_ipython().magic('reset -sf')
    
    
    # Close windows
    import matplotlib.pyplot as plt
    plt.close('all')
    
    return
