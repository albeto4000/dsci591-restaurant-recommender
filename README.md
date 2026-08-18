# BreadCrumbs

## Project Overview

BreadCrumbs is a restaurant recommender system developed for DSCI 591 at Drexel University. The system consists of an analysis of Yelp restaurant reviews, an ALS recommender pipeline, and a Django web-app. The Yelp Open Dataset used to develop this project can be found [here](https://business.yelp.com/data/resources/open-dataset/).

## Directory Structure
```
.
├── django_app/
│   ├── core/                             # Templates and routes used to display recommendations and restaurant details
│   ├── restaurant_recommender/           # Django app settings and config
│   └── manage.py                         # Auto-generated script used to run Django commands
|
├── notebooks/
│   ├── Breadcrumbs_Pyspark_EDA.ipynb     #PySpark notebook to analyze dataset summary statistics and geospatial features
│   ├── category-attribute-analysis.ipynb #Analysis of 'categories' and 'attributes' features
│   ├── data_preprocessing.ipynb          #Data preprocessing: convert raw Yelp Open Dataset JSON files (restaurants, users, reviews) to parquet format
│   ├── eda.ipynb                         #Analysis of recommender dataset summary statistics and relationship between user friend count/rating count
│   ├── nlp_review_analysis.ipynb         #Review text sentiment analysis
│   ├── photo_preprocessing.ipynb         #Data preprocessing: converts Yelp photos JSON to parquet. This data is not used for analysis
│   └── als_recommender.ipynb             #PySpark notebook to train and evaluate a PySpark Alternating Least Squares recommender pipeline
|
├── README.md
├── als_pipeline.zip                      #Trained PySpark ALS recommender model
└── pyproject.toml                        #UV environment files
```

## Dataset
* **Restaurants**: 52,268 restaurants across 11 metro areas. Attributes include name, location, categories, hours, and attributes.
* **Users**: 1,445,990 unique users. Includes information about user social interaction (friends) and review quality (helpful, cool, etc).
* **Reviews**: 4,724,471 reviews, including review_text and star_rating (out of 5)

## Methodology
1. **Data Preprocessing**: Loads Yelp JSON files, selects businesses with category 'Restaurant' and related reviews/users, then saves tables as parquets.
2. **EDA**: User/restaurant rating sparsity, regional category preferences, correlation between user social interaction and rating count, and relationship between review text sentiment and star rating. 
3. **Modeling**: Alternating Least Squares model estimates user ratings for new items by solving for U and P matrices, where ratings_matrix = U*P.

## Model Results
* **RMSE**: 0.7996
* **MAE**: 0.5739

## Future Work
* Prepare Django app for deployment
* Integrate recommender model with Django app
* Develop embedding-based recommender model informed by restaurant and user attributes
* Focus sentiment analysis on specific attributes/categories
