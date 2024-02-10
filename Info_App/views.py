import base64
from io import BytesIO
from math import ceil

from django.contrib.auth import logout
from django.shortcuts import render,redirect
from .models import Personal_Info, form_submission, save_data, mem_photo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection

from datetime import datetime
# for update image 
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

#datetime field convert
from datetime import datetime

#404 page
from django.http import Http404




def home(request):  
    # fetching all post objects from database 
    all_info=form_submission.objects.filter(member_lastname__startswith="A",holding_COP="no").order_by("member_lastname")
    context={'all_info':all_info}
    return render(request,'Info_App/home.html',context)


def validate_no(request):
    print("inside validate_no method")

    if request.method == "POST":
        membership_num = request.POST.get('membership_num')
        yr_of_membership = request.POST.get('yr_of_membership')
        Birth_date = request.POST.get('Birth_date')

        # Year pass to HTML membership year dropdown
        current_year = datetime.now().year
        year_list = list(range(1950, current_year + 1))

        # Validation on membership number
        if not membership_num:
            messages.error(request, "Please Enter Membership Number")
            return redirect('Info_App:validate_no')
        elif not yr_of_membership:
            messages.error(request, "Please Enter Membership Year")
            return redirect('Info_App:validate_no')
        elif not Birth_date:
            messages.error(request, "Please Enter Date Of Birth")
            return redirect('Info_App:validate_no')
        elif len(membership_num) > 6:
            messages.error(request, "Please input maximum 6 digit Membership number")
            return redirect('Info_App:validate_no')
        elif len(membership_num) < 5:
            messages.error(request, "Please input minimum 5 digit Membership number")
            return redirect('Info_App:validate_no')
        elif len(membership_num) ==5:
            messages.error(request, "Please add 0 if membership number is 5 digit ex 01234")
            return redirect('Info_App:validate_no')


        # Check if membership number exists
        existing_info = form_submission.objects.filter(membership_number=membership_num)

        if existing_info.exists():
            fetch_info = existing_info.first()
            if yr_of_membership != fetch_info.year_of_membership or Birth_date != str(fetch_info.DOB):
                messages.error(request,
                               "Membership Number already exists. Please enter correct Membership Year and/or DOB to View/Edit your details.")
                return redirect('Info_App:validate_no')
            else:
                if fetch_info and not fetch_info.new_photo:

                    mem_photo_entry = mem_photo.objects.filter(membership_number=membership_num).first()

                    if mem_photo_entry and mem_photo_entry.photo:
                        fetch_info.photo = mem_photo_entry.photo

                elif fetch_info.new_photo:
                    new_photo_base64 = base64.b64encode(fetch_info.new_photo).decode('utf-8')
                    fetch_info.new_photo_base64 = new_photo_base64
                elif fetch_info.photo:
                    photo_base64 = base64.b64encode(fetch_info.photo).decode('utf-8')
                    fetch_info.photo_base64 = photo_base64
                return render(request, 'Info_App/existing_info_table.html', {'fetch_info': fetch_info})
        else:
            return render(request, 'Info_App/submit_cainfo.html',
                          {'membership_num': membership_num, 'yr_of_membership': yr_of_membership,
                           'Birth_date': Birth_date})

    # Year pass to HTML membership year dropdown
    current_year = datetime.now().year
    year_list = list(range(1950, current_year + 1))
    return render(request, 'Info_App/validate_no.html', {'year_list': year_list})




def submit_cainfo(request):

    if request.method == "POST":


            # Print uploaded files
        for key, file in request.FILES.items():
            print(f"Uploaded file - {key}: {file.name} (size: {file.size} bytes)")

        member_firstname = request.POST.get('member_firstname')
        member_middlename = request.POST.get('member_middlename')
        member_lastname = request.POST.get('member_lastname')
        membership_number = request.POST.get('membership_number')
        year_of_membership = request.POST.get('year_of_membership')
        Phone_number = request.POST.get('Phone_number')
        prof_address = request.POST.get('prof_address')
        prof_area = request.POST.get('prof_area')
        prof_city = request.POST.get('prof_city')
        prof_pin_code = request.POST.get('prof_pin_code')
        residential_address = request.POST.get('residential_address')
        residential_area = request.POST.get('residential_area')
        residential_city = request.POST.get('residential_city')
        residential_pin_code = request.POST.get('residential_pin_code')
        blood_group = request.POST.get('blood_group')
        Date_Of_Birth = request.POST.get('DOB')
        Date_of_Marriage = request.POST.get('DOM')
        email_id = request.POST.get('email_id')
        organization = request.POST.get('organization')
        holding_COP = request.POST.get('holding_COP')
        photo = request.FILES.get('photo')



        # validation on membership number
        existing_info= form_submission.objects.values_list('membership_number')
        out1 = [item for t in existing_info for item in t]

        # # Assuming out1 is a list
        # out1_str = ', '.join(out1)  # Convert the list to a comma-separated string
        if photo:
            photo_data = photo.read()

        if membership_number not in out1:
            print("inside membership_number condition")
            form_submission.objects.create(member_firstname=member_firstname.upper(),member_middlename=member_middlename.upper(),member_lastname=member_lastname.upper(),membership_number=membership_number,year_of_membership=year_of_membership,Phone_number=Phone_number,prof_address=prof_address,
                                        prof_area=prof_area,prof_city=prof_city,prof_pin_code=prof_pin_code,residential_address=residential_address,residential_area=residential_area,residential_city=residential_city,residential_pin_code=residential_pin_code,
                                        blood_group=blood_group,DOB=Date_Of_Birth,DOM=Date_of_Marriage,email_id=email_id,
                                        organization=organization,new_photo=photo_data,holding_COP=holding_COP)


            print("True")
            return JsonResponse({'success': True})
        else:
            print("False")
            return JsonResponse({'success': False})
    return render(request,'Info_App/validate_no.html')


# def submit_cainfo(request):
#     try:
#         # Try to establish a connection to the database
#         cursor = connection.cursor()
#
#         # Execute a simple query to test the connection
#         cursor.execute("SELECT 1")
#
#         # Fetch the result (just to ensure the query was successful)
#         result = cursor.fetchone()
#
#         # If we reach this point without any exceptions, the connection is successful
#         print("Database connection successful")
#         print("Result of test query:", result)
#
#         obj = save_data.objects.create(id = 1, membership_number="22233")
#
#         print("Data saved sucessfully")
#
#     except Exception as e:
#         # If any exception occurs, it means there's an error in the connection
#         print("Database connection failed:", str(e))
#
#
#     if request.method == "POST":
#         print("inside submit ca_info method")
#         membership_number = request.POST.get('membership_number')
#
#         # Check if the membership number already exists in the database
#         if form_submission.objects.filter(membership_number=membership_number).exists():
#             print("Membership number already exists")
#             return JsonResponse({'success': False})
#         else:
#             member_firstname = request.POST.get('member_firstname')
#             member_middlename = request.POST.get('member_middlename')
#             member_lastname = request.POST.get('member_lastname')
#             year_of_membership = request.POST.get('year_of_membership')
#             Phone_number = request.POST.get('Phone_number')
#             prof_address = request.POST.get('prof_address')
#             prof_area = request.POST.get('prof_area')
#             prof_city = request.POST.get('prof_city')
#             prof_pin_code = request.POST.get('prof_pin_code')
#             residential_address = request.POST.get('residential_address')
#             residential_area = request.POST.get('residential_area')
#             residential_city = request.POST.get('residential_city')
#             residential_pin_code = request.POST.get('residential_pin_code')
#             blood_group = request.POST.get('blood_group')
#             Date_Of_Birth = request.POST.get('DOB')
#             Date_of_Marriage = request.POST.get('DOM')
#             email_id = request.POST.get('email_id')
#             organization = request.POST.get('organization')
#             holding_COP = request.POST.get('holding_COP')
#             photo = request.FILES.get('photo')
#
#             # Save the form submission to the database
#             form_submission.objects.create(
#                 member_firstname=member_firstname.upper(),
#                 member_middlename=member_middlename.upper(),
#                 member_lastname=member_lastname.upper(),
#                 membership_number=membership_number,
#                 year_of_membership=year_of_membership,
#                 Phone_number=Phone_number,
#                 prof_address=prof_address,
#                 prof_area=prof_area,
#                 prof_city=prof_city,
#                 prof_pin_code=prof_pin_code,
#                 residential_address=residential_address,
#                 residential_area=residential_area,
#                 residential_city=residential_city,
#                 residential_pin_code=residential_pin_code,
#                 blood_group=blood_group,
#                 DOB=Date_Of_Birth,
#                 DOM=Date_of_Marriage,
#                 email_id=email_id,
#                 organization=organization,
#                 new_photo=photo,
#                 holding_COP=holding_COP
#             )
#
#             print("Form submission saved successfully")
#             return JsonResponse({'success': True})
#
#     return render(request, 'Info_App/validate_no.html')


def edit_existing_cainfo(request, ca_id,random_no, mem_no ):

    membership_number_str = str(mem_no)

    # Check if the membership number has 5 digits
    if len(membership_number_str) == 5:
        # Add a leading zero by concatenating '0' with the membership number string
        membership_number_str = '0' + membership_number_str

    new_photo_base64 = None
    try:

        mymodel = form_submission.objects.get(id=ca_id, membership_number=membership_number_str)
        if mymodel and not mymodel.new_photo:
            mem_photo_entry = mem_photo.objects.filter(membership_number=membership_number_str).first()
            if mem_photo_entry and mem_photo_entry.photo:
                mymodel.photo = mem_photo_entry.photo
        else:
            new_photo_base64 = base64.b64encode(mymodel.new_photo).decode('utf-8')

    except form_submission.DoesNotExist:
        raise Http404("The requested CA info does not exist.")

    if request.method == 'POST':

        mymodel = form_submission.objects.get(id=ca_id, membership_number=membership_number_str)

        # get the new image from the request
        member_firstname = request.POST.get('member_firstname')
        member_middlename = request.POST.get('member_middlename')
        member_lastname = request.POST.get('member_lastname')
        membership_number = request.POST.get('membership_number')
        year_of_membership = request.POST.get('year_of_membership')
        Phone_number = request.POST.get('Phone_number')
        prof_address = request.POST.get('prof_address')
        prof_area = request.POST.get('prof_area')
        prof_city = request.POST.get('prof_city')
        prof_pin_code = request.POST.get('prof_pin_code')
        residential_address = request.POST.get('residential_address')
        residential_area = request.POST.get('residential_area')
        residential_city = request.POST.get('residential_city')
        residential_pin_code = request.POST.get('residential_pin_code')
        blood_group = request.POST.get('blood_group')
        Date_Of_Birth = request.POST.get('DOB')
        Date_of_Marriage = request.POST.get('DOM')
        email_id = request.POST.get('email_id')
        organization = request.POST.get('organization')
        holding_COP = request.POST.get('holding_COP')


        if request.FILES.get('photo'):
            # Get the uploaded image
            uploaded_photo = request.FILES['photo']

            # Read the image data
            image_data = uploaded_photo.read()

            # Convert the image data to Base64
            new_photo_base64 = base64.b64encode(image_data).decode('utf-8')

            # Update the model's new_photo field with the uploaded image
            mymodel.new_photo = image_data




        # date field convert String to yyyy-mm-dd formate
        date_dob = datetime.strptime(Date_Of_Birth, '%Y-%m-%d')
        
        if Date_of_Marriage:
            date_format = "%Y-%m-%d"
            date_dom = datetime.strptime(Date_of_Marriage, date_format)
        else:
            date_dom = None
            



        # update any other fields on the model as needed
        mymodel.member_firstname = member_firstname
        mymodel.member_middlename = member_middlename
        mymodel.member_lastname = member_lastname
        mymodel.membership_number = membership_number
        mymodel.year_of_membership = year_of_membership
        mymodel.Phone_number = Phone_number
        mymodel.prof_address = prof_address
        mymodel.prof_area = prof_area
        mymodel.prof_city = prof_city
        mymodel.prof_pin_code = prof_pin_code
        mymodel.residential_address = residential_address
        mymodel.residential_area = residential_area
        mymodel.residential_city = residential_city
        mymodel.residential_pin_code = residential_pin_code
        mymodel.blood_group = blood_group
        mymodel.DOB = date_dob
        mymodel.DOM = date_dom
        mymodel.email_id = email_id
        mymodel.organization = organization
        mymodel.member_firstname = member_firstname
        mymodel.member_firstname = member_firstname
        mymodel.holding_COP = holding_COP
        mymodel.save()

        if mymodel.new_photo:
            new_photo_base64 = base64.b64encode(mymodel.new_photo).decode('utf-8')
            mymodel.new_photo_base64 = new_photo_base64
        elif mymodel.photo:
            photo_base64 = base64.b64encode(mymodel.photo).decode('utf-8')
            mymodel.photo_base64 = photo_base64

        # return JsonResponse({'success': True})
        return render(request,'Info_App/existing_info_table.html',{'fetch_info':mymodel})
        # return render(request,'Info_App/validate_no.html')
    return render(request, 'Info_App/edit_existing_cainfo.html', {'mymodel': mymodel, 'new_photo_base64': new_photo_base64})




def existing_info_table(request):
    current_year = datetime.now().year
    year_list = list(range(1950, current_year+1))
    return render(request,'Info_App/validate_no.html',{'year_list': year_list})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the homepage after logout

