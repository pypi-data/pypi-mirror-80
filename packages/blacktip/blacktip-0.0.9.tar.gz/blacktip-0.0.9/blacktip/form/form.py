import os
import csv

class Form:
    """
    Abstract Data Type for SEC forms
    """
    def __init__(self, df):
        self.df = df


    def form(self):
        """
        getter method for the source format

        :return (df): the form dataframe
        """
        return self.df.copy()


    def filter(self, regex, index="tag"):
        """
        generates a data sheet based on a keyword regex

        :param regex (str): the keyword regular expression
        :param index (str): the dataframe index to search on ("tag" or "uom")
        :return (df): a subset of the whole dataframe filtered by the regex
        """
        form = self.form()
        # return form[form.tag.str.contains(regex)].reset_index(drop=True)
        # return self.form().filter(regex=regex, axis=axis)
        return form.loc[form.index.get_level_values(index).str.contains(regex)]


    def asset_sheet(self):
        """
        generates a data sheet of "Asset" values

        :return (df): a subset of the whole dataframe filtered by assets
        """
        return self.filter("Asset|Assets")


    def liability_sheet(self):
        """
        generates a data sheet of "Liability" values

        :return (df): a subset of the whole dataframe filtered by liabilities
        """
        return self.filter("Liability|Liabilities")


    def debt_sheet(self):
        """
        generates a data sheet of "Debt" values

        :return (df): a subset of the whole dataframe filtered by debts
        """
        return self.filter("Debt|Debts")


    def to_csv(
            self,
            path_or_buf=None,
            sep=",",
            na_rep="",
            float_format=None,
            columns=None,
            header=True,
            index=True,
            index_label=None,
            mode="w",
            encoding="utf-8",
            compression="infer",
            quoting=csv.QUOTE_MINIMAL,
            quotechar='"',
            line_terminator=os.linesep,
            chunksize=None,
            date_format=None,
            doublequote=True,
            escapechar=None,
            decimal="."
        ):
        """
        saves form as a csv according to: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

        :param path_or_buf (str or file handle): File path or object
        :param sep (str length 1): field delimiter
        :param na_rep (str): missing data representation
        :param float_format (str): format for floating point numbers
        :param columns (sequence): columns to write
        :param header (bool or list of str): write out the column names
        :param index (bool): write row names
        :param index_label (str or sequence, or False): column label for index columns if desired
        :param mode (str): python write mode
        :param encoding (str): encoding to use
        :param compression (str or dict): compression mode
        :param quoting (constance from csv module): csv value handling of numerics
        :param quotechar (str): character used to quote fields
        :param line_terminator (str): newline character
        :param chunksize (int or None): rows to write at a time
        :param date_format (str): format string for datetime objects
        :param doublequote (bool): control quoting of quotechar inside a field
        :param escapechar (str): character used to escape sep and quotechar
        :param decimal (str): character recognized as decimal separator
        :return: string of df if path_or_buf is None
        """

        return self.form().to_csv(
            path_or_buf, sep, na_rep, float_format, columns, header, index, index_label, mode,
            encoding, compression, quoting, quotechar, line_terminator, chunksize, date_format,
            doublequote, escapechar, decimal
        )


    def __str__(self):
        return str(self.form())

    def __getitem__(self, index):
        return self.form().__getitem__(index)


class Form10K(Form):
    """
    Abstract Data Type for the SEC Form 10-K
    """
    def __init__(self, df):
        self.raw = df
        super().__init__(df)
        self.df = Form10K._format(self.df)


    # def calc_ROA(self):
    #     """
    #     calculates ROA = net income / average total assets
    #
    #     :return (df): the ROA values
    #     """
    #     # self.df.groupby(["tag", "uom"]).first().reset_index()
    #     return


    def calc_ROE(self, as_list=False):
        """
        calculates ROE = net income / total stockholders equity

        :param as_list (boolean): returns values as a list if True, as a dataframe otherwise
        :return (df): the ROE values
        """
        net_income =  self.filter("^NetIncomeLoss$")
        stockholders_equity = self.filter("^StockholdersEquity$")
        years = net_income.columns.to_list()
        df = net_income.reindex([("ROE", "ratio")])

        for year in years:
            df[year] = net_income[year][0] / stockholders_equity[year][0]

        return df.values[0] if as_list else df


    def calc_CurrentRatio(self, as_list=False):
        """
        calculates the current ratio = current assets / current liabilities

        :param as_list (boolean): returns values as a list if True, as a dataframe otherwise
        :return (df): the current ratio values
        """
        current_assets = self.filter("^AssetsCurrent$")
        current_liabilities = self.filter("^LiabilitiesCurrent$")
        years = current_assets.columns.to_list()
        df = current_assets.reindex([("CurrentRatio", "ratio")])

        for year in years:
            df[year] = current_assets[year][0] / current_liabilities[year][0]

        return df.values[0] if as_list else df


    def calc_DebtToEquity(self, as_list=False):
        """
        calculates the debt-to-equity ratio = total liabilities / total stockholders equity

        :param as_list (boolean): returns values as a list if True, as a dataframe otherwise
        :return (df): the debt-to-equity ratio
        """
        total_liabilities = self.filter("^Liabilities$")
        stockholders_equity = self.filter("^StockholdersEquity$")
        years = total_liabilities.columns.to_list()
        df = total_liabilities.reindex([("DebtToEquity", "ratio")])

        for year in years:
            df[year] = total_liabilities[year][0] / stockholders_equity[year][0]

        return df.values[0] if as_list else df


    def calc_BookValue(self, as_list=False):
        """
        calculates the book value = total assets - total liabilities

        :param as_list (boolean): returns values as a list if True, as a dataframe otherwise
        :return (df): the book value
        """
        assets = self.filter("^Assets$")
        liabilities = self.filter("^Liabilities$")
        years = assets.columns.to_list()
        df = assets.reindex([("BookValue", "USD")])

        for year in years:
            df[year] = assets[year][0] - liabilities[year][0]

        return df.values[0] if as_list else df


    ########## Private Functions ##########

    @staticmethod
    def _format(df):
        """
        adds a column designating which source column dataframe values came from

        :param df (df): the dataframe
        :return (dF): the dataframe in source format
        """
        # df["source_column"] = df.groupby(["tag", "fy"]).cumcount().add(1)
        # df = df.set_index

        dataframe = df.pivot_table(
            index=["tag", "uom", "ddate", "fye"],
            columns="fy",
            values="value",
            aggfunc="max"
        )

        # dataframe = df.sort_values("ddate", ascending=False)
        dataframe["monthday"] = dataframe.index.get_level_values("ddate").map(lambda d: "{:02d}{:02d}".format(d.month, d.day))
        filtered = dataframe.loc[dataframe["monthday"] == dataframe.index.get_level_values("fye")]
        grouped = filtered.groupby(["tag", "uom"]).last()#.groupby(["tag", "uom"])
        return grouped.drop("monthday", axis=1) #.last().drop("monthday", axis=1)



class Form10Q(Form):
    """
    Abstract Data Type for the SEC Form 10-Q
    """
    def __init__(self, df):
        self.raw = df
        super().__init__(df)
        self.df = Form10Q._format(self.df)


    ########## Private Functions ##########

    @staticmethod
    def _format(df):
        dataframe = df.pivot_table(
            index=["tag", "uom", "ddate"],
            columns=["fy", "fp"],
            values="value",
            aggfunc="min"
        )
        return dataframe.groupby(["tag", "uom"]).last()

