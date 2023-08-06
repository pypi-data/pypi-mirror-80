# def _commitdb(self, command, data=None):
#     """
#     commit to the database
#     :param command: the command to execute
#     :param data: the values of the command
#
#     e.g.
#     command = "INSERT INTO employees (name, hire_date) VALUES (%s, %s)"
#     data = [
#       ('Jane', date(2005, 2, 12)),
#       ('Joe', date(2006, 5, 23)),
#       ('John', date(2010, 10, 3)),
#     ]
#     commitdb(command, database, data)
#     """
#
#     cursor = self.conn.cursor()
#     if data is None:
#         cursor.execute(command)
#     else:
#         cursor.executemany(command, data)
#
#     self.conn.commit()
#     print(cursor.rowcount, "rows inserted.")
#     cursor.close()



# def _querydb(self, command):
#     """
#     used to query information from the database
#     :param command: the string mySQL command to execute
#     :return: the results of the query
#     """
#
#     cursor = self.conn.cursor()
#     cursor.execute(command)
#     results = cursor.fetchmany(1e3)
#     cursor.close()
#     return results


# def query10K(self, ticker_or_CIK, years):
#     """
#     get company 10Ks for selected years
#     :param ticker_or_CIK (string): the company's ticker or SEC issued Central Index Key (CIK)
#     :param years (int or tuple): a year or tuple of years of interest
#     :return: dataframe
#     todo add multithreading
#     """
#     CIK = Angler._cik(ticker_or_CIK)
#
#     if type(years) is int:
#         year_where_clause = "fy={years}".format(years=years)
#     elif len(years) == 1:
#         year_where_clause = "fy={years}".format(years=years[0])
#     else:
#         year_where_clause = "fy IN {years}".format(years=tuple(years))
#
#     adsh_query = "SELECT adsh FROM sub WHERE cik={CIK} AND form='10-K' AND {year_where_clause}".format(CIK=CIK, year_where_clause=year_where_clause)
#     adsh_query_results = self._querydb(adsh_query)
#     if adsh_query_results is None:
#         return
#     adsh_query_results = [i[0] for i in adsh_query_results]
#
#     adsh_where_clause = "adsh='{adsh}'".format(adsh=adsh_query_results[0]) if len(adsh_query_results)==1 else "adsh IN {adsh}".format(adsh=tuple(adsh_query_results))
#     numerics_command = "SELECT tag, value, uom FROM num WHERE {adsh_where_clause}".format(adsh_where_clause=adsh_where_clause)
#     return pd.read_sql_query(numerics_command, self.conn)

# command = "SELECT tag, value, uom FROM num WHERE adsh IN (SELECT a.adsh FROM sub a WHERE cik={CIK} AND form='10-K' AND {year_where_clause})".format(
#     CIK = CIK,
#     year_where_clause = year_where_clause
# )


# def _create_engine(self):
#     """
#     establish connection to blacktip MySQL database
#     :return: SQLAlchemy engine instance
#     """
#     self.conn = mysql.connector.connect(
#         host=Angler.host,
#         port=Angler.port,
#         database=Angler.database,
#         user=self.username,
#         passwd=self.password,
#
#     )

if __name__ == "__main__":
    from modulefinder import ModuleFinder

    f = ModuleFinder()

    # Run the main script
    f.run_script('angler.py')

    # Get names of all the imported modules
    names = list(f.modules.keys())

    # Get a sorted list of the root modules imported
    basemods = sorted(set([name.split('.')[0] for name in names]))
    # Print it nicely
    print("\n".join(basemods))
