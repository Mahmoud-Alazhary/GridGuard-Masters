import datetime
'''
TIME_STAMP class to handle required date_time operations and manipulation
'''
class TIME_STAMP(object):
    __date_format = "%Y/%m/%d %H"
    
    def __init__(self,ref_date_string):
        self.__datetime_obj = datetime.datetime.strptime(ref_date_string, self.__date_format)
    
    def to_stamp_string(self):
        return self.__datetime_obj.strftime(self.__date_format)
    '''# Add hours to the datetime object'''
    def add_hours(self,hrs):
        
        self.__datetime_obj += datetime.timedelta(hours=hrs)
    def remove_hours(self,hrs):
        self.__datetime_obj -= datetime.timedelta(hours=hrs)
if __name__=='__main__':
    
    ts=TIME_STAMP("2019/12/29 23")
    print(ts.to_stamp_string())
    ts.add_hours(3)
    print(ts.to_stamp_string())
    ts.add_hours(24)
    print(ts.to_stamp_string())
    
    
