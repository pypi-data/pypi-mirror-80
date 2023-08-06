from csvkitcat import agate, parse_column_identifiers
from csvkitcat.agatable import AgatableUtil
from csvkitcat.exceptions import *
from csvkitcat.pandashelper import agate_to_df
import warnings

import altair_viewer as altview
import altair as alt


class ChartableUtil(AgatableUtil):
    description = """Chart type"""
    override_flags = ['f', 'L', 'blanks', 'date-format', 'datetime-format']

    def add_arguments(self):

        self.argparser.add_argument(metavar='FILE', nargs='?', dest='input_path',
                                    help='The CSV file to operate on. If omitted, will accept input as piped data via STDIN.')

        self.argparser.add_argument('-X', '--xvar', dest='xvar', type=str, default='1')
        self.argparser.add_argument('-Y', '--yvar', dest='yvar', type=str, default='2')

        self.argparser.add_argument('-W', '--width', dest='chart_width', type=int, default=80)


        self.argparser.add_argument('--printable', dest='printable_chars_only',
                                    default=False, action='store_true',
                                    help='Chart renderers only use printable chars. This is useful for testing mostly')


        self.argparser.add_argument('-y', '--snifflimit', dest='sniff_limit', type=int,
                                    help='Limit CSV dialect sniffing to the specified number of bytes. Specify "0" to disable sniffing entirely.')
        self.argparser.add_argument('-I', '--no-inference', dest='no_inference', action='store_true',
                                    help='Disable type inference when parsing the input.')


    def main():
        if self.additional_input_expected():
            self.argparser.error('You must provide an input file or piped data.')

        agtable = agate.Table.from_csv(
            self.input_file,
            skip_lines=self.args.skip_lines,
            sniff_limit=self.args.sniff_limit,
            **self.reader_kwargs
        )
        column_names = agtable.column_names

        _xid = parse_column_identifiers(
            self.args.xvar,
            column_names,
            column_offset=1,  # TK, do I need to worry about this?
            excluded_columns=getattr(self.args, 'not_columns', None)
        )

        _yid = parse_column_identifiers(
            self.args.yvar,
            column_names,
            column_offset=1,  # TK, do I need to worry about this?
            excluded_columns=getattr(self.args, 'not_columns', None)
        )

        if (len(_xid)) != 1:
            raise ArgumentErrorTK(f'--xvar must point to a single column id/name, not {_xid=}')
        elif (len(_yid)) != 1:
            raise ArgumentErrorTK(f'--yvar must point to a single column id/name, not {_yid=}')


        xcol = column_names[_xid[0]]
        ycol = column_names[_yid[0]]


        df = agate_to_df(agtable)
        # altair horizontal charts switch up how x and y are encoded
        # https://altair-viz.github.io/gallery/bar_chart_horizontal.html
        chart = alt.Chart(df).mark_bar().encode(y=xcol, x=ycol)
        altview.show(chart)
