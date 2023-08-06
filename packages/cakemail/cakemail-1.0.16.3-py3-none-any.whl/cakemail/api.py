import time

from cakemail.subapis.account import Account
from cakemail.subapis.campaign import Campaign
from cakemail.subapis.contact import Contact
from cakemail.subapis.custom_attribute import CustomAttribute
from cakemail.subapis.domain import Domain
from cakemail.subapis.form import Form
from cakemail.subapis.list import List
from cakemail.subapis.log import Log
from cakemail.subapis.logo import Logo
from cakemail.subapis.report import Report
from cakemail.subapis.segment import Segment
from cakemail.subapis.sender import Sender
from cakemail.subapis.sub_account import SubAccount
from cakemail.subapis.suppressed_email import SuppressedEmail
from cakemail.subapis.transactional_email import TransactionalEmail
from cakemail.subapis.user import User
from cakemail.token import Token
from cakemail_openapi import AccountApi, SubAccountApi, ApiClient, TokenApi, \
    Configuration, CampaignApi, ContactApi, CustomAttributeApi, DomainApi, \
    FormApi, ListApi, LogApi, LogoApi, ReportApi, UserApi, SegmentApi, \
    SenderApi, SuppressedEmailApi, TransactionalEmailApi


class Api:
    _api_client = None
    _config = None
    _token: Token = None

    account: Account
    sub_account: SubAccount
    campaign: Campaign
    contact: Contact
    custom_attribute: CustomAttribute
    domain: Domain
    form: Form
    list: List
    log: Log
    logo: Logo
    report: Report
    segment: Segment
    sender: Sender
    suppressed_email: SuppressedEmail
    transactional_email: TransactionalEmail
    user: User

    def __init__(
            self,
            username,
            password,
            url='https://api.cakemail.dev'
    ):
        self._config = Configuration(host=url)
        self._api_client = ApiClient(self._config)
        self._token = Token(
            email=username,
            password=password,
            token_api=TokenApi(self._api_client),
            configuration=self._config
        )

        self.account = Account(AccountApi(self._api_client))
        self.sub_account = SubAccount(SubAccountApi(self._api_client))
        self.campaign = Campaign(CampaignApi(self._api_client))
        self.contact = Contact(ContactApi(self._api_client))
        self.custom_attribute = CustomAttribute(
            CustomAttributeApi(self._api_client))
        self.domain = Domain(DomainApi(self._api_client))
        self.form = Form(FormApi(self._api_client))
        self.list = List(ListApi(self._api_client))
        self.log = Log(LogApi(self._api_client))
        self.logo = Logo(LogoApi(self._api_client))
        self.report = Report(ReportApi(self._api_client))
        self.segment = Segment(SegmentApi(self._api_client))
        self.sender = Sender(SenderApi(self._api_client))
        self.suppressed_email = SuppressedEmail(
            SuppressedEmailApi(self._api_client))
        self.transactional_email = TransactionalEmail(
            TransactionalEmailApi(self._api_client))
        self.user = User(UserApi(self._api_client))

    def __getattribute__(self, name):
        """ Refresh the token if expired """
        if name not in ['_api_client', '_config', '_token']:
            if self._token.expires_at < time.time():
                self._token.refresh()

        return super(Api, self).__getattribute__(name)
