__author__ = 'Umesh'

class MaterialProp:

    def __init__(self):
        # self.materialProp = ['Title', 'Id', 'Density', 'E1', 'E2', 'Mu', 'GAB', 'GBC', 'FBRT', 'YCFAC', 'XC', 'XT', 'YC', 'YT']
        """

        :return:
        """
        self.meshInfo = {}
        self.material_prop = {"Title":"PartName", "Id":1, "Density":4.4000e-09, "E1":5029.9333, "E2":1050.0, "PR":0.32, "E3":5029.9333,
                              "GAB":1905.2778, "GBC":397.7273, "FBRT":0.1, "YCFAC":2.0, "XC":22.59, "XT":45.182, "YC":5.504, "YT":11.01,
                              'CMO':1.0, 'CON1':7, 'CON2':7, 'SIGY':33.90, 'ETAN':146.00, 'FAIL':1E21, 'LCSS':0,

                              "mid":1,"ro":4.4000e-09,"ea":5029.9333,"eb":1050.0,"(ec)":5029.9333,"prba":0.32,"(prca)":0.32,"(prcb)":0.32,
                              "gab":1905.2778,"gbc":397.7273,"gca":1905.2778,"(kf)":"","aopt":"","2way":"",
                              "xp":0.0,"yp":0.0,"zp":0.0,"a1":0.0,"a2":0.0,"a3":0.0,"mangle":0.0,
                              "v1":0.0,"v2":0.0,"v3":0.0,"d1":0.0,"d2":0.0,"d3":0.0,"dfailm":"","dfails":"",
                              "tfail":0.0,"alph":0.0,"soft":1.0,"fbrt":0.0,"ycfac":2.0,"dfailt":0.0,"dfailc":0.0,"efs":0.0,
                              "xc":22.59,"xt":45.182,"yc":5.504,"yt":11.01,"sc":0.0,"crit":0.0,"beta":0.0,
                              "pel":"","epsf":"","epsr":"","tsmd":"","soft2":1.0,
                              "slimt1":"","slimc1":"","slimt2":"","slimc2":"","slims":"","ncyred":"","softg":1.0,
                              "lcxc":"", "lcxt":"", "lcyc":"", "lcyt":"", "lcsc":"", "dt":"",

                              "e":2920.0,"pr":0.4,"sigy":"","etan":0.0,"fail":10.E+20,"tdel":0.0,
                              "c":0.0,"p":0.0,"lcss":0,"lcsr":0,"vp":0.0,"lcf":0,
                              "eps1":0.0,"eps2":0.0,"eps3":0.0,"eps4":0.0,"eps5":0.0,"eps6":0.0,"eps7":0.0,"eps8":0.0,
                              "es1":0.0,"es2":0.0,"es3":0.0,"es4":0.0,"es5":0.0,"es6":0.0,"es7":0.0,"es8":0.0,

                              "n":0.0,"couple":0,"m":0,"alias":"",
                              "cmo":0.0,"con1":"","con2":"",
                              "lco or a1":0.0
                              }

        # Default values
        self.Title = "PartName"
        self.Id = 1
        self.Density = 4.4000e-09
        self.E1 = 5029.9333
        self.E2 = 1050.0
        self.Mu = 0.32
        self.GAB = 1905.2778
        self.GBC = 397.7273
        self.FBRT = 0.1
        self.YCFAC = 2.0
        self.XC = 22.591000
        self.XT = 45.181999
        self.YC = 5.5040002
        self.YT = 11.008000