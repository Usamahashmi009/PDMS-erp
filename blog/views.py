from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
# from .models import Profile, Tag, Article
from django.shortcuts import render, redirect
from .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from tenant.models import Tenant

# Django Q objects use to create complex queries
# https://docs.djangoproject.com/en/3.2/topics/db/queries/#complex-lookups-with-q-objects
from django.db.models import Q


# def home(request):

#     # feature articles on the home page
#     featured = Article.articlemanager.filter(featured=True)[0:3]

#     context = {
#         'articles': featured
#     }

#     return render(request, 'index.html', context)


# def articles(request):

#     # get query from request
#     query = request.GET.get('query')
#     # print(query)
#     # Set query to '' if None
#     if query == None:
#         query = ''

#     # articles = Article.articlemanager.all()
#     # search for query in headline, sub headline, body
#     articles = Article.articlemanager.filter(
#         Q(headline__icontains=query) |
#         Q(sub_headline__icontains=query) |
#         Q(body__icontains=query)
#     )

#     tags = Tag.objects.all()

#     context = {
#         'articles': articles,
#         'tags': tags,
#     }

#     return render(request, 'articles.html', context)


# def article(request, article):

#     article = get_object_or_404(Article, slug=article, status='published')

#     context = {
#         'article': article
#     }

#     return render(request, 'article.html', context)
def home(request):
    # Report 1: Number of client options in CRM model
    crm_reports = crm.objects.values('client_options').annotate(count=models.Count('client_options'))

    # Report 2: Details of properties to sell
    properties_to_sell = AddProperty.objects.filter(persontype='seller')
    
    # Report 3: Details of properties to purchase
    properties_to_purchase = AddProperty.objects.filter(persontype='purchaser')

    context = {
        'crm_reports': crm_reports,
        'properties_to_sell': properties_to_sell,
        'properties_to_purchase': properties_to_purchase,
    }

    return render(request, 'home.html', context)

def create_profile(request):
    if request.user.is_authenticated==True:
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('blog:profile_list')

        else:
            form = ProfileForm()

        return render(request, 'create_profile.html', {'form': form})
    return redirect("blog:user_login")

def add_property(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = AddPropertyForm(request.POST, request.FILES)
            if form.is_valid():
                property_instance = form.save(commit=False)
                property_instance.created_by = request.user
                property_instance.save()
                return redirect('blog:property_list')  # Redirect to a view showing the list of properties
        else:
            form = AddPropertyForm()
    else:
        return redirect('user_login')

    return render(request, 'add_property.html', {'form': form})

def profile_list(request):
    if request.user.is_authenticated==True:
        profiles = Profile.objects.all()
        return render(request, 'profile_list.html', {'profiles': profiles})
    return redirect("blog:user_login")


def property_list(request):
    if request.user.is_authenticated:
        properties = AddProperty.objects.all()

        # Get filter parameters from the request
        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        persontype = request.GET.get('persontype')
        profile_names = request.GET.get('profile_names')
        prop_size = request.GET.get('prop_size')

        # Apply filters based on user input
        if price_from:
            properties = properties.filter(price_from__gte=price_from)
        if price_to:
            properties = properties.filter(price_to__lte=price_to)
        if persontype:
            properties = properties.filter(persontype=persontype)
        if profile_names:
            properties = properties.filter(profile_names__name=profile_names)
        if prop_size:
            properties = properties.filter(prop_size=prop_size)

        return render(request, 'property_list.html', {'properties': properties})
    else:
        return redirect('user_login')

def edit_property(request, property_id, persontype):
    if request.user.is_authenticated:
        property_instance = get_object_or_404(AddProperty, id=property_id)

        if request.method == 'POST':
            form = AddPropertyForm(request.POST, instance=property_instance)
            if form.is_valid():
                form.save()
                return redirect('blog:property_list')
        else:
            form = AddPropertyForm(instance=property_instance)

        return render(request, 'edit_property.html', {'form': form, 'property_instance': property_instance})
    else:
        return redirect('user_login')

def delete_property(request, property_id, persontype):
    if request.user.is_authenticated:
        property_instance = get_object_or_404(AddProperty, id=property_id)

        if request.method == 'POST':
            property_instance.delete()
            return redirect('blog:property_list')

        return render(request, 'delete_property.html', {'property_instance': property_instance})
    else:
        return redirect('user_login')

def view_profile_details(request, property_id, persontype):
    if request.user.is_authenticated:
        try:
            property_instance = get_object_or_404(AddProperty, id=property_id)
        except Http404:
            raise Http404("Property does not exist")

        user_type = property_instance.persontype
        profile_name = property_instance.profile_names
        location = property_instance.location
        price_from = property_instance.price_from  
        price_to = property_instance.price_to
        plot_size = property_instance.prop_size
        prop_type = property_instance.prop_type

        suggestions = None
        remaining_data = None

        if user_type == 'seller':
            suggestions = AddProperty.objects.filter(
                
                persontype='purchaser',
                price_from__gte=price_from,
                price_to__lte=price_to,
            )
        elif user_type == 'purchaser':
            suggestions = AddProperty.objects.filter(
                
                persontype='seller',
                price_from__lte=price_from,
                price_to__lte=price_to,
            )

        if suggestions is not None:
            # Apply filters to remaining_data
            remaining_data = AddProperty.objects.exclude(id=property_instance.id, profile_names=profile_name)
            
        # Apply other filters similar to the sample code
        price_from_filter = request.GET.get('price_from')
        if price_from_filter:
            remaining_data = remaining_data.filter(price_from__gte=price_from_filter)

        price_to_filter = request.GET.get('price_to')
        if price_to_filter:
            remaining_data = remaining_data.filter(price_to__lte=price_to_filter)
            

        persontype_filter = request.GET.get('persontype')
        if persontype_filter:
            remaining_data = remaining_data.filter(persontype=persontype_filter)

        profile_names_filter = request.GET.get('profile_names')
        if profile_names_filter:
            remaining_data = remaining_data.filter(profile_names=profile_names_filter)

        prop_size_filter = request.GET.get('prop_size')
        if prop_size_filter:
            remaining_data = remaining_data.filter(prop_size=prop_size_filter)

        context = {
            'user_type': user_type,
            'location': location,
            'price_from': price_from,
            'price_to': price_to,
            'plot_size': plot_size,
            'suggestions': suggestions,
            'persontype': persontype,
            'prop_type': prop_type,
            'profile_name': profile_name,
            'remaining_data': remaining_data,
        }

        return render(request, 'view_profile_details.html', context)
    return redirect("blog:user_login")


def crm_details(request, property_id):
    property_instance = get_object_or_404(AddProperty, id=property_id)
    
    try:
        # Try to retrieve an existing CRM instance for the given property
        crm_instance = crm.objects.get(person_detail=property_instance.profile_names)
    except crm.DoesNotExist:
        # If not found, create an empty instance
        crm_instance = None
    # Fetch associated properties
    associated_properties =AddProperty.objects.all()
    if request.method == 'POST':
        crm_form = crmForm(request.POST, instance=crm_instance)
        if crm_form.is_valid():
            crm_instance = crm_form.save(commit=False)
            crm_instance.person_detail = property_instance.profile_names
            crm_instance.save()
            return redirect('blog:crm_details', property_id=property_id)
            
    else:
        crm_form = crmForm(instance=crm_instance)

    context = {
        'crm_form': crm_form,
        'property_instance': property_instance,
        'associated_properties': associated_properties,
    }

    return render(request, 'crm_details.html', context)




def user_logout(request):
    logout(request)
    return redirect("blog:user_login")

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                user_name = fm.cleaned_data['username']
                user_password = fm.cleaned_data['password']
                user = authenticate(username=user_name, password=user_password)
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect(reverse('blog:property_list'))   # Redirect to profile_list on successful login
        else:
            fm = AuthenticationForm()
        context = {
            "form": fm
        }
        return render(request, 'auth/userlogin.html', context)
    else:
        return HttpResponseRedirect(reverse('blog:property_list'))


def sign_up(request):
    if request.method =="POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,"Account created successfully::")
            fm.save()
            return HttpResponseRedirect("/signup/")
    else:
        fm = SignUpForm()
    context={
        "form":fm
    }
    return render(request, 'auth/signup.html', context)

