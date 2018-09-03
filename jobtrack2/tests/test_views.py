import unittest
import transaction

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        from ..models import get_tm_session,User
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('..models')
        self.config.include('..routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()
        sys_user = User(name='SYSTEM', role='ADMIN')
        self.sys_user=sys_user

    def init_database(self):
        from ..models.meta import Base
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        Base.metadata.create_all(engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def makeJob(self, title, salary):
        from ..models import Job
        job = Job(title = title, salary = salary, creator=self.sys_user)

        return job

    def makeAgency(self, name):
        from ..models import Agency
        return Agency(name=name, creator=self.sys_user)

    def makeAgent(self, name):
        from ..models import Agent
        return Agent(name=name, creator=self.sys_user)

    def makeCompany(self, name):
        from ..models import Company
        return Company(name=name, creator=self.sys_user)


class ViewAgencyTests(BaseTest):
    def _callFUT(self, request):
        from jobtrack2.views.agency import agencydetail
        return agencydetail(request)

    def test_it(self):
        from ..routes import AgencyResource

        # add a page to the db
        agency = self.makeAgency('Agency1a')

        self.session.add_all([agency])

        # create a request asking for the page we've created
        request = dummy_request(self.session)
        request.context = AgencyResource(agency)

        # call the view we're testing and check its behavior
        info = self._callFUT(request)
        self.assertEqual(info['agency'], agency)
#        NOTE: assertIn() may be a better approach to this
#        self.assertEqual(
#            info['content'],
#            'arbitrary content'
#           )
#        self.assertEqual(info['edit_url'],
#                         'http://example.com/IDoExist/edit_page')


class ViewAgentTests(BaseTest):
    def _callFUT(self, request):
        from jobtrack2.views.agent import agentdetail
        return agentdetail(request)

    def test_it(self):
        from ..routes import AgentResource

        # add a page to the db
        agent = self.makeAgent('Agent1a')

        self.session.add_all([agent])

        # create a request asking for the page we've created
        request = dummy_request(self.session)
        request.context = AgentResource(agent)

        # call the view we're testing and check its behavior
        info = self._callFUT(request)
        self.assertEqual(info['agent'], agent)


class ViewJobTests(BaseTest):
    def _callFUT(self, request):
        from jobtrack2.views.job import jobdetail
        return jobdetail(request)

    def test_it(self):
        from ..routes import JobResource

        # add a page to the db
        job = self.makeJob('job1a','salary1a')

        self.session.add_all([job])

        # create a request asking for the page we've created
        request = dummy_request(self.session)
        request.context = JobResource(job)

        # call the view we're testing and check its behavior
        info = self._callFUT(request)
        self.assertEqual(info['job'], job)


class ViewCompanyTests(BaseTest):
    def _callFUT(self, request):
        from jobtrack2.views.company import companydetail
        return companydetail(request)

    def test_it(self):
        from ..routes import CompanyResource

        # add a page to the db
        company = self.makeCompany('company1a')

        self.session.add_all([company])

        # create a request asking for the page we've created
        request = dummy_request(self.session)
        request.context = CompanyResource(company)

        # call the view we're testing and check its behavior
        info = self._callFUT(request)
        self.assertEqual(info['company'], company)
