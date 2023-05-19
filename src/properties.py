import requests
import warnings
from src.urls import URL


class Properties:
    '''further information at https://dev.easybroker.com/docs.'''

    def __init__(self, api_key):
        self.url = URL
        self.session = requests.session()
        self.session.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Authorization": api_key
        }

    @staticmethod
    def create_location(name, street, exterior_number, interior_number, cross_street, postal_code, latitude, longitude):
        '''Create a location object and use it on "create_a_property" method.

        :param name: A location string containing the neighborhood, city and the administrative division where the
        property is located. It must match a location found through the locations endpoint.
        :type name: str
        :param street: The name of the street where the property is located.
        :type street: str
        :param exterior_number: The property address exterior number.
        :type exterior_number: str
        :param interior_number: The property address interior number.
        :type interior_number: str
        :param cross_street: The property address cross street.
        :type cross_street: str
        :param postal_code: The property address postal code.
        :type postal_code: str
        :param latitude: The latitude where the property is located.
        :type latitude: float
        :param longitude: The longitude where the property is located.
        :type longitude: float
        :return: dict
        '''

        location = {
            "name": name,
            "street": street,
            "exterior_number": exterior_number,
            "interior_number": interior_number,
            "cross_street": cross_street,
            "postal_code": postal_code,
            "latitude": latitude,
            "longitude": longitude
        }
        return location

    @staticmethod
    def create_options(updated_after=None, updated_before=None):
        '''Example of how to create an options object to make things easier to the user

        :param updated_after: date in format "YYYY-MM-DD"
        :type updated_after: str
        :param updated_before: date in format "YYYY-MM-DD"
        :type updated_before: str
        :return:
        '''

        options = {}
        if updated_after is not None:
            options["search[updated_after]"] = updated_after

        if updated_before is not None:
            options["search[updated_before]"] = updated_before

        return options

    def print_all_properties_titles(self):
        '''Print all property's titles of the book'''

        i = 1
        limit = 50
        count = 0
        while True:
            allProperties = self.list_all_properties(page=i, limit=limit)
            total = allProperties["pagination"]["total"]
            limit = allProperties["pagination"]["limit"]
            for prop in allProperties["content"]:
                print(prop["title"])
            i += 1
            count += limit
            if count >= total:
                break

    def list_all_properties(self, page=1, limit=20, options=None):
        '''
        Returns a list of properties from your organization.

        :param page: Content's page
        :type page: int
        :param limit: Max results per page (Maximum: 50)
        :type limit: int
        :param options: additional options (more info at https://easybroker-staging.readme.io/reference/get_properties)
        :type options: dict
        :return: list
        '''

        if page < 1 or limit < 1:
            return {
                "error": "Bad request",
                "message": "page and limit params must be an integer greater than or equal to 1"
            }

        if limit > 50:
            limit = 50
            warnings.warn("Limit value must be less than or equal to 50, it has been settled to 50")

        if options is None:
            options = {}

        required_params = {
            "page": int(page),
            "limit": int(limit)
        }

        params = dict(**required_params, **options)
        response = self.session.get(self.url + "/properties", params=params)
        return response.json()

    def create_a_property(self, property_type, title, description, status, location, options=None):
        '''
        Creates a new property in your EasyBroker account. This endpoint is still in beta, please contact our support
        team if you have any problem or want to share any feedback.

        :param property_type: The property type. It should match one of the property types available for your account.
        :type property_type: str
        :param title: The property listing title.
        :type title: str
        :param description: The property listing description.
        :type description: str
        :param status: The property status
        :type status: str
        :param location: location of the property. Create a location using "create_location" method of this class
        :type location: dict
        :param options: additional options (more info at https://easybroker-staging.readme.io/reference/post_properties)
        :type options: dict
        :return: dict
        '''

        if options is None:
            options = {}

        body = {
            "property_type": property_type,
            "title": title,
            "description": description,
            "status": status,
            "location": location
        }

        json = dict(**body, **options)
        response = self.session.post(self.url + "/properties", json=json)
        return response.json()

    def retrieve_a_property(self, property_id):
        '''
        Returns the detailed information of a property from your EasyBroker account.

        :param property_id: The public or internal ID of the specified property
        :type property_id: str
        :return: dict
        '''

        response = self.session.get(self.url + "/properties/{}".format(property_id))
        return response.json()

    def update_a_property(self, property_id, property_type, title, description, status, options=None):
        '''
        Updates an existing property in your EasyBroker account. This endpoint is still in beta, please contact our
        support team if you have any problem or want to share any feedback.

        :param property_id: The public or internal ID of the specified property
        :type property_id: str
        :param property_type: The property type. It should match one of the property types available for your account.
        :type property_type: str
        :param title: The property listing title.
        :type title: str
        :param description: The property listing description.
        :type description: str
        :param status: The property status
        :type status: str
        :param options: additional options (more info at https://easybroker-staging.readme.io/reference/patch_properties-property-id)
        :type options: dict
        :return:
        '''

        if options is None:
            options = {}

        body = {
            "property_type": property_type,
            "title": title,
            "description": description,
            "status": status
        }

        json = dict(**body, **options)
        response = self.session.patch(self.url + "/properties/{}".format(property_id), json=json)
        return response.json()