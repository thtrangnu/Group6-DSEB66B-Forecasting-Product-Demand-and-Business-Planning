# Using Linear Regression for demand estimation and prediction of the store.
## *1. Overview*
In business operations, revenue forecasting plays a crucial role in supporting managerial decision-making, strategic planning, and resource optimization. An effective forecasting system can help enterprises anticipate future demand, adjust supply plans, manage inventory, and evaluate the effectiveness of marketing campaigns.
## *2. Research Methodology* 
In this study, the project focuses on **estimating and predicting store demand based on historical data**, with the primary methodological approach being **linear regression**. Essentially, linear regression assumes that the relationship between the dependent variable (revenue) and the independent variable (time or other factors) can be described by a linear function. Although this method is relatively simple, it possesses several significant advantages, such as:
Ease of implementation and interpretability;
No requirement for large datasets;
Transparency, allowing for a direct interpretation of the impact of input variables on revenue;
Suitability as a foundational approach for further development into more complex forecasting models.
The research process is conducted through the following key steps:
### a. Data Collection
The dataset includes store revenue information across multiple periods (daily, monthly, or yearly).
Data is stored in tabular formats (CSV, Excel), with key attributes such as time, revenue, product, or product category.
### b. Data Preprocessing
Cleaning the dataset by removing duplicates and handling missing values.
Standardizing date formats and converting them into appropriate data types.
Selecting relevant input variables to be included in the model.
### c. Exploratory Data Analysis (EDA)
Performing descriptive statistics to understand the fundamental characteristics of revenue.
Visualizing data to observe trends and fluctuations over time.
Examining the relationships between independent variables and the dependent variable (revenue).
### d. Model Construction
Applying Linear Approximation to model the relationship between time and revenue.
In cases with multiple independent variables, multiple linear regression is employed.
### e. Model Evaluation
Assessing model accuracy using error metrics such as:
MAE (Mean Absolute Error)
RMSE (Root Mean Square Error)
Comparing predicted values with actual observations to evaluate model performance.
### g. Visualization and Results Presentation
Plotting the linear regression line alongside actual data points.
Presenting predicted revenues for upcoming periods.
Interpreting the practical implications of the results for store management and decision-making
## *3. Data source* 
**Original dataset** : https://www.kaggle.com/datasets/felixzhao/productdemandforecasting

The raw dataset used for this study was derived from the original dataset through a filtering process. This step was conducted to simplify the data structure and make it more suitable for the analytical capacity and academic level of the student research group. By reducing unnecessary complexity, the dataset retains its essential characteristics while remaining accessible for analysis and model construction.
## *4. Conclusion*
The application of linear approximation facilitates the identification of future revenue trends. Although the linear model may not fully capture nonlinear factors inherent in business operations, it provides a solid scientific foundation for estimating overall tendencies. This, in turn, supports managers in business planning, enhances competitiveness, and serves as a reference point for the development of more advanced forecasting models in the future.
## *5. Team Contribution*
#### *Lê Thị Thuỳ Trang - Leader - 22%*
- Searched for project ideas and datasets, filtered the original dataset to create the dataset used in the project, and studied how to preprocess and prepare data for model building.
- Assigned tasks to team members.
- Learned how to build the web using Dash (Flask), combining CSS and HTML for better UI design.
- Studied machine learning models (mainly Linear Regression, and additionally Decision Tree and Random Forest).
- Coded the machine learning model, trained the model using both manual computation and sklearn.
- Proposed ideas for the web structure.
- Coded the Result page of the web application.
- Integrated code from all members, fixed errors, and delivered the final version for the web.
#### *Vũ Thị Thuý Hằng - 18%*
- Learned how to build the web using Dash (Flask), combining CSS and HTML.
- Coded the Dataset page of the web.
- Studied data processing methods.
- Handled and coded the frontend part of the website.
#### *Vũ Thị Thu Trang - 15%*
- Learned how to filter, clean data, and handle outliers.
- Coded the data filtering and cleaning part.
- Studied the Linear Regression model.
#### *Ninh Duy Đức - 15%*
- Learned how to perform data exploration.
- Coded the data exploration section.
- Studied the Linear Regression model.
#### *Nguyễn Gia Khánh - 15%*
- Learned how to build the web using Dash (Flask), combining CSS and HTML.
- Created the project slides.
- Coded the Homepage of the web.
#### *Trần Viết Long - 15%*
- Learned how to build the web using Dash (Flask), combining CSS and HTML.
- Identified the applications of NumPy in the project.
- Studied the Linear Regression model.
- Coded the EDA section of the web
## **6. How to Run This App**

### **a. Create a Virtual Environment**

We recommend creating a virtual environment using Python 3 before running the application.

### **b. Clone the repository and navigate to the project folder**

```bash
git clone https://github.com/thtrangnu/Group6-DSEB66B-Forecasting-Product-Demand-and-Business-Planning.git
cd Group6-DSEB66B-Forecasting-Product-Demand-and-Business-Planning/Project
python3 -m venv venv
```

### **c. Activate the virtual environment**

#### **macOS / Linux (Unix systems):**

```bash
source venv/bin/activate
```

#### **Windows:**

```bash
venv\Scripts\activate
```

### **d. Install required packages**

```bash
pip install -r requirements.txt
```

### **e. Run the app locally**

```bash
python app.py
```

### **f. Notes for macOS users**

If Python 2 is still present on your system, use `python3` and `pip3`:

```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 app.py
```

If you encounter `command not found: python`, create aliases:

```bash
alias python="python3"
alias pip="pip3"
```
3"
