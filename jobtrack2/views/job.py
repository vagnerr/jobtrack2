from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError

from ..models import Job,NextAction,JobType,Company,Location,Source,Agency,Agent,Status

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
        job = Job(
            title = request.params['title'],
            reference = request.params['reference'],
            nextaction_id = request.params['nextaction'],
            type_id = request.params['type'],
            salary = request.params['salary'],
            company_id = request.params['company'],
            location_id = request.params['location'],
            source_id = request.params['source'],
            agency_id = request.params['agency'],
            status_id = request.params['status'],
        )
        job.creator = request.user

        if 'agent' in request.params:
            agent = request.dbsession.query(Agent).filter_by(id=request.params['agent']).first()
            job.agents.append(agent)
        request.dbsession.add(job)
        request.dbsession.flush()
        next_url = request.route_url('job_detail', jobid=job.id)
        #next_url = request.route_url('job_list')
        request.session.flash("success:Job added.", "alerts")
        return HTTPFound(location=next_url)
    save_url = request.route_url('job_add')
    selectors = _get_job_selectors(request)
    if 'companyid' in request.params:
        # Adding agent via agency so we fix the agency
        company = request.dbsession.query(Company).filter_by(id=request.params['companyid']).first()
        selectors.update({'companies': company} )

    if 'agentid' in request.params:
        # Adding agent via agency so we fix the agency
        agent = request.dbsession.query(Agent).filter_by(id=request.params['agentid']).first()
        selectors.update({'agents': agent, 'agencies': None} )

    if 'agencyid' in request.params:
        # Adding agent via agency so we fix the agency
        agency = request.dbsession.query(Agency).filter_by(id=request.params['agencyid']).first()
        selectors.update({'agencies': agency} )
        if 'agents' not in selectors:
            # we have an agency, but no agent so allow a filtered selection
            selectors.update(
                {
                   'agents': request.dbsession.query(Agent).filter_by(agency_id=request.params['agencyid'])
                }
            )

    return dict(
        **selectors,
        pagedata='',
        job=Job(),
        save_url=save_url,
        page_title="New Job",
        )

@view_config(route_name='job_edit', renderer='../templates/jobedit.jinja2', permission='edit')
def jobedit(request):
    job = request.context.job

    if 'form.submitted' in request.params:
        job.title = request.params['title']
        job.reference = request.params['reference']
        job.nextaction_id = request.params['nextaction']
        job.type_id = request.params['type']
        job.salary = request.params['salary']
        job.company_id = request.params['company']
        job.location_id = request.params['location']
        job.source_id = request.params['source']
        job.agency_id = request.params['agency']
        job.status_id = request.params['status']

        request.session.flash("success:Job updated.", "alerts")
        next_url = request.route_url('job_detail', jobid=job.id)
        return HTTPFound(location=next_url)
    selectors = _get_job_selectors(request)
    if job.agency_id:
        agents = request.dbsession.query(Agent).filter_by(agency_id=job.agency_id)
        selectors.update({'agents': agents})

    return dict(
        **selectors,
        job=job,
        save_url=request.route_url('job_edit', jobid=job.id),
        page_title="Edit Job",
        )

def _get_job_selectors(request):
    return dict(
        nextactions=request.dbsession.query(NextAction),
        jobtypes=request.dbsession.query(JobType),
        companies=request.dbsession.query(Company),
        locations=request.dbsession.query(Location),
        sources=request.dbsession.query(Source),
        agencies=request.dbsession.query(Agency),
        statuses=request.dbsession.query(Status),
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
