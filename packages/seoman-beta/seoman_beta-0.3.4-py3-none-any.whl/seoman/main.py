import typer
from typing import Optional, List
from . import auth

from .utils.date_utils import (
    days_last_util,
    create_date,
    get_today,
    get_day_granularity,
    process_date,
)
from .utils.completion_utils import (
    dimensions,
    export_type,
    searchtype,
    month_complete,
)

from .utils.query_builder import query_builder

app = typer.Typer(add_completion=False, name="Seoman")


@app.command("auth")
def get_auth():
    """
    Get authenticated.
    """

    auth.get_authenticated()


@app.command("top-keywords")
def top_keywords(
    url: str = typer.Option(..., help="That's how world wide web works."),
    days_last: int = typer.Option(None, help="Show information from last given days."),
    days_from: str = typer.Option(
        None,
        help="Show information till today from given date.",
    ),
    search_type: str = typer.Option(
        None, help="Search type ", autocompletion=searchtype
    ),
    export_type: str = typer.Option(
        None,
        help="Specify export type ",
        autocompletion=export_type,
    ),
    row_limit: int = typer.Option(
        None, help="Maximum number of rows to return [Default is 1,000] "
    ),
    start_row: int = typer.Option(None, help="Set starting index [Default is 0]"),
    filter_dimension: List[str] = typer.Option(
        None,
        help="The dimension that this filter applies to. [Example: searchAppearance]",
    ),
    filter_operator: str = typer.Option(
        None,
        help="How your specified value must match the dimension value for the row. [Example: contains, equals]",
    ),
    filter_expression: List[str] = typer.Option(
        None, help="The value for the filter to match or exclude."
    ),
    granularity: str = typer.Option(
        None,
        help="Enter a parameter for granularating [Example: daily, twodaily, monday, tuesday, weekdays, weekends]",
    ),
):
    """
    Show top keywords from given url
    """

    service = auth.load_service()
    service.update_body({"dimensions": ["query"]})

    if all([filter_dimension, filter_expression]):
        service.update_body(
            {
                "dimensionFilterGroups": [
                    {
                        "filters": [
                            {"dimension": dimension, "expression": expression}
                            for dimension, expression in zip(
                                filter_dimension, filter_expression
                            )
                        ]
                    }
                ]
            }
        )

    if days_last:
        body = days_last_util(days_last)
        service.update_body(body)

    if search_type:
        service.update_body({"searchType": search_type})

    if row_limit:
        service.update_body({"rowLimit": row_limit})

    if start_row:
        service.update_body({"startRow": start_row})

    service.concurrent_query_asyncio(url=url, granularity=granularity)

    service.export(export_type=export_type, url=url, command="top-keywords")


@app.command("manuel")
def manuel(
    url: str = typer.Option(..., help="That's how world wide web works."),
    start_date: str = typer.Option(
        None, help="Give a date to start [Example: 2020-03, 2 months ago, 4 ay önce]"
    ),
    end_date: str = typer.Option(
        None,
        help="Give a date to end [Example: 2020-08-11, 23 hours ago, yaklaşık 23 saat önce]",
    ),
    search_type: str = typer.Option(
        None, help="Search type ", autocompletion=searchtype
    ),
    dimensions: List[str] = typer.Option(
        None, help="Add dimensions ", autocompletion=dimensions
    ),
    row_limit: int = typer.Option(
        None, help="Maximum number of rows to return [Default is 1,000] "
    ),
    start_row: int = typer.Option(None, help="Set starting index [Default is 0]"),
    export_type: str = typer.Option(
        None,
        help="Specify export type ",
        autocompletion=export_type,
    ),
    filter_dimension: List[str] = typer.Option(
        None,
        help="The dimension that this filter applies to. [Example: searchAppearance]",
    ),
    filter_operator: str = typer.Option(
        None,
        help="How your specified value must match the dimension value for the row. [Example: contains, equals]",
    ),
    filter_expression: List[str] = typer.Option(
        None, help="The value for the filter to match or exclude."
    ),
    granularity: str = typer.Option(
        None,
        help="Enter a parameter for granularating [Example: daily, twodaily, monday, tuesday, weekdays, weekends]",
    ),
):

    """
    Top pages in the site
    """
    service = auth.load_service()

    if start_date is not None:
        start = process_date(start_date)
    if end_date is not None:
        end = process_date(end_date)

    service.update_body({"startDate": start, "endDate": end or get_today()})

    if all([filter_dimension, filter_expression]):
        service.update_body(
            {
                "dimensionFilterGroups": [
                    {
                        "filters": [
                            {"dimension": dimension, "expression": expression}
                            for dimension, expression in zip(
                                filter_dimension, filter_expression
                            )
                        ]
                    }
                ]
            }
        )

    if len(dimensions) >= 1:
        if "all" in dimensions:
            service.update_body(
                {"dimensions": ["date", "page", "query", "country", "device"]}
            )
        else:
            service.update_body({"dimensions": [dimension for dimension in dimensions]})

    if search_type is not None:
        service.update_body({"searchType": search_type})

    if row_limit is not None:
        service.update_body({"rowLimit": row_limit})

    if start_row is not None:
        service.update_body({"startRow": start_row})

    service.concurrent_query_asyncio(url=url, granularity=granularity or "weekly")
    service.export(export_type=export_type, url=url, command="manuel")


@app.command("sites")
def show_sites(
    url: str = typer.Option(None, help="Retrieve information about specific site."),
    export_type: str = typer.Option(
        None,
        help="Specify export type ",
        autocompletion=export_type,
    ),
):
    """
    List all the web sites or the permission level for the specific site that associated with the account.
    """

    service = auth.load_service()

    service.sites(url=url or None)

    service.export(export_type=export_type, command="sites", url=url or "seoman")


@app.command("sitemaps")
def show_sitemap(
    url: str = typer.Option(
        ..., help="The site's URL [Example: http://www.example.com/]"
    ),
    feedpath: str = typer.Option(
        None,
        help="The URL of the actual sitemap [Example: http://www.example.com/sitemap.xml]",
    ),
    export_type: str = typer.Option(
        None,
        help="Specify export type ",
        autocompletion=export_type,
    ),
):
    """
    List sitemaps-entries or get specific the sitemaps.
    """

    service = auth.load_service()

    service.sitemaps(url=url or None, feedpath=feedpath or None)

    service.export(export_type=export_type, command="sitemaps", url=url or "seoman")


@app.command("feedback")
def give_feedback():
    """
    Give us a feedback about your experience.
    """

    import webbrowser

    webbrowser.open(url="https://github.com/zeoagency/seoman/issues/new")


@app.command("get-error")
def get_error():
    """
    Example behaviour for exceptions.
    """

    import webbrowser

    try:
        import ExampleError
    except Exception as e:
        webbrowser.open(url=f"https://www.google.com/search?q={e}")


@app.command("query-builder")
def build_query():
    """
    Build your queries interactively!
    """

    typer.secho(query_builder(), bold=True)


@app.command("version")
def show_version():
    """
    Show version and exit.
    """

    import pkg_resources

    typer.echo(pkg_resources.get_distribution("seoman").version)
