from influxdb import InfluxDBClient
from influxdb import exceptions

class db:
    dbname = ['pv_main']
    @staticmethod
    def dbsave(measurement, rawdat, defSeriesName='brushEvents'):
        mlist=db.dbname+[measurement]
        client = InfluxDBClient(host='elektrovit.cz', port=8086)
        for dbname in mlist:
            #client.create_database(dbname)
            try:
                client.switch_database(dbname)
                client.write_points([
                        {
                        "measurement": measurement if dbname == 'pv_main' else defSeriesName,
                        "fields": rawdat
                        }
                ])
            except  exceptions.InfluxDBClientError:
                pass
