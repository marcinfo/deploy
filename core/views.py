from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Tb_Registros,TbPragas
from .forms import LoginForm, UserRegistrationForm, \
                   UserEditForm, ProfileEditForm,RegistrosModelForm
import pandas as pd
from django.db.models import Avg,Count,Max,Min,Sum

import folium
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from geopy import distance

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated ' \
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'core/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            return render(request,
                          'core/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'core/register.html',
                  {'user_form': user_form})


@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html', {'section': 'dashboard'})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request,
                  'core/edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})



def index(request):
    registros = Tb_Registros.objects.select_related('usuario').all().filter(ativo=True).values()


    contador =registros.count()
    if contador != 0:

        praga_afetada = Tb_Registros.objects.values('praga').annotate(total=Count('praga')).order_by("-total")
        status_praga = Tb_Registros.objects.values('status',).annotate(total=Count('status')).order_by("-total")

        grupo_status =pd.DataFrame(status_praga)


        reg_ocorrencias = pd.DataFrame(registros)
        total=reg_ocorrencias['id_ocorrencia'].count()
        total_prejuizo = reg_ocorrencias['prejuizo'].sum()
        total_hectares = reg_ocorrencias['hectares'].sum()
        tipo_praga=reg_ocorrencias.groupby('praga')['praga'].unique().count()
        tipo_cultura = reg_ocorrencias.groupby('cultura')['cultura'].unique().count()
        dados = reg_ocorrencias[['praga','hectares','prejuizo','cultura','status']]

        print(dados)

        config={'displayModeBar':False}
        fonte_titulo='Times New Roman'
        largura= 400
        altura=200
        graf_grupo_cultura = px.histogram(dados, x=dados['praga'],
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['steelblue'])
        graf_grupo_cultura.update_layout(title={'text':'Ocorrências de Pragas.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_cultura.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'ocorrências','font':{'size':12}})
        chart_graf_grupo_cultura = graf_grupo_cultura.to_html(config = config)

        graf_grupo_praga = px.histogram(dados, x=dados['cultura'],
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['steelblue'])
        graf_grupo_praga.update_layout(title={'text':'Cultura Atacada.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_praga.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'ocorrências','font':{'size':12}},
                                         xaxis_title={'text': 'cultura', 'font': {'size': 12}})
        chart_graf_grupo_praga = graf_grupo_praga.to_html(config = config)



        graf_grupo_status= px.histogram(dados, y=dados['status'],
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['red'])
        graf_grupo_status.update_layout(title={'text':'Status das Pragas.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_status.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'total','font':{'size':12}},
                                         xaxis_title={'text': 'status', 'font': {'size': 12}})
        chart_graf_grupo_status = graf_grupo_status.to_html(config = config)

        graf_grupo_praga_prejuizo= px.histogram(dados, x=dados['praga'], y=dados['prejuizo'].astype(float),
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['red'])
        graf_grupo_praga_prejuizo.update_layout(title={'text':'Prejuizo por Praga.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_praga_prejuizo.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'R$','font':{'size':12}},
                                         xaxis_title={'text': 'praga', 'font': {'size': 12}})
        chart_graf_grupo_praga_prejuizo = graf_grupo_praga_prejuizo.to_html(config = config)

        graf_grupo_cultura_prejuizo= px.histogram(dados, x=dados['cultura'], y=dados['prejuizo'].astype(float),
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['red'])
        graf_grupo_cultura_prejuizo.update_layout(title={'text':'Prejuizo por Cultura.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_cultura_prejuizo.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'R$','font':{'size':12}},
                                         xaxis_title={'text': 'cultura', 'font': {'size': 12}})
        chart_graf_grupo_cultura_prejuizo = graf_grupo_cultura_prejuizo.to_html(config = config)

        graf_grupo_hectar_prejuizo= px.histogram(dados, x=dados['hectares'], y=dados['prejuizo'].astype(float),
                      height=altura,width=largura,template='simple_white',color_discrete_sequence=['red'])
        graf_grupo_hectar_prejuizo.update_layout(title={'text':'Prejuizo por hectar.','font':{'size':16}}, title_font_family=fonte_titulo,
                                         title_font_color='darkgrey',title_y=0.9,title_x=0.5)
        graf_grupo_hectar_prejuizo.update_layout(title_font_family='classic-roman',font_color='grey',
                                         yaxis_title={'text':'R$','font':{'size':12}},
                                         xaxis_title={'text': 'hectares', 'font': {'size': 12}})
        graf_grupo_hectar_prejuizo = graf_grupo_hectar_prejuizo.to_html(config = config)

        context = {
            'total': total, 'total_prejuizo': total_prejuizo, 'tipo_praga': tipo_praga,'total_hectares': total_hectares,
            'praga_afetada':praga_afetada,'tipo_cultura': tipo_cultura,'chart_graf_grupo_cultura':chart_graf_grupo_cultura,
            'chart_graf_grupo_praga':chart_graf_grupo_praga,'chart_graf_grupo_status':chart_graf_grupo_status,
            'chart_graf_grupo_praga_prejuizo':chart_graf_grupo_praga_prejuizo,
            'chart_graf_grupo_cultura_prejuizo':chart_graf_grupo_cultura_prejuizo,
            'graf_grupo_hectar_prejuizo':graf_grupo_hectar_prejuizo,
        }
        return render(request, 'core/index.html',context)
    else:
        print(contador)
        messages.info(request,'Não existem informações para exibir!')
        return render(request, 'core/index.html')



def cadastrarForm(request):

    if request.method == "GET":
        form=RegistrosModelForm()
        context={
            'form': form
        }
        return render(request, 'core/cadastrar.html',context=context)
    else:
        form = RegistrosModelForm(request.POST, request.FILES)
        if form.is_valid():
            regitro = form.save(commit=False)
            regitro.usuario = request.user
            registro = form.save()
            form = RegistrosModelForm()

        context = {
            'form':form
        }
        return render(request, 'core/cadastrar.html', context=context)


def mostra_ocorrencia(request):
    registros = Tb_Registros.objects.all().values()
    contador =registros.count()
    if contador != 0:
        l1 = " -15.793889"
        l2 = " -47.882778"
        lat_get = request.GET.get('lat')
        lon_get = request.GET.get('lon')
        zoom = 4
        loc_usuario = 'centralizado em Brasilia.'
        if (lat_get != None) & (lon_get != None):
            latitude = str(lat_get)
            longitude = str(lon_get)
            l1 = latitude
            l2 = longitude
            zoom = 9
            loc_usuario='Você esta aqui!'
        else:
            l1 = l1
            l2 = l2
        ocorrencias = Tb_Registros.objects.all().values()
        geo_loc_ocorrencias = pd.DataFrame(ocorrencias)
        lista_distancia = []
        for _, dis in geo_loc_ocorrencias.iterrows():
            distan = distance.distance((l1, l2), [float(dis['latitude']), dis['longitude']]).km
            distan = float(distan)
            distan = round(distan,1)
            lista_distancia += [distan]
        geo_loc_ocorrencias['distancia'] = lista_distancia
        geo_loc_ocorrencias = geo_loc_ocorrencias.nsmallest(100, 'distancia')
        geo_loc_ocorrencias['poupup']= ' data '+geo_loc_ocorrencias['Data da Ocorrência'].map(str)+' '+geo_loc_ocorrencias['praga']+ \
                          ' '+geo_loc_ocorrencias['observacao']+ ' distancia=  '+geo_loc_ocorrencias['distancia'].map(str) +'km'

        m = folium.Map(location=[l1, l2], zoom_start=zoom, control_scale=True, width=1090, height=450)
        folium.Marker(location=[float(l1), float(l2)]).add_to(m)
        for _, ocor  in geo_loc_ocorrencias.iterrows():

            folium.Marker(
                location=[ocor['latitude'], ocor['longitude']], popup=ocor['poupup'],
            ).add_to(m)
        folium.Marker(
            location=[l1, l2], popup=loc_usuario, icon=folium.Icon(color='green', icon='ok-circle'), ).add_to(m)
        context = {
            'vacin': 'Veja as ocorrencias mais proximas da sua localização.',
            'm': m._repr_html_()
        }

        print(lista_distancia )


        return render(request, 'core/mapa.html',context)

    else:
        print(contador)
        messages.info(request,'Não existem informações para exibir!')
        return render(request, 'core/mapa.html')

