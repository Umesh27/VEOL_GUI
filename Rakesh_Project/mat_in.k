*MAT_RIGID
$HMNAME MATERIALS         1rgd_bott                                                                        
         17.8500E-09  200000.0      0.33                                        
       1.0         7         7
         0
*MAT_RIGID
$HMNAME MATERIALS         2rgd_top                                                                         
         27.8500E-09  200000.0      0.33                                        
       1.0         6         7
         0
*MAT_PIECEWISE_LINEAR_PLASTICITY
$HMNAME MATERIALS         3PET                                                                             
         31.2200E-09    2920.0       0.4      33.9     146.0                    
*SECTION_SHELL
$HMNAME PROPERTIES         1shell                                                                           
         1        16       1.0         2                             0          
       1.0       1.0       1.0       1.0                                        
*SECTION_SHELL
$HMNAME PROPERTIES         3thk                                                                             
         3        16       1.0         2                                        
       3.1       3.1       3.1       3.1                                        
*SECTION_SOLID
$HMNAME PROPERTIES         2sld                                                                             
         2         2          
$$ Base Accelerations and Angular Velocities
*LOAD_BODY_Y
$HMNAME LOADCOLS       1grav                                                                    
$HWCOLOR LOADCOLS       1      11
         3      -1.0                                                  
*LOAD_BODY_PARTS
$HMNAME LOADCOLS       1grav                                                                    
$HWCOLOR LOADCOLS       1      11
         1
