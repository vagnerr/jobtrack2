from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from ..models import Job,NextAction,JobType,Company,Location,Source,Agency,Status

@view_config(route_name='job_list', renderer='../templates/joblist.jinja2')
def joblist(request):
    try:
        query = request.dbsession.query(Job)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'jobs': query.all(), 'project': 'JobTrack2'}


@view_config(route_name='job_detail', renderer='../templates/jobdetail.jinja2', permission='view')
def jobdetail(request):
    job = request.context.job
    return {'job': job, 'project': 'JobTrack2'}

@view_config(route_name='job_add', renderer='../templates/jobedit.jinja2',permission='create')
def jobadd(request):
    #pagename = request.context.pagename
    if 'form.submitted' in request.params:
        jobname = request.params['jobname']
        job = Job(name=jobname)
        job.creator = request.user
        request.dbsession.add(job)
        request.dbsession.flush()
        next_url = request.route_url('job_detail', jobid=job.id)
        #next_url = request.route_url('job_list')
        request.session.flash("success:Job added.", "alerts")
        return HTTPFound(location=next_url)
    save_url = request.route_url('job_add')
    return dict(pagedata='', job=None, save_url=save_url,page_title="New Job",)

@view_config(route_name='job_edit', renderer='../templates/jobedit.jinja2', permission='edit')
def jobedit(request):
    job = request.context.job

    if 'form.submitted' in request.params:
        job.name = request.params['jobname']
        request.session.flash("success:Job updated.", "alerts")
        next_url = request.route_url('job_detail', jobid=job.id)
        return HTTPFound(location=next_url)

    actions = list(request.dbsession.query(NextAction))
    return dict(
        job=job,
        nextactions=actions,
        jobtypes=request.dbsession.query(JobType),
        companies=request.dbsession.query(Company),
        locations=request.dbsession.query(Location),
        sources=request.dbsession.query(Source),
        agencies=request.dbsession.query(Agency),
        statuses=request.dbsession.query(Status),
        save_url=request.route_url('job_edit', jobid=job.id),
        page_title="Edit Job",
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
