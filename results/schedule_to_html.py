import copy
import pandas as pd
import numpy as np

TIME_SLOTS = 4
DAYS = 5
ROOMS = 7
SLOTS = TIME_SLOTS * DAYS * ROOMS


def save_html(schedule, loc, spread_points, capacity_points,
              lecture_points, mutual_course_malus):
    """
    Save the schedule and its points to a html to visualize schedule.
    """
    # Save schedule for a different schedule visualisation
    schedule1 = copy.copy(schedule)

    # Make a table for all the schedule points
    d = pd.Series([lecture_points, -mutual_course_malus, "", spread_points,
                  capacity_points, spread_points - capacity_points])
    d = pd.DataFrame(d)
    d.columns = ["Points"]
    d.index = ["Incorrectly placed lectures",
               "Incorrectly placed courses with 'mutual' courses", "",
               "Spread bonus points (out of 440)",
               "Capacity malus points (out of 1332)",
               "Total points"]

    # Add room to every timeslot
    flatten = np.array(schedule).flatten()
    counter = 0
    for i in range(len(flatten)):
        if flatten[i].name is not ' ':
            flatten[i] = str(flatten[i]) + " : " + str(loc[counter])
        counter += 1
        counter = counter % 7

    # Convert back to 1D list
    schedule = flatten.reshape(DAYS, TIME_SLOTS, ROOMS).tolist()

    # Make a big schedule for the whole week
    df = pd.DataFrame(schedule1)
    pd.set_option('display.max_colwidth', 600)
    df.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
    df.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Transpose rows and columns
    df = df.T

    # Make seperate schedules for every day in the week
    test = pd.DataFrame(schedule)
    pd.set_option('display.max_colwidth', 600)
    test.columns = ['9:00 - 11:00', '11:00 - 13:00', '13:00 - 15:00', '15:00 - 17:00']
    test.index = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # Transpose rows and columns
    test = test.T

    # Determine column names
    tags = df['Monday'].apply(pd.Series)
    tags.columns = [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6]]
    tuesday = df['Tuesday'].apply(pd.Series)
    tuesday.columns = [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6]]
    wednesday = df['Wednesday'].apply(pd.Series)
    wednesday.columns = [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6]]
    thursday = df['Thursday'].apply(pd.Series)
    thursday.columns = [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6]]
    friday = df['Friday'].apply(pd.Series)
    friday.columns = [loc[0], loc[1], loc[2], loc[3], loc[4], loc[5], loc[6]]

    # dataframes will be added to the html_string
    html_string = '''
    <html>
      <head><title>Schedule</title></head>
      <link rel="stylesheet" type="text/css" href="style.css" href="https://www.w3schools.com/w3css/4/w3.css"/>
      <body class="body bgcolor="#660000">
        <h1 class="h1" align="center"></h>
        {table}
      </body>
    </html>.
    '''

    # Write to the html file
    with open('results/schedule.html', 'w') as f:
        f.write(html_string.format(table=d.to_html(classes='points')))
        f.write(html_string.format(table=test.to_html(classes='style')))
        f.write("Monday")
        f.write(html_string.format(table=tags.to_html(classes='style')))
        f.write("Tuesday")
        f.write(html_string.format(table=tuesday.to_html(classes='style')))
        f.write("Wednesday")
        f.write(html_string.format(table=wednesday.to_html(classes='style')))
        f.write("Thursday")
        f.write(html_string.format(table=thursday.to_html(classes='style')))
        f.write("Friday")
        f.write(html_string.format(table=friday.to_html(classes='style')))

    print("Saved schedule to 'results/schedule.html'")
