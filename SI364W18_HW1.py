## HW 1
## SI 364 W18
## 1000 points

## Joshua Walker (joshwalk)

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

## Main resource for problem 4 to determine endpoints and necessary headers to access NBA stats comes from nba_py (https://github.com/seemethere/nba_py)
## Stackoverflow post that helped me understand how to use checkboxes with flask: https://stackoverflow.com/questions/31859903/get-the-value-of-a-checkbox-in-flask


## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
import requests
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def welcome():
	return 'Welcome to SI 364!'

@app.route('/movie/<filmtitle>')
def movie_search(filmtitle):
	response = requests.get("https://itunes.apple.com/search?term="+filmtitle+'&entity=movie')
	return response.text

@app.route('/question',methods=["GET","POST"])
def number_question():
	formstring = """<br><br>
	<form action="" method='POST'>
	Enter your favorite number: <br>
<input type="text" name="number"> <br>
<input type="submit" value="Submit">
"""
	if request.method == "POST":
		number_submitted = int(request.form["number"]) # casts string to int
		number_doubled = number_submitted * 2
		return formstring + "<br><br>Double your number is: " + str(number_doubled)
	else:
		return formstring

# My interactive data exchange takes a date as a user input and gets the NBA standings for each/both conferences for that day
@app.route('/problem4form', methods = ["GET","POST"])
def nba_standings():
	# this header allows the function to access the NBA stats API; copied from aforementioned nba_py project
	headers = {
	    'user-agent': ('Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'),
	    'Dnt': ('1'),
	    'Accept-Encoding': ('gzip, deflate, sdch'),
	    'Accept-Language': ('en'),
	    'origin': ('http://stats.nba.com')
	    }
	# html form setup that includes a text box and 2 checkboxes
	formstring = """
	<h1>NBA Standings by Day</h1>
	<form action="" method='POST'>
	Enter date in format mm/dd/yyyy: <br>
	<input type="text" name="date"> <br><br>
	Choose either conference or both: <br>
	<input type="checkbox" name="econf">Eastern Conference<br>
	<input type="checkbox" name="wconf">Western Conference<br><br>
	<input type="submit" value="Submit">
	</form>
"""
	if request.method == "POST":
		date = request.form['date']
		response = requests.get('http://stats.nba.com/stats/scoreboard/?GameDate='+ date + '&LeagueID=00&DayOffset=0', headers=headers)
		data = json.loads(response.text)
		east_standings = ""
		west_standings = ""
		east_results_formatted = ""
		west_results_formatted = ""
		if request.form.get("econf"): # if Eastern Conference box checked
			eastconf = data["resultSets"][4]
			for team in eastconf["rowSet"]: # builds a list with team name and its win percentage
				name_pct = "<li>" + team[5] + " " + str(team[9]) + "</li>"
				east_standings += name_pct
			east_results_formatted = "<h3>Eastern Conference</h3><ol>{}</ol>".format(east_standings) #organized into ordered list
		if request.form.get("wconf"): # if Western Conference box checked; the following code is modeled after the above
			westconf = data["resultSets"][5]
			for team in westconf["rowSet"]:
				name_pct = "<li>" + team[5] + " " + str(team[9]) + "</li>"
				west_standings += name_pct
			west_results_formatted = "<h3>Western Conference</h3><ol>{}</ol>".format(west_standings)
		date_header = "<h2>Standings for {}</h2>".format(date)
		return formstring + date_header + east_results_formatted + west_results_formatted

	else: # if anything hasn't been submitted, just show the blank form
		return formstring


if __name__ == '__main__':
	app.run()


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:
# {
#  "resultCount":0,
#  "results": []
# }
## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.
## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points
## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.
