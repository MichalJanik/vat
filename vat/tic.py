from decimal import Decimal as D
import re
import datetime
from six.moves import urllib
from lxml.html import soupparser

from .vrws import Rate, Rates

TIC_VATRATES_HISTORY = str('https://ec.europa.eu/taxation_customs/tic/public/vatRates/history.html?msa=')

_percent_re = re.compile(r'^(\d+\.*\d*)?%$')
_date_re = re.compile(r'^([0-9]{2})/([0-9]{2})/([0-9]{2,})$')


class TICException(Exception):
    pass


class TICHTTPException(TICException):
    def __init__(self, code, headers, body):
        self.code = code
        self.headers = headers
        self.body = body

    def __repr__(self):
        return 'TICHTTPException(%r, %r, %r)' % (self.code,
                                                 self.headers,
                                                 self.body)


type_classes = ['', 'noBorderBottom', 'noBorderTopAndBottom', 'noBorderTop']
rate_classes = ['rate', 'rate noBorderBottom', 'rate noBorderTopAndBottom',
                'rate noBorderTop']
date_classes = ['rateCell', 'rateCell noBorderBottom',
                'rateCell noBorderTopAndBottom', 'rateCell noBorderTop']

msa_map = {
    'AT': 1,
    'BE': 2,
    'BG': 3,
    'CY': 4,
    'CZ': 5,
    'DE': 6,
    'DK': 7,
    'EE': 8,
    'EL': 9,
    'ES': 10,
    'FI': 11,
    'FR': 12,
    'HR': 14,
    'HU': 15,
    'IE': 16,
    'IT': 17,
    'LT': 18,
    'LU': 19,
    'LV': 20,
    'MT': 21,
    'NL': 22,
    'PL': 23,
    'PT': 24,
    'RO': 25,
    'SE': 26,
    'SI': 27,
    'SK': 28
}


def get_rates(country, typeVR=None):
    """
    Retrieve the VAT rates for the specified country.  Returns a Rates object
    on success, or in case of error raises an exception.
    """
    url = str('{}{}'.format(TIC_VATRATES_HISTORY, msa_map[country]))
    req = urllib.request.Request(url)

    response = urllib.request.urlopen(req)

    status = response.getcode()

    if status != 200:
        raise TICHTTPException(status, response.info(), response.read())

    body = response.read()

    return parse_response(body, typeVR=typeVR)


def parse_response(response, typeVR=None):
    xml = soupparser.fromstring(response)

    type_values = []
    if typeVR is None:
        type_values.extend(('Standard', 'Reduced'))
    else:
        type_values.append(typeVR)

    types = {}
    categories = {}

    rows = xml.find('.//table[@id="categoriesRate"]/tbody')
    for row in rows:
        category = row.find('.//td[@colspan="4"]')
        if category is not None:
            rcategory = ''.join(category.itertext()).strip()
            continue

        for data in row:
            if data.attrib.get('class') in type_classes:
                text = ''.join(data.itertext()).strip()
                if any(vrtype in text for vrtype in ['Standard', 'Reduced']):
                    rdetail = None
                    if '\n' in text:
                        rtype, rdetail = text.split('\n', 1)
                        rdetail = rdetail.strip()
                    else:
                        rtype = text

            elif data.attrib.get('class') in rate_classes:
                value = ''.join(data.itertext()).strip()
                re_value = _percent_re.match(value)
                if not re_value:
                    raise TICException("didn't understand rate %s" % re_value)
                rvalue = D(re_value.group(1)).quantize(D('.1'))

            elif data.attrib.get('class') in date_classes:
                rdate = ''.join(data.itertext()).strip()
                m = _date_re.match(rdate)
                rdate = datetime.date(int(m.group(3)),
                                      int(m.group(2)),
                                      int(m.group(1)))

        if rcategory and rtype and rvalue and rdate:
            robj = Rate(rvalue, rdate, rdetail)
            if rtype in type_values:
                categories.setdefault(rcategory, []).append(robj)
                types.setdefault(rtype, []).append(robj)
            rdate = rvalue = None

    return Rates(types, categories)
