from django.db import models
from django.conf import settings
from stdimage import StdImageField


CONTROLE_CHOICE=(
    ("s",'Sim'),
    ("N","Não"),
)
class Base(models.Model):
    #inserido = models.DateField('Criado em',auto_now_add=True)
    #atualizado = models.DateField('Modificado em',auto_now_add=True)
    ativo = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    class Meta:
        verbose_name = "Tabela de Perfil"
        verbose_name_plural = "Tabela de Perfis"
    def __str__(self):
        return f'Profile for user {self.user.username}'






class TbPragas(models.Model):
    id_praga = models.AutoField(primary_key=True)
    cultura = models.CharField(max_length=45, blank=True, null=True)
    especie = models.CharField(max_length=45, blank=True, null=True)
    nome_comum = models.CharField(max_length=45)
    nome_comum2 = models.CharField(max_length=45)

    class Meta:

        verbose_name = "Tabela de Praga"
        verbose_name_plural = "Tabela de Pragas"


lista_praga = TbPragas.objects.select_related('nome_comum').values_list('nome_comum', 'nome_comum').order_by(
    "nome_comum").distinct()

lista_cultura = TbPragas.objects.select_related('cultura').values_list('cultura', 'cultura').order_by(
    "cultura").distinct()

class Tb_Registros(Base):
    id_ocorrencia = models.AutoField(primary_key=True)
    usuario =  models.CharField(name='Usuário',max_length=45)
    data_registro =  models.DateField(name='Data da Ocorrência',help_text='Data em que foi visualizada a praga.')
    praga = models.CharField(max_length=40,choices=lista_praga,help_text='Selecione qual o tipo de praga esta contaminando.')
    cultura =  models.CharField(name='Cultura',max_length=45,choices=lista_cultura,help_text='Qual plantação foi contaminada?')
    status = models.CharField(verbose_name='Controlada?', max_length=45, choices=CONTROLE_CHOICE,help_text='A praga esta controlada?')
    Nome_propriedade = models.CharField(name='Nome da Propriedade afetada',max_length=60,help_text='Nome da propriedade que esta sendo contaminada.')
    prejuizo=models.DecimalField(name='Total do prejuizo R$',max_digits=20, decimal_places=2,default=0.0,help_text='qual o valor do prejuizo?')
    hectares=models.IntegerField(name='Quantidade de hectar afetado',default=0,help_text='quantos hectares estão contaminados')
    latitude = models.CharField(max_length=45)
    longitude = models.CharField(max_length=45)
    imagem = StdImageField('Imagem',upload_to='images',help_text='Selecione as imagens da praga.',null=True,blank=True)
    observacao = models.TextField(name='Observações',null=True,blank=True)

    class Meta:

        verbose_name = "Tabela de Registro"
        verbose_name_plural = "Tabela de Registros"
    def __str__(self):
        return self.Usuário