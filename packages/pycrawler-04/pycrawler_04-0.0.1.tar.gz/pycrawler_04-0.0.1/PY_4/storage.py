"""Functions of database to handle database"""
import sqlite3
from sqlite3 import Error
import ast


class Store:
    def __init__(self):
        pass

    def gen_report(self, k):
        """report generation"""
        reports = {}
        listheader = [
            "report-id",
            "website",
            "total-links",
            "external-references",
            "internal-references",
            "broken-links",
        ]
        for i in range(len(listheader)):
            reports[listheader[i]] = k[0][i]

        reports["external-references"] = ast.literal_eval(
            reports["external-references"]
        )
        reports["internal-references"] = ast.literal_eval(
            reports["internal-references"]
        )
        reports["broken-links"] = ast.literal_eval(reports["broken-links"])
        return reports

    def connect_db(self):
        """Database Connection"""
        try:
            con = sqlite3.connect("webstats2.db")
            return con

        except Error:
            print(Error)

    def make_table(self, con):
        """make table for storing website"""
        try:
            cur = con.cursor()
            cur.execute(
                """CREATE TABLE IF NOT EXISTS WEB(
                        Reportid VARCHAR(6) PRIMARY KEY NOT NULL,
                        Website VARCHAR(255) NOT NULL,
                        Totallinks INTEGER,
                        EXTERNAL VARCHAR(255),
                        INTERNAL VARCHAR(255),
                        BROKEN VARCHAR(255),
                        datetime VARCHAR(50) NOT NULL)
                        """
            )
            con.commit()
        except Error as error:
            print(error)

    def insert(self, con, data):
        """insert website data"""
        try:
            cur = con.cursor()

            webdata = [
                (
                    data["report_id"],
                    data["website_link"],
                    data["total_links"],
                    str(data["external_links"]),
                    str(data["internal_links"]),
                    str(data["broken_links"]),
                    data["date_time"],
                )
            ]
            cur.executemany("Insert Into WEB Values (?,?,?,?,?,?,?)", webdata)
            con.commit()

        except Error as error:
            print(error)

    def fetch(self, con, arg, reportid=None):
        """fetch data"""
        try:
            reports = {}
            cur = con.cursor()
            # fetch list reports
            if arg == "list-reports" and reportid is None:
                for report in cur.execute("SELECT Reportid,datetime,Website FROM WEB;"):
                    reports[report[0]] = report
                return reports
            # fetch report by report id
            elif arg == "links-report" and reportid is not None:
                try:
                    cur.execute(
                        """SELECT Reportid, Website, Totallinks,EXTERNAL,INTERNAL,BROKEN FROM WEB
                        WHERE Reportid ='%s'"""
                        % reportid
                    )
                    row = cur.fetchall()
                    reports = self.gen_report(row)
                    return reports

                except:
                    print("Report Not Found!")
                    return None
            else:
                print("Invalid Command Given")
                return None
        except Error as error:
            print(error)
            return None

    def close_dbconnect(self, con):
        """close connection"""
        con.close()
