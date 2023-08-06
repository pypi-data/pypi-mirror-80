class Variables(object):
    agent_name = 'robotframework-reportportal'
    uuid = None
    endpoint = None
    launch_name = None
    project = None
    launch_doc = None
    log_batch_size = None
    launch_attributes = None
    launch_id = None
    test_attributes = None

    @staticmethod
    def check_variables(options):
        Variables.uuid = options.rp_uuid
        Variables.endpoint = options.rp_endpoint
        Variables.launch_name = options.rp_launch
        Variables.project = options.rp_project
        Variables.launch_attributes = options.rp_launch_attributes.split()
        Variables.launch_id = options.rp_launch_uuid
        Variables.launch_doc = options.rp_launch_doc
        Variables.log_batch_size = int(options.rp_log_batch_size)
        Variables.test_attributes = options.rp_test_attributes.split()
