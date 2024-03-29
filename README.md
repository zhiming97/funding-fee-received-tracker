# Daily Funding Fee Received Tracker
Tracking the funding fees received daily by sourcing raw data from exchanges, transforming the data pulled and displaying them in a chart using Tableau. Python is used to automate and streamline this process flow so that no human intervention is required.

## Step 1:

Selenium is used to automatically pulled the records of funding fee received/paid from the account's history log periodically.
<br>
<img width="1348" alt="image" src="https://github.com/zhiming97/funding-fee-received-tracker/assets/97498951/cf989034-fadc-46a4-b20d-0486e5413340">


## Step 2: 

The pulled data is then updated to google sheets using Sheets API.
<br>
<img width="670" alt="image" src="https://github.com/zhiming97/funding-fee-received-tracker/assets/97498951/5c039803-9934-4a75-9ce0-70343baa4749">


## Step 3: 

Visualization is created using Tableau by using the latest data in the google sheets.
<br>
<img width="999" alt="image" src="https://github.com/zhiming97/funding-fee-received-tracker/assets/97498951/dad10c5d-7147-4e70-8920-587c733b4666">
<br>
[Click Here To View the Dashboard](https://public.tableau.com/app/profile/zhiming/viz/FundingFeeReceivedTracker/Dashboard1)



