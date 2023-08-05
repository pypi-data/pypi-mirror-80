import numpy as np
import scipy.special as ss
from scipy.stats import norm

def separate_residual_function( Y , X ) :

    # e = Y - X * (X' * X ) ^ (-1) * X' * Y
    # e = Y -       Z              * X' * Y

    Z = np.dot ( X , np.linalg.inv ( np.dot ( np.transpose( X ) , X ) ) )

    e = Y - np.dot( np.dot ( Z , np.transpose( X ) ) , Y ) 

    return e

def regression_sieves( L , W , Y , sieve , exp , gauss_order , nodes ):
    
    if sieve == 'polynomial':
        
        L_sieve = np.zeros( ( np.size( L ) , exp ) )
        
        for i in range( 0 , exp ):
            
          L_sieve[ : , [i] ] = pow( L , i + 1 )
        
        
        
    elif sieve == 'gaussian':
        
        L_sieve = np.zeros( ( np.size( L ) , gauss_order ) )
        
        for i in range( 0 , gauss_order ):

          L_sieve[ : , [i] ] = ss.eval_hermite( i + 1, L ) * norm.pdf( L )
        
        
        
    elif sieve == 'linear_spline':
        
        k = np.size( nodes )
        nodes = np.array( nodes ).reshape( k , 1 )
        
        L_sieve = np.zeros( ( np.size(L) ,  ( np.size( nodes ) ) ) )  

        for i in range( 0 , np.size( nodes ) ):

          L_sieve[ : , [i] ] = ( L - nodes[ i ] ) * ( L >= nodes[ i ] )
        
        
    
    elif sieve == 'quadratic_spline':
        
        k = np.size( nodes )
        np_nodes = np.array( nodes ).reshape( k , 1 )
        
        P = 2
        
        L_sieve = np.zeros( ( np.size(L) ,  np.size( np_nodes ) * P ) ) 

        for i in range( 0 , np.size( np_nodes ) ):
    
          for p in range( 1 , P + 1 ):

           L_sieve[ : , [ P * (i) + ( p - 1 ) ] ] =  pow( L - np_nodes[ i ] , p ) * ( L >= np_nodes[ i ] )
 

    #Getting OMEGA
    #Omega = L_sieve* ( L_sieve' * L_sieve ) ^ (-1) * L_sieve'
    #Omega = L_sieve*         x                  * L_sieve'

    x = np.linalg.inv ( np.dot ( np.transpose( L_sieve ) , L_sieve ) )

    Omega = np.dot( np.dot( L_sieve , x ) , np.transpose( L_sieve ) )       
    
    
    # Y_Omega = Omega * Y
    
    Y_Omega = np.dot( Omega , Y ) 

    Delta = Y - Y_Omega 
      
    
    # Calculating the residuals

    eY = separate_residual_function( Y , L_sieve )

    eW = separate_residual_function( W , L_sieve )

    
    # Alpha  = (eW' * eW ) ^ (-1) * eW'
    # Alpha =        y           * eW'

    y = np.linalg.inv( np.dot ( np.transpose ( eW ) , eW ) )

    Alpha = np.dot( y , np.transpose( eW ) ) 
    

    #ATE
    ate = np.dot( Alpha , Delta ) 
    
    
    return( Omega , Delta , Alpha , ate , L_sieve ) 