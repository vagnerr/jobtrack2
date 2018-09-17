from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from ..models import Company

@view_config(route_name='company_list', renderer='../templates/companylist.jinja2')
def companylist(request):
    try:
        query = request.dbsession.query(Company)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'companies': query.all(), 'project': 'JobTrack2'}

@view_config(route_name='company_detail', renderer='../templates/companydetail.jinja2', permission='view')
def companydetail(request):
    company = request.context.company
    return {'company': company, 'project': 'JobTrack2'}

@view_config(route_name='company_add', renderer='../templates/companyedit.jinja2',permission='create')
def companyadd(request):
    #pagename = request.context.pagename
    if 'form.submitted' in request.params:
        companyname = request.params['companyname']
        company = Company(name=companyname)
        company.creator = request.user
        request.dbsession.add(company)
        request.dbsession.flush()
        next_url = request.route_url('company_detail', companyid=company.id)
        #next_url = request.route_url('company_list')
        request.session.flash("success:Company added.", "alerts")
        return HTTPFound(location=next_url)
    save_url = request.route_url('company_add')
    return dict(pagedata='', company=None, save_url=save_url,page_title="New Company",)

@view_config(route_name='company_edit', renderer='../templates/companyedit.jinja2', permission='edit')
def agencyedit(request):
    company = request.context.company

    if 'form.submitted' in request.params:
        company.name = request.params['companyname']
        request.session.flash("success:Company updated.", "alerts")
        next_url = request.route_url('company_detail', companyid=company.id)
        return HTTPFound(location=next_url)
    return dict(
        company=company,
        save_url=request.route_url('company_edit', companyid=company.id),
        page_title="Edit Company",
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
