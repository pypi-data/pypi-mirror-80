
import argparse
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt

from .plotSchedule import plotSchedule

def main():
    parser = argparse.ArgumentParser( description="Generate simple schedule plots")

    parser.add_argument('file_path')
    parser.add_argument('--labels','-l', nargs='+', default=None, help='columns for labels per event')
    parser.add_argument('--output','-o', help="output filename")
    parser.add_argument('--title','-t', help="plot title")

    args = parser.parse_args()

    file_path = args.file_path
    path,fname = os.path.split(file_path)
    bare_filename, ext = os.path.splitext(fname)
    outfile = args.output or bare_filename + '.png'
    title = args.title or 'Schedule'

    if ext in ['.csv', '.xlsx']:
        if ext == '.csv':
            df = pd.read_csv(file_path).fillna('')
        else:
            df = pd.read_excel(file_path).fillna('')

        print("found columns:", df.columns)
        sched = df.to_dict('records')
        if args.labels:
            print ("found labels:", args.labels)
            for d in sched:
                labels = []
                for col in args.labels:
                    val = d.get(col)
                    if val is None:
                        raise RuntimeError("Cannot find column:" + col)
                    labels.append(val)
                d.update(labels=labels)
            
        plotSchedule(sched, mainLabel=title)
        plt.savefig(outfile)

if __name__ == '__main__':
    main()
