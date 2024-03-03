import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
from calendar import month_name, month_abbr
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = df['date'].apply(pd.to_datetime)
df.set_index('date', inplace=True)
# Clean data
ignore_very_low_pv = df['value'] >= df['value'].quantile(0.025)
ignore_very_high_pv = df['value'] <= df['value'].quantile(0.975)
df = df.loc[(ignore_very_low_pv & ignore_very_high_pv)]


def draw_line_plot():
    # Draw line plot
    fig, axes = plt.subplots(figsize=(16,10))
    timerange_frame = df['5/2016':'12/2019']
    axes.plot(timerange_frame.index, timerange_frame.value, color='red')
    axes.set_ylabel('Page Views')
    axes.set_xlabel('Date')
    axes.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar.reset_index(inplace=True)
    df_bar['year'] = [d.year for d in df_bar.date]
    df_bar['month'] = [d.strftime('%B') for d in df_bar.date]
    df_bar.rename(columns={'value':'pageviews'}, inplace=True)

    month_name_lookup = list(month_name)
    df_bar = df_bar[['month','year', 'pageviews']].groupby(['year', 'month'])['pageviews'].mean().unstack('month')
    df_bar = df_bar[sorted(df_bar.columns, key=month_name_lookup.index)]
    fig, axes = plt.subplots(figsize=(16,10))
    df_bar.plot(ax=axes, kind='bar', xlabel='Years', ylabel='Average Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    df_box.rename(columns={'value':'pageviews'}, inplace=True)

    month_name_lookup = list(month_abbr)
    df_box_monthly_sorted = df_box.sort_values(by=['month'], key=lambda x : x.apply (lambda x : month_name_lookup.index(x)))

    fig, axes = plt.subplots(figsize=(30, 10), nrows=1, ncols=2)
    sns.boxplot(df_box, ax=axes[0], x='year', y='pageviews')\
        .set(ylabel='Page Views', xlabel='Year', title='Year-wise Box Plot (Trend)')
    sns.boxplot(df_box_monthly_sorted, ax=axes[1], x='month', y='pageviews')\
        .set(ylabel='Page Views', xlabel='Month', title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
