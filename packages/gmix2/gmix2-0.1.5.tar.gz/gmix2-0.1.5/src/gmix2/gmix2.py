import cgmix2

import logging
import operator as op

import numpy as np

from cgmix2 import *
from functools import reduce
from typing import List, Optional, Tuple

log = logging.getLogger(__name__)


def _make_mixture_names(names, n):
    names = np.array(names) if names else np.arange(n)
    return (
        np.char.mod('%03d', names)
        if all([isinstance(n, (int, np.int, np.int16, np.int32, np.int64)) for n in names])
        else names
    )


def _make_plot_range(x_min, x_max, mu, sigma):
    min_mu, max_mu, max_sigma = np.min(mu), np.max(mu), np.max(sigma)

    x_min = min_mu - 2.5 * max_sigma if x_min is None else x_min
    x_max = max_mu + 2.5 * max_sigma if x_max is None else x_max

    return x_min, x_max


def _make_mixture_parameters(weight, mean, std):
    import pandas as pd

    # A simple utility method for making a data frame for each parameter array
    # of the correct shape.
    def make_df(a: np.ndarray, value_name: str):
        t = pd.DataFrame(a.transpose())
        t.columns = np.arange(a.shape[0])
        t['kernel'] = np.arange(a.shape[1])

        return t.melt('kernel', var_name='mixture_name', value_name=value_name)

    # Merge each individual dataframe into a single one.
    dfs = (make_df(weight, 'weight'), make_df(mean, 'mu'), make_df(std, 'sigma'))
    return reduce(lambda a, b: pd.merge(a, b, how='left', on=['kernel', 'mixture_name']), dfs)


def _make_mixture_frame(weight, mean, std, x):
    import pandas as pd

    try:
        from scipy.stats import norm
    except ImportError:
        raise ImportError("You need scipy in order plot the individual mixtures.")

    param_df = _make_mixture_parameters(weight, mean, std)

    # Compute the weighted Normal pdf values for each row in the param_df and
    # store them in a new data frame.
    normal_df = pd.DataFrame(
        np.repeat(param_df.values, len(x), axis=0),
        columns=param_df.columns,
        index=np.tile(x, len(param_df))
    ).rename_axis('x').reset_index()

    # Calculate the pdf values for each data point
    normal_df['y'] = normal_df.apply(
        lambda r: r['weight'] * norm.pdf(r['x'], r['mu'], r['sigma']),
        axis=1
    )

    # Convert the kernel and group columns to categorical data types
    cat_columns = ['kernel', 'mixture_name']
    normal_df[cat_columns] = normal_df[cat_columns].apply(lambda t: t.astype('category'))

    # Reorder the columns to put y next to x (for human readability)
    normal_df = normal_df[['mixture_name', 'kernel', 'weight', 'mu', 'sigma', 'x', 'y']]

    df = normal_df[['mixture_name', 'x', 'y']].groupby(
        ['mixture_name', 'x']
    ).agg({
        'y': 'sum'
    }).reset_index()

    return normal_df, df


def _make_point_df(x, weight, mean, std, mixture_names):
    import pandas as pd

    y = [
        pdf(xv.item(), weight[None, i], mean[None, i], std[None, i])[0]
        for i, xv in enumerate(np.nditer(x))
    ]
    df = pd.DataFrame({'x': x, 'y': y, 'mixture_name': mixture_names})

    return df


# noinspection PyTypeChecker
def plot(
        weights: np.ndarray,
        means: np.ndarray,
        stds: np.ndarray,
        mixture_names: Optional[List[str]] = None,
        x_min: Optional[float] = None,
        x_max: Optional[float] = None,
        x_ticks: Optional[List[float]] = None,
        n_points: int = 1000,
        show_mixture: bool = False,
        show_mean: bool = False,
        show_median: bool = False,
        show_mode: bool = False,
        percent_interval: Optional[float] = None,
        legend_title: str = 'Mixture Name',
        wrap_cols: Optional[int] = None,
        palette: str = 'Dark2',
        figure_size: Tuple[float, float] = None
):
    """
    Plot one or more mixtures. By default multiple mixtures will be shown in the same plotting area each with
    a separate color. You can use ``wrap_cols`` to plot them in on separate areas with ``wrap_cols`` plots
    per row.

    :param weights: The weights of the mixtures to plot. This should be a 2 dimensional shape where each column
           is an individual weight (that sums to 1.0) and each row is a different mixture.
    :param means: The means of the mixtures.
    :param stds: The standard deviations of the mixtures.
    :param mixture_names: The names of each mixture, if given, otherwise generic names will be provided.
    :param x_min: The minimum x value to plot. If no value is given a default value based on the distributions
           will be used.
    :param x_max: The maximum x value to plot. If no value is given a default value based on the distributions
           will be used.
    :param x_ticks: Explicitly provide breaks for the x-axis tick marks.
    :param n_points: The number of points to plot. More points will provide a smoother curve, but will take
           more time to plot.
    :param show_mixture: If ``True``, each individual component will also be shown on the plot.
    :param show_mean: If ``True``, the mean value will be shown on the plot as a text annotation.
    :param show_median: If ``True``, the median value will be shown on the plot as a text annotation.
    :param show_mode: If ``True``, the modes of the plot will be shown on the plot as a text annotation.
    :param percent_interval: If this is not ``None`` the given percent interval will be highlighted on the plot.
    :param legend_title: Optionally, give the legend a specific title other than the default.
    :param wrap_cols: Plot each mixture individually and wrap the figure at this many columns.
    :param palette: Choose a colorbrewer palette for plotting multiple mixtures.
    :param figure_size: Specify a figure size in inches.
    :return: The `plotnine <https://plotnine.readthedocs.io/en/stable/>`_ object.
    """
    try:
        import pandas as pd
        import plotnine as p9
        # NOTE: pycairo needs to be installed separately otherwise matplotlib will complain
        #       You also need to install a package for rendering (e.g., pip install PyQt5 works)
    except ImportError:
        raise ValueError("You need Pandas and Plotnine to plot distributions")

    if weights.ndim == 1:
        weights = np.expand_dims(weights, 0)
        means = np.expand_dims(means, 0)
        stds = np.expand_dims(stds, 0)

    n_mixtures = weights.shape[0]
    mixture_names = _make_mixture_names(mixture_names, n_mixtures)

    x_min, x_max = _make_plot_range(x_min, x_max, means, stds)
    x = np.linspace(x_min, x_max, num=n_points)

    show_legend = n_mixtures > 1

    p = p9.ggplot()

    if show_mixture:
        normal_df, df = _make_mixture_frame(weights, means, stds, x)
        df['mixture_name'] = np.repeat(mixture_names, n_points)

        p += p9.geom_path(
            data=normal_df,
            mapping=p9.aes('x', 'y', color='mixture_name'),
            alpha=0.5,
            show_legend=False
        )

    # If we aren't showing the individual mixtures we can compute the pdf
    # using the C++ interface.
    the_pdf = pdf(x, weights, means, stds).ravel()
    df = pd.DataFrame(the_pdf, columns=['y'])
    df['x'] = np.tile(x, n_mixtures)

    df['mixture_name'] = np.repeat(mixture_names, n_points)

    # Add some end points so that the area under the curve gets filled in
    # completely along the x-axis by the geom_polygon.
    end_point_data = []
    for grp in mixture_names:
        end_point_data.append({'mixture_name': grp, 'x': x_min - 0.1, 'y': 0})
        end_point_data.append({'mixture_name': grp, 'x': x_max + 0.1, 'y': 0})
    end_point_df = pd.DataFrame(end_point_data)
    df = df.append(end_point_df)
    df.sort_values(['mixture_name', 'x'], inplace=True)

    p += p9.geom_polygon(
        data=df,
        mapping=p9.aes('x', 'y', fill='mixture_name'),
        alpha=0.25,
        color='black',
        show_legend=show_legend
    )

    if show_mean:
        mean_df = _make_point_df(cgmix2.mean(weights, means), weights, means, stds, mixture_names)
        segment_aes = p9.aes(x='x', xend='x', y=0, yend='y', color='mixture_name')
        text_aes = p9.aes(x='x', y=0, label='x')
        text_kw = {'format_string': 'μ: {:0.3f}', 'ha': 'left', 'va': 'top'}

        p += p9.geom_segment(mean_df, segment_aes, size=1.25, show_legend=False)
        p += p9.geom_text(text_aes, data=mean_df, **text_kw)

    if show_median or percent_interval:
        median_df = _make_point_df(median(weights, means, stds), weights, means, stds, mixture_names)
        segment_aes = p9.aes(x='x', xend='x', y=0, yend='y', color='mixture_name')
        text_aes = p9.aes(x='x', y='y', label='x')
        text_kw = {'format_string': 'x̃: {:0.3f}', 'ha': 'left', 'va': 'bottom'}

        p += p9.geom_segment(
            median_df,
            segment_aes,
            linetype='dashed',
            size=1.25,
            show_legend=False
        )
        p += p9.geom_text(text_aes, data=median_df, **text_kw)

    if show_mode:
        modes = mode(weights, means, stds)

        d = [
            dict(mixture_name=mixture_names[i], x=a, y=b)
            for i, m in enumerate(modes)
            for a, b in m
        ]

        mode_df = pd.DataFrame(d)

        segment_aes = p9.aes(x='x', xend='x', y=0, yend='y', color='mixture_name')
        text_aes = p9.aes(x='x', y='y/2', label='x', angle=-90)
        text_kw = {'format_string': 'x̂: {:0.3f}', 'ha': 'left', 'va': 'center', 'nudge_y': -0.005}

        p += p9.geom_segment(
            mode_df,
            segment_aes,
            linetype='dotted',
            size=1.25,
            show_legend=False
        )
        p += p9.geom_text(text_aes, data=mode_df, **text_kw)

    if percent_interval:
        if not 0 < percent_interval < 1:
            log.error(f"The percent interval must be between 0 and 100: {percent_interval}")
            raise ValueError("The percent interval must be between 0 and 100")

        def make_limit_df(bound_df, is_lower: bool):
            fn = op.le if is_lower else op.ge

            start = -1 if is_lower else 0
            stop = None if is_lower else 1

            # Select all the rows from the gmix_df that are outside the PI
            # for each group
            df_list = [
                df.loc[(fn(df.x, row.x)) & (df.mixture_name == row.mixture_name), ]
                for _, row in bound_df.iterrows()
            ]
            tmp_df = pd.concat(df_list)

            # We need to drop the polygon to zero at the interval boundary,
            # so create a new row that has the same x values of the last point
            # of the lower bound and the first point of the upper bound, but
            # set the y value to 0.
            last_point = tmp_df.groupby('mixture_name').apply(
                lambda g: pd.DataFrame(g.iloc[start:stop, ].values, columns=g.columns)
            )
            last_point['y'] = 0
            tmp_df = tmp_df.append(last_point)
            tmp_df.reset_index(drop=True, inplace=True)

            # Make sure the columns are of the correct type (for some reason they
            # get reset to 'object' above.
            tmp_df['mixture_name'] = tmp_df.mixture_name.astype('category')
            tmp_df[['x', 'y']] = tmp_df[['x', 'y']].apply(lambda c: c.astype('float'))

            return tmp_df

        h = (1 - percent_interval) / 2
        lb = h
        ub = percent_interval + h

        lb_df = _make_point_df(ppf(lb, weights, means, stds), weights, means, stds, mixture_names)
        up_df = _make_point_df(ppf(ub, weights, means, stds), weights, means, stds, mixture_names)

        lower_df = make_limit_df(lb_df, True)
        upper_df = make_limit_df(up_df, False)

        poly_kw = {'alpha': 0.6, 'show_legend': False}

        p += p9.geom_polygon(lower_df, p9.aes('x', 'y', fill='mixture_name'), **poly_kw)
        p += p9.geom_polygon(upper_df, p9.aes('x', 'y', fill='mixture_name'), **poly_kw)

    if wrap_cols and n_mixtures > 1:
        p += p9.facet_wrap('~ mixture_name', ncol=wrap_cols)

    if x_ticks:
        p += p9.scale_x_continuous(breaks=x_ticks)

    if n_mixtures == 1:
        p += p9.scale_fill_grey()
        p += p9.scale_color_grey()

        title = f"{mixture_names[0]}"

        if percent_interval:
            title += f" With {percent_interval:0.3f} PI"
    else:
        p += p9.scale_fill_brewer(palette=palette, type='qualitative', name=legend_title)
        p += p9.scale_color_brewer(palette=palette, type='qualitative')

        title = "Density Plot"

        if percent_interval:
            title += f" With {percent_interval:0.3f} PI"

    p += p9.ylab('Density')
    p += p9.ggtitle(title)
    p += p9.theme_bw()

    if figure_size:
        p += p9.theme(figure_size=figure_size)

    return p
