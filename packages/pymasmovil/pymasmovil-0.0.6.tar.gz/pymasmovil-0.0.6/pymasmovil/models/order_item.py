from pymasmovil.client import Client
from pymasmovil.models.new_line_request import NewLineRequest

from pymasmovil.errors.exceptions import NewLineRequestRequiredParamsError


class OrderItem():
    _route = '/v0'

    id = ''
    account_id = ''
    name = ''
    surname = ''
    productName = ''
    phone = ''
    orderType = ''
    status = ''
    createdDate = ''
    lastModifiedDate = ''
    attributes = {
        'Apellidos': '',
        'Fecha_Portabilidad_Saliente': '',
        'ICCID_Donante': '',
        'Nombre': '',
        'Numero_de_Documento': '',
        'Operador_Donante_Movil': '',
        'Operador_Receptor_Movil': '',
        'Tipo_de_Documento': '',
        'Tipo_de_Linea': '',
        'Fecha_de_solicitud_del_abonado': '',
        'Porcentaje_Consumo_Bono': ''
    }
    simAttributes = {
        'ICCID': '',
        'IMSI': '',
        'PIN': '',
        'PIN2': '',
        'PUK': '',
        'PUK2': ''
    }

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'attributes':
                for inner_key, inner_value in value.items():
                    if inner_key in self.attributes:
                        self.attributes[inner_key] = inner_value
            if key == 'simAttributes':
                for inner_key, inner_value in value.items():
                    if inner_key in self.simAttributes:
                        self.simAttributes[inner_key] = inner_value
            else:
                if hasattr(OrderItem, key):
                    setattr(self, key, value)

    @classmethod
    def get(cls, session, order_item_id):
        """
            Returns an OrderItem instance obtained by id.
            :param order_item_id:

            :return: OrderItem:
        """

        order_item = Client(session).get(
            route='{}/{}'.format(cls._route, order_item_id))

        return OrderItem(**order_item)

    @classmethod
    def create(cls, session, account, **new_order_item):
        """
            Creates an order-item and posts it to the given account

            :param account: account where we want to add the order-item
            :param **new_order_item:
            :return: order-item instance
        """

        post_route = '{}/accounts/{}/order-items'.format(cls._route, account.id)

        cls._check_required_attributes(new_order_item)

        Client(session).post(post_route, (), new_order_item)

        new_line_request = NewLineRequest(new_order_item, account.id)

        return OrderItem(**new_line_request.to_order_item())

    def _check_required_attributes(new_order_item):
        """ Check that all compulsary attributes for a portability request
        are present in the request dynamic fields """

        required_attributes = ['idLine', 'documentType', 'iccid', 'productInfo']

        is_portability = False
        new_line_info = new_order_item['lineInfo'][0]

        if new_line_info.get('phoneNumber'):
            is_portability = True
            required_attributes.extend(["docid", "donorOperator", "portabilityDate"])

        if new_line_info.get('documentType') == "CIF":
            # Organization client
            required_attributes.append("corporateName")

        elif new_line_info.get('documentType') in ("NIF", "NIE", "Pasaporte"):
            # Particular client
            required_attributes.extend(["name", "surname"])

        order_item_filled_attributes = set(filter(
            new_line_info.get,
            new_line_info.keys()))

        missing_attributes = set(required_attributes) - order_item_filled_attributes

        if len(missing_attributes) != 0:
            raise NewLineRequestRequiredParamsError(is_portability, sorted(missing_attributes))
