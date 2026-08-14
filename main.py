import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Configura o Faker para o Brasil
fake = Faker('pt_BR')
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Parâmetros da Simulação
NUM_COLABORADORES = 300
DATA_INICIO_OPERACOES = datetime(2021, 1, 1)
DATA_ATUAL = datetime(2026, 8, 13) # Data base atual

print("Iniciando a geração da base de dados de People Analytics...")

# ==========================================
# 1. DIMENSÃO: CARGOS E DEPARTAMENTOS
# ==========================================
departamentos_cargos = {
    'Tecnologia': ['Desenvolvedor Júnior', 'Desenvolvedor Pleno', 'Engenheiro de Dados', 'Tech Lead'],
    'Recursos Humanos': ['Assistente de RH', 'Analista de People Analytics', 'Business Partner', 'Gerente de RH'],
    'Comercial': ['Vendedor', 'Executivo de Contas', 'Gerente Comercial'],
    'Financeiro': ['Analista Financeiro', 'Coordenador de Controladoria']
}

dim_cargo_depto = []
id_cargo = 1
for depto, cargos in departamentos_cargos.items():
    for cargo in cargos:
        dim_cargo_depto.append({
            'ID_Cargo': id_cargo,
            'Departamento': depto,
            'Cargo': cargo
        })
        id_cargo += 1

df_dim_cargo = pd.DataFrame(dim_cargo_depto)
print("- Dimensão Cargos criada.")

# ==========================================
# 2. DIMENSÃO: COLABORADORES
# ==========================================
dim_colaboradores = []

for i in range(1, NUM_COLABORADORES + 1):
    # Data de admissão aleatória
    dias_operacao = (DATA_ATUAL - DATA_INICIO_OPERACOES).days
    data_admissao = DATA_INICIO_OPERACOES + timedelta(days=random.randint(0, dias_operacao))
    
    # Simulação de Turnover: 20% de chance de ter sido desligado
    status = np.random.choice(['Ativo', 'Desligado'], p=[0.8, 0.2])
    data_desligamento = pd.NaT
    
    if status == 'Desligado':
        dias_trabalhados = random.randint(30, (DATA_ATUAL - data_admissao).days)
        data_desligamento = data_admissao + timedelta(days=dias_trabalhados)
        
    dim_colaboradores.append({
        'ID_Colaborador': i,
        'Nome': fake.name(),
        'Data_Nascimento': fake.date_of_birth(minimum_age=18, maximum_age=65),
        'Genero': np.random.choice(['Feminino', 'Masculino', 'Outro'], p=[0.48, 0.48, 0.04]),
        'ID_Cargo': random.choice(df_dim_cargo['ID_Cargo'].tolist()), # Chave Estrangeira
        'Data_Admissao': data_admissao.date(),
        'Data_Desligamento': data_desligamento.date() if pd.notna(data_desligamento) else pd.NaT,
        'Status': status,
        'Salario_Base': round(random.uniform(2500, 15000), 2)
    })

df_dim_colaborador = pd.DataFrame(dim_colaboradores)
print("- Dimensão Colaboradores criada.")

# ==========================================
# 3. FATO: AUSÊNCIAS (Para análise estratégica de Absenteísmo)
# ==========================================
fato_ausencias = []
tipos_ausencia = ['Atestado Médico', 'Falta Injustificada', 'Licença Paternidade/Maternidade', 'Atraso']

# Gerar histórico de ausências apenas para o período em que o funcionário esteve ativo
for _, colab in df_dim_colaborador.iterrows():
    # Define o período de tempo em que a pessoa trabalhou na empresa
    inicio = colab['Data_Admissao']
    fim = colab['Data_Desligamento'] if pd.notna(colab['Data_Desligamento']) else DATA_ATUAL.date()
    
    dias_empresa = (fim - inicio).days
    if dias_empresa > 0:
        # Pessoas aleatórias têm diferentes taxas de ausência
        num_ocorrencias = random.randint(0, int(dias_empresa / 60)) 
        
        for _ in range(num_ocorrencias):
            data_ocorrencia = inicio + timedelta(days=random.randint(0, dias_empresa))
            
            # Se for atestado, geralmente são horas completas (8h), se atraso, menos horas.
            tipo = np.random.choice(tipos_ausencia, p=[0.6, 0.2, 0.05, 0.15])
            horas_perdidas = round(random.uniform(1, 8), 1) if tipo == 'Atraso' else 8.0
            
            fato_ausencias.append({
                'ID_Ocorrencia': fake.uuid4(),
                'ID_Colaborador': colab['ID_Colaborador'],
                'Data_Ausencia': data_ocorrencia,
                'Tipo_Ausencia': tipo,
                'Horas_Perdidas': horas_perdidas
            })

df_fato_ausencias = pd.DataFrame(fato_ausencias)
print("- Tabela Fato Ausências (Absenteísmo) criada.")

# ==========================================
# 4. EXPORTAÇÃO PARA O POWER BI
# ==========================================
# Salva os arquivos em CSV para importar no Power BI
df_dim_cargo.to_csv('dim_cargo.csv', index=False, encoding='utf-8')
df_dim_colaborador.to_csv('dim_colaborador.csv', index=False, encoding='utf-8')
df_fato_ausencias.to_csv('fato_ausencias.csv', index=False, encoding='utf-8')

print("\nSucesso! Arquivos CSV gerados no diretório atual.")