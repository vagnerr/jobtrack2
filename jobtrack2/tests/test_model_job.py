import unittest
import transaction

from pyramid import testing


class BaseTest(unittest.TestCase):

    def setUp(self):
        from ..models import get_tm_session
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('..models')
        self.config.include('..routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

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
        return Job(title=title, salary=salary)

#    def makeUser(self, name, role):
#        from ..models import User
#        return User(name=name, role=role)



class TestRelatedJob(BaseTest):
    def test_related_job(self):
        from ..models import JobRelated
        parent_job = self.makeJob('job1', 'salary1')
        child_job = self.makeJob('job2', 'salary2')
        #parent_job.child_jobs.append(child_job)
        jobrelate = JobRelated(parent=parent_job, child=child_job, description='relatedtest')
        self.assertEqual(jobrelate.parent.title, 'job1')
        self.assertEqual(jobrelate.child.title, 'job2')

        # not quite what I was expecting, but this is going to need
        # to be refactored anyway
        self.assertEqual(parent_job.child_jobs[0].child.title, 'job2')
        self.assertEqual(parent_job.child_jobs[0].parent.title, 'job1')
        self.assertEqual(child_job.parent_jobs[0].child.title, 'job2')
        self.assertEqual(child_job.parent_jobs[0].parent.title, 'job1')



class TestKeywords(BaseTest):

    # Issue with testing as it seems back-ref data may not exis untill
    # after the transaction as been commited.
    @unittest.skip("Need more research into unitesting many-many structures")
    def test_keywords(self):
        import datetime
        from ..models import User,Job,Keyword

        sys_user = User(name='SYSTEM', role='ADMIN')
        parent_job = Job(adddate=datetime.datetime.now(),title='job1', salary='salary1',creator=sys_user)
        child_job = Job(adddate=datetime.datetime.now(),title='job2', salary='salary2',creator=sys_user)
        keyword1 = Keyword(keyword='newkeyword')
        parent_job.keywords.append(keyword1)

        # This should pass
        self.assertEqual(parent_job.keywords[0].keyword, 'newkeyword')
        # This will fail with an index out of bounds currently
        self.assertEqual(keyword1.jobs[0].title, 'job2')
