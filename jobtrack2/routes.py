def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('job_list','/job')
    config.add_route('job_detail','/job/{jobid}')
    config.add_route('agency_list','/agency')
    config.add_route('agency_detail','/agency/{agencyid}')
    config.add_route('agent_list','/agent')
    config.add_route('agent_detail','/agent/{agentid}')
    config.add_route('company_list','/company')
    config.add_route('company_detail','/company/{companyid}')

