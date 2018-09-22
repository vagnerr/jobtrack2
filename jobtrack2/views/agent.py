from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from sqlalchemy.exc import DBAPIError


from ..models import Agent,Agency

@view_config(route_name='agent_list', renderer='../templates/agentlist.jinja2')
@view_config(route_name='agent_list_jn', renderer='json')  # TODO change to use predicates
def agentlist(request):
    try:
        query = request.dbsession.query(Agent)
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    if 'agencyid' in request.params:
        return {
            'agents': query.filter_by(agency_id=request.params['agencyid']),
            'project': 'JobTrack2'
        }
    return {'agents': query.all(), 'project': 'JobTrack2'}

@view_config(route_name='agent_detail', renderer='../templates/agentdetail.jinja2', permission='view')
def agentdetail(request):
    agent = request.context.agent
    return {'agent': agent, 'project': 'JobTrack2'}

@view_config(route_name='agent_add', renderer='../templates/agentedit.jinja2',permission='create')
def agentadd(request):
    #pagename = request.context.pagename
    if 'form.submitted' in request.params:
        agentname = request.params['agentname']
        agent = Agent(name=agentname)
        agent.creator = request.user
        agency = request.dbsession.query(Agency).filter_by(name=request.params['agency']).first()
        agent.agency = agency
        request.dbsession.add(agent)
        request.dbsession.flush()
        next_url = request.route_url('agent_detail', agentid=agent.id)
        #next_url = request.route_url('agent_list')
        request.session.flash("success:Agent added.", "alerts")
        return HTTPFound(location=next_url)
    save_url = request.route_url('agent_add')
    if 'agencyid' in request.params:
        # Adding agent via agency so we fix the agency
        agency = request.dbsession.query(Agency).filter_by(id=request.params['agencyid']).first()
        return dict(
                pagedata='',
                agent=None,
                agency=agency,
                save_url=save_url,
                page_title="Add Agent to Agency",
                )

    agencies = _agencylist(request)
    return dict(
            pagedata='',
            agent=None,
            agencies=agencies,
            save_url=save_url,
            page_title="New Agent",
            )

@view_config(route_name='agent_edit', renderer='../templates/agentedit.jinja2', permission='edit')
def agentedit(request):
    agent = request.context.agent
    if 'form.submitted' in request.params:
        agent.name = request.params['agentname']
        agency = request.dbsession.query(Agency).filter_by(name=request.params['agency']).first()
        agent.agency = agency
        request.session.flash("success:Agent updated.", "alerts")
        next_url = request.route_url('agent_detail', agentid=agent.id)
        return HTTPFound(location=next_url)

    agencies = _agencylist(request)
    return dict(
        agent=agent,
        agencies=agencies,
        save_url=request.route_url('agent_edit', agentid=agent.id),
        page_title="Edit Agent",
        )


def _agencylist(request, withnone=True):
    agencies = list(request.dbsession.query(Agency))
    if withnone:
        agencies.insert(0, Agency(name="--None--", id=0))

    return agencies


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
