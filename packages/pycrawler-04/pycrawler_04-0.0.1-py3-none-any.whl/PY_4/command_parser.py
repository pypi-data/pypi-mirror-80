import sys
try:
    from . import storage
    from . import representation
    from . import helpcode
    from . import crawler
except:
    import storage
    import representation
    import helpcode
    import crawler

import argparse

def cmd_execute():
    parser = argparse.ArgumentParser("Stats about websites you need to Crawl ")
    parser.add_argument('commands', type=str, nargs='*')
    args = parser.parse_args()

    store = storage.Store()
    con = store.connect_db()
    store.make_table(con)

    if len(args.commands) > 0:
        if args.commands[0] == "crawl" and len(args.commands)>1:
            ipurls = []
            for i in range(1, len(args.commands)):
                ipurls.append(args.commands[i])
            data = crawler.concurrency(ipurls)
            for i in range(len(data)):
                if data[i] is not None:
                    store.insert(con, data[i])
        elif args.commands[0] == "list-reports" and len(args.commands) == 1:
            reports = store.fetch(con, "list-reports")
            iteration = 1
            for i in reports:
                print(
                    str(iteration)
                    + ". "
                    + reports[i][0]
                    + " - "
                    + reports[i][1]
                    + " - "
                    + reports[i][2]
                )
                iteration += 1

        elif args.commands[0] == "links-report" and 1 < len(args.commands) < 4:
            report = store.fetch(con, "links-report", args.commands[1])
            if report is not None:
                if len(args.commands) == 2:
                    print(representation.main(report))
                elif args.commands[2] == "json" or args.commands[2] == "csv" or args.commands[2] == "html":
                    print(representation.main(report, args.commands[2]))
                else:
                    print("Wrong format selected")
                    print("Available Formats - YAML, HTML, JSON, CSV")
                    helpcode.help_func()

        else:
            helpcode.help_func()
    else:
        helpcode.help_func()
    store.close_dbconnect(con)
    
if __name__=="__main__":
    cmd_execute()