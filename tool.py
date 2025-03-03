"""
title: Currency Converter
author: @freerainboxbox
author_url: https://github.com/freerainboxbox
git_url: https://github.com/freerainboxbox/owui-currency-tool
description: Enables basic fetching of forex data for live and historic currency conversion.
requirements: currencyconverter
version: 0.0.1
"""

from currency_converter import CurrencyConverter, ECB_URL, SINGLE_DAY_ECB_URL
from pydantic import BaseModel, Field
from typing import String, Optional, Type
from enum import Enum
from datetime import date


class Direction(Enum):
    """
    This enum represents the direction of currency conversion between Currency A and Currency B.
    """

    A_TO_B = 0
    B_TO_A = 1


class Tools:
    """
    This class represents a tool that can be integrated into the Open WebUI to perform currency conversions.

    Attributes:
        valves (Valves): A subclass of BaseModel containing configurable parameters for the tool.

    Methods:
        __init__: Initializes the Tool with default settings or provided configurations.
    """

    class Valves(BaseModel):
        """
        This inner class defines the configurable parameters, or "valves", that can be adjusted
        by admins in the Open WebUI interface. It includes a default currency for conversions.

        Attributes:
            default_currency (str): The default currency code to use for conversions.
                                  Defaults to 'USD' if not specified.
        """

        default_currency: str = Field(
            "",
            description="Default currency code for conversions, when only one source or target is specified.",
        )

    def __init__(self):
        """
        Initializes the Tool instance with provided configurations or defaults.

        Args:
            **kwargs: Arbitrary keyword arguments that can be used to configure the tool's valves.
                    If no 'default_currency' is provided, it will default to 'USD'.
        """
        self.valves = self.Valves()

    def convert(
        self,
        direction: Direction,
        source_amount: float,
        a_currency_code: str,
        b_currency_code: Optional[str] = None,
        date: Optional[date] = None,
    ) -> str:
        """
        Converts the given amount from one currency to another based on the specified conversion rate.

        Args:
            direction (Direction): The direction of the conversion.
            source_amount (float): The amount in the source currency.
            a_currency_code (str): The code for Currency A.
            b_currency_code (Optional[str]): The code for the Currency B. If not provided, it will use the default currency.
            date (Optional[datetime.date]): The date of the conversion rate to be used. If not provided, it will use the latest available rate.

        Returns:
           str: The converted amount in the target currency. The user should see this value rounded to two decimal places (or whatever is appropriate for their country), though this tool will return the raw conversion.
           e.g.:
           - 3.33333... USD raw output -> 3.33 USD
           - 434.3434... JPY raw output -> 434 JPY (which has no decimal places)
           Errors will be returned as strings that are a description of the error.
        """
        if b_currency_code is None:
            if self.valves.default_currency == "":
                return "Error: No default currency set. Either set a default currency or specify two currency codes."
            b_currency_code = self.valves.default_currency
        c = None
        try:
            if date is None:
                c = CurrencyConverter(SINGLE_DAY_ECB_URL)
            else:
                c = CurrencyConverter(date)
        except Exception as e:
            return (
                "Error: Problem initializing conversion utility.\n===============================================\n"
                + str(e)
            )
        source_code = None
        target_code = None
        if direction == Direction.A_TO_B:
            source_code = a_currency_code
            target_code = b_currency_code
        else:
            source_code = b_currency_code
            target_code = a_currency_code
        try:
            if date is None:
                return c.convert(source_amount, source_code, target_code)
            else:
                return c.convert(source_amount, source_code, target_code, date=date)
        except Exception as e:
            return (
                "Error: Problem converting currency.\n===================================\n"
                + str(e)
            )
