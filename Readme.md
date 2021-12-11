# Python project part two - Consumer behaviour dashboard

Deployed on [Heroku]('https://python-project-pt2-visuals.herokuapp.com/')

---

## The Project brief
The administration of a well known retail store is interested in using data collected over time from their various branches to understand consumer behaviour in the different regions of the country. Our plan is to create interactive visualisations for them generated from their data which tells a story about their customers.
They’ve provided 10 years worth of data collected from all available branches. The data is inconsistent in terms of format and content as the data collection and storage strategy is decided by the manager of a store branch.
This project is split into two parts, data cleaning and visualisations. This is the visualisation part.
---

## User stories
- As an administrator, I want to see 5 most and 5 least purchased products by:
    - product 
    - product category
    - per region
    - per city
- As an administrator, I want to see 10 best and 10 worst performing branches:
    - overall  
        - quantity sold
        - monetary value
    - per region
        - quantity sold
        - monetary value
    - per city
        - quantity sold
        - monetary value
- As an administrator, I want to see top 10 performing branches in sales per hour
- As an administrator, I want to see top 10 and bottom 10 profitable branches and show how profitable they are
---
## Used technologies
- Python, CSS
- libraries: pandas, dash, ast, whitenoise
---
## Taken approach

1. Wrote down user stories based on project brief
2. Extract what data fields are going to be needed to achieve customers requirements
3. From provided data, extracted csv files for each visualisation. More on this process on [Project part one GitHub page]('https://github.com/TomasAdamcik-dotcom/Python-project-pt1-data-cleaning')
4. Created wireframes of each separate visual
![Wireframes](/schemas/wireframes.jpg)
5. Worked from last visual to the first - last visuals seemed easier to create than the first one and I needed to refresh dash
6. Once all visuals were built, I tested every chart and made sure it complies with customer requirements
    - second visualisation was not showing data as expected due to my misunderstanding of requirements, so I rebuilt it 
7. Added styling of graphs
8. Added header and footer of dashboard and added CSS styling
9. Prepared app for deployment and deployed to Heroku 
---

## Next development
- based on customer requirements no other development is needed, however I would advise customer to have visualisations per year/month/day as well as from my personal experience, this would provide much better overview of market and customer behaviour.
    - this kind of change would open possibilities to use more kinds of graphs, mainly line charts 

---
## List of favourite functions
- Drilldowns change based on other drippdown input - On first two visuals, second dropdown list changes based on selection from the first dropdown list. On page load, second dropdown is disabled with placeholder asking user to make selection in the first dropdown.
- Using txt files to update drilldown options - I had to find a way how to do this and found literal_eval method from ast library that allows me to read text file as it is and therefore use it as options to a dropdown lists. I have created three dropdown list files for counties, product categories and regions as these are passed onto dropdown list based on selection from other dropdown.

---
## Difficulties during development
- When starting to build 1st drilldown, I ended up stuck on using two separate drilldowns and a submit button to subtmit selections. After I unsuccessfully tried for some time, I decided to start building dashboard from last visual. This helped me to build on complexity and when I worked on first visual (at last) I managed to buld it smoothly and also made it better by removing button. 
- At this stage, I realised that some data for branches are duplicated. There was no pattern to it so I drilled down into where are these data coming from and found that I need to remove duplicated in data cleaning process.
- When I deployed my project, CSS was not showing. Teached fortunatelly helped me to resolve this and recommended whitenoise library that resolved this issue
---
## List of known issues
 - no known issues
 
## Used resources
- literal_eval from ast library: [literal eval](https://www.aipython.in/python-literal_eval/)

