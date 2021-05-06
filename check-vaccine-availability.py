from twilio.rest import Client 
import urllib.request
import pdb
import json
import copy
from tqdm import tqdm
import time
import urllib
from fake_useragent import UserAgent
ua = UserAgent()
ua.update()

global__last_messages_sent = []

#######################   Add the TODOs are listed here  ##############################
AGE_LIMIT = 18      # Change it to "45" if you want to searrch for slots for age 45+
DISTRICT_ID = 318   ## TODO: CHange the district ID
PHONE_NUMBERS = [
    ## TODO: Add a list of phone nos e.g. 1234567890 to whom you want to send the Whatsapp message
]
TWILIO_WHATSAPP_FROM = 'whatsapp:+141552XXXXX'      ## TODO: Change this to appropriate twilio phone number
TWILIO_ACCOUNT_SID = '<< account-sid >>'            ## TODO: Add the twilio account SID
TWILIO_AUTH_TOKEN = '<< auth_token >>'              ## TODO: Add the twilio auth_token
#######################################################################################



AVOID_REPEATED_MSGS = True
TIME_DELAY = 60 * 1        ## 30 mins
TIME_SPREAD_BETWEEN_REQUESTS = 5    ## 5 seconds

VACCINATION_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={}&date={}"
PIN_CODES = ['_']

# VACCINATION_URL = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={}&date={}"
# PIN_CODES = [456001,456002,456003,456004,456005,456007,456008,456009,456010]

CHAR_LIMIT = 1600
WEEK_DATES = [
    '05-05-2021',
    '12-05-2021',
    '19-05-2021',
    # '26-05-2021',
]




def create_message(this_center, this_session):
    return """
Center: {}
Address: {}
Pincode: {}
Age: {}
Fee?: {}
Vaccine: {}
Available: {}
Date: {}
""".format(
        this_center['name'],
        this_center['address'],
        this_center['pincode'],
        this_session['min_age_limit'],
        this_center['fee_type'],
        this_session['vaccine'],
        this_session['available_capacity'],
        this_session['date']
    )

def check_vacancy():
    global global__last_messages_sent

    print("===========================================================================================")
    msg_body = ""
    all_messages = []
    pbar = tqdm(total=len(PIN_CODES)*len(WEEK_DATES), desc="Search for {} pin-codes and {} week-dates....".format(len(PIN_CODES), len(WEEK_DATES)))
    for pin_code in PIN_CODES:
        time.sleep(TIME_SPREAD_BETWEEN_REQUESTS)
        for _date in WEEK_DATES:
            time.sleep(TIME_SPREAD_BETWEEN_REQUESTS)
            contents = None
            while contents == None:
                try:
                    # pdb.set_trace()
                    req = urllib.request.Request(
                        # url=VACCINATION_URL.format(pin_code, _date),
                        url=VACCINATION_URL.format(DISTRICT_ID, _date),
                        headers={
                            'User-Agent': ua.google
                        }
                    )
                    f = urllib.request.urlopen(req)
                    contents = f.read().decode('utf-8')
                except Exception as e:
                    print("Forbidden... Waiting 60 seconds ---->", e)
                    time.sleep(60)
                    continue

            contents = json.loads(contents)

            for _center in contents['centers']:
                for _session in _center['sessions']:
                    if _session['min_age_limit'] == AGE_LIMIT and _session['available_capacity'] > 0:

                        ## Create message
                        _msg = create_message(_center, _session)
                        if len(msg_body + _msg) > CHAR_LIMIT:
                            all_messages.append(msg_body)
                            msg_body = ""
                        msg_body = msg_body + _msg
            pbar.update(1)
    pbar.close()

    if len(msg_body) > 0:
        all_messages.append(msg_body)

    if len(msg_body) <= 0:
        print(">> Skipping as no msg to send... BYE.")
        return

    print("\n".join(all_messages))
    print("Total Messags:", len(all_messages))

    ## Skip repeated messages
    if AVOID_REPEATED_MSGS and global__last_messages_sent == all_messages:
        print(">> Skipping as the last-message is the same... BYE.")
        return

    global__last_messages_sent = copy.deepcopy(all_messages)
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    for phone_no in PHONE_NUMBERS:
        for this_msg in all_messages:
            message = client.messages.create( 
                                        from_=TWILIO_WHATSAPP_FROM,  
                                        body=this_msg,      
                                        to='whatsapp:+91{}'.format(phone_no)
                                    )
            print(phone_no, message.sid)


while 1:
    check_vacancy()
    time.sleep(TIME_DELAY)
