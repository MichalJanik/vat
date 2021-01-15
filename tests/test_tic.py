import vat
import pytest

from vat import vrws, rates, tic
from vat.rates import RateManager


def test_tic():
    rates = RateManager()
    for ms in tic.msa_map:
        try:
            rate = tic.get_rates(ms)
            rate_count = len(rate.types[vrws.STANDARD])
            rate_standard = tic.get_rates(ms, typeVR=vrws.STANDARD)
            rate_standard_count = len(rate_standard.types[vrws.STANDARD])
            eservices_rate1 = rates.category_rate(ms, category=vrws.ESERVICES, source=tic, typeVR=vrws.STANDARD)
            eservices_rate2 = tic.get_rates(ms, typeVR=vrws.STANDARD).categories.get(vrws.ESERVICES)[-1]

            assert isinstance(rate, vat.Rates)
            assert len(rate.types[vrws.STANDARD]) > 0
            assert rate_count == rate_standard_count
            assert eservices_rate1.rate == eservices_rate2.rate
            assert eservices_rate1.application_date == eservices_rate2.application_date
        except vat.TICHTTPException as e:
            if 500 <= e.code <= 599:
                pytest.skip('EU pages are not available, so skipping test')
            else:
                raise


def test_tic_be():
    try:
        rates = tic.get_rates('BE')
        standard_rates = tic.get_rates('BE', typeVR=vrws.STANDARD)
        standard_rate = standard_rates.categories.get('E-Services')[-1].rate
        reduced_rates = tic.get_rates('BE', typeVR=vrws.REDUCED)
        reduced_rate = reduced_rates.categories.get('E-Services')[-1].rate

        assert standard_rate > reduced_rate
        assert len(rates.types[vrws.REDUCED]) > 0
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise


def test_tic_fr():
    try:
        rates = tic.get_rates('FR')
        rates_count = len(rates.types[vrws.STANDARD]) + len(rates.types[vrws.REDUCED])
        rates_standard = tic.get_rates('FR', typeVR=vrws.STANDARD)
        rates_standard_count = len(rates_standard.types[vrws.STANDARD])
        rates_reduced = tic.get_rates('FR', typeVR=vrws.REDUCED)
        rates_reduced_count = len(rates_reduced.types[vrws.REDUCED])
        detail1 = rates.types[vrws.REDUCED][0].detail
        detail2 = rates.types[vrws.REDUCED][1].detail

        assert detail1 != detail2
        assert len(rates.types[vrws.REDUCED]) > 0
        assert rates_count == rates_standard_count + rates_reduced_count
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise
