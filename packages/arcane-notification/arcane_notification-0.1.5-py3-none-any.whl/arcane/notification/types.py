from enum import Enum
from typing import Dict, Optional
from email.utils import parseaddr
import logging
import re
from typing import List, Union
from datetime import datetime
from dateutil.parser import isoparse

from .notification_config import KEY_SEPARATOR as _KEY_SEPARATOR


class Severity(Enum):
    """ severity of the notification characterising how often to send the notification"""
    HIGH = 'HIGH'
    MEDIUM = 'MEDIUM'
    LOW = 'LOW'
    NONE = 'NONE'

    def _value(self):
        return {'HIGH': 3, 'MEDIUM': 2, 'LOW': 1}.get(self.value, 0)

    def __ge__(self, other: 'Severity') -> bool:
        return self._value() >= other._value()

    def __gt__(self, other: 'Severity') -> bool:
        return self._value() > other._value()

    def __lt__(self, other: 'Severity') -> bool:
        return not self >= other

    def __le__(self, other: 'Severity') -> bool:
        return not self > other

    # as we use string correspondences we have to define this.
    def __repr__(self):
        return f'<{self.__class__.__name__}.{self.name}>'


SEVERITY_MAPPING = {item.value: item for item in Severity}


class NotificationKey(object):
    def __init__(self,
                 sender_service: str,  # which service is sending the notification
                 notification_name: str,  # how the service will name the notification (in communications)
                 ):
        if _KEY_SEPARATOR in sender_service:
            raise ValueError(f'sender_service should not contain the keyword "{_KEY_SEPARATOR}"')
        self.sender_service = sender_service
        self.notification_name = notification_name

    def __repr__(self):
        return f'Service: "{self.sender_service}", Notification: "{self.notification_name}"'


class Notification(NotificationKey):
    _SHORT_MESSAGE_MAX_LEN = 150
    _EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def __init__(self,
                 sender_service: str,     # which service is sending the notification
                 notification_name: str,  # how the service will name the notification (in communications)
                 severity: Union[Severity, str],  # how often the notification should be reminded to the recipients
                 short_message: str,  # summary of the message (ideally less than 150 chars)
                 long_message: str,  # what will be displayed (can and should use html)
                 recipients: List[str],   # who to send the notification to
                 client_id: Union[str, None] = None,  # which client is concerned by this notification
                 send_on_activation: bool = False,  # whether this notification must be sent when it becomes active
                 trigger_date: Union[datetime, None, str] = None,  # the last time this notification became active
                 end_date: Union[datetime, None, str] = None,  # when this notification expires. Str format corresponds to https://github.com/arcane-run/Working-Standards/blob/master/BestPractices/Microservices/WorkingWithDatetimes.md
                 ):
        """ may raise ValueError in case of invalid parameter type"""
        super(Notification, self).__init__(sender_service=sender_service, notification_name=notification_name)
        self.severity = severity
        self.short_message = short_message
        self.long_message = long_message
        self.recipients = [recipient.lower() for recipient in recipients]
        self.client_id = client_id
        self.send_on_activation = send_on_activation
        self.end_date = end_date
        if trigger_date is None:
            self._trigger_date = None
        else:
            self.trigger_date = trigger_date

    def to_dict(self):
        """ returns a dict of the type notification"""
        return dict(sender_service=self.sender_service,
                    notification_name=self.notification_name,
                    severity=self.severity.value,
                    short_message=self.short_message,
                    long_message=self.long_message,
                    recipients=self.recipients,
                    client_id=self.client_id,
                    send_on_activation=self.send_on_activation,
                    trigger_date=self.trigger_date,
                    end_date=self.end_date)

    @property
    def severity(self) -> Severity:
        return self._severity

    @severity.setter
    def severity(self, severity: Union[Severity, str]):
        if not isinstance(severity, Severity):
            try:
                severity = SEVERITY_MAPPING[severity]
            except KeyError:
                raise ValueError(
                    f'serenity should be one of {list(SEVERITY_MAPPING.keys())} '
                    f'and not "{severity}"')
        self._severity = severity

    @property
    def short_message(self) -> str:
        return self._short_message

    @short_message.setter
    def short_message(self, short_message: str):
        if len(short_message) > self.__class__._SHORT_MESSAGE_MAX_LEN:
            logging.warning(f'short_message for  has '
                            f'{len(short_message)} characters which is more than '
                            f'the {self.__class__._SHORT_MESSAGE_MAX_LEN} currently allowed')
        elif len(short_message) == 0:
            raise ValueError('short_message cannot be empty.')
        self._short_message = short_message

    @property
    def long_message(self) -> str:
        return self._long_message

    @long_message.setter
    def long_message(self, long_message: str):
        if len(long_message) == 0:
            raise ValueError('long_message cannot be empty.')
        self._long_message = long_message

    @property
    def recipients(self) -> List[str]:
        return self._recipients

    @recipients.setter
    def recipients(self, recipients: List[str]):
        new_recipients_value = []
        for recipient_index, recipient in enumerate(recipients):
            if not isinstance(recipient, str):
                logging.error(f'recipients {recipient_index} of notification '
                              f'should be a string and not {type(recipient)}')
                continue
            # basic verification of parseaddr
            # returns a tuple real_name, email_address
            _, parsed_address = parseaddr(recipient)
            if not self.__class__._EMAIL_REGEX.match(parsed_address):
                logging.error(f'recipients {recipient_index} of notification has invalid email '
                              f'{parsed_address}')
                continue
            new_recipients_value.append(parsed_address)
        if not new_recipients_value:
            raise ValueError(f'notification should have at least 1 recipient')
        self._recipients = new_recipients_value

    @property
    def trigger_date(self) -> datetime:
        return self._trigger_date

    @trigger_date.setter
    def trigger_date(self, trigger_date: Union[datetime, str]):
        self._set_date('_trigger_date', trigger_date)

    @property
    def end_date(self) -> Union[datetime, None]:
        return self._end_date

    @end_date.setter
    def end_date(self, end_date: Union[datetime, None, str]):
        if end_date is None:
            self._end_date = None
        else:
            self._set_date('_end_date', end_date)

    def _set_date(self, property_name: str, value: Union[datetime, str]) -> None:
        """ checks that the value is a datetime or datetime like and """
        if isinstance(value, datetime):
            setattr(self, property_name, value)
            return
        elif not isinstance(value, str):
            raise ValueError(
                f'{property_name} should be one of types <None>, <str>, <datetime> and not {type(value)}')
        try:
            datetime_value = isoparse(value)
        except ValueError as e:
            raise ValueError(
                f"Failed to parse {property_name}, invalid string : {e}")
        setattr(self, property_name, datetime_value)


class NotificationDB(Notification):
    def __init__(self,
                 recipients_start_date: Optional[Dict[str, datetime]] = None,
                 **kwargs
                ):
        super().__init__(**kwargs)
        self.recipients_start_date: Dict[str, datetime] = recipients_start_date if recipients_start_date is not None else {}

    def to_dict(self):
        super_dict = super().to_dict()
        super_dict['recipients_start_date'] = self.recipients_start_date
        return super_dict
