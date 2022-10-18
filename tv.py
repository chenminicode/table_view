#!/usr/bin/env python

import sys
import argparse
import re
import pandas as pd


def arg_parse():
    parser = argparse.ArgumentParser(
        description='Select columns, align and view'
    )
    parser.add_argument('-i', '--input', dest='input',
                        required=True, help='input file')
    parser.add_argument(
        '-c',
        '--columns',
        dest='columns',
        default='all-columns',
        help='column names, seprated by ","')
    parser.add_argument(
        '-d',
        '--delimiter',
        dest='delimiter',
        help='table delimiter',
        default='\t')
    parser.add_argument(
        '-s',
        '--stlye',
        dest='style',
        help='print style, use "t" to print tab seprated table, "a" to align columns, "f50" to fix 50 width',
        default='t')

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()
    return args


def get_select_columns(col, df):
    '''
    parse input colmun symbol, and return selected columns of df
    
    Paremeters
    ----------
    col : str
        input column argument
    df : DataFrame
        table DataFrame
    
    Returns
    -------
    select_columns : list
        selected columns
    '''
    if col == 'all-columns':
        return list(df.columns)
    else:
        return col.split(',')


def pprint_df(df, style):
    '''
    pertty print DataFrame

    Parameters
    ----------
    df : DataFrame
        DataFrame needed to print
    style : str
        print style
        - t: tab seprated table
        - a: align columns
    '''
    columns = list(df.columns)
    if style == 't':
        print('\t'.join(columns))
        for index, row in df.iterrows():
            print('\t'.join(row))
    elif style == 'a':
        col_max_len = df.apply(lambda s: s.str.len(), axis=1).max().fillna(0)
        col_space = 2
        col_align = list(col_max_len + col_space)
        for s, f in zip(columns, col_align):
            print(f'{s:<{f}}', end='')
        print()
        for index, row in df.iterrows():
            for s, f in zip(row, col_align):
                print(f'{s:<{f}}', end='')
            print()
    elif re.match(r'f\d+', style):
        fix_len = int(style[1:])
        col_max_len = df.apply(lambda s: s.str.len(), axis=1).max().fillna(0)
        col_space = 2
        col_align = col_max_len + col_space
        col_align[col_align > fix_len] = fix_len

        for s, f in zip(columns, col_align):
            if f < fix_len:
                sub_s = s
            else:
                sub_s = '..' + s[-fix_len:]
            print(f'{sub_s:<{f+4}}', end='')
        print()
        for index, row in df.iterrows():
            for s, f in zip(row, col_align):
                if f < fix_len:
                    sub_s = s
                else:
                    sub_s = '..' + s[-fix_len:]
                print(f'{sub_s:<{f+4}}', end='')
            print()
    else:
        print('Invalid style: {style}.')


def main():
    args = arg_parse()

    # read table
    df = pd.read_table(args.input, sep=args.delimiter)

    # select columns
    columns = get_select_columns(args.columns, df)
    selected_df = df[columns]

    # print selected columns
    pprint_df(selected_df, args.style)


if __name__ == '__main__':
    main()
