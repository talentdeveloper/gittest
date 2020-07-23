# bot/views.py
from django.shortcuts import render
from bot.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from os import path
from selenium.webdriver.support.ui import Select
from bot.models import CamsLogInfo,UserProfileInfo
from django.contrib.auth.models import User

def search_user():
    driver = webdriver.Chrome()

    driver.maximize_window()
    wait = WebDriverWait(driver, 20)
    # while True:
    users = CamsLogInfo.objects.all()
    for entry in users.values('chaturbate_username'):
        driver.get('https://es.chaturbate.com/' + entry['chaturbate_username'])
        if len(driver.find_elements_by_css_selector('#close_entrance_terms')) > 0:
            driver.find_element_by_id('close_entrance_terms').click()
        print(driver.find_elements_by_css_selector('#main div div:nth-child(6) div:nth-child(1)').text)
        sleep(20)

    # driver.quit()
    return 'ass'


def index(request):
    return render(request, 'bot/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


def chaturbate_login(driver, wait, username, password):
    url = 'https://es.chaturbate.com/auth/login/'

    driver.get(url)

    wait.until(ec.visibility_of_element_located((By.ID, 'id_username')))

    driver.find_element_by_id('id_username').send_keys(username)

    driver.find_element_by_id('id_password').send_keys(password + Keys.ENTER)

    wait.until(ec.visibility_of_element_located((By.ID, 'close_entrance_terms')))

    driver.find_element_by_id('close_entrance_terms').click()

    obj, created = CamsLogInfo.objects.get_or_create(chaturbate_username=username, defaults={'status': 'Online'})

    print(obj)

    return True


def get_profile(driver, wait, username, password):
    driver.get('https://es.chaturbate.com/p/' + username + '/?tab=bio')

    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, '#tabs_content_container  dl dd:nth-child(4)')))

    gender = driver.find_element_by_css_selector('#tabs_content_container  dl dd:nth-child(4)').text

    interested_in = driver.find_element_by_css_selector('#tabs_content_container  dl dd:nth-child(6)').text

    return gender, interested_in


@login_required
def chaturbate_start(request):
    user=UserProfileInfo.objects.filter(user_id=request.user.id).values()
    username = user[0]['chaturbate_username']
    password = user[0]['chaturbate_password']
    driver = webdriver.Chrome()


    driver.maximize_window()

    wait = WebDriverWait(driver, 100)

    chaturbate_login(driver, wait, username, password)

    gender, _ = get_profile(driver, wait, username, password)

    if 'mujeres' in gender.strip().lower():
        driver.get('https://es.chaturbate.com/male-cams/')
    elif 'hombres' in gender.strip().lower():
        driver.get('https://es.chaturbate.com/trans-cams/')

    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, 'li.room_list_room')))

    page = 0

    urllist = []

    while len(driver.find_elements_by_css_selector('a.next.endless_page_link')) > 0:
        page = page + 1
        driver.get(driver.find_element_by_css_selector('a.next.endless_page_link').get_attribute('href'))
        # print(CamsLogInfo.objects.filter(chaturbate_username=username))
        cams=CamsLogInfo.objects.filter(chaturbate_username=username,status='Online').count()
        if page >= 5:
            if page >= 7 or cams==0:
                break
            for elem in driver.find_elements_by_css_selector('li.room_list_room div.title a'):
                urllist.append(elem.get_attribute('href'))

    urllist = list(set(urllist))
    batch = 5
    urllist = [urllist[i:i + batch] for i in range(0, len(urllist), batch)]
    loopout=False
    for urls in urllist:
        for url in urls:
            if CamsLogInfo.objects.filter(chaturbate_username=username,status='Online').count()>0:
                a = "window.open('" + url + "','_blank');"
                driver.execute_script(a)
                sleep(3)
            else:
                loopout=True
                break
        if loopout:
            break
        sleep(80)
        while len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
    if loopout:
        driver.quit()
    return HttpResponse("Bot stopped")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def chaturbate_stop(request):
    user = UserProfileInfo.objects.filter(user_id=request.user.id).values()
    username = user[0]['chaturbate_username']
    cam = CamsLogInfo.objects.get(chaturbate_username=username)
    cam.status='offline'
    cam.save()
    return HttpResponse("Bot stopped")

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            # if 'profile_pic' in request.FILES:
            #   print('found it')
            #  profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'bot/registration.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                print(user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'bot/login.html', {})


# search_user()
