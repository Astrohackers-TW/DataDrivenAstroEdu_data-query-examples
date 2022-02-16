import streamlit as st
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive


def app():
    st.title('取得太陽系外行星資料的範例')
    st.info('[太陽系外行星](https://zh.wikipedia.org/wiki/%E5%A4%AA%E9%99%BD%E7%B3%BB%E5%A4%96%E8%A1%8C%E6%98%9F)(以下簡稱系外行星)是指位於太陽系之外的行星，此教材示範如何藉由Astroquery套件取得NASA系外行星資料庫提供的資料。')
    st.header('藉由Astroquery套件取得NASA系外行星資料庫提供的資料')
    st.code(example_code, language='python')

    st.header('延伸應用：能篩選系外行星資料並將資料表匯出CSV檔的介面')
    with st.spinner('從[NASA太陽系外行星資料庫](https://exoplanetarchive.ipac.caltech.edu/)載入資料中，請稍候...'):
        exoplanet_data = get_exoplanet_data_by_astroquery()

    col1, col2 = st.columns([1, 3])
    with col1:
        disc_year_min = int(exoplanet_data['發現年份'].min())
        disc_year_max = int(exoplanet_data['發現年份'].max())
        disc_year = st.slider(
            '1. 篩選截至某年所發現的系外行星：', disc_year_min, disc_year_max, disc_year_max, 1
        )
        exoplanet_data = exoplanet_data[
            exoplanet_data['發現年份'] <= disc_year
        ].reset_index(drop=True)

        discovery_methods = st.multiselect(
            '2. 以「發現方法」篩選系外行星資料',
            exoplanet_data['發現方法'].unique(),
            exoplanet_data['發現方法'].unique()
        )
        exoplanet_data = exoplanet_data[
            exoplanet_data['發現方法'].isin(discovery_methods)
        ].reset_index(drop=True)

        st.download_button(
            label='將資料匯出成CSV檔',
            data=exoplanet_data.to_csv(index=False),
            file_name='exoplanet_data.csv',
            mime='text/csv'
        )
    with col2:
        st.text('系外行星資料列表')
        st.dataframe(exoplanet_data, height=500)


example_code = '''
"""
設定要取得的資料欄位，並用astroquery套件的nasa_exoplanet_archive模組取得資料
欄位名稱意義請參考：https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html
nasa_exoplanet_archive模組的文件：https://astroquery.readthedocs.io/en/latest/ipac/nexsci/nasa_exoplanet_archive.html
"""
from astroquery.nasa_exoplanet_archive import NasaExoplanetArchive

parameters = 'hostname,pl_name,sy_dist,pl_bmasse,pl_orbper,pl_rade,disc_year,discoverymethod'
exoplanet_data = NasaExoplanetArchive.query_criteria(table='pscomppars', select=parameters)
exoplanet_data = dataexoplanet_data.to_pandas()
'''


@st.cache(show_spinner=False)
def get_exoplanet_data_by_astroquery():
    parameters = 'hostname,pl_name,sy_dist,pl_bmasse,pl_orbper,pl_rade,disc_year,discoverymethod'
    exoplanet_data = NasaExoplanetArchive.query_criteria(table='pscomppars', select=parameters)
    exoplanet_data = exoplanet_data.to_pandas()    
    exoplanet_data = exoplanet_data.sort_values(
        by=['sy_dist'], ascending=False, ignore_index=True
    )
    renamed_columns_dict = {
        'hostname': '母恆星名稱',
        'pl_name': '行星名稱',
        'sy_dist': '距離(秒差距)',
        'pl_bmasse': '行星質量',
        'pl_orbper': '行星軌道週期',
        'pl_rade': '行星半徑',
        'disc_year': '發現年份',
        'discoverymethod': '發現方法'
    }
    exoplanet_data = exoplanet_data.rename(columns=renamed_columns_dict)

    return exoplanet_data
