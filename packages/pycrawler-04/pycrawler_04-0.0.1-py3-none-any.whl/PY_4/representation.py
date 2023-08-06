
"""Generation of Report in different forms"""
import json
import csv
import yaml
import os
import webbrowser


class Representation:
    """generate report in different format"""

    def __init__(self, data):
        self.data = data

    def selecttype(self, representation_format=None):
        """select format"""
        if representation_format == "json":
            return self.json_report()
        if representation_format == "csv":
            return self.csv_report()
        if representation_format == "html":
            return self.html_report()
        return self.yaml_report()

    def dict_to_html_table(self):
        tbl_fmt = """
        <table>{}
        </table>"""

        row_fmt = """
        <tr>
            <td>{}</td>
            <td>{}</td>
        </tr>"""
        return tbl_fmt.format(
            "".join([row_fmt.format(k, v) for k, v in self.data.items()])
        )

    def yaml_report(self):
        """report in yaml"""
        yaml_data = yaml.dump(self.data)
        # print(self.yaml_data)
        yaml_dte = ""
        yaml_data1 = yaml.load_all(yaml_data, Loader=yaml.FullLoader)
        for doc in yaml_data1:
            yaml_dte += "report-id: " + doc["report-id"] + "\n"
            yaml_dte += "website: " + doc["website"] + "\n"
            yaml_dte += "total-links: " + str(doc["total-links"]) + "\n\n"
            yaml_dte += "external-references: " + "\n"
            yaml_dte += (
                "   # [ links-to-external-websites, response-time-in-seconds ] \n"
            )
            for j in range(len(doc["external-references"])):
                yaml_dte += (
                    "   - [ "
                    + doc["external-references"][j][0]
                    + ", "
                    + doc["external-references"][j][1]
                    + " ]\n"
                )
            yaml_dte += "\n"
            yaml_dte += "internal-references: " + "\n"
            yaml_dte += "   # [ links-to-internal-webpages-and-resources, response-time-in-seconds ]\n"
            for j in range(len(doc["internal-references"])):
                yaml_dte += (
                    "   - [ "
                    + doc["internal-references"][j][0]
                    + ", "
                    + doc["internal-references"][j][1]
                    + " ]\n"
                )
            yaml_dte += "\n"
            yaml_dte += "broken-links: " + "\n"
            yaml_dte += (
                "   # [ links-that-could-not-be-resolved, http-error-status-code ]\n"
            )
            for j in range(len(doc["broken-links"])):
                yaml_dte += (
                    "   - [ "
                    + doc["broken-links"][j][0]
                    + ", "
                    + doc["broken-links"][j][1]
                    + " ]\n"
                )

        return yaml_dte

    # html_report_generation
    def html_report(self):
        x = self.dict_to_html_table()
        filename = "reportgenerated.html"
        print(x)
        f = open(filename, "w")
        f.write(x)
        f.close()
        return webbrowser.open("file://" + os.path.realpath(filename))

    # json_report_generation
    def json_report(self):
        """report in json"""
        json_data = json.dumps(self.data, indent=2)
        return json_data

    # csv_report_generation
    def csv_report(self):
        """report in csv"""
        with open("./csv_report.csv", "w") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in self.data.items():
                writer.writerow([key, value])
        doc = open("./csv_report.csv", "r")
        return doc.read()


def main(data, representation_format=None):
    """return format data"""
    representation = Representation(data)
    return representation.selecttype(representation_format)
