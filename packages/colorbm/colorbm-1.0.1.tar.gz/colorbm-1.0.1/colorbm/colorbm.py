from matplotlib.colors import ListedColormap, to_hex, LinearSegmentedColormap
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os
from .color_palettes import palettes_hex

"""
Color palettes for scientific plots, extracted from
ggsci: https://nanx.me/ggsci/index.html
paintings: https://designshack.net/articles/inspiration/10-free-color-palettes-from-10-famous-paintings/
misc: https://github.com/Timothysit/sciplotlib
"""

hex_npg = palettes_hex.hex_npg
npg = ListedColormap(palettes_hex.hex_npg)
hex_aaas = palettes_hex.hex_aaas
aaas = ListedColormap(palettes_hex.hex_aaas)
hex_nejm = palettes_hex.hex_nejm
nejm = ListedColormap(palettes_hex.hex_nejm)
hex_lancet = palettes_hex.hex_lancet
lancet = ListedColormap(palettes_hex.hex_lancet)
hex_jama = palettes_hex.hex_jama
jama = ListedColormap(palettes_hex.hex_jama)
hex_jco = palettes_hex.hex_jco
jco = ListedColormap(palettes_hex.hex_jco)
hex_ucscgb = palettes_hex.hex_ucscgb
ucscgb = ListedColormap(palettes_hex.hex_ucscgb)
hex_d3_10 = palettes_hex.hex_d3_10
hex_d3_20 = palettes_hex.hex_d3_20
hex_d3_20b = palettes_hex.hex_d3_20b
hex_d3_20c = palettes_hex.hex_d3_20c
d3_10 = ListedColormap(palettes_hex.hex_d3_10)
d3_20 = ListedColormap(palettes_hex.hex_d3_20)
d3_20b = ListedColormap(palettes_hex.hex_d3_20b)
d3_20c = ListedColormap(palettes_hex.hex_d3_20c)
hex_locuszoom = palettes_hex.hex_locuszoom
locuszoom = ListedColormap(palettes_hex.hex_locuszoom)
hex_igv = palettes_hex.hex_igv
hex_igv_alternating = palettes_hex.hex_igv_alternating
igv = ListedColormap(palettes_hex.hex_igv)
igv_alternating = ListedColormap(palettes_hex.hex_igv_alternating)
hex_cosmic_hallmarks_dark = palettes_hex.hex_cosmic_hallmarks_dark
hex_cosmic_hallmarks_light = palettes_hex.hex_cosmic_hallmarks_light
hex_cosmic_signature_substitutions = palettes_hex.hex_cosmic_signature_substitutions
cosmic_hallmarks_dark = ListedColormap(palettes_hex.hex_cosmic_hallmarks_dark)
cosmic_hallmarks_light = ListedColormap(palettes_hex.hex_cosmic_hallmarks_light)
cosmic_signature_substitutions = ListedColormap(palettes_hex.hex_cosmic_signature_substitutions)
hex_uchicago = palettes_hex.hex_uchicago
hex_uchicago_light = palettes_hex.hex_uchicago_light
hex_uchicago_dark = palettes_hex.hex_uchicago_dark
uchicago = ListedColormap(palettes_hex.hex_uchicago)
uchicago_light = ListedColormap(palettes_hex.hex_uchicago_light)
uchicago_dark = ListedColormap(palettes_hex.hex_uchicago_dark)
hex_startrek = palettes_hex.hex_startrek
startrek = ListedColormap(palettes_hex.hex_startrek)
hex_tron = palettes_hex.hex_tron
tron = ListedColormap(palettes_hex.hex_tron)
hex_futurama = palettes_hex.hex_futurama
futurama = ListedColormap(palettes_hex.hex_futurama)
hex_rickandmorty = palettes_hex.hex_rickandmorty
rickandmorty = ListedColormap(palettes_hex.hex_rickandmorty)
hex_simpsons = palettes_hex.hex_simpsons
simpsons = ListedColormap(palettes_hex.hex_simpsons)
hex_economist = palettes_hex.hex_economist
hex_economist_alternative = palettes_hex.hex_economist_primary
hex_economist_primary = palettes_hex.hex_economist_alternative
economist = ListedColormap(palettes_hex.hex_economist)
economist_primary = ListedColormap(palettes_hex.hex_economist_primary)
economist_alternative = ListedColormap(palettes_hex.hex_economist_alternative)
hex_starrynight = palettes_hex.hex_starrynight
starrynight = ListedColormap(palettes_hex.hex_starrynight)
hex_monalisa = palettes_hex.hex_monalisa
monalisa = ListedColormap(palettes_hex.hex_monalisa)
hex_scream = palettes_hex.hex_scream
scream = ListedColormap(palettes_hex.hex_scream)
hex_lastsupper = palettes_hex.hex_lastsupper
lastsupper = ListedColormap(palettes_hex.hex_lastsupper)
hex_afternoon = palettes_hex.hex_afternoon
afternoon = ListedColormap(palettes_hex.hex_afternoon)
hex_optometrist = palettes_hex.hex_optometrist
optometrist = ListedColormap(palettes_hex.hex_optometrist)
hex_kanagawa = palettes_hex.hex_kanagawa
hex_kanagawa_alternative = palettes_hex.hex_kanagawa_alternative
kanagawa = ListedColormap(palettes_hex.hex_kanagawa)
kanagawa_alternative = ListedColormap(palettes_hex.hex_kanagawa_alternative)
hex_kiss = palettes_hex.hex_kiss
kiss = ListedColormap(palettes_hex.hex_kiss)
hex_memory = palettes_hex.hex_memory
memory = ListedColormap(palettes_hex.hex_memory)
hex_lilies = palettes_hex.hex_lilies
lilies = ListedColormap(palettes_hex.hex_lilies)
hex_antique = palettes_hex.hex_antique
antique = ListedColormap(hex_antique)
hex_bold = palettes_hex.hex_bold
bold = ListedColormap(hex_bold)
hex_pastel = palettes_hex.hex_pastel
pastel = ListedColormap(hex_pastel)
hex_prism = palettes_hex.hex_prism
prism = ListedColormap(hex_prism)
hex_safe = palettes_hex.hex_safe
safe = ListedColormap(hex_safe)
hex_vivid = palettes_hex.hex_vivid
vivid = ListedColormap(hex_vivid)


class available_colormaps():
    # Colormap Lists
    # SEABORN
    seabornDiv = ['icefire', 'vlag']
    seabornSeq = ['mako', 'rocket', 'crest', 'flare']
    seaborn = seabornDiv + seabornSeq

    # SCIENTIFIC
    scientificDiv = ['broc', 'cork', 'vik', 'lisbon', 'tofino', 'berlin', 'oleron']
    scientificSeq = ['acton', 'bamako', 'batlow', 'bilbao', 'buda', 'davos', 'devon', 'grayc', 'hawaii', 'imola',
                     'lajolla', 'lapaz', 'nuuk', 'oslo', 'roma', 'tokyo', 'turku', 'romao', 'broco', 'corko',
                     'viko']
    scientific = scientificDiv + scientificSeq

    # CMasher
    CMasherDiv = ['iceburn', 'redshift', 'watermelon', 'wildfire', 'guppy', 'pride', 'fusion', 'seasons', 'viola',
                  'waterlily']
    CMasherSeq = ['amber', 'apple', 'arctic', 'bubblegum', 'chroma', 'dusk', 'eclipse', 'ember', 'fall', 'flamingo',
                  'freeze', 'gem', 'gothic', 'heat', 'horizon', 'jungle', 'lavender', 'lilac', 'neon', 'neutral',
                  'nuclear', 'ocean', 'pepper', 'rainforest', 'savanna', 'sepia', 'sunburst', 'swamp', 'toxic', 'tree',
                  'voltage']
    CMasher = CMasherDiv + CMasherSeq

    # cmocean
    cmoceanDiv = ['topo', 'balance', 'delta', 'curl', 'diff', 'tarn']
    cmoceanSeq = ['thermal', 'haline', 'solar', 'ice', 'gray', 'oxy', 'deep', 'dense', 'algae', 'matter', 'turbid',
                  'speed', 'amp', 'tempo', 'rain', 'phase']
    cmocean = cmoceanDiv + cmoceanSeq

    # CARTO
    CARTODiv = ['armyrose', 'fall', 'geyser', 'tealrose', 'tropic', 'earth']
    CARTOSeq = ['burg', 'burgyl', 'redor', 'oryel', 'peach', 'pinkyl', 'mint', 'blugrn', 'darkmint', 'emrld', 'bluyl',
                'teal', 'tealgrn', 'purp', 'purpor', 'sunset', 'magenta', 'sunsetdark', 'brwnyl']
    CARTO = CARTODiv + CARTOSeq

    # Material Design
    matDiv = []
    matSeq = ['matred', 'matpink', 'matpurple', 'matdpurple', 'matindigo', 'matblue', 'matlblue', 'matcyan', 'matteal',
              'matgreen', 'matlgreen', 'matlime', 'matyellow', 'matamber', 'matorange', 'matdorange', 'matbrown',
              'matgrey', 'matbgrey']
    mat = matDiv + matSeq

    # MISC
    miscDiv = []
    miscSeq = ['oliveblue', 'gsea', 'turbo', 'parula']
    misc = miscDiv + miscSeq

    colormapsDiv = seabornDiv + scientificDiv + CMasherDiv + cmoceanDiv + CARTODiv + miscDiv
    colormapsSeq = seabornSeq + scientificSeq + CMasherSeq + cmoceanSeq + CARTOSeq + miscSeq
    colormaps = colormapsDiv + colormapsSeq

    def __init__(self, scheme=None):
        self.scheme = scheme

    @property
    def all(self):
        if self.scheme is None:
            return available_colormaps.colormaps
        elif self.scheme == 'seaborn':
            return available_colormaps.seaborn
        elif self.scheme == 'scientific':
            return available_colormaps.scientific
        elif self.scheme == 'CMasher':
            return available_colormaps.CMasher
        elif self.scheme == 'cmocean':
            return available_colormaps.cmocean
        elif self.scheme == 'CARTO':
            return available_colormaps.CARTO
        elif self.scheme == 'misc':
            return available_colormaps.misc
        elif self.scheme == 'mat':
            return available_colormaps.mat
        else:
            print('No such colormap scheme')

    @property
    def div(self):
        if self.scheme is None:
            return available_colormaps.colormapsDiv
        elif self.scheme == 'seaborn':
            return available_colormaps.seabornDiv
        elif self.scheme == 'scientific':
            return available_colormaps.scientificDiv
        elif self.scheme == 'CMasher':
            return available_colormaps.CMasherDiv
        elif self.scheme == 'cmocean':
            return available_colormaps.cmoceanDiv
        elif self.scheme == 'CARTO':
            return available_colormaps.CARTODiv
        elif self.scheme == 'misc':
            return available_colormaps.miscDiv
        elif self.scheme == 'mat':
            return available_colormaps.matDiv
        else:
            print('No such colormap scheme')

    @property
    def seq(self):
        if self.scheme is None:
            return sorted(available_colormaps.colormapsSeq, key=str.lower)
        elif self.scheme == 'seaborn':
            return available_colormaps.seabornSeq
        elif self.scheme == 'scientific':
            return available_colormaps.scientificSeq
        elif self.scheme == 'CMasher':
            return available_colormaps.CMasherSeq
        elif self.scheme == 'cmocean':
            return available_colormaps.cmoceanSeq
        elif self.scheme == 'CARTO':
            return available_colormaps.CARTOSeq
        elif self.scheme == 'misc':
            return available_colormaps.miscSeq
        elif self.scheme == 'mat':
            return available_colormaps.matSeq
        else:
            print('No such colormap scheme')


class available_palattes(object):
    # Palettes List
    # ggsci
    ggsci = ['npg', 'aaas', 'nejm', 'lancet', 'jama', 'jco', 'ucscgb', 'd3_10', 'd3_20', 'd3_20b', 'd3_20c', 'd3_10',
             'd3_20', 'd3_20b', 'd3_20c', 'locuszoom', 'igv', 'igv.alternating', 'cosmic_hallmarks_dark',
             'cosmic_hallmarks_light', 'cosmic_signature_substitutions', 'uchicago', 'uchicago_light', 'uchicago_dark',
             'startrek', 'tron', 'futurama', 'rickandmorty', 'simpsons']

    # paintings
    paintings = ['starrynight', 'monalisa', 'scream', 'lastsupper', 'afternoon', 'optometrist', 'kanagawa',
                 'kanagawa_alternative', 'kiss', 'memory', 'lilies']

    # CARTO
    CARTO = ['antique', 'bold', 'pastel', 'prism', 'safe', 'vivid']

    # misc
    misc = ['economist', 'economist_primary', 'economist_alternative']

    palettesAll = ggsci + paintings + CARTO + misc

    def __init__(self, palName=None):
        self.palName = palName

    @property
    def all(self):
        if self.palName is None:
            return available_palattes.palettesAll

    @property
    def get(self):
        if self.palName == 'ggsci':
            return available_palattes.ggsci
        elif self.palName == 'paintings':
            return available_palattes.paintings
        elif self.palName == 'CARTO':
            return available_palattes.CARTO
        elif self.palName == 'misc':
            return available_palattes.misc
        else:
            print('No such palettes')


class seq:
    def __init__(self, cmap, n=256):
        self.cmap = cmap
        self.rgb = np.loadtxt(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'sequential\{}.rgb'.format(self.cmap)),
            delimiter=',')
        self.n = n

    @property
    def as_cmap(self):
        return LinearSegmentedColormap.from_list(self.cmap, self.rgb, N=self.n)

    @property
    def as_cmap_r(self):
        return LinearSegmentedColormap.from_list(self.cmap, self.rgb[::-1], N=self.n)

    @property
    def as_hex(self):
        self.hex = seq.srgblist_to_hex(self.rgb)
        return self.hex

    @property
    def as_rgb(self):
        return self.rgb

    # Convert RBG list to HEX list
    @staticmethod
    def srgblist_to_hex(s):
        hex = []
        for x in enumerate(s):
            hex += [to_hex(x[1])]
        return hex


class div(seq):
    def __init__(self, cmap, n=256):
        self.cmap = cmap
        self.rgb = np.loadtxt(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'diverging\{}.rgb'.format(self.cmap)),
            delimiter=',')
        self.n = n


class pcolor(object):

    def __init__(self, cmap, n=256):
        self.cmap = cmap
        self.n = n
        if self.cmap in available_colormaps().div:
            self.type = 'diverging'
        elif self.cmap in available_colormaps().seq:
            self.type = 'sequential'
        elif self.cmap in available_palattes().all:
            self.type = 'palettes'
        else:
            print('No such colormap or palette')

    def show(self, **kwargs):
        if self.type == 'palettes':
            testPlots(self.cmap).scatterPlot
        else:
            rev = kwargs.get('reversed', False)
            if not rev:
                if self.type == 'diverging':
                    testPlots(self.cmap).imagePlot(div(self.cmap, self.n).as_cmap, div=True)
                elif self.type == 'sequential':
                    testPlots(self.cmap).imagePlot(seq(self.cmap, self.n).as_cmap)

            else:
                if self.type == 'diverging':
                    testPlots(self.cmap).imagePlot(div(self.cmap, self.n).as_cmap_r, div=True)
                elif self.type == 'sequential':
                    testPlots(self.cmap).imagePlot(seq(self.cmap, self.n).as_cmap_r)


class testPlots(object):

    def __init__(self, cmap):
        self.cmap = cmap

    def imagePlot(self, cmapObj, **kwargs):

        x = np.random.random((128, 128))

        divPlot = kwargs.get('div', False)
        if divPlot:
            x -= 0.5
        else:
            pass

        fig, ax = plt.subplots()
        ax.set_aspect('equal')
        im = ax.imshow(x, extent=[-x.shape[1] / 2., x.shape[1] / 2., -x.shape[0] / 2., x.shape[0] / 2.],
                       interpolation='gaussian',
                       cmap=cmapObj)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.2)
        plt.colorbar(im, cax=cax)
        plt.show()

    @property
    def scatterPlot(self):

        pal_dic = {'npg': npg, 'aaas': aaas, 'nejm': nejm, 'lancet': lancet, 'jama': jama, 'jco': jco, 'ucscgb': ucscgb,
                   'd3_10': d3_10,
                   'd3_20': d3_20, 'd3_20b': d3_20b, 'd3_20c': d3_20c, 'd3_10': d3_10, 'd3_20': d3_20, 'd3_20b': d3_20b,
                   'd3_20c': d3_20c,
                   'locuszoom': locuszoom, 'igv': igv, 'alternating': igv_alternating,
                   'cosmic_hallmarks_dark': cosmic_hallmarks_dark,
                   'cosmic_hallmarks_light': cosmic_hallmarks_light,
                   'cosmic_signature_substitutions': cosmic_signature_substitutions,
                   'uchicago': uchicago, 'uchicago_light': uchicago_light, 'uchicago_dark': uchicago_dark,
                   'startrek': startrek,
                   'tron': tron, 'futurama': futurama, 'rickandmorty': rickandmorty, 'simpsons': simpsons,
                   'starrynight': starrynight,
                   'monalisa': monalisa, 'scream': scream, 'lastsupper': lastsupper, 'afternoon': afternoon,
                   'optometrist': optometrist,
                   'kanagawa': kanagawa, 'kanagawa_alternative': kanagawa_alternative, 'kiss': kiss, 'memory': memory,
                   'lilies': lilies,
                   'antique': antique, 'bold': bold, 'pastel': pastel, 'prism': prism, 'safe': safe, 'vivid': vivid,
                   'economist': economist, 'economist_primary': economist_primary,
                   'economist_alternative': economist_alternative}

        # cmap = ListedColormap(palettes_hex.hex_'{}'.format())
        plt.rcParams['scatter.edgecolors'] = 000000

        np.random.seed(19680801)
        N = 100
        x = np.random.rand(N)
        y = np.random.rand(N)

        fig, ax = plt.subplots()
        colors = np.random.rand(N)
        area = (30 * np.random.rand(N)) ** 2  # 0 to 15 point radii

        ax.scatter(x, y, s=area, c=colors, alpha=0.5, cmap=pal_dic[self.cmap])
        plt.show()
