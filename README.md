# covid19-vaccine-availability-notifier

**NOTE**: `Vaccines would be hard to find for 18+ age group especially in remote areas. You could use this script to be notified whenever a slot becomes available. This would be very useful for someone who urgently needs a 2nd dose of a vaccinne or has known ailments.`

*Please use this judiciously, and do not spam the COWIN servers. I have kept relaxed time delays that should be good enough for everyone.*

### Setup
1. Requires `python2` or `python3`, make sure you have it installed.
2. Install all the requirements using the command `pip install -r requirements.txt`
3. Create an account on `twilio.com` and then copy the `account_sid` and the `auth_token` and change it in the script
4. Go to [this](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1) url and then send add the number mentiond on the page on whatsapp and then send the message as mentioned in thee instructions.
5. Find the district code from this page [https://www.cowin.gov.in/home](https://www.cowin.gov.in/home) and change it in the script
6. Add list of phone numbers you want to receive the messages on. You would have to repeat Step-4 for all the numbers on which you want to receive the notifications.


### Run
Run the script using `python check_vaccine_availability.py` which will check availability and notify once its available

