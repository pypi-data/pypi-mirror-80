import re
import requests
import pandas as pd
from sqlalchemy import create_engine

from .errors.errors import TickerNotFoundError, NestedDepthError
from .form.form import Form10K, Form10Q

class Angler:
    """
    Blacktip Research Angler API

    This API is used to interact with the Blacktip XBRL database. To use it, create an instance by
    executing:
        instance = Angler(username, password)

    From there, you are signed in and can use the pre-made querying functions:
        form10K = instance.query10K("AAPL", 2019)
    And you can get data by:
        df = form10K.form()
    """

    host = "database-blacktip.cpeql2xeyjqq.us-east-2.rds.amazonaws.com"
    port = 3306
    database = "xbrl"


    def __init__(self, username, password):
        self.username = "temporary_free_access" #username
        self.password = "FreeAtLast2020_" #password
        self.engine = self._create_engine()


    @staticmethod
    def queryCIK(ticker):
        """
        Inspired by Micah Morris (https://gist.github.com/dougvk/8499335#gistcomment-2135443)

        :param ticker: stock market ticker
        :return: (ticker, cik)
        """
        URL = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK={}&Find=Search&owner=exclude&action=getcompany'
        CIK_RE = re.compile(r'.*CIK=(\d{10}).*')
        r = requests.get(URL.format(ticker), stream = True)
        results = CIK_RE.findall(r.text)
        if len(results):
            results[0] = int(re.sub('\.[0]*', '.', results[0]))
            return str(ticker).upper(), str(results[0])


    def queryName(self, ticker_or_CIK):
        """
        query the name of a company from their ticker or CIK

        :param ticker_or_CIK (int or str): the ticker or CIK number
        :return (str): the name of the company
        """
        CIK = Angler._cik(ticker_or_CIK)
        command = "SELECT name FROM sub WHERE cik={CIK}".format(CIK=CIK)
        return self.query(command).first()[0]


    def query10K(self, ticker_or_CIK, years):
        """
        get company 10Ks for selected years

        :param ticker_or_CIK (string): the company's ticker or SEC issued Central Index Key (CIK)
        :param years (int or iterable): a year or iterable of years of interest
        :return: Form10K

        Note: supplying the CIK instead of the ticker considerably improves runtime as it eliminates
        the query to determine CIK from ticker

        todo add multithreading to CIK query
        """

        CIK = Angler._cik(ticker_or_CIK)

        if type(years) is int:
            year_where_clause = "fy={years}".format(years=years)
        elif len(years) == 1:
            year_where_clause = "fy={years}".format(years=years[0])
        else:
            year_where_clause = "fy IN {years}".format(years=tuple(years))

        command = ("SELECT a.fy, a.fye, b.tag, b.value, b.uom, b.ddate "
                   "FROM num b JOIN sub a ON a.adsh=b.adsh "
                   "WHERE cik={CIK} AND form='10-K' AND {year_where_clause}".format(
            CIK = CIK,
            year_where_clause = year_where_clause
        ))

        return Form10K(pd.read_sql_query(command, self.engine))


    def query10Q(self, ticker_or_CIK, periods):
        """
        get company 10Qs for selected periods

        :param ticker_or_CIK (string): the company's ticker or SEC issued Central Index Key (CIK)
        :param periods (int): the year of interest, will get all quarters
                       (iterable of ints): years of interest, will get all quarters
                       (tuple): (year, quarter) pair
                       (iterable of tuples): (year, quarter) pairs of interest
        :return: dataframe

        Ex:
        Angler.query10Q("AAPL", 2019)
        Angler.query10Q("AAPL", [2018, 2019])
        Angler.query10Q("AAPL", (2019, "q1"))
        Angler.query10Q("AAPL", [(2019, "q1"), (2019, "q2")]

        Note: quarter 4 is represented in the form 10K, not in the form 10Q

        Note: supplying the CIK instead of the ticker considerably improves runtime as it eliminates
        the query to determine CIK from ticker

        todo add multithreading to CIK query
        """
        CIK = Angler._cik(ticker_or_CIK)

        depth = Angler._depth(periods)
        if depth == 0:
            periods = [(periods, quarter) for quarter in ["q1", "q2", "q3", "q4"]]
        elif depth == 1:
            if type(periods) is tuple:
                periods = [periods]
            else:
                periods = [(year, quarter) for year in periods for quarter in ["q1", "q2", "q3", "q4"]]
        elif depth > 2:
            raise NestedDepthError(input_depth=depth, correct_depth=[0, 1, 2])


        period_where_clause = "(" + \
            "".join(
            "(a.fy={year} AND a.fp='{quarter}') OR ".format(
                year=year,
                quarter=quarter
            ) for year,quarter in periods)[:-4] + \
            ")"

        command = ("SELECT a.fy, a.fp, b.tag, b.value, b.uom, b.ddate "
                   "FROM num b JOIN sub a ON a.adsh=b.adsh "
                   "WHERE cik={CIK} AND form='10-Q' AND {period_where_clause}".format(
            CIK = CIK,
            period_where_clause = period_where_clause
        ))

        return Form10Q(pd.read_sql_query(command, self.engine))


    def query(self, command):
        """
        used to query information from the database

        :param command: the string mySQL command to execute
        :return: the results of the query
        """
        with self.engine.connect() as connection:
            return connection.execute(command)


    def dispose(self):
        """
        closes the database connection
        """
        self.engine.dispose()




    ########## Private Functions ##########


    def _create_engine(self):
        """
        establish connection to blacktip MySQL database

        :return: SQLAlchemy engine instance
        """
        engine = create_engine(
            "mysql+pymysql://{username}:{password}@{host}:{port}/{database}".format(
                username = self.username,
                password = self.password,
                host = Angler.host,
                port = Angler.port,
                database = Angler.database
            )
        )
        return engine


    @staticmethod
    def _cik(ticker_or_CIK):
        """
        takes in a ticker or CIK number and returns just the CIK number. Acts as a convenience function

        :param ticker_or_CIK: ticker string or CIK number
        :return: CIK number
        """
        if type(ticker_or_CIK) is int:
            CIK = ticker_or_CIK
        elif len(str(ticker_or_CIK)) != 10 and str([s for s in ticker_or_CIK if s.isdigit()]) != str(ticker_or_CIK):
            # check if input is a ticker or a CIK. CIKs are 10 digit numbers, tickers are <= 5 character alphanumeric strings
            # if this if statement is true, then the input is a ticker
            ticker = ticker_or_CIK
            CIK_query_results = Angler.queryCIK(ticker)
            if CIK_query_results is None:
                raise TickerNotFoundError(ticker)
            _, CIK = CIK_query_results
        else:
            CIK = ticker_or_CIK

        return CIK


    def _commitdb(self, table_name, dataframe):
        """
        commit data to the database

        :param table_name (string): the name of the table to commit to
        :param dataframe (pandas dataframe): the data to commit to the table
        """
        dataframe.to_sql(table_name, self.engine, index=False, if_exists="append")


    @staticmethod
    def _depth(iterable):
        """
        calculate the nested depth of an iterable

        :param iterable (iterable): the iterable to calculate the depth of
        :return (int): the depth
        """
        depth_func = lambda L: (isinstance(L, list) or isinstance(L, tuple)) and max(map(depth_func, L)) + 1
        depth = depth_func(iterable)
        return depth if depth is not False else 0









