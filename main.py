import typer
from datetime import datetime
from datetime import timedelta
import json

app = typer.Typer()

def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
            raise ValueError
        return True
    except ValueError:
        return False

def add_timed_session(start_time, end_time):
    date = str(start_time.date())
    with open('dw.json', 'r') as f:
        all_dw = json.load(f)
    if date not in all_dw:
        all_dw[date] = {"sessions" : [], "untimed" : 0}
    session = {}
    session["start_time"] = str(start_time)
    session["end_time"] = str(end_time)
    session["duration"] = round((end_time - start_time).total_seconds() / 60.0)
    all_dw[date]["sessions"].append(session)
    with open('dw.json', 'w') as f:
            json.dump(all_dw, f)

@app.command()
def status():
    """
    Print the current status of today's deep work.
    """
    print("---")
    with open('status.json', 'r') as f:
        status = json.load(f)
        active = status["active"]
        sessionstart = status["sessionstart"]
    if active:
        print("You are currently tracking deep work.")
        datetime_start = datetime.strptime(status["sessionstart"], "%Y-%m-%d %H:%M:%S.%f")
        datetime_end = datetime.now()
        minutes_diff = round((datetime_end - datetime_start).total_seconds() / 60.0)
        string_start = datetime_start.strftime("%H:%M")
        print(f"Your current session started at {string_start}, and you have been working for {minutes_diff} minutes.")
    else:
        print("You are not currently tracking deep work.")
    if "goal" in status:
        if status["goal"] != 0:
            # Print what percent of the goal the user has tracked today
            with open('dw.json', 'r') as f:
                all_dw = json.load(f)
            date = str(datetime.now().date())
            if date in all_dw:
                total_minutes = all_dw[date]["untimed"]
                for session in all_dw[date]["sessions"]:
                    total_minutes += session["duration"]
                # If currently tracking an active session, add that to the total
                if active:
                    datetime_start = datetime.strptime(sessionstart, "%Y-%m-%d %H:%M:%S.%f")
                    datetime_end = datetime.now()
                    minutes_diff = round((datetime_end - datetime_start).total_seconds() / 60.0)
                    total_minutes += minutes_diff
                goal = status["goal"]
                percent = (total_minutes / goal) * 100
                print()
                # List the total amount of deep work done today
                print(f"You have done a total of {total_minutes} minutes of deep work today.")
                print(f"You have completed {percent:.0f}% of your goal.")
                if percent <= 100:
                    bar_length = 40
                    block = int(round(bar_length * percent / 100))
                    progress_bar = "▓" * block + "-" * (bar_length - block)
                    print(f"[{progress_bar}] {percent:.0f}%")
                else:
                    print("Congratulations! \N{party popper}\N{party popper}\N{party popper}")
    print("---")


@app.command()
def go():
    """
    Start a new session of deep work.
    """
    sessionstart = datetime.now()
    with open('status.json', 'r') as f:
        status = json.load(f)
    if status["active"] == True:
        print("A session is already active.")
    else:
        status["active"] = True
        status["sessionstart"] = str(sessionstart)
        string_start = sessionstart.strftime("%H:%M")
        with open('status.json', 'w') as f:
            json.dump(status, f)
        print(f"Deep work session started at {string_start}.")

@app.command()
def stop():
    """
    Stop the current session of deep work, and add it to the log.
    """
    with open('status.json', 'r') as f:
        status = json.load(f)
        active = status["active"]
    if not active:
        print("There is no active session to end.")
    else:
        # Update status
        start_time = datetime.strptime(status["sessionstart"], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.now()
        minutes_diff = round((end_time - start_time).total_seconds() / 60.0)
        status["active"] = False
        status["sessionstart"] = 0
        with open('status.json', 'w') as f:
            json.dump(status, f)
        # Add the session to the big json of all deep work
        add_timed_session(start_time, end_time)
        # Tell user we're done
        print(f"Session ended. You did {minutes_diff} minutes of deep work.")

@app.command()
def cancel():
    """
    Cancel the current session of deep work, and do not record it.
    """
    with open('status.json', 'r') as f:
        status = json.load(f)
        active = status["active"]
    if not active:
        print("There is no active session to end.")
    else:
        sure = typer.confirm(f"Are you sure you want to cancel your session?")
        if not sure:
            print("Ok, not cancelling.")
            raise typer.Abort()
        # Update status
        start_time = datetime.strptime(status["sessionstart"], "%Y-%m-%d %H:%M:%S.%f")
        end_time = datetime.now()
        minutes_diff = round((end_time - start_time).total_seconds() / 60.0)
        status["active"] = False
        status["sessionstart"] = 0
        with open('status.json', 'w') as f:
            json.dump(status, f)
        print(f"Session canceled.")

@app.command()
def reset(date: str = str(datetime.now().date())):
    """
    Completely reset all data for DATE. By default, DATE is today.
    """
    if validate(date):
        sure = typer.confirm(f"Are you sure you want to reset all data for {date}?")
        if not sure:
            print("Ok, not resetting.")
            raise typer.Abort()
        with open('dw.json', 'r') as f:
            all_dw = json.load(f)
        if date in all_dw:
            del all_dw[date]
        with open('dw.json', 'w') as f:
                json.dump(all_dw, f)
    else:
        print("Error: Not a valid date.")

@app.command()
def add(duration: int, date: str = str(datetime.now().date())):
    """
    Add DURATION to the total amount of deep work done on a given DATE. By default, DATE is today.
    """
    if validate(date):
        with open('dw.json', 'r') as f:
            all_dw = json.load(f)
        if date not in all_dw:
            all_dw[date] = {"sessions" : [], "untimed" : 0}
        all_dw[date]["untimed"] += duration
        with open('dw.json', 'w') as f:
                json.dump(all_dw, f)
        dur_hrs = duration // 60
        dur_mins = duration % 60
        print(f"Added {dur_hrs}h{dur_mins}m of additional deep work for {date}.")
    else:
        print("Error: Not a valid date.")

@app.command()
def set(duration: int, date: str = str(datetime.now().date())):
    """
    Set DURATION as the total amount of deep work done on a given DATE. By default, DATE is today.
    """
    if validate(date):
        with open('dw.json', 'r') as f:
            all_dw = json.load(f)
        if date not in all_dw:
            all_dw[date] = {"sessions" : [], "untimed" : 0}
        else:
            previous = all_dw[date]["untimed"]
            overwrite = typer.confirm(f"{previous}m of deep work are already logged on that date. Are you sure you want to overwrite?")
            if not overwrite:
                print("Ok, not overwriting.")
                raise typer.Abort()
        all_dw[date]["untimed"] = duration
        with open('dw.json', 'w') as f:
            json.dump(all_dw, f)
    else:
        print("Error: Not a valid date.")

@app.command()
def day(date: str = str(datetime.now().date())):
    """
    Prints the total amount of deep work for a given DATE. By default, DATE is today.
    """
    if validate(date):
        with open('dw.json', 'r') as f:
            all_dw = json.load(f)
        if date not in all_dw:
            print(f"No work was tracked on {date}.")
            raise typer.Abort()
        date_dict = all_dw[date]
        tot = date_dict["untimed"]
        for session in date_dict["sessions"]:
            tot += session["duration"]
        hrs = tot // 60
        mins = tot % 60
        print("---")
        print(f"You have done {hrs}h{mins}m of deep work on {date}:")
        # List the sessions completed on the given date
        for session in date_dict["sessions"]:
            start_time = datetime.strptime(session["start_time"], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")
            end_time = datetime.strptime(session["end_time"], "%Y-%m-%d %H:%M:%S.%f").strftime("%H:%M")
            duration = session["duration"]
            print(f" - {start_time} to {end_time:<11} ({duration} minutes)")
        if 'untimed' in date_dict and date_dict['untimed'] != 0:
            print(f" - Additional deep work ({date_dict['untimed']} minutes)")
        print("---")
    else:
        print("Error: Not a valid date.")

@app.command()
def week(date: str = str(datetime.now().date())):
    """
    Prints a summary of the total amount of deep work done in the week leading up to the given DATE. By default, DATE is today.
    """
    if validate(date):
        given_date = datetime.strptime(date, "%Y-%m-%d")
        start_of_week = given_date - timedelta(days=given_date.weekday())
        end_of_week = min(start_of_week + timedelta(days=6), datetime.now())
        total_minutes = 0

        with open('dw.json', 'r') as f:
            all_dw = json.load(f)

        for single_date in (start_of_week + timedelta(n) for n in range((end_of_week - start_of_week).days + 1)):
            date_str = single_date.strftime("%Y-%m-%d")
            if date_str in all_dw:
                day_data = all_dw[date_str]
                total_minutes += day_data["untimed"]
                for session in day_data["sessions"]:
                    total_minutes += session["duration"]

        hrs = total_minutes // 60
        mins = total_minutes % 60
        print("---")
        print(f"You have done {hrs}h{mins}m of deep work from {start_of_week.date()} to {end_of_week.date()}.")
        print()
        # Print a summary with a new line for every day of the week up to the current date
        for single_date in (start_of_week + timedelta(n) for n in range((end_of_week - start_of_week).days + 1)):
            date_str = single_date.strftime("%Y-%m-%d")
            day_minutes = 0
            if date_str in all_dw:
                day_data = all_dw[date_str]
                day_minutes += day_data["untimed"]
                for session in day_data["sessions"]:
                    day_minutes += session["duration"]
            day_hrs = day_minutes // 60
            day_mins = day_minutes % 60
            weekday_name = single_date.strftime("%A")
            date_str_abbrv = single_date.strftime("%m-%d")
            print(f"{weekday_name:<10} {date_str_abbrv}: {day_hrs:>2}h{day_mins:02}m")
        print("---")
    else:
        print("Error: Not a valid date.")

@app.command()
def year(date: str = str(datetime.now().date())):
    """
    Prints a summary of the total amount of deep work done in the year containing the given DATE. By default, DATE is today.
    """
    if validate(date):
        given_date = datetime.strptime(date, "%Y-%m-%d")
        start_of_year = datetime(given_date.year, 1, 1)
        end_of_year = min(datetime(given_date.year, 12, 31), datetime.now())
        total_minutes = 0

        with open('dw.json', 'r') as f:
            all_dw = json.load(f)

        for single_date in (start_of_year + timedelta(n) for n in range((end_of_year - start_of_year).days + 1)):
            date_str = single_date.strftime("%Y-%m-%d")
            if date_str in all_dw:
                day_data = all_dw[date_str]
                total_minutes += day_data["untimed"]
                for session in day_data["sessions"]:
                    total_minutes += session["duration"]

        hrs = total_minutes // 60
        mins = total_minutes % 60
        print("---")
        print(f"You did {hrs}h{mins}m of deep work in {given_date.year}.")
        print()

        # Print a summary with a new line for every month of the year up to the given date
        for month in range(1, end_of_year.month + 1):
            start_of_month = datetime(given_date.year, month, 1)
            end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            month_minutes = 0

            for single_date in (start_of_month + timedelta(n) for n in range((end_of_month - start_of_month).days + 1)):
                date_str = single_date.strftime("%Y-%m-%d")
                if date_str in all_dw:
                    day_data = all_dw[date_str]
                    month_minutes += day_data["untimed"]
                    for session in day_data["sessions"]:
                        month_minutes += session["duration"]

            month_hrs = month_minutes // 60
            month_mins = month_minutes % 60
            month_name = start_of_month.strftime("%B")
            print(f"{month_name:<10}: {month_hrs:>2}h{month_mins:02}m")
        print("---")
    else:
        print("Error: Not a valid date.")

@app.command()
def goal(goal: int):
    """
    Sets a daily deep work goal.
    """
    with open('status.json', 'r') as f:
        status = json.load(f)
    if "goal" in status and status["goal"] != 0:
        previous = status["goal"]
        prev_hrs = previous // 60
        prev_mins = previous % 60
        overwrite = typer.confirm(f"A goal of {prev_hrs}h{prev_mins}m has already been set. Are you sure you want to change it?")
        if not overwrite:
            print("Ok, not overwriting.")
            raise typer.Abort()

    status["goal"] = goal
    goal_hrs = goal // 60
    goal_mins = goal % 60
    with open('status.json', 'w') as f:
        json.dump(status, f)
    print(f"You set a daily goal to do {goal_hrs}h{goal_mins}m deep!")

if __name__ == "__main__":
    app()