
# -*- coding: utf-8 -*-

import os, datetime
import re
from unidecode import unidecode

from flask import Flask, request, render_template, redirect, abort

# import all of mongoengine
# from mongoengine import *
from flask.ext.mongoengine import mongoengine

# import data models
import models

app = Flask(__name__)   # create our flask app
app.config['CSRF_ENABLED'] = False

# --------- Database Connection ---------
# MongoDB connection to MongoLab's database
mongoengine.connect('mydata', host=os.environ.get('MONGOLAB_URI'))
app.logger.debug("Connecting to MongoLabs")


categories = ['web','physical computing','programming','video','music','installation','social media','developing nations','business','networks', 'fabrication', 'theory', 'art']

# --------- Routes ----------

@app.route("/", methods=['GET','POST'])

	return render_template('input.html')

# this is our main page
@app.route("/input", methods=['GET','POST'])
def input():

	app.logger.debug(request.form.getlist('categories'))

	# get Idea form from models.py
	course_form = models.CourseForm(request.form)
	
	request.method == "POST" and course_form.validate()
	
	# get form data - create new idea
	course = models.Course()
	course.title = request.form.get('title')
	course.slug = slugify(course.title)
	course.description = request.form.get('description','')
	course.instructor = request.form.get('instructor')
	course.semester = request.form.get('semester')
	course.year = request.form.get('year')
	course.categories = request.form.getlist('categories')
	course.units = request.form.get('units')
	
	course.save()

	return redirect('/courses/%s' % course.slug)


@app.route("/category/<cat_name>")
def by_category(cat_name):

	try:
		ideas = models.Idea.objects(categories=cat_name)
	except:
		abort(404)

	templateData = {
		'current_category' : {
			'slug' : cat_name,
			'name' : cat_name.replace('_',' ')
		},
		'ideas' : ideas,
		'categories' : categories
	}

	return render_template('category_listing.html', **templateData)




@app.route("/courses/<course_slug>")
def course_display(course_slug):

	# get idea by idea_slug
	try:
		course = models.Course.objects.get(slug=course_slug)
	except:
		abort(404)

	# prepare template data
	templateData = {
		'course' : course
	}

	# render and return the template
	return render_template('idea_entry.html', **templateData)
	



@app.route("/ideas/<idea_id>/comment", methods=['POST'])
def idea_comment(idea_id):

	name = request.form.get('name')
	comment = request.form.get('comment')

	if name == '' or comment == '':
		# no name or comment, return to page
		return redirect(request.referrer)


	#get the idea by id
	try:
		idea = models.Idea.objects.get(id=idea_id)
	except:
		# error, return to where you came from
		return redirect(request.referrer)


	# create comment
	comment = models.Comment()
	comment.name = request.form.get('name')
	comment.comment = request.form.get('comment')
	
	# append comment to idea
	idea.comments.append(comment)

	# save it
	idea.save()

	return redirect('/ideas/%s' % idea.slug)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


# slugify the title 
# via http://flask.pocoo.org/snippets/5/
_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')
def slugify(text, delim=u'-'):
	"""Generates an ASCII-only slug."""
	result = []
	for word in _punct_re.split(text.lower()):
		result.extend(unidecode(word).split())
	return unicode(delim.join(result))


# --------- Server On ----------
# start the webserver
if __name__ == "__main__":
	app.debug = True
	
	port = int(os.environ.get('PORT', 5000)) # locally PORT 5000, Heroku will assign its own port
	app.run(host='0.0.0.0', port=port)



	