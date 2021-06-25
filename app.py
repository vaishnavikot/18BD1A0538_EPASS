from flask import Flask,render_template
from flask import request
from twilio.rest import Client
import requests
import requests_cache
account_sid="AC51caf0ac9cf2c1e199213c4d81661e7b"
auth_token='a3d4fe0af9392aae0e2f1b3e349951ac'
client=Client(account_sid,auth_token)

app=Flask(__name__, static_url_path='/static')
@app.route('/')
def registration_form():
    return render_template('login_page.html')

@app.route('/login_page',methods=['POST','GET'])

def login_registration_dtls():
    first_name=request.form['fname']
    last_name=request.form['lname']
    email_id=request.form['eid']
    source_st=request.form['source_st']
    source_dt=request.form['source']
    destination_st=request.form['destination_st']
    destination_dt=request.form['destination']
    phone_number=request.form['phno']
    id_proof=request.form['idcard']
    date=request.form['trip']
    full_name=first_name+"."+last_name
    r=requests.get('https://api.covid19india.org/v4/data.json')
    json_data=r.json()
    cnt=json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop=json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass=(cnt/pop)*100
    if travel_pass<30 and request.method =='POST':
        status='CONFIRMED'
        client.messages.create(to="whatsapp:+916303399473",
                               from_="whatsapp:+14155238886",
                               body="Hello" + " " + full_name + " " + "Your travel from" + " " + source_dt + " " + "to" + " " + destination_dt + " " + "Has" + " " + status + " " + "on" + " " + date + " ")

        return render_template('user_registration_dtls.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phone_number,var8=date,var9=status)
    else:
        status='Not Confirmed'
        client.messages.create(to="whatsapp:+916303399473",
                               from_="whatsapp:+14155238886",
                               body="Hello " + " " + full_name + "  " + "your travel from" + source_dt + " " + "To" + " " + destination_dt + " "
                                    + "Has" + " " + status + " " + " On" + " " + date + " " + ",Please Apply later")

        return render_template('user_registration_dtls.html',var=full_name,var1=email_id,var2=id_proof,
                               var3=source_st,var4=source_dt,var5=destination_st,var6=destination_dt,
                               var7=phone_number,var8=date,var9=status)

if __name__ == "__main__":
    app.run(port=9000,debug=True)