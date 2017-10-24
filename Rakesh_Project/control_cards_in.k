*CONTROL_TERMINATION
$$  ENDTIM    ENDCYC     DTMIN    ENDENG    ENDMAS     NOSOL
      30.0                                                  
*CONTROL_HOURGLASS
$$     IHQ        QH
         4       0.1
*CONTROL_IMPLICIT_AUTO
$$   IAUTO    ITEOPT    ITEWIN     DTMIN     DTMAX     DTEXP     KFAIL    KCYCLE
         1                           0.1       0.5                              
*CONTROL_IMPLICIT_GENERAL
$$  IMFLAG       DT0    IMFLAG      NSBS       IGS     CNSTN      FORM    ZERO_V
         1                                                                      
*CONTROL_IMPLICIT_SOLVER
$$  LSOLVR    LPRINT     NEGEV     ORDER      DRCM    DRCPRM   AUTOSPC   AUTOTOL
         4                                                                      

*CONTROL_IMPLICIT_SOLUTION
$$  NSOLVR    ILIMIT    MAXREF     DCTOL     ECTOL     RCTOL     LSTOL    ABSTOL
         2                                                                      
*CONTROL_ENERGY
$$    HGEN      RWEN    SLNTEN     RYLEN
         2         2         2         2
$$DATABASE_OPTION -- Control Cards for ASCII output
*DATABASE_ELOUT
$$      DT    BINARY      LCUR      IOPT
       0.3         0                    
*DATABASE_GLSTAT
$$      DT    BINARY      LCUR      IOPT
       3.0         0                    
*DATABASE_MATSUM
$$      DT    BINARY      LCUR      IOPT
       0.3         0                    
*DATABASE_RCFORC
$$      DT    BINARY      LCUR      IOPT
      0.15         0                    
*DATABASE_RWFORC
$$      DT    BINARY      LCUR      IOPT
      0.15         0                    
*DATABASE_SSSTAT
$$      DT    BINARY      LCUR      IOPT
       0.3         0                    
*DATABASE_BINARY_D3PLOT
$$ DT/CYCL      LCDT      BEAM     NPLTC    PSETID
       0.3                                        
          
*DATABASE_EXTENT_BINARY
$$   NEIPH     NEIPS    MAXINT    STRFLG    SIGFLG    EPSFLG    RLTFLG    ENGFLG
                                       1                                        
$$  CMPFLG    IEVERP    BEAMIP     DCOMP      SHGE     STSSZ    N3THDT   IALEMAT
                                                                                
$$ NINTSLD   PKP_SEN      SCLP     HYDRO     MSSCL     THERM    INTOUT    NODOUT
                                                                                
$$    DTDT    RESPLT     NEIPB
*BOUNDARY_PRESCRIBED_MOTION_RIGID
$HMNAME LOADCOLS       2disp                                                                    
$HWCOLOR LOADCOLS       2       4
         2         2         2         2       1.0                              
*DEFINE_CURVE
$HMNAME CURVES         1laminate                                                                
$HWCOLOR CURVES         1      11
$HMCURVE     1    2 laminate                                                                        
         1                 1.0       1.0                    
                 0.0                 0.0
              0.0161               5.783
               0.033              11.761
              0.0491               14.85
              0.0649              16.803
              0.0803              18.074
              0.0956              18.964
              0.1106              19.589
              0.1254              20.052
                0.14               20.36
              0.1544              20.666
              0.1686              20.972
              0.1708              21.033
*DEFINE_CURVE
$HMNAME CURVES         2disp                                                                    
$HWCOLOR CURVES         2      11
$HMCURVE     1    3 disp                                                                            
         2                 1.0       1.0                    
                 0.0                 0.0
                30.0               -30.0
*DEFINE_CURVE
$HMNAME CURVES         3grav                                                                    
$HWCOLOR CURVES         3      11
$HMCURVE     1    1 grav                                                                            
         3                 1.0       1.0                    
                 0.0              9810.0
                 1.0              9810.0
$$ Base Accelerations and Angular Velocities
*LOAD_BODY_Y
$HMNAME LOADCOLS       1grav                                                                    
$HWCOLOR LOADCOLS       1      11
         3      -1.0                                                  
*LOAD_BODY_PARTS
$HMNAME LOADCOLS       1grav                                                                    
$HWCOLOR LOADCOLS       1      11
         1