import os
from flask import Flask, jsonify
import json
import logging
from trello import TrelloClient
from google.appengine.api import memcache

api_key = os.environ['TRELLO_API_KEY']
api_secret = os.environ['TRELLO_API_SECRET']
token = os.environ['TRELLO_TOKEN']
token_secret = os.environ['TRELLO_TOKEN_SECRET']
board_name = os.environ['TRELLO_BOARD_NAME']

backlog_list = ['To Do']
release_list = ['Sprint', 'Doing', 'Test']
ready_list = ['Done']

client = TrelloClient(
	api_key=api_key, 
	api_secret=api_secret, 
	token=token, 
	token_secret=token_secret
)

app = Flask(__name__)


def get_board_by_name(name):
	boards = client.list_boards()
	for b in boards:
		if b.name == name:
			return b
	return None 


def get_list_by_name(board, name):
	lists = board.all_lists()
	for l in lists:
		if l.name == name:
			return l
	return None


def get_all_cards(list_name):
	board = get_board_by_name(board_name)
	list = get_list_by_name(board, list_name)
	cards = list.list_cards()
	cards_list = []
	for c in cards:
		cards_list.append({ 'name': c.name, 'description': c.description })
	return cards_list


@app.errorhandler(404)
def page_not_found(e):
	"""Return a custom 404 error."""
	return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def page_not_found(e):
	"""Return a custom 500 error."""
	return 'Sorry, unexpected error: {}'.format(e), 500


@app.route("/_ah/warmup")
def warmup():
	return ''


@app.route("/api/v1/backlog")
def get_backlog_cards():
	"""Return a friendly HTTP greeting."""
	backlog = memcache.get('backlog:cards')
	if backlog is None:
		backlog = []
		for l in backlog_list:
			backlog.extend(get_all_cards(l))
		if not memcache.add('backlog:cards', backlog, 3600):
			logging.error('Memcache set failed.')
	return jsonify(backlog=backlog)


@app.route("/api/v1/release")
def get_release_cards():
	"""Return a friendly HTTP greeting."""
	release = memcache.get('release:cards')
	if release is None:
		release = []
		for l in release_list:
			release.extend(get_all_cards(l))
		if not memcache.add('release:cards', release, 3600):
			logging.error('Memcache set failed.')
	return jsonify(release=release)


@app.route("/api/v1/ready")
def get_ready_cards():
	"""Return a friendly HTTP greeting."""
	ready = memcache.get('ready:cards')
	if ready is None:
		ready = []
		for l in ready_list:
			ready.extend(get_all_cards(l))
		if not memcache.add('ready:cards', ready, 3600):
			logging.error('Memcache set failed.')
	return jsonify(ready=ready)