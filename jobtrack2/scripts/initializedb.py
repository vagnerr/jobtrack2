import os
import sys
import transaction

from pyramid.paster import (
    get_appsettings,
    setup_logging,
    )

from pyramid.scripts.common import parse_vars

from ..models.meta import Base
from ..models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    )

from ..models import (
    JobType,
    NextAction,
    Status,
    User,
    Job,
    JobRelated,
    Keyword,
    CompanyContact,
    ContactType,
    Company,
    Agent,
    Agency,
    AgentContact,
    AgencyContact,
    Source,
)

def usage(argv):
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri> [var=value]\n'
          '(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def main(argv=sys.argv):
    if len(argv) < 2:
        usage(argv)
    config_uri = argv[1]
    options = parse_vars(argv[2:])
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, options=options)

    engine = get_engine(settings)
    Base.metadata.create_all(engine)

    session_factory = get_session_factory(engine)

    with transaction.manager:
        dbsession = get_tm_session(session_factory, transaction.manager)

        # SYSTEM user for ownership of initial bootstrap constants
        sys_user = User(name='SYSTEM', role='ADMIN')
        dbsession.add(sys_user)

        # TODO: Move bootstrap data to its own file
        next_actions=[
            [ 1,'NONE','Do Nothing'],
            [ 2,'CALL','Call'],
            [ 3,'EMAIL','EMail'],
            [ 4,'CHECK','Check Status'],
            [ 5,'POST','Write to them'],
            [ 6,'CLOSE','Close Job'],
        ]
        for action in next_actions:
            nextaction = NextAction(
                            id=action[0],
                            keyword=action[1],
                            description=action[2],
                            creator=sys_user
                        )
            dbsession.add(nextaction)


        statuses = [
            [ 1,'OPEN','Open',1],
            [ 2,'HOLD','On Hold',1],
            [ 3,'NORESP','Closed - No response',0],
            [ 4,'REJECTED','Closed - Rejected',0],
            [ 5,'CLOSED','Closed - Other',0],
            [ 6,'NOVAC','Closed - No Vacancies',0],
        ]
        for status in statuses:
            stat = Status(
                            id=status[0],
                            keyword=status[1],
                            description=status[2],
                            active=status[3],
                            creator=sys_user
                        )
            dbsession.add(stat)

        jobtypes = [
            [ 1,'PERM','Permanent'],
            [ 2,'CONTRACT','Contract'],
            [ 3,'PART','Part Time'],
        ]

        for jobtype in jobtypes:
            jtype = JobType(
                            id=jobtype[0],
                            keyword=jobtype[1],
                            description=jobtype[2],
                            creator=sys_user
                        )
            dbsession.add(jtype)

        #Still to add...
        #   contact_type, job_data_type(?)

        contacttypes = [
            [ 1,'PHONE','Telephone'],
            [ 2,'PHONEDL','Direct Line'],
            [ 3,'FAX','Fax Number'],
            [ 4,'EMAIL','EMail Address'],
            [ 5,'ADDRESS','Address'],
            [ 6,'URL','Web Address'],
        ]
        for contacttype in contacttypes:
            ctype = ContactType(
                id=contacttype[0],
                keyword=contacttype[1],
                description=contacttype[2],
                creator=sys_user
            )
            dbsession.add(ctype)

        # Not Bothering with prefilled Location data this time.



        # testing data...
        # TODO: (#6) Figure out how to make this into proper unit tests
        import datetime
        ct = ctype  # just grab the last created contact type for testing
        parent_job = Job(title='job1', salary='salary1',creator=sys_user)
        child_job = Job(title='job2', salary='salary2',creator=sys_user)
        keyword1 = Keyword(keyword='newkeyword')
        keyword2 = Keyword(keyword='new2')
        parent_job.keywords.append(keyword1)
        child_job.keywords.append(keyword1)
        child_job.keywords.append(keyword2)
        #parent_job.child_jobs.append(child_job)
        jobrelate = JobRelated(parent=parent_job, child=child_job, description='relatedtest')
        dbsession.add(parent_job)
        dbsession.add(child_job)
        dbsession.add(jobrelate)


        source1 = Source(keyword='AGENT', description='Agent',creator=sys_user)
        source2 = Source(keyword='SOJOBS', description='StackOverflow',creator=sys_user)
        parent_job.source=source1
        child_job.source=source2
        parent_job.type_id=1
        child_job.type_id=2
        parent_job.status_id=1
        child_job.status_id=2
        # checking contacts


        company = Company(name="foo bar Ltd", creator=sys_user)
        parent_job.company=company
        #ct = ContactType(keyword='PHONE', description='Phone', creator=sys_user)

        cont = CompanyContact(contacttype=ct, data='123456789')
        company.contacts.append(cont)

        agency = Agency(name='Agents R US', creator=sys_user)
        agent = Agent(name='Mr Smith', creator=sys_user)
        agency.agents.append(agent)

        aycont = AgencyContact(contacttype=ct, data='987654321')
        ctcont = AgentContact(contacttype=ct, data='99999999')

        agency.contacts.append(aycont)
        agent.contacts.append(ctcont)

        parent_job.agents.append(agent)
        parent_job.agency=(agency)

        agency.jobs.append(child_job)
        #print(keyword1.jobs[0].title, '---job2')