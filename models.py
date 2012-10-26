# -*- coding: utf-8 -*-
from mongoengine import *

from flask.ext.mongoengine.wtf import model_form
from datetime import datetime


class Comment(EmbeddedDocument):
	name = StringField(required=False)
	comment = StringField()
	timestamp = DateTimeField(default=datetime.now())

class Course(Document):

	title = StringField(max_length=120, required=True, verbose_name="Class name")
	description = StringField()
	slug = StringField()
	instructor = StringField(required=True)
	semester = StringField()
	year = StringField()
	categories = ListField( StringField() )
	units = IntField()
	# rating

	# Comments is a list of Document type 'Comments' defined above
	comments = ListField( EmbeddedDocumentField(Comment) )


CourseForm = model_form(Course)

	

