from typing import List
import discord
from discord.ui import Select, View, Modal
from discord.utils import MISSING

announcement_embed = discord.Embed()

class AnunciosModal(Modal):
  def __init__(self):
    super().__init__(title='Anúncios de Mesa')
    
  titulo_modal = discord.ui.TextInput(label='Título da Mesa', placeholder='Waterdeep: Dragon Heist')
  jogadores_modal = discord.ui.TextInput(label='Jogadores/Vagas', placeholder='3', required=False)
  horario_modal = discord.ui.TextInput(label='Dia e Hora', placeholder='Todo domingo às 18h')
  sinopse_modal = discord.ui.TextInput(label='Sinopse', style=discord.TextStyle.long, max_length=2000)
  observacao_modal = discord.ui.TextInput(label='Observações', required=False, style=discord.TextStyle.long, max_length=2000)
  
  async def on_submit(self, interaction: discord.Interaction):
    
    announcement_embed.title = str(self.titulo_modal)
    
    announcement_embed.add_field(name='Sinopse', value=str(self.sinopse_modal), inline=False)
    announcement_embed.add_field(name='Jogadores/Vagas', value=str(self.jogadores_modal), inline=True)
    announcement_embed.add_field(name='Dia e Hora', value=str(self.horario_modal), inline=False)
    
    announcement_embed.set_footer(text=str(self.observacao_modal))
    
    await interaction.response.send_message("Selecione as opções de informações para a sua mesa:", view=AnuncioView(SistemaSelect()), ephemeral=True)
    ...

class AnuncioView(View):
  def __init__(self, select: discord.ui.Select):
    super().__init__()
    self.add_item(select)

class SistemaSelect(Select):
  def __init__(self):
    opt = [
      discord.SelectOption(label='🐲 Dungeons & Dragons', emoji='🐲'),
      discord.SelectOption(label='⚡ Tormenta 20', emoji='⚡'),
      discord.SelectOption(label='🛠️ Sistema Próprio', emoji='🛠️'),
    ]
    super().__init__(placeholder='Sistema de RPG', options=opt, min_values=1, max_values=1)  

  async def callback(self, interaction: discord.Interaction):
    self.disabled = True
    announcement_embed.add_field(name='Sistema: ', value=self.values[0])
    await interaction.response.send_message(f"Você selecionou: {self.values[0]}", ephemeral=True)
    await interaction.followup.send(view=AnuncioView(TipoMesaSelect()), ephemeral=True)
    
class TipoMesaSelect(Select):
  def __init__(self):
    opt = [
      discord.SelectOption(label='📚 Campanha', emoji='📚'),
      discord.SelectOption(label='📜 One Shot', emoji='📜'),
    ]
    super().__init__(placeholder='Tipo de Mesa', options=opt, min_values=1, max_values=1)
  
  async def callback(self, interaction: discord.Interaction):
    self.disabled = True
    announcement_embed.add_field(name='Tipo da Mesa:', value=self.values[0])
    await interaction.response.send_message(f"Você selecionou: {self.values[0]}", ephemeral=True)
    await interaction.followup.send(view=AnuncioView(CategoriasSelect()), ephemeral=True)
    
class CategoriasSelect(Select):
  def __init__(self):
    opt = [
      discord.SelectOption(label='🧙🏻‍♂️ Fantasia', emoji='🧙🏻‍♂️'),
      discord.SelectOption(label='🤖 Cyberpunk', emoji='🤖'),
      discord.SelectOption(label='⚔️ Medieval', emoji='⚔️'),
      discord.SelectOption(label='⚙️ Steampunk', emoji='⚙️'),
      discord.SelectOption(label='🚶🏻‍♂️ Realista', emoji='🚶🏻‍♂️'),
    ]
    super().__init__(placeholder='Categorias', options=opt, min_values=1, max_values=5)
  
  async def callback(self, interaction: discord.interactions):
    self.values.append(" ")
    self.values.reverse()

    self.disabled = True
    announcement_embed.add_field(name='Categorias', value='\n- '.join(self.values[item] for item in range(len(self.values))), inline=False)
    self.disabled = True
    await interaction.response.send_message(f"Você selecionou: {self.values}", ephemeral=True)
    await interaction.followup.send(view=AnuncioView(PlataformaSelect()), ephemeral=True)
    
class PlataformaSelect(Select):
  def __init__(self):
    opt = [
      discord.SelectOption(label='Discord'),
      discord.SelectOption(label='Roll20'),
      discord.SelectOption(label='Outros'),
    ]
    super().__init__(placeholder='Plataformas', options=opt, min_values=1, max_values=3)
  
  async def callback(self, interaction: discord.interactions):
    self.values.append(" ")
    self.values.reverse()
    
    self.disabled = True
    announcement_embed.add_field(name='Plataformas', value='\n- '.join(self.values[item] for item in range(len(self.values))) , inline=False)
    await interaction.response.send_message(f"Você selecionou: {self.values}", ephemeral=True)
    await interaction.followup.send(view=AnuncioView(FaixaEtariaSelect()), ephemeral=True)
    
    
class FaixaEtariaSelect(Select):
  def __init__(self):
    opt = [
      discord.SelectOption(label='Menores de 18 anos', emoji='🧒🏻'),
      discord.SelectOption(label='Maiores de 18 anos', emoji='👴🏻'),
    ]
    super().__init__(placeholder='Faixa Etária', options=opt, min_values=1, max_values=1)
  
  async def callback(self, interaction: discord.Interaction):
    self.disabled = True
    announcement_embed.add_field(name='Faixa Etária', value=self.values[0])
    await interaction.response.send_message(f"Você selecionou: {self.values[0]}", ephemeral=True)
    await interaction.followup.send(embed=announcement_embed, ephemeral=True)

