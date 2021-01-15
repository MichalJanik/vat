import datetime
from decimal import Decimal as D

from . import vrws
from . import tic


class RateManager(object):
    """
    Manages VAT rates fetched from europa.eu's VATRateWebService/vatRates URLs.
    """

    def _get_rates(self, member_state, source=None, typeVR=None):
        """Retrieve the set of rates for the given member state."""
        if not isinstance(member_state, str):
            member_state = member_state.code
        today = datetime.date.today()

        if source is None:
            try:
                rates = vrws.get_rates(member_state, date=today, typeVR=typeVR)
            except vrws.VRWSException:
                rates = tic.get_rates(member_state, date=today, typeVR=typeVR)

        elif source == vrws:
            try:
                rates = vrws.get_rates(member_state, date=today, typeVR=typeVR)
            except vrws.VRWSException:
                raise

        elif source == tic:
            try:
                rates = tic.get_rates(member_state, typeVR=typeVR)
            except tic.TICException:
                raise

        return rates

    @staticmethod
    def _best_rate(rates):
        """Selects current rate from the list of obtained rates."""
        today = datetime.date.today()
        rate_date = None
        best_rate = None
        for rate in rates:
            if rate.application_date > today:
                continue
            if rate_date is None or rate.application_date >= rate_date:
                rate_date = rate.application_date
                best_rate = rate
        return best_rate

    def standard_rates(self, member_state):
        """
        Retrieve the set of standard rates for the given member state.

        N.B.: This method returns a LIST of rates, and you should use the
        date and detail information to find the appropriate one.  There may
        be multiple rates with different application dates, *and* there may
        be rates with detail specifications in the list.
        """
        rates = self._get_rates(member_state)
        return rates.types.get(vrws.STANDARD, [])

    def standard_rate(self, member_state):
        """Return today’s ordinary standard rate for the given member state."""
        return self._best_rate(self.standard_rates(member_state))

    @staticmethod
    def _to_rate(rate_info, the_date):
        if isinstance(rate_info, tuple):
            return vrws.Rate(rate_info[0], the_date, rate_info[1])
        else:
            return vrws.Rate(rate_info, the_date, None)

    def reduced_rates(self, member_state):
        """
        Retrieve the set of reduced rates for the given member state.

        N.B.: This method returns a LIST of rates, and you should use the
        date and detail information to find the appropriate one.  There may
        be multiple rates with different application dates, *and* there may
        be rates with detail specifications in the list.
        """
        rates = self._get_rates(member_state)
        rates = rates.types.get(vrws.REDUCED, None)
        return rates

    def reduced_rate(self, member_state):
        """Return today’s ordinary reduced rate for the given member state."""
        return self._best_rate(self.reduced_rates(member_state))

    def category_rates(self, member_state, category, source=None, typeVR=None):
        """
        Retrieve the set of rates for the given member state and category.

        N.B.: This method returns a LIST of rates, and you should use the
        date and detail information to find the appropriate one.  There may
        be multiple rates with different application dates, *and* there may
        be rates with detail specifications in the list.
        """
        rates = self._get_rates(member_state, source, typeVR)
        return rates.categories.get(category, [])

    def category_rate(self, member_state, category, source=None, typeVR=None):
        """Return today’s rate for the given member state and category."""
        return self._best_rate(self.category_rates(member_state,
                                                   category,
                                                   source,
                                                   typeVR))

    def categories(self, member_state):
        """Return a list of categories for the given member state."""
        rates = self._get_rates(member_state)
        return list(rates.categories)
