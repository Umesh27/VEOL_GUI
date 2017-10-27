*KEYWORD                                         
*CONTROL_TERMINATION
$$  ENDTIM    ENDCYC     DTMIN    ENDENG    ENDMAS
$ENDTIM$         0       0.0       0.0       0.0
*CONTROL_TIMESTEP
$$  DTINIT    TSSFAC      ISDO    TSLIMT     DT2MS      LCTM     ERODE     MSIST
       0.0$TIMESTSC$         0       0.0$DT2MS$         0         0         0
       0.0         0         0
*CONTROL_HOURGLASS
$$     IHQ        QH
         2      0.14
*CONTROL_CONTACT
$$  SLSFAC    RWPNAL    ISLCHK    SHLTHK    PENOPT    THKCHG     ORIEN    ENMASS
       0.0       0.0         0         2         1         0         0         2
$$  USRSTR    USRFRC     NSBCS    INTERM     XPENE     SSTHK      ECDT   TIEDPRJ
         0         0         0         0       4.0         1         0$TIEDPRJ$
$$   SFRIC     DFRIC       EDC    INTVFC        TH     TH_SF    PEN_SF
       0.0       0.0       0.0       0.0       0.0       0.0       0.0
$$  IGNORE    FRCENG   SKIPRWG    OUTSEG   SPOTSTP   SPOTDEL   SPOTHIN
         0         0         0         0         0         0       0.0
$$    ISYM    NSEROD    RWGAPS    RWGDTH     RWKSF      ICOV    SWRADF    ITHOFF
         0         0         1       0.0       1.0         0       0.0         0
$$  SHLEDG    PSTIFF    ITHCNT    TDCNOF     FTALL              SHLTRW          
         0         0         0         0         0                 0.0          
*CONTROL_ENERGY
$$    HGEN      RWEN    SLNTEN     RYLEN
         2         2         2         2
*CONTROL_ACCURACY
$$ OSU           INN    PIDOSU
         1         2         0
$$DATABASE_OPTION -- Control Cards for ASCII output
*DATABASE_ELOUT
$$      DT    BINARY      LCUR      IOPT
$DT$         3         0         1
*DATABASE_SLEOUT
$#      dt    binary      lcur     ioopt     
$DT$         3         0         1
*DATABASE_GLSTAT
$$      DT    BINARY      LCUR      IOPT
$DT$         3         0         1
*DATABASE_MATSUM
$$      DT    BINARY      LCUR      IOPT
$DT$         3         0         1
*DATABASE_NODOUT
$$      DT    BINARY      LCUR      IOPT      DTHF     BINHF
$DT$         3         0         1       0.0         0
*DATABASE_RCFORC
$$      DT    BINARY      LCUR      IOPT
$DT$         3         0         1
*DATABASE_RWFORC
$$      DT    BINARY      LCUR      IOPT
$DT$         3         0         1
*DATABASE_BINARY_D3DUMP
$#    cycl      lcdt      beam     npltc    psetid      
$D3DUMP$         0         0         0         0
*DATABASE_BINARY_D3PLOT
$$ DT/CYCL      LCDT      BEAM     NPLTC    PSETID
$DT$         0         0         0         0
         0
*DATABASE_EXTENT_BINARY
$$   NEIPH     NEIPS    MAXINT    STRFLG    SIGFLG    EPSFLG    RLTFLG    ENGFLG
         0         0         3         0         1         1         1         1
$$  CMPFLG    IEVERP    BEAMIP     DCOMP      SHGE     STSSZ    N3THDT   IALEMAT
         1         0         0         2         1         1         2         1
$$ NINTSLD   PKP_SEN      SCLP     HYDRO     MSSCL     THERM    INTOUT    NODOUT
         0         0       1.0         0         0         0    STRESS    STRESS
$$    DTDT
         0
$DEFINE_CURVE$
$BPM$
$LBY$
$LBP$