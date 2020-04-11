from django.shortcuts import render
from rest_framework import views, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.conf import settings
from main.models import SMSDevice
from main.utils import get_tokens_for_user, send_thanks_email_to_donor
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User=get_user_model()
from main.models import Recipient, Donor, Donation
from django.http import HttpResponse

class PhoneVerifyView(views.APIView):

	def post(self,request,format=None):
		try:
			data = QueryDict(request.body)
			mobile = data.get("mobile")

			try:
				device = SMSDevice.objects.get(number=mobile)
			except ObjectDoesNotExist:
				device = SMSDevice(number = mobile)
				device.save()
			
			flag = device.sendotp()

			if settings.SMS_DEBUG:
				return Response({'otp':flag}, status=status.HTTP_201_CREATED)

			if flag:	
				return Response(status=status.HTTP_201_CREATED)

		except Exception as e:
			return Response({'exception':e}, status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class OTPVerifyView(views.APIView):

	def post(self,request,format=None):
		data = QueryDict(request.body)
		mobile = data.get("mobile")
		token = data.get("token")
		try:
			device = SMSDevice.objects.get(number = mobile)
			newUser = False

			if device.verify_token(token):
				try:
					user = User.objects.get(mobile=mobile)
				except ObjectDoesNotExist:
					user = User.objects.create_user(mobile)
					user.mobile = mobile
					user.save()
					newUser = True

				token = get_tokens_for_user(user)
				device.delete()

				return Response({'token': token,'newUser':newUser}, status=status.HTTP_201_CREATED)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		return Response(status=status.HTTP_400_BAD_REQUEST)


class RecipientProfileView(views.APIView):

	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):

		user = request.user

		try:
			recipient = Recipient.objects.get(user=user)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		data = {
					"recipient_photo": recipient.recipient_photo,
					"business_photo": recipient.business_photo,
					"first_name": recipient.user.first_name,
					"last_name": recipient.user.last_name,
					"address": recipient.address,
					"business_name": recipient.business_name,
					"business_type": recipient.business_type,
					"business_address": recipient.business_address,
					"lat": recipient.latitude,
					"long": recipient.longitude,
				}

		return Response(data, status=status.HTTP_200_OK)

	def post(self, request, format=None):
		try:
			data = QueryDict(request.body)
			recipient_photo = data.get("recipient_photo")
			business_photo = data.get("business_photo")
			first_name = data.get("first_name")
			last_name = data.get("last_name")
			address = data.get("address")
			business_name = data.get("business_name")
			business_type = data.get("business_type")
			business_address = data.get("business_address")
			latitude = data.get("lat")
			longitude = data.get("long")

			user = request.user
			user.first_name = first_name
			user.last_name = last_name
			user.save()

			new_recipient = Recipient.objects.create(
					user=user,
					recipient_photo=recipient_photo,
					business_photo = business_photo,
					address=address,
					business_name=business_name,
					business_address=business_address,
					business_type=business_type,
					latitude=latitude,
					longitude=longitude
				)
			new_recipient.save()
			
			return Response(status=status.HTTP_201_CREATED)
		except Exception as e:
			return Response({'exception':e}, status=status.HTTP_400_BAD_REQUEST)


class RecipientDetailView(views.APIView):
	
	permission_classes = (IsAuthenticated,)

	def get(self, request, format=None):

		user = request.user
		recipient = Recipient.objects.get(user=user)

		donation_list = Donation.objects.all().filter(recipient=recipient)
		donors = [None]
		for donation in donation_list:
			donors.append(donation.donor)

		return Response({'recipient':recipient, 'donors':donors}, status=status.HTTP_200_OK)


class SendThanksView(views.APIView):

	def post(self, request, format=None):
		data = QueryDict(request.body)
		donor_id = data.get("donor_id")

		try:
			donor = Donor.objects.get(id = donor_id)
		except ObjectDoesNotExist:
			return Response(status=status.HTTP_400_BAD_REQUEST)

		if donor is not None:
			donor_name = donor.user.get_full_name()
			donor_email = donor.email
			email_fun_response = send_thanks_email_to_donor(donor_name, donor_email) 

			if email_fun_response:
				return Response(status=status.HTTP_200_OK)
			else:
				return Response(status=status.HTTP_400_BAD_REQUEST)
			
		else:
			return Response(status=status.HTTP_400_BAD_REQUEST)
