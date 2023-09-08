from django.contrib import admin
from .models import Profile, Tb_Registros, TbPragas


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']


@admin.register(Tb_Registros)
class Tb_OcorrenciasAdmin(admin.ModelAdmin):
    list_display = ['id_ocorrencia','Usuário', 'Data da Ocorrência','Cultura', 'praga','status','imagem', 'Nome da Propriedade afetada',
                    'Quantidade de hectar afetado', 'Total do prejuizo R$', 'latitude', 'longitude', 'Observações']
    search_fields = ('id_ocorrencia', 'praga')
    ordering = ['praga']


@admin.register(TbPragas)
class TbPragasAdmin(admin.ModelAdmin):
    list_display = [ 'cultura','especie', 'nome_comum', 'nome_comum2']
