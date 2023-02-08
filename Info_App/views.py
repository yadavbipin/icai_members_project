from math import ceil
from django.shortcuts import render,redirect
from .models import Personal_Info,form_submission
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from django.http import JsonResponse
import json
from django.core import serializers
from django.contrib import messages


# Create your views here.
def index(request):  
    # fetching all post objects from database 
    all_info=Personal_Info.objects.all()
    # creating a paginator object
    paginator=Paginator(all_info,8)
    # getting the desired page number from url
    page_number=request.GET.get('page')
    # returns the desired page object
    try:
        page_obj = paginator.get_page(page_number) 
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    
    context={'all_info':all_info,'page_obj': page_obj}
    return render(request,'Info_App/index.html',context)



def home(request):  
    # fetching all post objects from database 
    # all_info=Personal_Info.objects.all()[:20]
    all_info=Personal_Info.objects.filter(member_lastname__startswith="A",holding_COP="yes").order_by('member_lastname')[:100]
    # all_info=Personal_Info.objects.filter(len('membership_number') = 4)
    context={'all_info':all_info}
    return render(request,'Info_App/home.html',context)


def pdf_report_create(request):   
    all_info=Personal_Info.objects.all()
    template_path = 'Info_App/pdf_report_create.html'
    context = {'all_info': all_info}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="users_report.pdf"'
    response['Content-Disposition'] = 'filename="users_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



def submit_cainfo(request):
    if request.method == "POST":
        member_firstname = request.POST['member_firstname']
        member_middlename = request.POST['member_middlename']
        # member_middlename=request.POST.get('member_middlename')
        member_lastname = request.POST['member_lastname']
        membership_number = request.POST['membership_number']
        year_of_membership = request.POST['year_of_membership']
        Phone_number = request.POST['Phone_number']
        photo = request.POST['photo']
        prof_address = request.POST['prof_address']
        prof_area = request.POST['prof_area']
        prof_city = request.POST['prof_city']
        prof_pin_code = request.POST['prof_pin_code']
        residential_address = request.POST['residential_address']
        residential_area = request.POST['residential_area']
        residential_city = request.POST['residential_city']
        residential_pin_code = request.POST['residential_pin_code']
        corr_prof_address = request.POST['corr_prof_address']
        corr_prof_area = request.POST['corr_prof_area']
        corr_prof_city = request.POST['corr_prof_city']
        corr_prof_pin_code = request.POST['corr_prof_pin_code']
        blood_group = request.POST['blood_group']
        Date_Of_Birth = request.POST['DOB']
        Date_of_Marriage = request.POST['DOM']
        email_id = request.POST['email_id']
        organization = request.POST['organization']
        holding_COP = request.POST['holding_COP']   
        print(member_middlename)
        print("##################")
        # validation on membership number
        existing_info= form_submission.objects.values_list('membership_number')
        out1 = [item for t in existing_info for item in t]
        
        if  membership_number not in out1:   
            form_submission.objects.create(member_firstname=(str(member_firstname) +" " +str( member_middlename)).upper(),member_lastname=member_lastname.upper(),membership_number=membership_number,year_of_membership=year_of_membership,Phone_number=Phone_number,prof_address=prof_address,
                                        prof_area=prof_area,prof_city=prof_city,prof_pin_code=prof_pin_code,residential_address=residential_address,residential_area=residential_area,residential_city=residential_city,residential_pin_code=residential_pin_code,
                                        corr_prof_address=corr_prof_address,corr_prof_area=corr_prof_area,corr_prof_city=corr_prof_city,corr_prof_pin_code=corr_prof_pin_code,blood_group=blood_group,DOB=Date_Of_Birth,DOM=Date_of_Marriage,email_id=email_id,
                                        organization=organization,photo=photo,holding_COP=holding_COP).save()
            
            # submitinfo_memno=form_submission.objects.values_list('membership_number')
            # out = [item for t in submitinfo_memno for item in t]
            
            
            # data = serializers.serialize("json", form_submission.objects.only('membership_number'))
            # struct = json.loads(data)
            # data = json.dumps(struct)
            return JsonResponse({'message':'submit successfully'})
        else:
            return JsonResponse({'message':'Membership Number already exist'})
    return render(request,'Info_App/validate_no.html')






def validate_no(request):
    if request.method == "POST":
        membership_number = request.POST['membership_number']
        # validation on membership number
        existing_info= form_submission.objects.values_list('membership_number')
        out1 = [item for t in existing_info for item in t]
        
        if membership_number=="":
            messages.error(request,"Please Enter Membership Number ")
            return redirect('Info_App:validate_no')
        elif membership_number in out1:
            messages.error(request,"Membership Number Already Exist")
            return redirect('Info_App:validate_no')
        elif len(membership_number) > 6 :
            messages.error(request,"Please put maximum 6 digit Membership number")
            return redirect('Info_App:validate_no')
        elif len(membership_number) < 5 :
            messages.error(request,"Please put minimum 5 digit Membership number")
            return redirect('Info_App:validate_no')
        else:
            # messages.success(request,"validate Membership Number successfully, please fill below Details") 
            # return redirect('Info_App:submit_cainfo')
            return render(request,'Info_App/submit_cainfo.html',{'membership_number':membership_number})
            
    return render(request,'Info_App/validate_no.html')
