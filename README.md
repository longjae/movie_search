# 영화 검색기

GPT-4 기반 데이터에서 SQL 검색을 통한 영화 검색기입니다.

gpt-4-0125-preview 모델을 사용하였으며 캐글에 있는 Full TMDB Movies Dataset 2024 (1M Movies) 데이터셋을 사용했습니다.

SQLite를 사용해 데이터셋을 DB화 시켰으며, Gradio를 사용해 간단한 UI를 적용했습니다.

SQL 검색을 사용한 이유는 SQL 검색 시 소요되는 시간을 확인하기 위함이었으며, 최종 결과물 산출까지 소요되는 시간은 약 15초 내외였습니다.

쿼리를 통해 SQL 처리를 위한 LLM 모델에서 쿼리를 가져오고 쿼리와 LLM 모델을 통해 결과물을 얻는 구조입니다.

<p align="center"> 
    <img src="./img/movie_archi.png"> 
</p>

<p align="center"> 
    <img src="./img/img_1.png"> 
</p>