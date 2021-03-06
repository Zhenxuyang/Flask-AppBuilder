from flask_appbuilder import ModelRestApi
from flask_appbuilder.api import BaseApi, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface

from . import appbuilder, db
from .models import Contact, ContactGroup, Gender


def fill_gender():
    try:
        db.session.add(Gender(name="Male"))
        db.session.add(Gender(name="Female"))
        db.session.add(Gender(name="Nonbinary"))
        db.session.commit()
    except Exception:
        db.session.rollback()


db.create_all()
fill_gender()


class GreetingApi(BaseApi):
    resource_name = "greeting"
    openapi_spec_methods = {
        "greeting": {
            "get": {
               "description": "Override description",
            }
        }
    }

    @expose('/')
    def greeting(self):
        """Send a greeting
        ---
        get:
          responses:
            200:
              description: Greet the user
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      message:
                        type: string
        """
        return self.response(200, message="Hello")


appbuilder.add_api(GreetingApi)


class ContactModelApi(ModelRestApi):
    resource_name = "contact"
    datamodel = SQLAInterface(Contact)
    allow_browser_login = True

    openapi_spec_methods = {
        "get_list": {
            "get": {
                "description": "Get all contacts, filter and pagination",
            }
        }
    }


appbuilder.add_api(ContactModelApi)


class GroupModelApi(ModelRestApi):
    resource_name = "group"
    datamodel = SQLAInterface(ContactGroup)
    allow_browser_login = True


appbuilder.add_api(GroupModelApi)
