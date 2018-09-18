from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPFound,
)
from pyramid.security import (
    Allow,
    Everyone,
)


from .models import Job,Agency,Agent,Company

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('job_list','/job')
    config.add_route('job_detail','/job/{jobid}', factory=job_factory)
    config.add_route('agency_list','/agency')
    config.add_route('agency_detail','/agency/{agencyid}', factory=agency_factory)
    config.add_route('agent_list','/agent')
    config.add_route('agent_detail','/agent/{agentid}', factory=agent_factory)
    config.add_route('company_list','/company')
    config.add_route('company_detail','/company/{companyid}', factory=company_factory)
    config.add_route('agency_add', '/add_agency', factory=new_resource_factory)
    config.add_route('agency_edit', '/agency/{agencyid}/edit', factory=agency_factory)
    config.add_route('agent_add', '/add_agent', factory=new_resource_factory)
    config.add_route('agent_edit', '/agent/{agentid}/edit', factory=agent_factory)
    config.add_route('company_add', '/add_company', factory=new_resource_factory)
    config.add_route('company_edit', '/company/{companyid}/edit', factory=company_factory)
    config.add_route('job_add', '/add_job', factory=new_resource_factory)
    config.add_route('job_edit', '/job/{jobid}/edit', factory=job_factory)



#def new_page_factory(request):
#    pagename = request.matchdict['pagename']
#    if request.dbsession.query(Page).filter_by(name=pagename).count() > 0:
#        next_url = request.route_url('edit_page', pagename=pagename)
#        raise HTTPFound(location=next_url)
#    return NewPage(pagename)
#def page_factory(request):
#    pagename = request.matchdict['pagename']
#    page = request.dbsession.query(Page).filter_by(name=pagename).first()
#    if page is None:
#        raise HTTPNotFound
#    return PageResource(page)
#class PageResource(object):
#    def __init__(self, page):
#        self.page = page
#
#    def __acl__(self):
#        return [
#            (Allow, Everyone, 'view'),
#            (Allow, 'role:editor', 'edit'),
#            (Allow, str(self.page.creator_id), 'edit'),
#        ]

def job_factory(request):
    jobid = request.matchdict['jobid']
    job = request.dbsession.query(Job).filter_by(id=jobid).first()
    if job is None:
        raise HTTPNotFound
    return JobResource(job)



class JobResource(object):
    def __init__(self, job):
        self.job = job

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'role:editor', 'edit'),
            (Allow, str(self.job.creator_id), 'edit'),
        ]



def agency_factory(request):
    agencyid = request.matchdict['agencyid']
    agency = request.dbsession.query(Agency).filter_by(id=agencyid).first()
    if agency is None:
        raise HTTPNotFound
    return AgencyResource(agency)

class AgencyResource(object):
    def __init__(self, agency):
        self.agency = agency

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'role:editor', 'edit'),
            (Allow, str(self.agency.creator_id), 'edit'),
        ]

def agent_factory(request):
    agentid = request.matchdict['agentid']
    agent = request.dbsession.query(Agent).filter_by(id=agentid).first()
    if agent is None:
        raise HTTPNotFound
    return AgentResource(agent)

class AgentResource(object):
    def __init__(self, agent):
        self.agent = agent

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'role:editor', 'edit'),
            (Allow, str(self.agent.creator_id), 'edit'),
        ]


def company_factory(request):
    companyid = request.matchdict['companyid']
    company = request.dbsession.query(Company).filter_by(id=companyid).first()
    if company is None:
        raise HTTPNotFound
    return CompanyResource(company)

class CompanyResource(object):
    def __init__(self, company):
        self.company = company

    def __acl__(self):
        return [
            (Allow, Everyone, 'view'),
            (Allow, 'role:editor', 'edit'),
            (Allow, str(self.company.creator_id), 'edit'),
        ]

#Generic new resource to attach ACL to
def new_resource_factory(request):
    return NewResource()

class NewResource(object):
    #def __init__(self):

    def __acl__(self):
        return [
            (Allow, 'role:editor', 'create'),
            (Allow, 'role:basic', 'create'),
        ]
