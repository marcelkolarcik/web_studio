import json
import os

import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from appointments.models import Appointment
from projects.models import Project
from .forms import FreelancerForm
from .models import Freelancer


def register_form(request):
    return render(request, 'freelancers/register_form.html')


def register_freelancer(request):
    template = 'freelancers/register_form.html'

    def user_name_present(name):
        if User.objects.filter(username=name).exists():
            return True

        return False

    def user_email_present(email):
        if User.objects.filter(email=email).exists():
            return True

        return False

    form_data = {
        'name': request.POST['name'],
        'email': request.POST['email'],
        'password': 'dummy_password',
        'skills': request.POST['skills'],
        'portfolio_link': request.POST['portfolio_link'],
        'about': request.POST['about'],

    }

    form = FreelancerForm(form_data)
    context = {
        'form': form
    }
    # user already registered with his email
    if user_email_present(request.POST['email']):
        messages.error(request,
                       'It appears that you already registered.Please login with '
                       ' your credentials to manage your account. Thank you! '
                       )

        return render(request, template, context)

    # username used already, Django won't create new user with the same name
    if user_name_present(request.POST['name']):
        messages.error(request, 'User name taken. Please use different user name!')

        return render(request, template, context)

    if form.is_valid():
        try:
            """
            IF FORM IS VALID, WE WILL SAVE IT TO DB AND WILL CREATE
            NEW USER WITH CREDENTIALS FROM THE FORM
            SO THAT HE CAN LOG IN INTO HIS ACCOUNT
            
            """
            form.password = ''
            form.save()
            new_user = User.objects.create_user(request.POST['name'],
                                                request.POST['email'],
                                                request.POST['password'])
            new_user.save()

            messages.success(request, 'Your account was created successfully. Please login with your '
                                      'credentials.')
            # user can sign in with his credentials

            # sending email to owner of the website, informing him about new appointment

            # request_url = "https://api.eu.mailgun.net/v3/globtopus.com/messages"
            # key = os.getenv('MAILGUN_API_KEY')
            # recipient = 'marcelkolarcik@gmail.com'
            # requests.post(request_url, auth=('api', key), data={
            #     'from': 'marcellidesigns marcelkolarcik@gmail.com',
            #     'to': recipient,
            #     'subject': 'New appointment',
            #     "template": "marcellidesigns_appointment",
            #     "h:X-Mailgun-Variables":
            #         json.dumps(
            #             {'welcome': 'New appointment : ' + site_types[request.POST['site_type']],
            #              'body_1': request.POST['email'] + ' - ' + request.POST['phone_num'] + ' - ' + request.POST[
            #                  'name'],
            #              'body_2': request.POST['project'],
            #              'question': times[request.POST['time_slot']],
            #              'sign-in': 'Site',
            #              'welcome_team': 'Marcelli Designs', })
            # })
            #
            # # sending email to customer, informing him about new appointment
            #
            # recipient = request.POST['email']
            # requests.post(request_url, auth=('api', key), data={
            #     'from': 'marcellidesigns marcelkolarcik@gmail.com',
            #     'to': recipient,
            #     'subject': 'Your appointment',
            #     "template": "marcellidesigns_customer_appointment",
            #     "h:X-Mailgun-Variables":
            #         json.dumps(
            #             {'welcome': 'Your appointment',
            #              'customer_name': request.POST['name'],
            #              'time': times[request.POST['time_slot']],
            #              'phone': request.POST['phone_num'],
            #              'project': request.POST['project'],
            #              'site_type': site_types[request.POST['site_type']],
            #              'welcome_team': 'Marcelli Designs', })
            # })
            return redirect(reverse('account_login'))

        except:
            messages.error(request, 'There was an error with your form. \
                                                              Please double check your information')

            context['form'] = form

            return render(request, template, context)
    else:
        context['form'] = form
        return render(request, template, context)


def freelancer(request):
    freelancer = Freelancer.objects.get(email=request.user.email)
    form = FreelancerForm(instance=freelancer)

    try:
        appointment = Appointment.objects.get(project_number=freelancer.current_project)

    except:
        appointment = False


    try:
        project = Project.objects.get(project_number=freelancer.current_project)
    except:
        project = False


    context = {
        'freelancer': freelancer,
        'form': form,
        'appointment':appointment,
        'project':project
    }
    return render(request, 'freelancers/dashboard.html', context)


def update_freelancer(request, freelancer_id):
    freelancer_i = get_object_or_404(Freelancer, id=freelancer_id)
    if request.method == 'POST':

        form = FreelancerForm(request.POST, instance=freelancer_i)

        if form.is_valid():
            form.save()
            messages.success(request,
                             'Details updated successfully! '

                             )
            return redirect(reverse('freelancer'))


        else:
            messages.error(request,
                           'There is something wrong with your form '
                           ' Please check your input! '
                           )

            return render(request, 'freelancers/dashboard.html', {'form': form})