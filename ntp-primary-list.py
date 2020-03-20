import argparse
import requests
import socket
import sys
import collections
import pycountry
import ntplib
from ntplib import ref_id_to_text
from ntplib import NTPException


base = "http://support.ntp.org"

ntp_servers = collections.defaultdict(list)
countries = ["fr", "us", "de", "ie ", "nl", "uk", "gb", "ch"]


def country_code_to_name(code):
    """
    Convert country code to human readable name
    """
    if code is None:
        return None
    code = code.strip()
    name = [i.name for i in list(pycountry.countries) if i.alpha_2.lower() == code]
    if len(name) == 0:
        return None
    return name[0] if code is not None else None


def ntp_request(host):
    """
    Request NTP server host to retrieve attributes
    """
    try:
        socket.getaddrinfo(host, "ntp")
    except socket.gaierror as error:
        sys.stderr.write("Cannot resolve host '{}': {}\n".format(host, error))
        sys.stderr.flush()
        return None

    client = ntplib.NTPClient()
    attrs = {}
    try:
        response = client.request(host)

        # print("{host}: offset={offset},delay={delay},root_delay={root_delay},leap={leap},version={version}".format(
        #     host=host,
        #     offset=response.offset,
        #     delay=response.delay,
        #     root_delay=response.root_delay,
        #     leap=response.leap,
        #     version=response.version
        # ))

        for attr in [
            "offset",
            "delay",
            "root_delay",
            "leap",
            "version",
            "stratum",
            "mode",
            "ref_id",
        ]:
            attrs[attr] = getattr(response, attr)

        attrs["ref_id"] = ref_id_to_text(attrs["ref_id"], attrs["stratum"])
    except NTPException as error:
        pass

    return NTPResponse(host, **attrs)


class NTPResponse(object):
    """
    Class represent a NTP response packet object
    """

    def __init__(self, host, country_code=None, *largs, **kwargs):
        self.host = host
        self.country = country_code_to_name(country_code)
        self.attrs = kwargs

    @property
    def offset(self):
        return self.attrs.get("offset")

    @property
    def delay(self):
        return self.attrs.get("delay")

    @property
    def root_delay(self):
        return self.attrs.get("root_delay")

    @property
    def version(self):
        return self.attrs.get("version")

    def __str__(self):
        return "NTPResponse(host={host}, attrs={attrs})".format(
            host=self.host, attrs=self.attrs
        )

    def __repr(self):
        return "<{}>".format(self.__str__())


def ntp_get_hostname(url):
    """
    Scrap Hostname
    """
    hostname = None

    data = requests.get(url)
    prev_line = ""
    for line in iter(data.text.splitlines()):
        if "Hostname" in prev_line:
            hostname = line
        prev_line = line

    return hostname


def ntp_request_s1():
    """
    Scrap StartumOne Time Servers
    """
    data = requests.get(
        "{base}/bin/view/Servers/StratumOneTimeServers".format(base=base)
    )
    html = data.text
    for line in html.split("\n"):
        for country in [c.upper() for c in countries]:
            if country in line:
                fields = line.split()
                link = fields[-3]
                if link.startswith("href"):
                    link = link.split("=")[1].replace('"', "")
                    link = base + link
                    ntp_servers[country].append(link)

    for country in sorted(countries):
        print("Country: {}({})".format(country_code_to_name(country), country))
        for server in ntp_servers[country.strip().upper()]:
            host = ntp_get_hostname(server)
            resp = ntp_request(host) if "." in host else None
            print(resp)

        print()


def main():

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    ntp_request_s1()

    # request most famous ntp sources
    print(ntp_request("time.google.com"))
    print(ntp_request("time.facebook.com"))
    print(ntp_request("time.apple.com"))
    print(ntp_request("time.windows.com"))
    print(ntp_request("0.amazon.pool.ntp.org"))
    print(ntp_request("0.freebsd.pool.ntp.org"))
    print(ntp_request("0.netbsd.pool.ntp.org"))
    print(ntp_request("0.openbsd.pool.ntp.org"))
    print(ntp_request("0.centos.pool.ntp.org"))
    print(ntp_request("0.gentoo.pool.ntp.org"))
    print(ntp_request("0.ubuntu.pool.ntp.org"))
    print(ntp_request("0.debian.pool.ntp.org"))


if __name__ == "__main__":
    sys.exit(main())
