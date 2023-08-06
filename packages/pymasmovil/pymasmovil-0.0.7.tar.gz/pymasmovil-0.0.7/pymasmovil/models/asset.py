from pymasmovil.models.contract import Contract


class Asset(Contract):
    _route = '/v1/assets'

    maxNumTariff = ''
    numTariff = ''
    productRelation = ''
    assetType = ''
    initDate = ''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
