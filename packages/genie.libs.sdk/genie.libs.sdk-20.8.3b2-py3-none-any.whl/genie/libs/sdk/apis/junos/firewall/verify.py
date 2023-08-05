"""Common verify functions for firewall"""

# Python
import re
import logging
import operator

# Genie
from genie.utils import Dq
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def verify_firewall_filter(
    device: object, 
    expected_filter: str,
    max_time: int = 60,
    check_interval: int = 10,
    invert: bool = False,
    ) -> bool:
    """Verify firewall filter exists

    Args:
        device (object): Device object
        expected_filter (str): Filter to check for
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        invert (bool, optional): Invert function. Defaults to False.

    Returns:
        bool: True/False
    """

    op = operator.contains
    if invert:
        op = lambda filters, ex_filter : operator.not_(operator.contains(filters, ex_filter))

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show firewall')
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "firewall-information": {
        #     "filter-information": [
        #         {
        #             "filter-name": str,

        filters_ = out.q.get_values('filter-name')
        if op(filters_, expected_filter):
            return True
        
        timeout.sleep()
    return False

def verify_firewall_packets(
    device: object, 
    expected_packet_count: int,
    filter: str,
    counter_name: str,
    max_time: int = 60,
    check_interval: int = 10,
    invert: bool = False,
    ) -> bool:
    """Verify firewall filter exists

    Args:
        device (object): Device object
        expected_packet_count (int): Expected packets to find
        filter (str): Filter to check
        counter_name (str): Counter name to check
        max_time (int, optional): Maximum timeout time. Defaults to 60.
        check_interval (int, optional): Check interval. Defaults to 10.
        invert (bool, optional): Invert function. Defaults to False.

    Returns:
        bool: True/False
    """

    op = operator.eq
    if invert:
        op = operator.ne

    expected_packet_count = int(expected_packet_count)

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show firewall counter filter {filter} {counter_name}'.format(
                filter=filter,
                counter_name=counter_name,
            ))
        except SchemaEmptyParserError:
            timeout.sleep()
            continue

        # Example dict
        # "firewall-information": {
        #     "filter-information": [
        #         {
        #           Optional("counter"): {
        #               "packet-count": str

        packet_count_ = out.q.get_values('packet-count', 0)
        if packet_count_:
            packet_count_ = int(packet_count_)
        if op(expected_packet_count, packet_count_):
            return True
        
        timeout.sleep()
    return False
