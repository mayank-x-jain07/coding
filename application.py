from flask import Flask,request
from flask import Flask,render_template
from flask import jsonify
from flask import json
import MySQLdb


application = Flask(__name__)

@application.route('/parking', methods= ['GET', 'POST'])
# Finding the Spots In A Location.
def parking():
    myres=[]
    print "Entered Parking"

    try:
        #lat=request.args['lat']
        dist=request.args['radius']
        #Converting the Radius in Miles
        #dist=float(dist)*0.000621371
        #lon=float(request.args['lon'])

        #q='SELECT *,(3959 * acos ( cos ( radians('+str(lat)+') ) * cos( radians( p_lat ) ) * cos( radians( p_long ) - radians('+str(lon)+') ) + sin ( radians('+str(lat)+') ) * #sin( radians( p_lat ) ))) AS distance From parking_spots where available="Y" HAVING distance < '+str(dist)+' ORDER BY distance'
        q="select * from parking_spots"

        db = MySQLdb.connect(host='mjdbpyhoninstance.ccunictkoaw7.us-west-2.rds.amazonaws.com', port=3306, db='mjdbpython', user='mayank', passwd='mayank123')
        cursor = db.cursor()
        cursor.execute(q)
        res=cursor.fetchall()
        if len(res)>0:
            for i in res:
                #Converting the Miles to Meters for Returning The JSON Result
                dist_mtrs=float(i[6])*1609.34
                myres.append(dict([('spotID',i[0]),
                                         ('lat',str(i[1])),
                                         ('dist_mtrs',str(dist_mtrs)),
                                         ('lon',str(i[2]))
                                         ]))
        else:
            myres.append(dict([('msg','No Parking Spots Found')
                                     ]))


    except:
        myres.append(dict([('msg','Some Error Occoured')
                                     ]))

    return jsonify(myres)


@application.route('/parking_update', methods= ['GET', 'POST'])
# Booking a Parking Spot
def parking_update():
    myres=[]
    print "In Parking Update"
    try:
        spot_id=str(request.args['spot_id'])
        from_time=str(request.args['from_time'])
        to_time=str(request.args['to_time'])
        db = MySQLdb.connect(host='mjdbpyhoninstance.ccunictkoaw7.us-west-2.rds.amazonaws.com', port=3306, db='mjdbpython', user='mayank', passwd='mayank123')
        cursor = db.cursor()
        query='select count(*)  from parking_spots where available="Y" and spot_id='+spot_id+' and to_time < "'+from_time+'"'
        cursor.execute(query)
        res=cursor.fetchall()
        if res[0][0]==1:
            query='update parking_spots set available="N", from_time="'+from_time+'", to_time="'+to_time+'" where spot_id='+spot_id
            cursor.execute(query)
            db.commit()
            myres.append(dict([('msg','Spot Booked Successfully!')
                                     ]))
        else:
           myres.append(dict([('msg','Spot Not Available')
                                     ]))
    except:
       myres.append(dict([('msg','Some Error Occoured')
                                     ]))

    return jsonify(myres)


# run the app.
if __name__ == "__main__":
    application.debug = True
    application.run()
