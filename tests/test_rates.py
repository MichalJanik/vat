import vat
import pytest

from vat import vrws, rates, tic
from vat.rates import RateManager


def test_rates():
    rates = RateManager()
    try:
        for ms in tic.msa_map:
            rate = rates._get_rates(ms)
            categories = rates.categories(ms)
            eservices_rate1 = rates.category_rate(
                ms, category=vrws.ESERVICES, typeVR=vrws.STANDARD)
            eservices_rate2 = rates._get_rates(
                ms, typeVR=vrws.STANDARD).categories.get(vrws.ESERVICES)[0]

            assert isinstance(rate, vat.Rates)
            assert len(rate.types[vrws.STANDARD]) > 0
            assert vrws.ESERVICES in categories
            assert eservices_rate1.rate == eservices_rate2.rate
            assert eservices_rate1.application_date == eservices_rate2.application_date
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise e


def test_rates_vrws_tic():
    rates = RateManager()
    for ms in tic.msa_map:
        try:
            vrws_standard = vrws.get_rates(ms, typeVR=vrws.STANDARD)
            vrws_standard_rate = vrws_standard.categories.get(vrws.ESERVICES)[0].rate
            tic_standard = tic.get_rates(ms, typeVR=vrws.STANDARD)
            tic_standard_rate = tic_standard.categories.get(vrws.ESERVICES)[-1].rate
            category_vrws = rates.category_rate(
                ms, category=vrws.ESERVICES, source=vrws, typeVR=vrws.STANDARD)
            category_tic = rates.category_rate(
                ms, category=vrws.ESERVICES, source=tic, typeVR=vrws.STANDARD)

            assert vrws_standard_rate == tic_standard_rate
            assert category_vrws.rate == category_tic.rate
            assert category_vrws.application_date == category_tic.application_date
            assert category_vrws.detail == category_tic.detail
        except (vat.VRWSHTTPException, vat.TICHTTPException) as e:
            if 500 <= e.code <= 599:
                pytest.skip('EU server is malfunctioning, so skipping test')
            else:
                raise
