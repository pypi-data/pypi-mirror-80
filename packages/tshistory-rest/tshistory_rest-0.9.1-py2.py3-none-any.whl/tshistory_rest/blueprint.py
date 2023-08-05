import json

import pandas as pd
import werkzeug
from flask import (
    Blueprint,
    request,
    make_response
)
from flask_restx import (
    Api as baseapi,
    inputs,
    Resource,
    reqparse
)

from tshistory import api as tsapi, util

from tshistory_rest.util import (
    enum,
    has_formula,
    has_supervision,
    onerror,
    series_response,
    todict,
    utcdt
)


def no_content():
    # see https://github.com/flask-restful/flask-restful/issues/736
    resp = make_response('', 204)
    resp.headers.clear()
    return resp


base = reqparse.RequestParser()

base.add_argument(
    'name', type=str, required=True,
    help='timeseries name'
)

update = base.copy()
update.add_argument(
    'series', type=str,
    help='json representation of the series'
)
update.add_argument(
    'author', type=str, required=True,
    help='author of the insertion'
)
update.add_argument(
    'insertion_date', type=utcdt, default=None,
    help='insertion date can be forced'
)
update.add_argument(
    'tzaware', type=inputs.boolean, default=True,
    help='tzaware series'
)
update.add_argument(
    'metadata', type=todict, default=None,
    help='metadata associated with this insertion'
)
update.add_argument(
    'replace', type=inputs.boolean, default=False,
    help='replace the current series entirely with the provided series '
    '(no update semantics)'
)
if has_supervision():
    update.add_argument(
        'supervision', type=inputs.boolean, default=False,
        help='tell if this is a supervised update'
    )
update.add_argument(
    'bseries', type=werkzeug.datastructures.FileStorage,
    location='files',
    help='series in binary format (if "tshpack" is chosen)'
)
update.add_argument(
    'format', type=enum('json', 'tshpack'), default='json'
)

rename = base.copy()
rename.add_argument(
    'newname', type=str, required=True,
    help='new name of the series'
)

metadata = base.copy()
metadata.add_argument(
    'all', type=inputs.boolean, default=False,
    help='get all metadata, including internal'
)
metadata.add_argument(
    'type', type=enum('standard', 'type', 'interval'),
    default='standard',
    help='specify the kind of needed metadata'
)

put_metadata = base.copy()
put_metadata.add_argument(
    'metadata', type=str, required=True,
    help='set new metadata for a series'
)

insertion_dates = base.copy()
insertion_dates.add_argument(
    'from_insertion_date', type=utcdt, default=None
)
insertion_dates.add_argument(
    'to_insertion_date', type=utcdt, default=None
)

get = base.copy()
get.add_argument(
    'insertion_date', type=utcdt, default=None,
    help='insertion date can be forced'
)
get.add_argument(
    'from_value_date', type=utcdt, default=None
)
get.add_argument(
    'to_value_date', type=utcdt, default=None
)
get.add_argument(
    '_keep_nans', type=inputs.boolean, default=False,
    help='keep erasure information'
)
get.add_argument(
    'format', type=enum('json', 'tshpack'), default='json'
)

delete = base.copy()

history = base.copy()
history.add_argument(
    'from_insertion_date', type=utcdt, default=None
)
history.add_argument(
    'to_insertion_date', type=utcdt, default=None
)
history.add_argument(
    'from_value_date', type=utcdt, default=None
)
history.add_argument(
    'to_value_date', type=utcdt, default=None
)
history.add_argument(
    'diffmode', type=inputs.boolean, default=False
)
history.add_argument(
    '_keep_nans', type=inputs.boolean, default=False
)
history.add_argument(
    'format', type=enum('json', 'tshpack'), default='json'
)

staircase = base.copy()
staircase.add_argument(
    'delta', type=pd.Timedelta, required=True,
    help='time delta in iso 8601 duration'
)
staircase.add_argument(
    'from_value_date', type=utcdt, default=None
)
staircase.add_argument(
    'to_value_date', type=utcdt, default=None
)
staircase.add_argument(
    'format', type=enum('json', 'tshpack'), default='json'
)

catalog = reqparse.RequestParser()
catalog.add_argument(
    'allsources', type=inputs.boolean, default=True
)

# supervision

edited = base.copy()
edited.add_argument(
    'insertion_date', type=utcdt, default=None,
    help='select a specific version'
)
edited.add_argument(
    'from_value_date', type=utcdt, default=None
)
edited.add_argument(
    'to_value_date', type=utcdt, default=None
)
edited.add_argument(
    'format', type=enum('json', 'tshpack'), default='json'
)

# formula

formula = base.copy()
formula.add_argument(
    'expanded', type=inputs.boolean, default=False,
    help='return the recursively expanded formula'
)

formula_components = base.copy()
formula_components.add_argument(
    'expanded', type=inputs.boolean, default=False,
    help='return the recursively expanded formula components'
)

register_formula = base.copy()
register_formula.add_argument(
    'text', type=str, required=True,
    help='source of the formula'
)
register_formula.add_argument(
    'reject_unknown', type=inputs.boolean, default=True,
    help='fail if the referenced series do not exist'
)
register_formula.add_argument(
    # note: `update` won't work as it is a method of parse objects
    'force_update', type=inputs.boolean, default=False,
    help='accept to update an existing formula if true'
)

log = base.copy()
log.add_argument(
    'limit', type=int, default=None,
    help='number of revisions from the most recent'
)
log.add_argument(
    'fromdate', type=utcdt, default=None,
    help='minimal date'
)
log.add_argument(
    'todate', type=utcdt, default=None,
    help='maximal date'
)


def blueprint(tsa,
              title='tshistory api',
              description=(
                  'reading and updating time series state, '
                  'histoy, formulas and metadata'
              )):

    # warn against playing proxy games
    assert isinstance(tsa, tsapi.dbtimeseries)

    bp = Blueprint(
        'tshistory_rest',
        __name__,
        template_folder='tshr_templates',
        static_folder='tshr_static',
    )

    # api & ns

    class Api(baseapi):

        # see https://github.com/flask-restful/flask-restful/issues/67
        def _help_on_404(self, message=None):
            return message or 'No such thing.'

    api = Api(
        bp,
        version='1.0',
        title=title,
        description=description
    )
    api.namespaces.pop(0)  # wipe the default namespace

    ns = api.namespace(
        'series',
        description='Time Series Operations'
    )

    # routes

    @ns.route('/metadata')
    class timeseries_metadata(Resource):

        @api.expect(metadata)
        @onerror
        def get(self):
            args = metadata.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            if args.type == 'standard':
                meta = tsa.metadata(args.name, all=args.all)
                return meta, 200
            elif args.type == 'type':
                stype = tsa.type(args.name)
                return stype, 200
            else:
                assert args.type == 'interval'
                try:
                    ival = tsa.interval(args.name)
                except ValueError as err:
                    return no_content()
                tzaware = tsa.metadata(args.name, all=True).get('tzaware', False)
                return (tzaware,
                        ival.left.isoformat(),
                        ival.right.isoformat()), 200

        @api.expect(put_metadata)
        @onerror
        def put(self):
            args = put_metadata.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            metadata = json.loads(args.metadata)
            try:
                tsa.update_metadata(args.name, metadata)
            except ValueError as err:
                if err.args[0].startswith('not allowed to'):
                    api.abort(405, err.args[0])
                raise

            return '', 200


    @ns.route('/state')
    class timeseries_state(Resource):

        @api.expect(update)
        @onerror
        def patch(self):
            args = update.parse_args()
            if args.format == 'json':
                series = util.fromjson(
                    args.series,
                    args.name,
                    args.tzaware
                )
            else:
                assert args.format == 'tshpack'
                series = util.unpack_series(
                    args.name,
                    args.bseries.stream.read()
                )

            exists = tsa.exists(args.name)
            try:
                if args.replace:
                    diff = tsa.replace(
                        args.name, series, args.author,
                        metadata=args.metadata,
                        insertion_date=args.insertion_date,
                        manual=args.supervision
                    )
                else:
                    diff = tsa.update(
                        args.name, series, args.author,
                        metadata=args.metadata,
                        insertion_date=args.insertion_date,
                        manual=args.supervision
                    )
            except ValueError as err:
                if err.args[0].startswith('not allowed to'):
                    api.abort(405, err.args[0])
                raise

            return series_response(
                args.format,
                diff,
                tsa.metadata(args.name, all=True),
                200 if exists else 201
            )

        @api.expect(rename)
        @onerror
        def put(self):
            args = rename.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')
            if tsa.exists(args.newname):
                api.abort(409, f'`{args.newname}` does exists')

            try:
                tsa.rename(args.name, args.newname)
            except ValueError as err:
                if err.args[0].startswith('not allowed to'):
                    api.abort(405, err.args[0])
                raise

            return no_content()

        @api.expect(get)
        @onerror
        def get(self):
            args = get.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            series = tsa.get(
                args.name,
                revision_date=args.insertion_date,
                from_value_date=args.from_value_date,
                to_value_date=args.to_value_date,
                _keep_nans=args._keep_nans
            )
            # the fast path will need it
            # also it is read from a cache filled at get time
            # so very cheap call
            metadata = tsa.metadata(args.name, all=True)
            assert metadata is not None, f'series {args.name} has no metadata'

            return series_response(
                args.format,
                series,
                metadata,
                200
            )

        @api.expect(delete)
        @onerror
        def delete(self):
            args = delete.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            try:
                tsa.delete(args.name)
            except ValueError as err:
                if err.args[0].startswith('not allowed to'):
                    api.abort(405, err.args[0])
                raise

            return no_content()

    @ns.route('/insertion_dates')
    class timeseries_idates(Resource):

        @api.expect(history)
        @onerror
        def get(self):
            args = insertion_dates.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            idates = tsa.insertion_dates(
                args.name,
                from_insertion_date=args.from_insertion_date,
                to_insertion_date=args.to_insertion_date,
            )
            response = make_response({'insertion_dates':
                [
                    dt.isoformat() for dt in idates
                ]
            })
            response.headers['Content-Type'] = 'text/json'
            return response

    @ns.route('/history')
    class timeseries_history(Resource):

        @api.expect(history)
        @onerror
        def get(self):
            args = history.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            hist = tsa.history(
                args.name,
                from_insertion_date=args.from_insertion_date,
                to_insertion_date=args.to_insertion_date,
                from_value_date=args.from_value_date,
                to_value_date=args.to_value_date,
                diffmode=args.diffmode,
                _keep_nans=args._keep_nans
            )
            metadata = tsa.metadata(args.name, all=True)

            if args.format == 'json':
                if hist is not None:
                    response = make_response(
                        pd.DataFrame(hist).to_json()
                    )
                else:
                    response = make_response('null')
                response.headers['Content-Type'] = 'text/json'
                return response

            response = make_response(
                util.pack_history(metadata, hist)
            )
            response.headers['Content-Type'] = 'application/octet-stream'
            return response

    @ns.route('/staircase')
    class timeseries_staircase(Resource):

        @api.expect(staircase)
        @onerror
        def get(self):
            args = staircase.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            series = tsa.staircase(
                args.name, delta=args.delta,
                from_value_date=args.from_value_date,
                to_value_date=args.to_value_date,
            )
            metadata = tsa.metadata(args.name, all=True)

            if args.format == 'json':
                if series is not None:
                    response = make_response(
                        series.to_json(orient='index', date_format='iso')
                    )
                else:
                    response = make_response('null')
                response.headers['Content-Type'] = 'text/json'
                return response

            response = make_response(
                util.pack_series(metadata, series)
            )
            response.headers['Content-Type'] = 'application/octet-stream'
            return response

    @ns.route('/catalog')
    class timeseries_catalog(Resource):

        @api.expect(catalog)
        @onerror
        def get(self):
            args = catalog.parse_args()
            cat = {
                f'{uri}!{ns}': series
                for (uri, ns), series in tsa.catalog(allsources=args.allsources).items()
            }
            return cat

    @ns.route('/log')
    class series_log(Resource):

        @api.expect(formula)
        @onerror
        def get(self):
            args = log.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            logs = []
            for item in tsa.log(
                args.name,
                limit=args.limit,
                fromdate=args.fromdate,
                todate=args.todate):
                item['date'] = item['date'].isoformat()
                logs.append(item)

            return logs, 200

    if has_supervision():

        @ns.route('/supervision')
        class series_supervision(Resource):

            @api.expect(edited)
            @onerror
            def get(self):
                args = edited.parse_args()
                if not tsa.exists(args.name):
                    api.abort(404, f'`{args.name}` does not exists')
                if getattr(tsa, 'formula', False):
                    if tsa.formula(args.name):
                        api.abort(404, f'`{args.name}` is a formula')

                series, markers = tsa.edited(
                    args.name,
                    revision_date=args.insertion_date,
                    from_value_date=args.from_value_date,
                    to_value_date=args.to_value_date,
                )
                metadata = tsa.metadata(args.name, all=True)
                assert metadata is not None, f'series {args.name} has no metadata'

                if args.format == 'json':
                    if series is not None:
                        df = pd.DataFrame()
                        df['series'] = series
                        df['markers'] = markers
                        response = make_response(
                            df.to_json(orient='index',
                                       date_format='iso')
                        )
                    else:
                        response = make_response('null')
                    response.headers['Content-Type'] = 'text/json'
                    response.status_code = 200
                    return response

                assert args.format == 'tshpack'
                markersmeta = util.series_metadata(markers)
                response = make_response(
                    util.pack_many_series(
                        [
                            (metadata, series),
                            (markersmeta, markers)
                        ]
                    )
                )
                response.headers['Content-Type'] = 'application/octet-stream'
                response.status_code = 200
                return response


    if not has_formula():
        return bp

    # formula extension if the plugin is there

    @ns.route('/formula')
    class timeseries_formula(Resource):

        @api.expect(formula)
        @onerror
        def get(self):
            args = formula.parse_args()
            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            if not tsa.type(args.name):
                api.abort(409, f'`{args.name}` exists but is not a formula')

            form = tsa.formula(args.name, args.expanded)
            return form, 200


        @api.expect(register_formula)
        @onerror
        def patch(self):
            args = register_formula.parse_args()

            exists = tsa.formula(args.name)
            try:
                tsa.register_formula(
                    args.name,
                    args.text,
                    reject_unknown=args.reject_unknown,
                    update=args.force_update
                )
            except TypeError as err:
                api.abort(409, err.args[0])
            except ValueError as err:
                api.abort(409, err.args[0])
            except AssertionError as err:
                api.abort(409, err.args[0])
            except SyntaxError:
                api.abort(400, f'`{args.name}` has a syntax error in it')
            except Exception:
                raise

            return '', 200 if exists else 201

    @ns.route('/formula_components')
    class timeseries_formula_components(Resource):

        @api.expect(formula_components)
        def get(self):
            args = formula_components.parse_args()

            if not tsa.exists(args.name):
                api.abort(404, f'`{args.name}` does not exists')

            if not tsa.type(args.name):
                api.abort(409, f'`{args.name}` exists but is not a formula')

            form = tsa.formula_components(args.name, args.expanded)
            return form, 200

    return bp
