from math import ceil
from django.shortcuts import render,redirect
from .models import Personal_Info,form_submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

from datetime import datetime
# for update image 
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

#datetime field convert
from datetime import datetime



# Create your views here.
# def index(request):  
#     # fetching all post objects from database 
#     all_info=Personal_Info.objects.all()
#     # creating a paginator object
#     paginator=Paginator(all_info,8)
#     # getting the desired page number from url
#     page_number=request.GET.get('page')
#     # returns the desired page object
#     try:
#         page_obj = paginator.get_page(page_number) 
#     except PageNotAnInteger:
#         # if page_number is not an integer then assign the first page
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         # if page is empty then return last page
#         page_obj = paginator.page(paginator.num_pages)
    
#     context={'all_info':all_info,'page_obj': page_obj}
#     return render(request,'Info_App/index.html',context)



def home(request):  
    # fetching all post objects from database 
    all_info=form_submission.objects.filter(member_lastname__startswith="A",holding_COP="no").order_by("member_lastname")
    context={'all_info':all_info}
    return render(request,'Info_App/home.html',context)


def validate_no(request):
    if request.method == "POST":
        membership_num = request.POST['membership_num']
        yr_of_membership = request.POST['yr_of_membership']
        Birth_date = request.POST['Birth_date']
      
        #Year pass to html membership year dropdown
        current_year = datetime.now().year
        year_list = list(range(1950, current_year+1))
        
        # validation on membership number
        existing_info= form_submission.objects.values_list('membership_number')
        info_list = [item for t in existing_info for item in t]
                
        if membership_num=="":
            messages.error(request,"Please Enter Membership Number ")
            return redirect('Info_App:validate_no')
        elif yr_of_membership=="":
            messages.error(request,"Please Enter Membership Year")
            return redirect('Info_App:validate_no')
        elif Birth_date=="":
            messages.error(request,"Please Enter Date Of Birth")
            return redirect('Info_App:validate_no')
        elif len(membership_num) > 6 :
            messages.error(request,"Please put maximum 6 digit Membership number")
            return redirect('Info_App:validate_no')
        elif len(membership_num) < 5 :
            messages.error(request,"Please put minimum 5 digit Membership number")
            return redirect('Info_App:validate_no')
        elif membership_num in info_list:
            #fetch info corresponding entered membershipnumber
            fetch_info=form_submission.objects.get(membership_number=membership_num)
            if yr_of_membership != fetch_info.year_of_membership or Birth_date != str(fetch_info.DOB):
                messages.error(request,"Membership Number already exists, Please enter correct Membership Year and/or DOB to View/Edit your details")
                return redirect('Info_App:validate_no')
            else:
                return render(request,'Info_App/existing_info_table.html',{'fetch_info':fetch_info})
        else:
            messages.error(request,"Membership Number does not exists, cannot register new member!")
            return redirect('Info_App:validate_no')
            # return render(request,'Info_App/submit_cainfo.html',{'membership_num':membership_num,'yr_of_membership':yr_of_membership,'Birth_date':Birth_date})
    
    #Year pass to html membership year dropdown
    current_year = datetime.now().year
    year_list = list(range(1980, current_year+1))
    return render(request,'Info_App/validate_no.html',{'year_list': year_list})




def submit_cainfo(request):
    if request.method == "POST":
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
        
        if  membership_number not in out1:   
            form_submission.objects.create(member_firstname=member_firstname.upper(),member_middlename=member_middlename.upper(),member_lastname=member_lastname.upper(),membership_number=membership_number,year_of_membership=year_of_membership,Phone_number=Phone_number,prof_address=prof_address,
                                        prof_area=prof_area,prof_city=prof_city,prof_pin_code=prof_pin_code,residential_address=residential_address,residential_area=residential_area,residential_city=residential_city,residential_pin_code=residential_pin_code,
                                        blood_group=blood_group,DOB=Date_Of_Birth,DOM=Date_of_Marriage,email_id=email_id,
                                        organization=organization,new_photo=photo,holding_COP=holding_COP).save()
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request,'Info_App/validate_no.html')


def edit_existing_cainfo(request, ca_id):
    mymodel =form_submission.objects.get(id=ca_id)
    if request.method == 'POST':
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
        if request.FILES.get('photo')=="":
          new_image =mymodel.photo
        else:
          new_image = request.FILES.get('photo')
          
        # date field convert to yyyy-mm-dd formate
        try:
            date_dob = datetime.strptime(Date_Of_Birth, '%m/%d/%Y')
        except ValueError:
            date_dob = datetime.strptime(Date_Of_Birth, '%B %d, %Y')
        DOB_date_str = date_dob.strftime('%Y-%m-%d')

        try:
            date_dom = datetime.strptime(Date_of_Marriage, '%m/%d/%Y')
        except ValueError:
            date_dom = datetime.strptime(Date_of_Marriage, '%B %d, %Y')
        DOM_date_str = date_dom.strftime('%Y-%m-%d')

        # if a new image was provided, update the model's image field
        if new_image:
            # save the new image to disk
            filename = default_storage.save(new_image.name, ContentFile(new_image.read()))

            # delete the old image
            mymodel.new_photo.delete()

            # update the model's image field with the new image
            mymodel.new_photo.save(filename, new_image)

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
        mymodel.DOB = DOB_date_str
        mymodel.DOM = DOM_date_str
        mymodel.email_id = email_id
        mymodel.organization = organization
        mymodel.member_firstname = member_firstname
        mymodel.member_firstname = member_firstname
        mymodel.holding_COP = holding_COP
        mymodel.save()

        return JsonResponse({'success': True})
    return render(request,'Info_App/edit_existing_cainfo.html',{'mymodel': mymodel})





def existing_info_table(request):
    return render(request,'Info_App/existing_info_table.html')

