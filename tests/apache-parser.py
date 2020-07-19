import os, sys
import argparse
import pandas as pd
import numpy as no
from apachelogs import LogParser
from datetime import datetime
##### Uncomment if you want to try the termgraph chart. not wurking.
# from termgraph import termgraph as tg
# from termgraph.termgraph import chart
# import tempfile



formatLog = r'%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-Agent}i" "%V"'
parser = LogParser(formatLog)
#sample = '109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-" "Mozilla/5.0 (Windows NT 6.0; rv:34.0) Gecko/20100101 Firefox/34.0" "-"'
# data_sample = parser.parse(sample)



class parseTool:
    def __init__(self):
        self.storageList=[]
    def appendList(self, newLine):
        self.storageList.append(newLine)
    def printList(self):
        for singleLine in self.storageList:
            print(singleLine)
    def setDataFrame(self):
        df = pd.DataFrame(self.storageList)
        df = df.rename(columns={0:'IP', 1:'URI', 2: 'Date'})
        df["URI"] = df['URI'].str.split(' ').str[1]
        df["Date"] = pd.to_datetime(df['Date'], utc=True, format='%Y-%m-%d')
        return df
    def readLogTest(self):
        y = self.setDataFrame()
        print(y)
    def doTest1(self):
        df = self.setDataFrame()
        z = df["URI"].value_counts().rename_axis('URI:').reset_index(name='Hits:').head(10)
        print(z.to_string(index=False))
    def doTest2(self):
        df = self.setDataFrame()
        z=df["IP"].value_counts().rename_axis('Hosts:').reset_index(name='Hits:').head(10)
        print(z.to_string(index=False))
    def doTest3(self):
        df = self.setDataFrame()
        z=df.set_index('Date').resample('1M')['URI'].count().reset_index(name='Hits')
        # Change  Month - Year view, remove hours and days
        z['Date'] = z['Date'].dt.strftime('%Y %b')
        # print(z.to_string(index=False))
        for date, hits in z.values:
            print(date, "hits count -", hits)
    def doTest4(self):
        df = self.setDataFrame()
        z=df.set_index(['Date']).resample('1M')['IP'].nunique().reset_index(name="Uniq Visits")
        z['Date'] = z['Date'].dt.strftime('%Y %b')
        # print(z.to_string(index=False))
        for date, visits in z.values:
            print(date, "unique visits -", visits)
        # print(z.loc['2015-12-01':'2016-01-01'])
    def doTest5(self):
        df = self.setDataFrame()
        df.set_index(['Date'])
        z = df.set_index(['Date']).resample('1M')['IP'].value_counts().reset_index(name='Visits')
        z['Date'] = z['Date'].dt.strftime('%Y-%m')
        cd = z.drop(columns=['IP', 'Visits'])
        # Making a list with the dates
        my_dates = cd.drop_duplicates(subset = ['Date'])
        list_dates=my_dates['Date'].values
        for dm in list_dates:
            # The data for the Month-Year for "tname"
            f = z.loc[ z.Date == dm ].head(10).drop(columns=['Date'])
            do = datetime.strptime(dm, '%Y-%m')
            # The Month - Year
            tname=do.strftime('%b %Y')
            # print(tname)
            # print(f.values)
            # print('\n\n\n')
            # Create .csv output files for charting
            f.to_csv(r'./charts/{}.csv'.format(tname), header=False, sep=' ', encoding='utf-8', index=False)
            os.system('echo "\n\n\n"'+""+tname + "\n" + 'awk \'{print $2, $1}\'' + " " + "'./charts/{}.csv'".format(tname) + '| bash barchart.sh')
            ########### not finished - Uncoment next lines to use tg.chart. Need fix data...
            ### Data has to be converted to str and remove single quotes from IPs, so charting isnt working for now....
            # labelsip = z.loc[ z.Date == dm ].head(10).drop(columns=['Date', 'Visits'])
            # datav = z.loc[ z.Date == dm ].head(10).drop(columns=['Date', 'IP'])
            # ips = labelsip.values
            # visits = datav.values
            # args = { 'stacked': False, 'width': 50, 'no_labels': False, 'format': '{:<5.2f}', 'suffix': '', 'vertical': False , 'histogram': False , 'delim': '' }
            # colors=[]
            ###############
            ### Uncomment from here to activate broken plotting. Bec per line...
            # def plot(data):
            ## def plot(colors, data, args, labels):
            #     with tempfile.NamedTemporaryFile(mode='a+') as f:
            #         for row in data:
            #             f.write('\t'.join(map(str,row)))
            #             f.seek(0)
            #             original_argv = sys.argv
            #             sys.argv = [sys.argv[0], f.name]
            #             tg.main()
            #             # tg.chart(colors, data, args, labels)
            #             # tg.stacked_graph(colors, data, args, labels)
            #             sys.argv = original_argv
            # plot(f.values)
            ### to here
            ## plot(colors, visits, args, ips)
            ## chart(colors=[], data=visits, args=args, labels=ips)
            ### tg.chart - not working, cant use the IP list data correctly.
            ### 
    def clear(self):
        self.storageList=[]


parseRecord = parseTool()

argParser = argparse.ArgumentParser(description='Run Example: python parser.py -i access.log --test 1')
argParser.add_argument('-i', type=str, help='use the access.log file', required=True)
argParser.add_argument('--test', type=str, default='1', help='Please select a test - 1, 2 ,3, 4, 5. Example: --test 1', required=True)

parsedArg = vars(argParser.parse_args())
args = argParser.parse_args()

inputFile = (parsedArg['i'])


if not os.path.exists(inputFile):
    print("File is missing")


class ApacheLogParserError(Exception):
    pass

def parse_log():
    with open(inputFile, 'r') as fileLog:
        for line in fileLog:
            if not line.strip():
               continue
            try:
                data =  parser.parse(line)
            except:
                sys.stderr.write("Unable to parse %" % line)
            host = data.remote_host
            path = data.request_line
            date = data.request_time
            parseRecord.appendList([host, path, date])
    fileLog.close()

if __name__ == '__main__':
    if (args == None and args.length == None):
        argParser.print_help
    elif args.test == '1':
        print('Task 1. Top 10 requested URLs sorted by Hits')
        parse_log()
        parseRecord.doTest1()
    elif args.test == '2':
        print('Task 2. Top 10 visitors by IP sorted by Hits')
        parse_log()
        parseRecord.doTest2()
    elif args.test == '3':
        print('Task 3. Total Hits per Month sorted by Month')
        parse_log()
        parseRecord.doTest3()
    elif args.test == '4':
        print('Task 4. Unique Visits (by IP) per Month')
        parse_log()
        parseRecord.doTest4()
    elif args.test == '5':
        print('Task 5. Top 10 IPs barchart per Month')
        print('Task 5 will create a new ./charts folder in the current directory for storing .csv')
        print('and it will download bar charting script from github in the current dir')
        while True:
            if input('Ctrl+C if you want to cancel. To execute type y/yes '):
                break
        os.system('curl -s https://gist.githubusercontent.com/markusfisch/4612424/raw/0508526e7b7649bb726a54beb802d312cbddb998/bars.sh -o barchart.sh')
        # Create "./charts" dir for storing .csv files
        try:
            os.mkdir("./charts")
        except:
            pass
        parse_log()
        parseRecord.doTest5()
    else:
        print("Pick test option --test 1,2,3,4 or 5")
