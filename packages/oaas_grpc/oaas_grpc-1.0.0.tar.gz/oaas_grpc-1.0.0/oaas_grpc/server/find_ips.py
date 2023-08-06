from typing import List

import netifaces


def find_ips() -> List[str]:
    result: List[str] = []

    for interface in netifaces.interfaces():
        ifaddresses = netifaces.ifaddresses(interface)

        if netifaces.AF_INET not in ifaddresses:
            continue

        for link in ifaddresses[netifaces.AF_INET]:
            result.append(link["addr"])

    return result
