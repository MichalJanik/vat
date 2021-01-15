# Python VAT package

Provides range of VAT rates applicable in each Member State of the EU to the supplies of telecommunications, broadcasting and electronically supplied services.

### Source: 
https://ec.europa.eu/ 's VATRateWebService and vatRates URLs.

### How to use in another app:

Insert following into requirements:
```
vat @ git+https://git@github.com/MichalJanik/vat.git@master#egg=vat-{current_version}
```

### Tests:

[Pytest](https://docs.pytest.org/en/stable/index.html) library is used for the purpose.

```
pytest tests/
```

[Pycodestyle](https://pycodestyle.pycqa.org/en/latest/intro.html) library is used to check Python code against some of the style conventions in PEP 8.
```
pycodestyle
```

### Notes about origin and current state:
Library is originally fork of https://github.com/SevoLukas/vat (fork of another library that no longer exists).
Due to inconsistency with europa.eu's VATRateWebService, thorough cleanup was done and only few blocks of code were maintained.

Kept under MichalJanik for easier maintenance.
