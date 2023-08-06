# Kornpob Bhirombhakdi
# kbhirombhakdi@stsci.edu

from scipy.interpolate import interp2d
import numpy as np

class PhotApCorr:
    """
    PhotApCorr is a class containing tables for computing aperture correction for photometry with HST observations.
    For instantiation, PhotApCorr() without argument will provide all tables.
    - self.available_table = access all available tables
      - each table is recorded with keyword instrument such as 'HST-WFC3-IR'.
      - self.available_instrument = access available instruments
    Use PhotApCorr(instrument) to properly instantiate the object.
    - self.table will be available to access the table given instrument.
    Use compute() method to compute aperture correction.
    - self.apsize and self.wave must be specified to start the computation. This can be assigned during the instantiation or after.
    - aptype, apshape, apunit, waveunit will be checked with the table. If mismatch, ValueError will be raised.
    - self.apcorr contains the correction value.
    """
    def __init__(self,instrument=None,apsize=None,wave=None,aptype='radius',apshape='circle',apunit='arcsec',waveunit='A'):
        self.available_table = self._get_table()
        self.available_instrument = self.available_table.keys()
        if instrument is not None and instrument not in self.available_instrument:
            raise ValueError('instrument = {0} is not supported. Use self.available_instrument to check for support.'.format(instrument))
        else:
            self.instrument = instrument
        if instrument is not None and instrument in self.available_instrument:
            self.table = self.available_table[instrument]
        else:
            self.table = 'instrument was not specified when instantiated.'
        self.instrument = instrument
        self.apsize = apsize
        self.wave = wave
        self.aptype = aptype
        self.apshape = apshape
        self.apunit = apunit
        self.waveunit = waveunit
    def compute(self):
        try:
            table = self.available_table[self.instrument]
        except:
            string = 'instrument = {0} is not supported. Use self.available_instrument to check for support instrument.'.format(self.instrument)
            raise ValueError(string)
        if self.aptype != table['aptype']:
            raise ValueError('Only aptype = {0} is supported.'.format(table['aptype']))
        if self.apshape != table['apshape']:
            raise ValueError('Only apshape = {0} is supported.'.format(table['apshape']))
        if self.apunit != table['apunit']:
            raise ValueError('Only apunit = {0} is supported.'.format(table['apunit']))
        if self.waveunit != table['waveunit']:
            raise ValueError('Only waveunit = {0} is supported.'.format(table['waveunit']))
        if self.apsize is None or self.wave is None:
            raise ValueError('apsize and wave must be specified.')
        model = self._model(table['wave'],table['apsize'],table['value'])
        apcorr = model(self.wave,self.apsize)
        self.apcorr = apcorr
    def _model(self,wave,apsize,value):
        model = interp2d(wave,apsize,value,kind='linear',copy=True,bounds_error=True)
        return model
    def _get_table(self):
        ##########
        # Start with HST/WFC3/IR
        ##########
        TABLE = {'HST-WFC3-IR': 
                 {'ref': ['WFC3 Instrument Handbook, Ch 7.6 + 9.3'],
                  'scale': 0.13,
                  'scaleunit': 'arcsec/pix',
                  'aptype': 'radius',
                  'apshape': 'circle',
                  'apunit': 'arcsec',
                  'waveunit': 'A',
                  'row': 'apsize',
                  'col': 'wave',
                  'apsize': np.array((0.10,0.15,0.20,0.25,0.30
                                       ,0.40,0.50,0.60,0.80,1.00
                                       ,1.50,2.00
                                      )),
                  'wave': np.array((7000.,8000.,9000.,10000.,11000.,12000.,13000.,14000.,15000.,16000.,17000.)),
                  'value' : np.array(((0.575,0.549,0.524,0.502,0.484,0.468,0.453,0.438,0.426,0.410,0.394),
                                       (0.736,0.714,0.685,0.653,0.623,0.596,0.575,0.558,0.550,0.539,0.531),
                                       (0.802,0.794,0.780,0.762,0.739,0.712,0.683,0.653,0.631,0.608,0.590),
                                       (0.831,0.827,0.821,0.813,0.804,0.792,0.776,0.756,0.735,0.708,0.679),
                                       (0.850,0.845,0.838,0.833,0.828,0.822,0.816,0.808,0.803,0.789,0.770),
                                       (0.878,0.876,0.869,0.859,0.850,0.845,0.841,0.838,0.840,0.836,0.832),
                                       (0.899,0.894,0.889,0.884,0.878,0.868,0.858,0.852,0.852,0.850,0.848),
                                       (0.916,0.913,0.904,0.897,0.893,0.889,0.883,0.875,0.870,0.863,0.859),
                                       (0.937,0.936,0.929,0.924,0.918,0.909,0.903,0.900,0.903,0.900,0.895),
                                       (0.951,0.951,0.946,0.941,0.935,0.930,0.925,0.920,0.917,0.912,0.909),
                                       (0.967,0.969,0.967,0.965,0.963,0.959,0.954,0.951,0.952,0.948,0.943),
                                       (0.974,0.977,0.976,0.975,0.973,0.972,0.969,0.967,0.970,0.967,0.963)
                                     )),
                  'ZPunit': ('filter','pivot wavelength Angstrom','ABMAG ZP INF'),
                  'ZP': {'F098M': (9864.7,25.68),
                          'F105W': (10551.0,26.27),
                          'F110W': (11534.4,26.82),
                          'F125W': (12486.1,26.24),
                          'F140W': (13922.8,26.46),
                          'F160W': (15369.1,25.95)
                         },
                  'model': None
                 },
                 'HST-WFC3-UVIS':
                 {'ref': ['WFC3 Instrument Handbook, Ch 6.6 + 9.3'],
                  'scale': 0.0395,
                  'scaleunit': 'arcsec/pix',
                  'aptype': 'radius',
                  'apshape': 'circle',
                  'apunit': 'arcsec',
                  'waveunit': 'A',
                  'row': 'apsize',
                  'col': 'wave',
                  'apsize': np.array((0.10,0.15,0.20,0.25,0.30
                                       ,0.40,0.50,0.60,0.80,1.00
                                       ,1.50,2.00
                                      )),
                  'wave': np.array((2000.,3000.,4000.,5000.,6000.,7000.,8000.,9000.,10000.,11000.)),
                  'value' : np.array(((0.660,0.739,0.754,0.745,0.720,0.687,0.650,0.623,0.612,0.605),
                                       (0.717,0.793,0.823,0.834,0.832,0.823,0.807,0.778,0.742,0.699),
                                       (0.752,0.822,0.845,0.859,0.859,0.857,0.853,0.847,0.844,0.829),
                                       (0.781,0.844,0.864,0.875,0.877,0.874,0.870,0.867,0.868,0.864),
                                       (0.802,0.858,0.880,0.888,0.890,0.889,0.883,0.879,0.879,0.876),
                                       (0.831,0.880,0.899,0.911,0.910,0.907,0.906,0.904,0.900,0.894),
                                       (0.861,0.894,0.912,0.923,0.925,0.923,0.918,0.915,0.918,0.917),
                                       (0.884,0.906,0.922,0.932,0.934,0.933,0.931,0.927,0.927,0.923),
                                       (0.936,0.928,0.936,0.944,0.947,0.946,0.945,0.942,0.944,0.942),
                                       (0.967,0.946,0.948,0.954,0.955,0.955,0.955,0.952,0.955,0.952),
                                       (0.989,0.984,0.973,0.970,0.970,0.969,0.967,0.966,0.970,0.968),
                                       (0.994,0.992,0.989,0.985,0.980,0.977,0.976,0.975,0.978,0.976)
                                     )),
                  'ZPunit': ('filter','pivot wavelength Angstrom','ABMAG ZP INF'),
                  'ZP': {'F200LP':(4970.9,27.36),
                          'F606W': (5887.5,26.08),
                          'F814W': (8029.9,25.10)
                         },
                  'model': None
                 }
                }
        return TABLE
                 
                 
                 
#                  'HST-ACS-WFC':
#                  {'ref': ['http://www.stsci.edu/hst/instrumentation/acs/data-analysis/aperture-corrections'
#                           ,'https://ui.adsabs.harvard.edu/abs/2016AJ....152...60B/abstract'
#                           ,'ACS Instrument Handbook'
#                           ,'https://acszeropoints.stsci.edu/results_all/?date=2019-12-05&detector=WFC'
#                          ]
#                   ,'scale': 0.05
#                   ,'scaleunit': 'arcsec/pix'
#                   ,'type': 'radius'
#                   ,'row': 'apsize'
#                   ,'col': 'filter'
#                   ,'apunit': 'arcsec'
#                   ,'apsize': np.array((0.05,0.1,0.15,0.2,0.25
#                                        ,0.3,0.35,0.4,0.45,0.5
#                                        ,1.,2.
#                                       ))
#                   ,'filter': np.array(('F435W','F475W','F502N','F555W','F550M',
#                                        'F606W','F625W','F658N','F660N','F775W',
#                                        'F814W','F892N','F850LP'))
#                   ,'value' : np.array(((0.330,0.663,0.792,0.839,0.863,0.877,0.887,0.895,0.902,0.907,0.941,0.979),
#                                        (0.329,0.670,0.794,0.842,0.868,0.883,0.893,0.901,0.907,0.912,0.944,0.979),
#                                        (0.328,0.670,0.794,0.842,0.869,0.884,0.894,0.902,0.909,0.914,0.945,0.978),
#                                        (0.328,0.668,0.794,0.841,0.868,0.885,0.895,0.903,0.910,0.915,0.946,0.977),
#                                        (0.328,0.666,0.794,0.840,0.867,0.885,0.896,0.904,0.910,0.915,0.947,0.976),
#                                        (0.328,0.661,0.795,0.839,0.866,0.885,0.896,0.904,0.910,0.916,0.947,0.975),
#                                        (0.330,0.655,0.795,0.838,0.864,0.884,0.896,0.904,0.911,0.916,0.948,0.974),
#                                        (0.331,0.651,0.794,0.838,0.863,0.883,0.896,0.904,0.911,0.916,0.948,0.973),
#                                        (0.331,0.650,0.794,0.838,0.863,0.883,0.896,0.904,0.911,0.916,0.948,0.973),
#                                        (0.329,0.625,0.783,0.836,0.858,0.877,0.894,0.904,0.910,0.916,0.949,0.972),
#                                        (0.322,0.611,0.770,0.830,0.853,0.871,0.889,0.901,0.908,0.914,0.949,0.972),
#                                        (0.278,0.546,0.705,0.787,0.818,0.840,0.860,0.877,0.889,0.897,0.942,0.970),
#                                        (0.268,0.532,0.690,0.776,0.810,0.833,0.853,0.871,0.884,0.893,0.940,0.970)
#                                      )).T
#                   ,'ZP': {'F435W': (4329.2,25.662),
#                           'F475W': (4746.2,26.053),
#                           'F502N': (5023.0,22.282),
#                           'F555W': (5360.9,25.711),
#                           'F550M': (5581.5,24.853),
#                           'F606W': (5922.0,26.495),
#                           'F625W': (6312.0,25.902),
#                           'F658N': (6584.0,22.761),
#                           'F660N': (6599.4,21.711),
#                           'F775W': (7693.2,25.664),
#                           'F814W': (8045.0,25.942),
#                           'F892N': (8914.8,22.397),
#                           'F850LP': (9033.2,24.856)
#                          }
#                   ,'ZPunit': ('filter','pivot wavelength Angstrom','ABMAG ZP INF')
#                   ,'model': None
#                  },
                 
                 
                 
    