class lic_info:

    def __init__(self,match):
        self.match = match

        # self.bsc_name= 'N/A'
        # self.bsc_cnum = 'N/A'
        # self.licence_code = 'N/A'
        # self.licence_name = 'N/A'
        # self.licence_capacity = 'N/A'
        # self.licence_filename = 'N/A'
        # self.serial = 'N/A'
        # self.order_identifier = 'N/A'
        # self.customer_id = 'N/A'
        # self.customer_name = 'N/A'
        # self.target_ne_type = 'N/A'
        # self.target_id = 'N/A'
        # self.licence_state = 'N/A'
        # self.start_date = 'N/A'
        # self.expiration_warning = 'N/A'

        self.value = ['--']*len(self.match)




class ucap:

    def __init__(self):
        self.bsc_name = 'N/A'
        self.bsc_cnum = 'N/A'
        self.feature_code = 'N/A'
        self.capacity_usage = 'N/A'

