import covidcountydata as ccd


def multiple_dataset_all(c=ccd.Client()):
    """
    This example loads multiple datasets (demographics and covid) for all
    us fips
    """
    c.demographics().covid_us(limit=100, order="location")
    df = c.fetch()
    return df


def multiple_dataset_states_only(c=ccd.Client()):
    """
    This example loads multiple datasets (demographics and covid) for all
    us states -- It selects states by only taking fips < 100
    """
    c.demographics().covid_us(location="<100", limit=100)
    df = c.fetch()
    return df


def multiple_dataset_counties_only(c=ccd.Client()):
    """
    This example loads multiple datasets (demographics and covid) for all
    us states -- It selects counties by only taking fips >= 1000
    """
    c.demographics().covid_us(location=">999", limit=100, order="location")
    df = c.fetch()
    return df


def single_dataset_all(c=ccd.Client()):
    """
    This example loads the within county mobility data for all fips
    and all dates
    """
    c.mobility_devices(limit=100)
    df = c.fetch()
    return df


def single_dataset_deaths_filter(c=ccd.Client()):
    """
    This example loads a subset of the demographic data by selecting
    a few variables and a few fips codes
    """
    c.covid_us(location="<100", variable="deaths_total", value=">100", limit=100)
    df = c.fetch()
    return df


def single_dataset_multiplestatesallcounties(c=ccd.Client()):
    """
    This example loads the within county mobility data for all counties
    in multiple states and all dates
    """
    c.mobility_devices(state=["CA", "TX"], limit=100)
    # Could replace "CA" or "TX" with ("Californa", 6, "06") or
    # ("Texas", 48, "48") respectively
    df = c.fetch()
    return df


def single_dataset_onestateallcounties(c=ccd.Client()):
    """
    This example loads the within county mobility data for a single
    state (CA) and all dates
    """

    c.mobility_devices(state="CA", limit=100)
    # Could also do any of the below
    # c.mobility_devices(state=6)
    # c.mobility_devices(state="California")
    # c.mobility_devices(state="06")
    df = c.fetch()
    return df


def single_dataset_variableselect(c=ccd.Client()):
    """
    This example loads a subset of the demographic data by selecting
    a few variables and a few fips codes
    """
    c.demographics(
        variable=[
            "Total population",
            "Fraction of population over 65",
            "Median age",
            "Mean household income",
            "Percent of civilian population with no health insurance",
        ],
        limit=100,
    )
    df = c.fetch()
    return df


def covid_sources(c=ccd.Client()):
    """
    Fetch source for all covid variables
    """
    return c.covid_sources(limit=100).fetch()


def covid_start_date(c=ccd.Client()):
    "fetch all covid for Orange County FL since Sep 1, 2020"
    return c.covid_us(location=12045, dt={"start": "2020-09-01"}).fetch()


def covid_end_date(c=ccd.Client()):
    "Fetch all covid for Orange County FL up to April 1, 2020"
    return c.covid_us(location=12045, dt={"end": "2020-04-01"}).fetch()


def covid_start_end_date(c=ccd.Client()):
    "Fetch all covid for Orange County FL for august 2020"
    return c.covid_us(
        location=12045, dt={"start": "2020-08-01", "end": "2020-08-31"}
    ).fetch()


def covid_start_date_string(c=ccd.Client()):
    "fetch all covid for Orange County FL since Sep 1, 2020"
    return c.covid_us(location=12045, dt=">=2020-09-01").fetch()


def covid_end_date_string(c=ccd.Client()):
    "Fetch all covid for Orange County FL up to April 1, 2020"
    return c.covid_us(location=12045, dt="<=2020-04-01").fetch()
