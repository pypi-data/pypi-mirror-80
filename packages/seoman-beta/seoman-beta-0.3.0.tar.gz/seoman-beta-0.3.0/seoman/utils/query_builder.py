import typer

from seoman.utils.date_utils import process_date

from typing import List


def process(filter_str: str) -> List[str]:

    if ":" in filter_str:
        filter_str = [
            [filters.strip() for filters in temp.split(",")]
            for temp in filter_str.split(":")
        ]
    else:
        filter_str = [filters.strip() for filters in filter_str.split(",")]

    filters = [
        filter_list
        for filter_list in filter_str
        if len(filter_list) > 1 and "" not in filter_list
    ]

    return [
        f"--filter-dimension {filter}"
        if filter in ["page", "query", "date", "device", "country"]
        else f"--filter-operator {filter}"
        if filter in ["contains", "equals", "notContains", "notEquals"]
        else f"--filter-expression {filter}"
        for filter_list in filters
        for filter in filter_list
    ]


def query_builder() -> str:
    typer.secho(
        """
    FORMATTING AND TIPS

    GENERAL FORMATTING
        [Tip] You are not supposed to answer questions if it is not [REQUIRED] 
        If you want to skip that question, just press space then enter.

    URL
        [Formatting: sc-domain:example.com or https://example.com]

    DATES
        [Formatting] Dates are in YYYY-MM-DD format.
        [Example] 23 march 2020 | 2020-03-10 | 2 weeks and 4 months ago 

    FILTERS
        [Formatting] If you want to add multiple filters split them by ':' 
        [Example] country, equals, FRA : device, notContains, tablet
        [Suggested Format] dimensions, operator, expression
    
    GRANULARITY
        Granularity specifies the frequency of the data, higher frequency means higher response time.
        You must enter a one parameter.
        [Valid Parameters] daily, twodaily, threedaily, fourdaily, fivedaily, sixdaily, weekly, twoweekly, threeweekly, monthly, twomonthly, quarterly, yearly
        [Valid Parameters] monday, tuesday, wednesday, thursday, friday, saturday, sunday, weekends, weekdays
        [Examples] If you specify 'monday' seoman returns results only from mondays between start date and end date.
        [Examples] If you specify 'fivedaily' it sends splits your date range by 5 then runs unique queries.
        if your start date is 2020-03-10 and the end date is 2020-04-10 it first sends query for 03-10 to 03-15 then 03-15 to 03-20 then merges them all.   

    DIMENSIONS
        [Valid Parameters] page, query, date, device, country | for simplicity you can type 'all' to include all of them.
    
    EXPORT TYPE
        [Valid Parameters] excel, csv, json, tsv, sheets.

    ROW LIMIT
        [Valid Parameters] Must be a number from 1 to 25000.

    START ROW 
        [Valid Parameters] Must be a non-negative number.

    """,
        fg=typer.colors.BRIGHT_GREEN,
        bold=True,
    )
    url = typer.prompt("[Required] The site's URL ")
    end_date = typer.prompt("[Required] Start date of the requested date range")
    start_date = typer.prompt("[Required] End date of the requested date range")
    dimensions = typer.prompt("Zero or more dimensions to group results by ")
    filters = typer.prompt(
        "Zero or more groups of filters to apply to the dimension grouping values"
    )
    granularity = typer.prompt("Set a frequency or group your queries.")
    start_row = typer.prompt("Zero-based index of the first row in the response")
    row_limit = typer.prompt("The maximum number of rows to return")
    search_type = typer.prompt("The search type to filter for ")
    export_type = typer.prompt("The export type for the results ")

    query = ["seoman", "manuel"]
    all_dimensions = ["page", "query", "date", "device", "country"]
    all_granularities = [
        "daily",
        "twodaily",
        "threedaily",
        "fourdaily",
        "fivedaily",
        "sixdaily",
        "weekly",
        "twoweekly",
        "threeweekly",
        "monthly",
        "twomonthly",
        "quarterly",
        "yearly",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "weekends",
        "weekdays",
    ]

    if len(url) > 5:
        query.append(f"--url {url.strip()}")

    if start_date.strip() != "":
        query.append(f"--start-date {process_date(start_date)}")

    if end_date.strip() != "":
        query.append(f"--end-date {process_date(end_date)}")

    if dimensions.strip() != "":
        new_dimensions = [dim.strip() for dim in dimensions.split(",") if dim != ""]

        if "all" in new_dimensions:
            for dimension in all_dimensions:
                query.append(f"--dimensions {dimension}")
        else:
            for dimension in new_dimensions:
                if dimension in all_dimensions:
                    query.append(f"--dimensions {dimension}")

    if granularity.strip() != "" and granularity.strip().lower() in all_granularities:
        query.append(f"--granularity {granularity.strip().lower()}")

    if filters.strip() != "":
        grouped_filters = query.extend(process(filters))

    if start_row.strip() != "" and start_row.isnumeric():
        query.append(f"--start-row {start_row.strip()}")

    if row_limit.strip() != "" and row_limit.isnumeric():
        query.append(f"--row-limit {row_limit.strip()}")

    if search_type.strip() != "":
        query.append(f"--search-type {search_type.strip().lower()}")

    if export_type.strip() != "":
        query.append(f"--export-type {export_type.lower().strip()}")

    typer.secho("\nYour query is ready\n", fg=typer.colors.BRIGHT_GREEN, bold=True)
    return " ".join(query)
