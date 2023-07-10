import json
from flask import Flask, render_template, request, redirect, flash, url_for, abort
import datetime


def loadClubs():
    with open('clubs.json') as c:
        list_of_clubs = json.load(c)['clubs']
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as comps:
        list_of_competitions = json.load(comps)['competitions']
        return list_of_competitions


def check_competition_date(date):
    converted_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    now = datetime.datetime.now()
    return converted_date > now


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except Exception as e:
        print(e)
        abort(400, description="Sorry, that email was not found.")
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        if check_competition_date(foundCompetition["date"]):
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("You can't book a previous competition")
            return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])

    if placesRequired > int(club["points"]):
        abort(400, description="Sorry, you're not allowed to use unavalaible points.")
    elif placesRequired > 12:
        abort(400, description="Sorry, you can't buy more than 12 places per competitions.")
    elif placesRequired > int(competition['numberOfPlaces']):
        abort(400, description="Sorry, you can't buy more than places avalaible in this competition.")
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    club["points"] = int(club["points"]) - placesRequired

    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/pointsBoard')
def pointsBoard():
    return render_template('board.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
