from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

from .exceptions import GoogleAdsAccountLostAccessException
from .helpers import make_request_account_id

_GOOGLE_ADS_VERSION = "v5"


def get_google_ads_client(credentials_path: str) -> GoogleAdsClient:
    return GoogleAdsClient.load_from_storage(credentials_path)


def get_google_ads_service(service_name: str, google_ads_client: GoogleAdsClient, version: str = _GOOGLE_ADS_VERSION):
    return google_ads_client.get_service(service_name, version=version)


def check_access_account(account_id: str, google_ads_client: GoogleAdsClient):
    """From an account id check if Arcane has access to it"""
    customer_service = get_google_ads_service('CustomerService', google_ads_client)
    ressource_name = customer_service.customer_path(make_request_account_id(account_id))
    try:
        customer = customer_service.get_customer(ressource_name)
    except GoogleAdsException as err:
        if "USER_PERMISSION_DENIED" in str(err):
                raise GoogleAdsAccountLostAccessException(f"We cannot access your Google Ads account with the id: {account_id}. Are you sure you granted access?")
        elif "CUSTOMER_NOT_FOUND" in str(err):
            raise GoogleAdsAccountLostAccessException(f"We cannot find this account ({account_id}). Are you sure you entered the correct id?")
        else:
            raise GoogleAdsAccountLostAccessException(
                f"We cannot access this account ({account_id}). Are you sure you entered the correct id?")

    if customer.manager:
        raise GoogleAdsAccountLostAccessException('This account ID is a MCC. Please enter a Google Ads Account.')
