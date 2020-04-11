from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
import smtplib

#SNS Connection
# import boto3
# snsclient = boto3.client('sns')
# snsclient.set_sms_attributes(attributes={'DefaultSMSType':'Transactional'})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def send_thanks_email_to_donor(donor_name, donor_email):

    mail = smtplib.SMTP('smtp.gmail.com', settings.EMAIL_PORT)
    mail.ehlo()
    mail.starttls()

    thank_you_message = 'Dear ' + \
        str(donor_name) + ', \nThanks a lot for your kindness. Your Donation means a lot to us. I promise to return back the amount to you in goods'
    mail_failure_message = 'Mail to' + \
        str(donor_name) + ' at ' + str(donor_email) + ' failed !!!'

    mail.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    try:
        mail.sendmail(settings.EMAIL_HOST_USER, donor_email, thank_you_message)
        return 1
    except:
        print('Mail to' + str(donor_name) + ' at ' +
              str(donor_email) + ' failed !!!')
        mail.sendmail(settings.EMAIL_HOST_USER,
                      settings.EMAIL_HOST_USER, mail_failure_message)
        return 0

    print('Mail Sent to donor' + str(donor_name) + ' at ' + str(donor_email))
    mail.close()


def send_otp_util(number,otp):
    # response=snsclient.publish(PhoneNumber=number,Message='The otp is '+otp)
    # if(response['ResponseMetadata']['HTTPStatusCode']==200):
    #     return True
    
    return False
    # message = settings.OTP_TWILIO_TOKEN_TEMPLATE.format(token=token)

    # if settings.OTP_TWILIO_ACCOUNT is None:
    #     raise ImproperlyConfigured('OTP_TWILIO_ACCOUNT must be set to your Twilio account identifier')
    # if settings.OTP_TWILIO_AUTH is None:
    #     raise ImproperlyConfigured('OTP_TWILIO_AUTH must be set to your Twilio auth token')
    # if settings.OTP_TWILIO_FROM is None:
    #     raise ImproperlyConfigured('OTP_TWILIO_FROM must be set to one of your Twilio phone numbers')

    # url = 'https://api.twilio.com/2010-04-01/Accounts/{0}/Messages.json'.format(settings.OTP_TWILIO_ACCOUNT)
    # data = {
    #     'From': settings.OTP_TWILIO_FROM,
    #     'To': self.number,
    #     'Body': str(token),
    # }

    # response = requests.post(
    #     url, data=data,
    #     auth=(settings.OTP_TWILIO_ACCOUNT, settings.OTP_TWILIO_AUTH)
    # )

    # try:
    #     response.raise_for_status()
    # except Exception as e:
    #     logger.exception('Error sending token by Twilio SMS: {0}'.format(e))
    #     raise

    # if 'sid' not in response.json():
    #     message = response.json().get('message')
    #     logger.error('Error sending token by Twilio SMS: {0}'.format(message))
    #     raise Exception(message)

    # challenge = settings.OTP_TWILIO_CHALLENGE_MESSAGE.format(token=token)
    # return challenge

        
