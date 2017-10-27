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
                              'CMO':1.0, 'CON1':7, 'CON2':7, 'SIGY':33.90, 'ETAN':146.00, 'FAIL':1E21, 'LCSS':0}

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