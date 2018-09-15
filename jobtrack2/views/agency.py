from pyramid.response import Response

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Agency

@view_config(route_name='agency_list', renderer='../templates/agencylist.jinja2')
def agencylist(request):
    try:
        query = request.dbsession.query(Agency)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'agencies': query.all(), 'project': 'JobTrack2'}

@view_config(route_name='agency_detail', renderer='../templates/agencydetail.jinja2', permission='view')
def agencydetail(request):
    agency = request.context.agency
    return {'agency': agency, 'project': 'JobTrack2'}

@view_config(route_name='agency_add', renderer='../templates/agencyedit.jinja2',permission='create')
def agencyadd(request):
    #pagename = request.context.pagename
    if 'form.submitted' in request.params:
        agencyname = request.params['agencyname']
        agency = Agency(name=agencyname)
        agency.creator = request.user
        request.dbsession.add(agency)
        request.dbsession.flush()
        next_url = request.route_url('agency_detail', agencyid=agency.id)
        #next_url = request.route_url('agency_list')
        request.session.flash("success:Agency added.", "alerts")
        return HTTPFound(location=next_url)
    save_url = request.route_url('agency_add')
    return dict(pagedata='', agency=None, save_url=save_url)

@view_config(route_name='agency_edit', renderer='../templates/agencyedit.jinja2', permission='edit')
def agencyedit(request):
    agency = request.context.agency

    if 'form.submitted' in request.params:
        agency.name = request.params['agencyname']
        request.session.flash("success:Agency updated.", "alerts")
        next_url = request.route_url('agency_detail', agencyid=agency.id)
        return HTTPFound(location=next_url)
    return dict(
        agency=agency,
        save_url=request.route_url('agency_edit', agencyid=agency.id),
        )

#TODO: Probably should put this error message somewhere central
db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_jobtrack2_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
