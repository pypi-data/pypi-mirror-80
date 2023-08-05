from pymasmovil.client import Client
from pymasmovil.models.order_item import OrderItem
from pymasmovil.errors.exceptions import AccountRequiredParamsError


class Account():
    _route = '/v0/accounts'

    town = ""
    surname = ""
    stair = ""
    roadType = ""
    roadNumber = ""
    roadName = ""
    region = ""
    province = ""
    postalCode = ""
    phone = ""
    name = ""
    id = ""
    flat = ""
    email = ""
    door = ""
    documentType = ""
    documentNumber = ""
    corporateName = ""
    buildingPortal = ""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(Account, key):
                setattr(self, key, value)

    @classmethod
    def get(cls, session, account_id):
        """
        Returns a account instance obtained by id.

        :param id:
        :return: Account:
        """

        account_response = Client(session).get(
            route='{}/{}'.format(cls._route, account_id))

        return Account(**account_response)

    @classmethod
    def create(cls, session, **new_account):
        """
            Creates an account instance.

            :param **new_account:
            :return:
        """

        cls._check_required_attributes(new_account)

        new_account_id = Client(session).post(cls._route, (), new_account)

        return Account(id=new_account_id, **new_account)

    def get_order_item_by_phone(self, session, phone):
        """
            Retrieve the order_item associated to a given account and filter one
            corresponding to a given phone number, from the MM sytem.

            :param : MM login session, phone of the OrderItem we expect
            :return: an OrderItem instance
        """

        params = {
            "rowsPerPage": 1,
            "actualPage": 1,
            "phone": phone
        }

        response = Client(session).get(
            "{}/{}/order-items".format(self._route, self.id),
            **params)

        return OrderItem(**response["rows"][0])

    def _check_required_attributes(new_account):
        required_attributes = ['documentNumber', 'documentType', 'email',
                               'phone', 'postalCode', 'province', 'region', 'roadName',
                               'roadNumber', 'roadType', 'town']

        if new_account.get('documentType') == "1":
            # CIF. Organization client
            required_attributes.append("corporateName")
        else:
            # VAT/NIF. Particular client
            required_attributes.extend(["name", "surname", "nationality"])

        account_filled_attributes = set(filter(
            new_account.get,
            new_account.keys()))

        missing_attributes = set(required_attributes) - account_filled_attributes

        if len(missing_attributes) != 0:
            raise AccountRequiredParamsError(sorted(missing_attributes))
