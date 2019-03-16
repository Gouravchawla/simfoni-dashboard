from datetime import datetime, timedelta
import random

import numpy as np
import pandas as pd

from django.conf import settings as conf

from .utils import normalize_days


def get_chart_config(title, categories, series_data, series_name):
    chart_config = {
        'chart': {
            'type': 'column',
            'height': 300,
            'width': 300,
            'spacingBottom': 100
        },
        'legend': {
            'enabled': False
        },
        'credits': {
            'enabled': False
        },
        'title': {
            'text': title,
            'useHTML': True,
            'color': '#588BAE',
            'align': 'left',
            'verticalAlign': 'bottom',
            'y': 30,
            'x': 5
        },
        'xAxis': {
            'enabled': False,
            'visible': False,
            'categories': categories
        },
        'yAxis': {
            'visible': False
        },
        'plotOptions': {
            'column': {
                'pointPadding': 0,
                'groupPadding': 0.1
            },
            'series': {
                'color': '#588BAE'
            }
        },
        'series': [
            {
                'id': f'series-{random.randint(1,101)}',
                'name': series_name,
                'data': series_data
            }
        ]
    }

    return chart_config


def get_chart_config2(title, categories, series_data, series_name):
    chart_config = {
        'chart': {
            'type': 'column',
            'height': 500,
            'width': 500,
            'spacingBottom': 60
        },
        'legend': {
            'enabled': False
        },
        'credits': {
            'enabled': False
        },
        'title': {
            'text': title,
            'color': '#588BAE',
        #     'align': 'left',
        #     'verticalAlign': 'bottom',
        #     'y': 30,
        #     'x': 5
        },
        'xAxis': {
            'enabled': True,
            'visible': True,
            'categories': categories
        },
        'yAxis': {
            'visible': True
        },
        'plotOptions': {
            'column': {
                'pointPadding': 0,
                'groupPadding': 0.1
            },
            'series': {
                'color': '#588BAE'
            }
        },
        'series': [
            {
                'id': f'series-{random.randint(1,101)}',
                'name': series_name,
                'data': series_data
            }
        ]
    }

    return chart_config


def read_data_file():
    file = conf.DATA_DIR + 'test_data.xlsx'

    xl = pd.ExcelFile(file)

    # Load a sheet into data frame
    df = xl.parse('TestData')
    # df = xl.parse('Raw data')

    # Transform/Clean data
    df['Request Date'] = df['Request Date'].transform(lambda x: datetime.strptime(x, '%d/%m/%Y'))
    df['Request to Quote Cycle Time'] = df['Request to Quote Cycle Time'].transform(normalize_days)
    df['Supplier Response Cycle Time'] = df['Supplier Response Cycle Time'].transform(normalize_days)

    return df


def initial_data(buyer=None, department=None, member=None, start_date=None, end_date=None):

    df = read_data_file()
    # Drop NAN and get unique values in column and return as list
    data = dict({'buyers': df['Buyer'].dropna().unique().tolist()})
    data['departments'] = df['Department'].dropna().unique().tolist()
    data['members'] = df['Requester Name'].dropna().unique().tolist()

    if buyer:
        df = df.loc[df['Buyer'] == buyer]
        # data['departments'] = df['Department'].dropna().unique().tolist()
        # data['members'] = df['Requester Name'].dropna().unique().tolist()

    if department:
        df = df.loc[df['Department'] == department]
        # data['buyers'] = df['Buyer'].dropna().unique().tolist()
        # data['members'] = df['Requester Name'].dropna().unique().tolist()

    if member:
        df = df.loc[df['Requester Name'] == member]
        # data['buyers'] = df['Buyer'].dropna().unique().tolist()
        # data['departments'] = df['Department'].dropna().unique().tolist()

    if start_date and end_date:
        data['start_date'] = start_date
        data['end_date'] = end_date

        start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        df = df.loc[(df['Request Date'] > start_date) & (df['Request Date'] < end_date)]

    print(df)
    # Filter data of last 6 months
    # last_one_year = datetime.now() - timedelta(days=540)
    # df = df[df['Request Date'] < last_one_year]

    # charts = [{'categories': [], 'series_data': [], 'config': {}, 'title': ''}]
    charts = []
    chart = {}

    # Chart 1
    grouped_data = df.groupby('Request Date')
    chart['title'] = f"{df['Request Number'].shape[0]} Requests"

    chart['categories'] = []
    chart['series_data'] = []
    for key, value in grouped_data['Request Number'].agg(np.size).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Total Requests'

    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    # Chart 2
    chart = {}

    filtered_data = df.loc[df['Quote Selected?'] == 'Yes']
    grouped_data = filtered_data.groupby('Request Date')

    chart['title'] = f"${int(filtered_data['Total Quote Price'].agg(np.sum))} in spend " \
                     f"<small>(Only on 'Closed Accepted' requests)</small>"
    chart['categories'] = []
    chart['series_data'] = []
    for key, value in grouped_data['Total Quote Price'].agg(np.sum).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Total Quote Price'
    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    # Chart 3
    chart = {}

    filtered_data = df.loc[df['Quote Selected?'] == 'Yes']
    grouped_data = filtered_data.groupby('Request to Quote Cycle Time')

    chart['title'] = f"Avg. {filtered_data['Request to Quote Cycle Time'].agg(np.mean)} days - Request to" \
                     f" Quote cycle time <small>(Only on quoted requests)</small>"
    chart['categories'] = []
    chart['series_data'] = []

    for key, value in grouped_data['Request Number'].agg(np.size).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Total Requests'
    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    # Chart 4
    chart = {}

    filtered_data = df.loc[df['Status'] == 'Closed Accepted']
    grouped_data = filtered_data.groupby('Request Date')

    chart['title'] = f"{filtered_data['Request Number'].shape[0]} Closed requests"

    chart['categories'] = []
    chart['series_data'] = []
    for key, value in grouped_data['Request Number'].agg(np.size).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Total Requests'

    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    # Chart 5
    chart = {}

    filtered_data = df.loc[df['Status'] == 'Closed Accepted']
    grouped_data = filtered_data.groupby('Request Date')

    chart['title'] = f"${int(df['Savings amount'].agg(np.sum))} in savings <small>(Only on 'Closed Accepted' requests)</small>"

    chart['categories'] = []
    chart['series_data'] = []
    for key, value in grouped_data['Savings amount'].agg(np.sum).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Savings amount'

    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    # Chart 6
    chart = {}

    filtered_data = df.loc[df['Status'] == 'Closed Accepted']
    grouped_data = filtered_data.groupby('Supplier Response Cycle Time')

    chart['title'] = f"Avg. {filtered_data['Supplier Response Cycle Time'].agg(np.mean)} days - Supplier" \
                     f" response cycle time <small>(Only on quoted requests)</small>"
    chart['categories'] = []
    chart['series_data'] = []

    for key, value in grouped_data['Request Number'].agg(np.size).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = 'Total Requests'
    chart['chart_config'] = get_chart_config(chart['title'], chart['categories'], chart['series_data'], series_name)
    charts.append(chart)

    data['default_charts'] = charts
    return data


def get_aggregate_function(func_name):
    function_names = {
        'size': np.size,
        'mean': np.mean,
        'sum': np.sum
    }

    return function_names[func_name]


def generate_chart(dimension, measure, aggregate_function):
    df = read_data_file()
    # Drop NAN and get unique values in column and return as list
    # data = dict({'buyers': df['Buyer'].dropna().unique().tolist()})
    # data['departments'] = df['Department'].dropna().unique().tolist()
    # data['members'] = df['Requester Name'].dropna().unique().tolist()
    #
    # if buyer:
    #     df = df.loc[df['Buyer'] == buyer]
    #     # data['departments'] = df['Department'].dropna().unique().tolist()
    #     # data['members'] = df['Requester Name'].dropna().unique().tolist()
    #
    # if department:
    #     df = df.loc[df['Department'] == department]
    #     # data['buyers'] = df['Buyer'].dropna().unique().tolist()
    #     # data['members'] = df['Requester Name'].dropna().unique().tolist()
    #
    # if member:
    #     df = df.loc[df['Requester Name'] == member]
    #     # data['buyers'] = df['Buyer'].dropna().unique().tolist()
    #     # data['departments'] = df['Department'].dropna().unique().tolist()
    #
    # if start_date and end_date:
    #     data['start_date'] = start_date
    #     data['end_date'] = end_date
    #
    #     start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    #     end_date = datetime.strptime(end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    #     df = df.loc[(df['Request Date'] > start_date) & (df['Request Date'] < end_date)]
    #
    # print(df)
    # Filter data of last 6 months
    # last_one_year = datetime.now() - timedelta(days=540)
    # df = df[df['Request Date'] < last_one_year]

    # chart = {'categories': [], 'series_data': [], 'config': {}, 'title': ''}
    aggregate_function = get_aggregate_function(aggregate_function)
    chart = {}

    grouped_data = df.groupby(dimension)
    chart['title'] = f"{dimension} vs {measure}"

    chart['categories'] = []
    chart['series_data'] = []
    for key, value in grouped_data[measure].agg(aggregate_function).items():
        chart['categories'].append(key)
        chart['series_data'].append(value)

    series_name = measure

    chart['chart_config'] = get_chart_config2(chart['title'], chart['categories'], chart['series_data'], series_name)

    return chart

