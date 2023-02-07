import flask
import regdb
import regdetailsdb

#-----------------------------------------------------------------------

app = flask.Flask(__name__, template_folder = '.')

#-----------------------------------------------------------------------

def _reg_error_response(msg):
    html_code = flask.render_template('regerror.html', error_msg=msg)
    response = flask.make_response(html_code)
    return response

def _regdetails_error_response(msg):
    html_code = flask.render_template('regdetailserror.html',
        error_msg=msg)
    response = flask.make_response(html_code)
    return response

@app.route('/searchresults', methods=['GET'])
def search_results():
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''
    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum = ''
    area = flask.request.args.get('area')
    if area is None:
        area = ''
    title = flask.request.args.get('title')
    if title is None:
        title = ''

    rows = regdb.database(dept, coursenum, area, title)

    # handle database related errors
    if rows[0] is True:
        response = flask.make_response(rows[1])
        return response

    html_code = '<table class="table table-striped">'
    html_code += '<tbody class="col-sm-12">'
    html_code += '<tr><td><strong>ClassId</strong></td>'
    html_code += '<td><strong>Dept</strong></td>'
    html_code += '<td><strong>Num</strong></td>'
    html_code += '<td><strong>Area</strong></td>'
    html_code += '<td><strong>Title</strong></td></tr>'
    pattern = '<tr><td><a target="_blank" href="%s">%s</a></td>'
    pattern += '<td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'

    for row in rows[1]:
        link = flask.url_for('regdetails', classid=row[0])
        html_code += pattern % (link, row[0], row[4], row[5], row[6],
            row[7])

    html_code += '</tbody></table>'

    response = flask.make_response(html_code)

    return response

@app.route('/', methods=['GET'])
def index():
    dept = flask.request.args.get('dept')
    if dept is None:
        dept = ''
    coursenum = flask.request.args.get('coursenum')
    if coursenum is None:
        coursenum = ''
    area = flask.request.args.get('area')
    if area is None:
        area = ''
    title = flask.request.args.get('title')
    if title is None:
        title = ''

    rows = regdb.database(dept, coursenum, area, title)

    # handle database related errors
    if rows[0] is True:
        return _reg_error_response(rows[1])

    html_code = flask.render_template('index.html', rows=rows[1],
        dept=dept, coursenum=coursenum, area=area, title=title)

    response = flask.make_response(html_code)

    return response

@app.route('/regdetails', methods=['GET'])
def regdetails():
    classid = flask.request.args.get('classid')

    # handle missing classid case
    if classid is None or classid == '':
        return _regdetails_error_response('missing classid')

    # handle non-integer classid caser
    digits = set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    for i in classid:
        if i not in digits:
            return _regdetails_error_response('non-integer classid')

    classid = int(classid)
    info = regdetailsdb.database(classid)

    # handle database related errors
    if info[0] is True:
        return _regdetails_error_response(info[2])

    # handle non-existing classid case
    if info[1] is True:
        return _regdetails_error_response(info[2])

    # handle valid, existing classid with no database related error case
    details, dept, num, prof, classid = regdetailsdb.database(classid)
    html_code = flask.render_template('regdetails.html',
        classid=classid, details=details, dept=dept, num=num, prof=prof,
        zip=zip)
    response = flask.make_response(html_code)

    return response
