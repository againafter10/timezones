import os,datetime,sys,json
from datetime import timedelta
from pytz import timezone

dict = {}
path = os.path.join(os.path.normpath(os.getcwd()), sys.argv[1])
melbourne = timezone("Australia/Melbourne") #local time used for scheduling

for root,dir,files in os.walk(path):
    if len(files) > 0 and [i for i in files if i.endswith("_schedule.json")]:
        file = [i for i in files if i.endswith("_schedule.json")]
        with open(os.path.join(root, file[0]),'r') as infile:
            print(os.path.join(root, file[0]))
            dict = json.loads(infile.read())
            for i in dict:
                try:
                    if dict["SCH_job_interval_mins"] is not None:
                        #add a day to the time
                        temp = (dict["SCH_job_start_time"].split(" "))
                        temp[0] = (datetime.datetime.now(melbourne) + timedelta(days=1)).strftime("%Y-%m-%d")
                        dict["SCH_job_start_time"] = str(temp)
                        dict["SCH_job_start_time"] = " ".join([str(temp[0]), str(temp[1])])
                        temp_file = os.path.join(root, file[0]) + "_temp"
                        with open(temp_file,'w') as tempfile:
                            tempfile.write(json.dumps(dict))
                except  ValueError as err:
                    print(os.path.join(root, file[0]),"  &&&&   ",err)
        os.remove(os.path.join(root, file[0]))
        os.rename(temp_file, os.path.join(root, file[0]))