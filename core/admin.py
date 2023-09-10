from django.contrib import admin
from .models import Profile, Tb_Registros, TbPragas


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Tb_Registros)
class Tb_OcorrenciasAdmin(admin.ModelAdmin):
    list_display = ['id_ocorrencia','ativo','usuario','inserido', 'Data da Ocorrência','cultura', 'praga','status','imagem', 'nome_propriedade',
                    'hectares', 'prejuizo', 'latitude', 'longitude', 'observacao']
    search_fields = ('id_ocorrencia','inserido', 'praga')
    ordering = ['praga']


@admin.register(TbPragas)
class TbPragasAdmin(admin.ModelAdmin):
    list_display = [ 'cultura','especie', 'nome_comum', 'nome_comum2']
