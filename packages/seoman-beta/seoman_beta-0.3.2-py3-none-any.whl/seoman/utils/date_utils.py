from datetime import datetime, timedelta, date
from typing import Optional, Dict, List, Optional, Union
from typer import secho, confirm, colors, prompt
from dateparser import parse


def get_start_date(days: int) -> str:
    """
    Create a start and end day. If days is 60 it will return timedelta(days=60) - datetime.today()
    """
    return str(datetime.today().date() - timedelta(days=days))


def get_today() -> str:
    """
    Get todays date.
    """
    return str(datetime.today().date())


def days_last_util(days: int) -> Dict[str, str]:
    """
    Create a start and end day.
    """
    startDate = get_start_date(days)
    endDate = get_today()
    return {"startDate": startDate, "endDate": endDate}


def create_date(year: str = None, month: str = None) -> str:
    """
    Create a datetime from given year and month if both params are None, use datetime.year.
    """
    if year and month:
        return f"{year}-{month}-01"
    if year:
        return f"{year}-01-01"
    if month:
        return f"{datetime.now().year}-{month}-01"
    else:
        return f"{datetime.now().year}-01-01"


def granularity_days(granularity: int, start: date, end: date) -> List[str]:
    """
    Create weekdays or weekends, or specific days from given granularity.
    """
    if isinstance(start, str):
        start = datetime.strptime(start, "%Y-%m-%d").date()
    if isinstance(end, str):
        end = datetime.strptime(end, "%Y-%m-%d").date()
    if granularity in [1, 2, 3, 4, 5, 6, 7]:
        return [
            (start + timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range((end - start).days + 1)
            if (start + timedelta(days=x)).isoweekday() == granularity
        ]

    elif granularity == 67:
        return [
            (start + timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range((end - start).days + 1)
            if (start + timedelta(days=x)).isoweekday() == 6
            or (start + timedelta(days=x)).isoweekday() == 7
        ]

    elif granularity == 12345:
        return [
            (start + timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range((end - start).days + 1)
            if (start + timedelta(days=x)).isoweekday() == 1
            or (start + timedelta(days=x)).isoweekday() == 5
        ]

    elif granularity == 10:
        return [
            (start + timedelta(days=x)).strftime("%Y-%m-%d")
            for x in range((end - start).days + 1)
        ]


# TODO FIX DATE
def create_date_range(
    days: Optional[int] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    granularity: Optional[str] = None,
) -> List[datetime]:
    """
    Creates a list of dates from the given range and granularity
    Example: [2020-03-15, 2020-03-16,...]
    """

    if start is not None and end is not None:
        if granularity is not None:
            if get_weekday_by_name(granularity) != 10:
                granularity = get_weekday_by_name(granularity)
                return granularity_days(granularity=granularity, start=start, end=end)
            else:
                day_interval = get_day_granularity(granularity)

        new_end, new_start = (
            datetime.strptime(end, "%Y-%m-%d").date() + timedelta(days=1),
            datetime.strptime(start, "%Y-%m-%d").date(),
        )

        day_diff = (new_end - new_start).days

        if day_diff < 0:
            secho(
                f"There must be a problem with your start({new_start}) and end date({new_end}).",
                fg=colors.GREEN,
                bold=True,
            )
            secho(
                "Exiting..",
                fg=colors.RED,
            )
            exit()
        if day_interval > day_diff:
            secho(
                f"Your date range is {day_diff}, it can not be smaller than your frequency which is {day_interval}.",
                fg=colors.GREEN,
                bold=True,
            )
            secho(
                "Exiting..",
                fg=colors.RED,
            )
            exit()
        dates = sorted(
            [
                (new_start + timedelta(days=x)).strftime("%Y-%m-%d")
                for x in range(0, abs(day_diff), day_interval)
            ]
        )
        if dates[0] != start:
            dates.insert(0, start)
        if dates[-1] != end:
            dates.append(end)
        return dates

    elif granularity is not None:
        start_date, end_date = create_date(year=2020), get_today()
        granularity = (
            get_weekday_by_name(granularity)
            if get_weekday_by_name(granularity) != 10
            else get_day_granularity(granularity)
        )
        return granularity_days(granularity=granularity, start=start_date, end=end_date)

    elif days is not None:
        return sorted(
            [
                (datetime.today().date() - timedelta(days=x)).strftime("%Y-%m-%d")
                for x in range(days)
            ]
        )


def get_day_granularity(granularity: str) -> int:
    return {
        "daily": 1,
        "twodaily": 2,
        "threedaily": 3,
        "fourdaily": 4,
        "fivedaily": 5,
        "sixdaily": 6,
        "weekly": 7,
        "twoweekly": 14,
        "threeweekly": 21,
        "monthly": 30,
        "twomonthly": 60,
        "quarterly": 90,
        "yearly": 365,
    }.get(granularity, 1)


def get_weekday_by_name(day_name: str) -> int:
    return {
        "monday": 1,
        "tuesday": 2,
        "wednesday": 3,
        "thursday": 4,
        "friday": 5,
        "saturday": 6,
        "sunday": 7,
        "weekends": 67,
        "weekdays": 12345,
    }.get(day_name, 10)


def process_date(dt: Union[str, date, datetime]) -> str:
    """
    Process human readable datetime strings, to date objects then to str in %Y-%m-%d fmt.
    2 months ago -> datetime.date(2020, 7, 22) -> '2020-07-22'
    """
    try:
        new_dt = parse(
            dt, languages={"tr", "en", "pt", "es", "ru", "fr", "de", "it"}
        ).date()
    except AttributeError:
        secho(
            """There must be a problem at your date or the language is not supported yet.""",
            bold=True,
            fg=colors.BRIGHT_RED,
        )
        enter_new = confirm("Do you want to enter a new date?")
        if enter_new:
            new_dt = prompt("Enter here")
            try:
                new_dt = parse(
                    new_dt, languages={"tr", "en", "pt", "es", "ru", "fr", "de", "it"}
                ).date()
            except AttributeError:
                secho(
                    """There must be a problem at your date or the language is not supported yet 😕,you might want to send a feedback with 'seoman feedback' then we can support your language.""",
                    bold=True,
                    fg=colors.BRIGHT_RED,
                )
                exit()
        if enter_new is False:
            secho(
                "Aborting...",
                bold=True,
                fg=colors.BRIGHT_RED,
            )
            exit()

    return new_dt.strftime("%Y-%m-%d")
