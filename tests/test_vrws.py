import vat
import pytest

from vat import vrws, rates, tic


def test_vrws_all():
    try:
        for ms in tic.msa_map:
            # E-Services standard tax rate for LU is not provided by vrws
            # since 10-01-2022
            if ms == 'LU':
                continue
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


def test_vrws_lu():
    # E-Services Standard tax rate for LU is not provided by vrws since
    # 10-01-2022. It is still provided by TIC history page so we don't know
    # if vrws issue is only temporary or rate has been removed permanently
    # and E-Sevices has no specific rate anymore. Test will fail in case vrws
    # provides it again.
    try:
        standard_rates = vrws.get_rates('LU', typeVR=vrws.STANDARD)

        assert len(standard_rates.categories) == 2
        assert standard_rates.categories.get('E-Services') is None
        assert len(standard_rates.types.get('Standard')) == 2
    except vat.VRWSHTTPException as e:
        if 500 <= e.code <= 599:
            pytest.skip('EU VRWS server is malfunctioning, so skipping test')
        else:
            raise
