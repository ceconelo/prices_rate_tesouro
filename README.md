# Scraping prices and tax on treasury bonds

Basically the project consists of 5 stages

The project is divided into 7 stages:

1. Load the last day
    Get the local file that was saved the day before
2. Get the current day
    Get the current day from the treasure website
3. Format the current day
    In the step above we have all bonds in the same object, at this stage we will separate them into 
    buy and sell (invest / redeem)
4. Calculate the variation
    Calculate the variation between the current day and the last day
5. Aggregate the variation
    As there are securities that have more than one investment option, changing only the year of maturity, 
    so let's group them by name.
6. Prepare the text to publish 
    Construction of the text that will be used in tweets (same pattern already used) with the exception that 
    all securities can now be posted.
7. Publish the text
    Here you need to get the API and integrate it into this project.
8. Save the current day
    Add the key xlsLastUpdated to the current day and save it to the local file (last_day.json).