from influxdb_client import InfluxDBClient
#from influxdb_client import InfluxDBClientError

class db:
    dbname = ['pv_main']
    #dbname = ['buck01']
    url='http://myurl.org:8086'
    org = 'My Organiyation l.t.d'
    token='F7my_token_._____my_token________________my_token_________________my_token____________=='
    @staticmethod
    def dbsave(measurement, rawdat, defSeriesName='brushEvents'):
        mlist=db.dbname+[measurement]
        client = InfluxDBClient(url=db.url, org=db.org, token=db.token)
        write_api = client.write_api()
        for dbname in mlist:
            #client.create_database(dbname)
            try:
                #client.switch_database(dbname)
                write_api.write(bucket=dbname+'/autogen', org=db.org, record= [
                        {
                        "measurement": measurement if dbname == 'pv_main' else defSeriesName,
                        "fields": rawdat
                        }
                ])
            except:
                print("DB Error "+dbname)
        write_api.close()
