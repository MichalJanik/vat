import vat
import pytest

from vat import vrws, rates, tic


def test_vrws_all():
    try:
        for ms in tic.msa_map:
            rates = vrws.get_rates(ms)
            rates_eservices = vrws.get_rates(ms, category=vrws.ESERVICES)

            assert isinstance(rates, vat.Rates)
            assert len(rates.types[vrws.STANDARD]) > 0
            assert len(rates_eservices.types[vrws.STANDARD]) == 1
            assert rates_eservices is not None
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise


def test_vrws_be():
    try:
        rates = vrws.get_rates('BE')
        standard_rates = vrws.get_rates('BE', typeVR=vrws.STANDARD)
        standard_rate = standard_rates.categories.get('E-Services')[0].rate
        reduced_rates = vrws.get_rates('BE', typeVR=vrws.REDUCED)
        reduced_rate = reduced_rates.categories.get('E-Services')[0].rate

        assert standard_rate > reduced_rate
        assert len(rates.types[vrws.REDUCED]) > 0
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise


def test_vrws_fr():
    try:
        rates = vrws.get_rates('FR')
        rates_count = len(rates.types[vrws.STANDARD]) + len(rates.types[vrws.REDUCED])
        rates_standard = vrws.get_rates('FR', typeVR=vrws.STANDARD)
        rates_standard_count = len(rates_standard.types[vrws.STANDARD])
        rates_reduced = vrws.get_rates('FR', typeVR=vrws.REDUCED)
        rates_reduced_count = len(rates_reduced.types[vrws.REDUCED])
        rates_eservices = vrws.get_rates('FR', category=vrws.ESERVICES)
        detail1 = rates.types[vrws.REDUCED][0].detail
        detail2 = rates.types[vrws.REDUCED][1].detail

        assert detail1 != detail2
        assert len(rates.types[vrws.REDUCED]) > 0
        assert len(rates_eservices.categories.keys()) == 1
        assert rates_count == rates_standard_count + rates_reduced_count
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise
