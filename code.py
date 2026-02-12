from scipy.stats import ttest_ind
from statsmodels.stats.proportion import proportions_ztest
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
import datetime as dt

df = pd.read_csv('/datasets/logs_exp_us.csv',sep='\t')
print(df)

df['EventTimestamp'] = pd.to_datetime(df['EventTimestamp'], unit ='s')
df['date'] = df['EventTimestamp'].dt.date
df['hora'] = df['EventTimestamp'].dt.hour
print(df)

print(df['EventName'].nunique())

print(df['DeviceIDHash'].nunique())

prom_eve = df.groupby('DeviceIDHash').agg({'EventName':'nunique'})
print(prom_eve.mean())


date_max = df['EventTimestamp'].max()
date_min = df['EventTimestamp'].min()
prom_date = date_max - date_min
print(prom_date)

rouped  = df.groupby(['hora','date']).agg({'DeviceIDHash':'nunique',})
plt.figure(figsize=(30,20))
grouped.plot(kind='line')
plt.xticks(rotation=50)
plt.title('identificar unico por fecha y hora')
plt.xlabel('fecha y hora')
plt.ylabel('numeros de id')
plt.show()


df['EventHour'] = df['EventTimestamp'].dt.floor('H')
event_counts = df.groupby('EventHour')['DeviceIDHash'].count()
plt.figure(figsize=(15, 5))
event_counts.plot()
plt.title("Cantidad de eventos por hora")
plt.xlabel("Fecha y hora")
plt.ylabel("Número de eventos")
plt.tight_layout()
plt.show()

df_clean = df[df['EventTimestamp']>='2019-08-01']
print(f"perdiodo de los datos {df_clean['EventTimestamp'].min()} a {df_clean['EventTimestamp'].max()}")

date_anti = df[df['EventTimestamp']<='2019-07-30']
count_events = date_anti.groupby('EventName').agg({'EventTimestamp':'count'})
print(f"eventos perdidos:{count_events} ")
count_user = date_anti['DeviceIDHash'].nunique()
print(f"usarios perdidos: {count_user} ")

usuarios_por_grupo = df_clean.groupby('ExpId')['DeviceIDHash'].nunique()
print(usuarios_por_grupo)


event_frecu = df_clean.groupby('EventName').agg({'DeviceIDHash':'count'})
event_sort = event_frecu.sort_values(by='DeviceIDHash',ascending= False)
plt.figure(figsize=(15,7))
event_sort.plot(kind='bar')
plt.title('eventos por frecuencia')
plt.xlabel('eventos')
plt.ylabel('frecuencia')
plt.show()

group_user_events = df_clean.groupby('EventName').agg({'DeviceIDHash':'nunique'})
group_user_events = group_user_events.sort_values(by='DeviceIDHash',ascending=False)
print(group_user_events)

total_usuarios = df_clean['DeviceIDHash'].nunique()
proporcion = (group_user_events/total_usuarios) *100
print(proporcion)

user_table = df_clean.pivot_table(
    index='DeviceIDHash',
    columns='EventName',
    values = 'EventTimestamp',
    aggfunc= 'min'
)
step_1 = ~user_table['MainScreenAppear'].isna()
step_A = step_1 & (user_table['OffersScreenAppear']>user_table['MainScreenAppear'])
step_B = step_A & (user_table['CartScreenAppear']>user_table['OffersScreenAppear'])
step_C = step_B & (user_table['PaymentScreenSuccessful']>user_table['CartScreenAppear'])
nu_a = user_table[step_A].shape[0]
nu_b = user_table[step_B].shape[0]
nu_c = user_table[step_C].shape[0]
print('numero de evento a:',nu_a,)
print('numero de evento b:',nu_b,)
print('numero de evento c:',nu_c,)
print('proporcion de B respecto a A:',(nu_b/nu_a)*100)
print('proporcion de C respecto a B:',(nu_c/nu_b)*100)

print('porcentaje de usarios desde la primera etapa hasta la ultima:',(nu_c/nu_a)*100)

usuariosbygruop = df.groupby('ExpId')['DeviceIDHash'].nunique()
usertotal = df['DeviceIDHash'].nunique()
print("\nDistribución de usuarios:")
for grupo, usuarios in usuariosbygruop.items():
    porcentaje = (usuarios / total_usuarios) * 100
    print(f"Grupo {grupo}: {usuarios} usuarios ({porcentaje:.1f}%)")


event_by_users = df_clean.groupby(['ExpId','DeviceIDHash']).size().reset_index(name='num_eventos')
grupo_247A = event_by_users[event_by_users['ExpId']==247]['num_eventos']
grupo_246A = event_by_users[event_by_users['ExpId']==246]['num_eventos']
alpha = 0.05
t_stat,p_value = ttest_ind(grupo_246A,grupo_247A, equal_var=False)
print('p value:',p_value)
if(p_value<alpha):
    print('Hay diferencia estadísticamente significativa')
else:
    print('No hay diferencia significativa')


count_event = df['EventName'].value_counts()
evento_mas_popular = count_event.index[0]
print('evento mas popular:',evento_mas_popular)
      

evento_unico = df_clean['EventName'].unique()
aa_usarios_246 =  df_clean[df_clean['ExpId']==246]['DeviceIDHash'].nunique()
aa_usarios_247 =  df_clean[df_clean['ExpId']==247]['DeviceIDHash'].nunique()

print('total de usarios 246:',aa_usarios_246)
print('total de usarios 247:',aa_usarios_247)


def comparacion_evento(evento):
    df_event = df_clean[df_clean['EventName'] == evento]
    
    evento_usuarios_246 = df_event[df_event['ExpId'] == 246]['DeviceIDHash'].nunique()
    evento_usuarios_247 = df_event[df_event['ExpId'] == 247]['DeviceIDHash'].nunique()

    proporciones_246 = evento_usuarios_246 / aa_usarios_246
    proporciones_247 = evento_usuarios_247 / aa_usarios_247

    test_count = np.array([evento_usuarios_246, evento_usuarios_247])
    test_n = np.array([aa_usarios_246, aa_usarios_247])
    
    stat, p_value = proportions_ztest(test_count, test_n)

    return {
        'evento': evento,
        'usuarios_246': evento_usuarios_246,
        'usuarios_247': evento_usuarios_247,
        'proporcion_246': proporciones_246,
        'proporcion_247': proporciones_247,
        'pvalue': p_value
    }

resultado_total_def = [comparacion_evento(e) for e in evento_unico]

df_resultado = pd.DataFrame(resultado_total_def)

eventos_sigmi = df_resultado[df_resultado['pvalue'] < 0.05]

print("Todos los eventos:")
print(df_resultado.sort_values(by='pvalue'))

print("Eventos con diferencia significativa entre grupos:")
print(eventos_sigmi)



def comparar_eventos_fuentes_alternativas(df, eventos, group_a, group_b, name_a='grupo_a', name_b='grupo_b'):
    results = []
    
    user_aa = df[df['ExpId'] == group_a]['DeviceIDHash'].nunique()
    user_bb = df[df['ExpId'] == group_b]['DeviceIDHash'].nunique()

    for evento in eventos:
        df_events = df[df['EventName'] == evento]

        user_event_aa = df_events[df_events['ExpId'] == group_a]['DeviceIDHash'].nunique()
        user_event_bb = df_events[df_events['ExpId'] == group_b]['DeviceIDHash'].nunique()

        proporcion_a = user_event_aa / user_aa if user_aa > 0 else 0
        proporcion_b = user_event_bb / user_bb if user_bb > 0 else 0

        count_eve = np.array([user_event_aa, user_event_bb])
        n_eve = np.array([user_aa, user_bb])

        try:
            stat, p_value = proportions_ztest(count_eve, n_eve)
        except:
            stat, p_value = np.nan, np.nan

        results.append({
            'evento': evento,
            f'usuarios_{name_a}': user_event_aa,
            f'usuarios_{name_b}': user_event_bb,
            f'proporcion_{name_a}': proporcion_a,
            f'proporcion_{name_b}': proporcion_b,
            'pvalue': p_value
        })

    return pd.DataFrame(results)

grupo_246aa1= 246
grupo_247aa2= 247
grupo_248bb3= 248


comparacion_1 = comparar_eventos_fuentes_alternativas(df_clean,evento_unico,grupo_248bb3,grupo_246aa1, 'experimental', 'control_246')
comparacion_2 = comparar_eventos_fuentes_alternativas(df_clean,evento_unico,grupo_248bb3,grupo_247aa2, 'experimental', 'control_247')

df_combined = df_clean[df_clean['ExpId'].isin([246,247])].copy()
df_combined['ExpId'] = 777


dfexper = df_clean[df_clean['ExpId']==grupo_248bb3]
df_complet = pd.concat([df_combined,dfexper])
comparacion_3 = comparar_eventos_fuentes_alternativas(df_complet,evento_unico,grupo_248bb3,777, 'experimental', 'control_777')


print('comparacion del grupo 246',comparacion_1)
print('comparacion del grupo 247',comparacion_2)
print('comparacion del grupo combinado',comparacion_3)



alpha = 0.05
numero_eventos = len(evento_unico)*3
print(' pruebas de hipótesis estadísticas realizadas:',numero_eventos)
alpha_corr = alpha/numero_eventos
comparacion_1['sigmificancia'] = comparacion_1['pvalue']<alpha_corr
comparacion_2['sigmificancia'] = comparacion_2['pvalue']<alpha_corr
comparacion_3['sigmificancia'] = comparacion_3['pvalue']<alpha_corr
print(comparacion_1['sigmificancia'])
print(comparacion_2['sigmificancia'])
print(comparacion_3['sigmificancia'])