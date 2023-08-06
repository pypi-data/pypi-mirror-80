from typing import Dict, Any, List, IO, Optional, Union, Tuple

from .utils.service_utils import create_body_list, path_exists, regenerate_credentials
from .utils.export_utils import Export

from click import progressbar
from typer import secho, colors

from datetime import datetime


class SearchAnalytics:
    def __init__(self, service, credentials) -> None:
        self.service = service
        self.credentials = credentials
        self.data = {}
        self.body = {
            "startRow": 0,
            "rowLimit": 25000,
        }

    def update_body(self, body) -> None:
        """
        Updates the body, that we are going to use in the query
        """

        self.body.update(**body)

    def date(
        self,
        start: Optional[str] = None,
        end: Optional[str] = None,
        days: Optional[int] = None,
        year: Optional[int] = None,
        month: Optional[int] = None,
    ):
        """
        all time low.
        """

        if start and end:
            self.body.update({"startDate": start, "endDate": end})

        elif start:
            self.body.update({"startDate": start, "endDate": get_today()})

        elif days:
            self.body.update(days_last_util(days=days))

        else:
            self.body.update(
                {
                    "startDate": create_date(year=year, month=month),
                    "endDate": get_today(),
                }
            )

        return self

    def dimensions(self, *dimensions: Tuple[str]):
        """
        Update the body with the dimensions,

        Example: service.dimensions('date', 'query', 'country', 'device')
        """

        self.body["dimensions"] = list(dimensions)

        return self

    def search_type(self, search_type: str):
        """
        Set a search type.

        Example: service.search_type('page')
        """

        self.data["searchType"] = search_type

        return self

    def row_limit(self, limit: int) -> None:
        """
        Change the row limit.

        Example: service.row_limit(25000)
        """

        self.body["rowLimit"] = limit

        return self

    def start_row(self, start_row: int) -> None:
        """
        Change the starting row.

        Example: service.start_row(0)
        """

        self.body["startRow"] = start_row

        return self

    def filters(
        self,
        dimension: List[str],
        expression: List[str],
        operator: Optional[List[str]],
    ):

        self.body.update(
            {
                "dimensionFilterGroups": [
                    {
                        "filters": [
                            {
                                "dimension": dimension,
                                "expression": expression,
                                "operator": operator or "equals",
                            }
                            for dimension, expression, operator in zip(
                                dimension, expression, operator
                            )
                        ]
                    }
                ]
            }
        )

        return self

    @regenerate_credentials
    def query(self, url: str):
        """
        Just a simplified wrapper to the searchanalytics
        """

        self.data.update(
            self.service.searchanalytics().query(siteUrl=url, body=self.body).execute()
        )

        return self

    @regenerate_credentials
    def concurrent_query_asyncio(self, url: str, granularity: str = None):
        """
        Run queries concurrently.
        """

        import asyncio
        from googleapiclient.errors import HttpError
        from typer import confirm

        bodies = create_body_list(self.body, granularity=granularity)
        extra_bodies = []

        async def con_query(body, query_type: str):
            start_row = 25000
            try:
                data = (
                    self.service.searchanalytics()
                    .query(siteUrl=url, body=body)
                    .execute()
                )
            except HttpError:
                await asyncio.sleep(2)
                try:
                    data = (
                        self.service.searchanalytics()
                        .query(siteUrl=url, body=body)
                        .execute()
                    )
                except HttpError:
                    await asyncio.sleep(2)
                    try:
                        data = (
                            self.service.searchanalytics()
                            .query(siteUrl=url, body=body)
                            .execute()
                        )
                    except HttpError:
                        pass

            try:
                self.data.setdefault("rows", []).append(data["rows"])

                if len(data["rows"]) > 24999 and query_type == "first":
                    new_body = body.copy()
                    new_body.update({"startRow": 24999})
                    extra_bodies.append(new_body)

            except (KeyError, UnboundLocalError):
                pass

        async def main(body_list: List[Dict[Any, Any]], message: str, query_type: str):
            with progressbar(
                body_list,
                label=message,
                length=len(body_list),
                fill_char="█",
                empty_char=" ",
            ) as bod:
                for body in bod:
                    await con_query(body, query_type=query_type)

        asyncio.run(main(body_list=bodies, message="Fetching data", query_type="first"))

        if len(extra_bodies) >= 1:
            confirm_rows = confirm(
                f"More than 25.000 rows found for {len(extra_bodies)} query, do you want to include them too?"
            )
            if confirm_rows:
                asyncio.run(
                    main(
                        body_list=extra_bodies,
                        message="Fetching more data",
                        query_type="second",
                    )
                )

        return self

    @regenerate_credentials
    def sites(self, url: Union[None, str] = None):
        """
        List all the web sites associated with the account.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sites.html
        """

        if url:
            self.data.update(self.service.sites().get(siteUrl=url).execute())

        else:
            self.data.update(self.service.sites().list().execute())

    @regenerate_credentials
    def sitemaps(self, url: str, feedpath: Union[None, str] = None):
        """
        Lists the sitemaps-entries submitted for the given site.

        Info: https://developers.google.com/resources/api-libraries/documentation/webmasters/v3/python/latest/webmasters_v3.sitemaps.html
        """

        if url and feedpath:
            self.data.update(
                self.service.sitemaps().get(siteUrl=url, feedpath=feedpath).execute()
            )

        elif url:
            self.data.update(self.service.sitemaps().list(siteUrl=url).execute())

    def export(
        self,
        export_type: Union[None, str] = None,
        url: Union[None, str] = None,
        command: Union[None, str] = None,
    ) -> None:
        """
        Specify the export type.
        """
        if self.data == {"rows": []}:
            secho("Results are empty. Exiting...", fg=colors.RED, bold=True)
            quit()

        export_data = Export(self.data)
        export_types = ["csv", "json", "tsv", "sheets", "table"]

        if export_type in ["CSV", "JSON", "TSV", "SHEETS", "TABLE"]:
            export_type = export_type.lower()

        if export_type == "csv":
            export_data.export_to_csv(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "json":
            export_data.export_to_json(
                filename=self._create_filename(
                    url=url, command=command, filetype=export_type
                )
            )

        if export_type == "sheets":
            export_data.export_to_sheets(
                filename=self._create_filename(
                    url=url, command=command, filetype="xlsx"
                )
            )

        if export_type == "tsv":
            export_data.export_to_tsv(
                filename=self._create_filename(url=url, command=command, filetype="tsv")
            )

        if export_type == "table":
            export_data.export_to_table()

        try:
            if (
                export_type == "excel"
                or export_type == "xlsx"
                or export_type.lower() not in export_types
            ):
                export_data.export_to_excel(
                    filename=self._create_filename(
                        url=url, command=command, filetype="xlsx"
                    )
                )

        except AttributeError:
            export_data.export_to_excel(
                filename=self._create_filename(
                    url=url, command=command, filetype="xlsx"
                )
            )

    def _create_filename(self, url: str, command: str, filetype: str) -> str:
        """
        Creates a file name from timestamp, url and command.
        """

        from datetime import datetime

        def __clean_url(url: str) -> str:
            for t in (
                ("https", ""),
                ("http", ""),
                (":", ""),
                ("sc-domain", ""),
                ("//", ""),
                ("/", "-"),
                ("--", "-"),
                (".", "-"),
                (",", "-"),
            ):
                url = url.lower().replace(*t)

            return url

        def __create_name(file_exists: bool = False) -> str:
            from random import randint

            if not file_exists:
                return "-".join(
                    [
                        __clean_url(url) or "sites",
                        command,
                        datetime.now().strftime("%d-%B-%Y-%H-%M") + f".{filetype}",
                    ]
                )
            return "-".join(
                [
                    __clean_url(url) or "sites",
                    command,
                    f"report-{randint(1,10000)}",
                    datetime.now().strftime("%d-%B-%Y-%H-%M") + f".{filetype}",
                ]
            )

        return (
            __create_name()
            if not path_exists(__create_name())
            else __create_name(file_exists=True)
            if not path_exists(__create_name(file_exists=True))
            else __create_name(file_exists=True)
        )
