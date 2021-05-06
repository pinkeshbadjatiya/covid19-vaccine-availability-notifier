# covid19-vaccine-availability-notifier


### Setup
1. Create an account on `twilio.com` and then copy the `account_sid` and the `auth_token` and change it in the script
2. Go to [this](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn?frameUrl=%2Fconsole%2Fsms%2Fwhatsapp%2Flearn%3Fx-target-region%3Dus1) url and then send add the number mentiond on the page on whatsapp and then send the message as mentioned in th instructions.
3. Find the district code from this page [https://www.cowin.gov.in/home](https://www.cowin.gov.in/home) and change it in the script
4. Add list of phone numbers you want to receive the messages on. You would have to repeat step-2 for all the numbers you want to receive notifications.


### Run
Run the script using `python check_availability.py` which will check availability and notify once its available

