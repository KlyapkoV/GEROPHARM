import streamlit as st
import pandas as pd
from numerize import numerize
import plotly.express as px

# НАСТРОЙКА ПАРАМЕТРОВ СТРАНИЦЫ

st.set_page_config(page_title='GEROPHARM', layout='wide')

st.image(r'https://gxp-academy.org/upload/medialibrary/135/m4okmfo6fqxplkozpdt54h25c8afz88z.jpg')


###############################################################################################
############################## ФОРМИРОВАНИЕ ОСНОВНОГО ДАТАФРЕЙМА ##############################
###############################################################################################

uploader_file = st.file_uploader('Загрузите файл с исходными данными', type='xlsx')

try:
    df = pd.read_excel(uploader_file)
except ValueError:
    pass

df['Выполнение плана в %'] = (df['Факт'] / df['План'] * 100).astype(int)
df['Прирост по продуктам'] = (df['Факт'] - df['Факт предыдущий период']).astype(int)
df['Прирост по продуктам в %'] = ((df['Факт'] / df['Факт предыдущий период'] - 1) * 100).astype(int)
df['Факт предыдущий период'] = df['Факт предыдущий период'].astype(int)


###############################################################################################
################################ ВЫБОР ПРОДУКТА ПО ОТДЕЛЬНОСТИ ################################
###############################################################################################

d = st.multiselect(
                   label='Продукт',
                   options=df['Продукты'].to_list(),
                   default=df['Продукты'].to_list()
                  )

df = df.loc[(df['Продукты'].isin(d))]


###############################################################################################
####################################### МЕТРИКИ КАРТОЧЕК ######################################
###############################################################################################

# ПРОДАЖИ ТЕКУЩЕГО ПЕРИОДА (итог)
fact_sum = numerize.numerize(
                             int(
                                 df['Факт'].sum()
                                )
                            )

# ПЛАН ПРОДАЖ (итог)
plan_sum = numerize.numerize(
                             int(
                                 df['План'].sum()
                                )
                            )

# ПРОДАЖИ ПРЕДЫДУЩЕГО ПЕРИОДА (итог)
prev_sum = numerize.numerize(
                             int(
                                 df['Факт предыдущий период'].sum()
                                )
                            )

# ВЫПОЛНЕНИЕ ПЛАНА (%)
plan_execution_percent = numerize.numerize(
                                           int(
                                               (df['Факт'].sum() / df['План'].sum()) * 100
                                              )
                                          )
# ВЫПОЛНЕНИЕ ПЛАНА (итог)
plan_execution = numerize.numerize(
                                   int(
                                       df['Факт'].sum() - df['План'].sum()
                                      )
                                  )

# ПРИРОСТ ПРОДАЖ (итог)
sales_growth = numerize.numerize(
                                 int(
                                     df['Прирост по продуктам'].sum()
                                    )
                                )

# ПРИРОСТ ПРОДАЖ (%)
sales_growth_percent = numerize.numerize(
                                         int(
                                             (df['Факт'].sum() / df['Факт предыдущий период'].sum() - 1) * 100
                                            )
                                        )


###############################################################################################
########################################## КАРТОЧКИ ###########################################
###############################################################################################

col1, col2, col3, col4 = st.columns(4)

# ПРОДАЖИ ТЕКУЩЕГО ПЕРИОДА (итог)
with col1:
    st.markdown(
                "<h1 style='text-align: center; color: #000000; font-size:30px;'>Факт</h1>"
                , unsafe_allow_html=True
               )
    st.markdown(
                f"<h1 style='text-align: center; color: #008000; font-size:60px;'>{fact_sum}</h1>"
                , unsafe_allow_html=True
               )
    st.markdown(
                f"<h1 style='text-align: center; color: #808080; font-size:20px;'>факт предыдущий({prev_sum})</h1>"
                , unsafe_allow_html=True
               )

# ПЛАН ПРОДАЖ (итог)
with col2:
    st.markdown(
                "<h1 style='text-align: center; color: #000000; font-size:30px;'>План продаж</h1>"
                , unsafe_allow_html=True
               )
    st.markdown(
                f"<h1 style='text-align: center; color: #000000; font-size:60px;'>{plan_sum}</h1>"
                , unsafe_allow_html=True
               )

# ВЫПАЛНЕНИЕ ПЛАНА (%)
with col3:
    st.markdown(
                "<h1 style='text-align: center; color: #000000; font-size:30px;'>Выполнение плана</h1>"
                , unsafe_allow_html=True
               )
    if int(
           (df['Факт'].sum() / df['План'].sum()) * 100
          ) >= 100:
        st.markdown(
                    f"<h1 style='text-align: center; color: #008000; font-size:60px;'>🡅{plan_execution_percent} %</h1>"
                    , unsafe_allow_html=True
                   )
    else:
        st.markdown(
                    f"<h1 style='text-align: center; color: #FF8C00; font-size:60px;'>🡇{plan_execution_percent} %</h1>"
                    , unsafe_allow_html=True
                   )
    if int(df['Факт'].sum() - df['План'].sum()) >= 100:
        st.markdown(
                    f"<h1 style='text-align: center; color: #008000; font-size:30px;'>(+{plan_execution})</h1>"
                    , unsafe_allow_html=True
                   )
    else:
        st.markdown(
                    f"<h1 style='text-align: center; color: #FF8C00; font-size:30px;'>({plan_execution})</h1>"
                    , unsafe_allow_html=True
                   )

#  ПРИРОСТ ПРОДАЖ (%)
with col4:
    st.markdown(
                "<h1 style='text-align: center; color: #000000; font-size:30px;'>Прирост продаж </h1>"
                , unsafe_allow_html=True
               )
    if int(
           (df['Факт'].sum() / df['Факт предыдущий период'].sum() - 1) * 100
          ) > 0:
        st.markdown(
                    f"<h1 style='text-align: center; color: #008000; font-size:60px;'>🡅{sales_growth_percent} %</h1>"
                    , unsafe_allow_html=True
                   )
    else:
        st.markdown(
                    f"<h1 style='text-align: center; color: #FF8C00; font-size:60px;'>🡇{sales_growth_percent} %</h1>"
                    , unsafe_allow_html=True
                   )

    if int(
            (df['Факт'].sum() / df['Факт предыдущий период'].sum() - 1) * 100
    ) > 0:
        st.markdown(
            f"<h1 style='text-align: center; color: #008000; font-size:30px;'>(+{sales_growth})</h1>"
            , unsafe_allow_html=True
        )
    else:
        st.markdown(
                    f"<h1 style='text-align: center; color: #FF8C00; font-size:30px;'>({sales_growth})</h1>"
                    , unsafe_allow_html=True
                   )


###############################################################################################
########################################## ГРАФИКИ ############################################
###############################################################################################

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
                 x=df['Выполнение плана в %'].sort_values(),
                 y=df['Продукты'],
                 text=df['Выполнение плана в %'].sort_values().map(lambda x: '{0:1.0f}%'.format(x)),
                 color_discrete_sequence=['#008000']
                )
    fig.update_layout(
                      title={
                             'text': 'Выполнение плана продаж',
                             'x': 0.5,
                             'xanchor': 'center',
                             'font_size': 30
                            },
                      uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      yaxis_title=None,
                      xaxis_title=None
                     )
    fig.update_yaxes(title='', visible=True)
    fig.update_xaxes(
                     title='',
                     visible=True,
                     showticklabels=False
                    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)


with col2:
    fig = px.bar(
                 x=df['Прирост по продуктам в %'].sort_values(),
                 y=df['Продукты'],
                 text=df['Прирост по продуктам в %'].sort_values().map(lambda x: '{0:1.0f}%'.format(x)),
                 color_discrete_sequence=['#008000'],
                )
    fig.update_layout(
                      title={
                             'text': 'Прирост по продуктам',
                             'x': 0.5,
                             'xanchor': 'center',
                             'font_size': 30
                            },
                      uniformtext_minsize=12,
                      uniformtext_mode='hide',
                      yaxis_title=None,
                      xaxis_title=None
                     )

    fig.update_yaxes(title='', visible=True)
    fig.update_xaxes(
                     title='',
                     visible=True,
                     showticklabels=False
                    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, theme='streamlit', use_container_width=True)


df = df.sort_values('Прирост по продуктам', ascending=0).head(5)
fig = px.bar(
             x=df['Прирост по продуктам'].sort_values(),
             y=df['Продукты'],
             text_auto=True,
             color_discrete_sequence=['#008000']
            )
fig.update_layout(
                  title={
                         'text': 'Топ-5 продуктов по приросту',
                         'x': 0.5,
                         'xanchor': 'center',
                         'font_size': 30
                        },
                  uniformtext_minsize=15,
                  uniformtext_mode='hide',
                  yaxis_title=None,
                  xaxis_title=None
                  )
fig.update_yaxes(title='', visible=True)
fig.update_xaxes(
                 title='',
                 visible=True,
                 showticklabels=False
                )
fig.update_traces(textposition='outside')

st.plotly_chart(fig, theme='streamlit', use_container_width=True)
