from django.db import models
from django.contrib.auth.models import User
import datetime
from gallery.models import Gallery
import calendar_functions

class Blog_Site(models.Model):
	title = models.CharField(max_length = 50)
	
	def month_as_table(self, year, month):
		events = self.blog_set.filter(creation_date__year=year, creation_date__month=month)
		month_name = calendar_functions.month_name(month)
		days_in_month = calendar_functions.days_in_month(month, year)
		first_of_month = datetime.date(year, month, 1)
		buffer_days = first_of_month.isoweekday()
		if buffer_days == 7:
			buffer_days = 0
		today = datetime.date.today()
		next_year = year
		last_year = year
		last_month = month - 1
		if last_month == 0:
			last_month = 12
			last_year -= 1
		next_month = month + 1
		if next_month == 13:
			next_month = 1
			next_year += 1

		month_html = ("<caption>\
			<a href = \"/blog/%d/%02d/\"> < </a>\
			<em><a href=\"/blog/%d/%02d\">%s</a> | %s</em>\
			<a href = \"/blog/%d/%02d/\"> > </a>\
			</caption>\n\
			<tr><th>Sun</th><th>Mon</th><th>Tue</th>\
			<th>Wed</th><th>Thu</th><th>Fri</th>\
			<th>Sat</th></tr>\n<tr>" % (last_year, last_month, year, month, month_name, year, next_year, next_month))
		for day in range(0,buffer_days):
			month_html += ("<td class = \"buffer\"></td>")
		day_of_week = buffer_days
		for day in range(1,days_in_month+1):
			this_day = datetime.date(year, month, day)
			try:
				todays_events = Blog.objects.filter(creation_date__year = year, creation_date__month = month, creation_date__day = day)
			except:
				todays_events = []
			#What kind of day is it? Today, event day, or empty day?
			if this_day == today:
				month_html += ("<td class = \"today\">")
			elif todays_events:
				month_html += ("<td class = \"event_day\">")
			else:
				month_html += ("<td class = \"empty_day\">")
			#Next we create a link for a day's blog entries, unless there are none
			if todays_events:
				month_html += ("<a class = \"day_link\" href = \"/blog/" +str(year) +
				"/%02d/%02d\">" + str(day) + "</a>") % (month, day,)
			else:
				month_html += ("<span class =\"date\">" + str(day) +
					"</span>")
			month_html += ("</td>")
			day_of_week += 1
			if day_of_week == 7 and day < days_in_month:
				day_of_week = 0
				month_html += ("</tr><tr>")
			
		return month_html


class Blog(models.Model):
	author = models.ForeignKey(User)
	title = models.CharField(max_length = 50)
	body = models.TextField(max_length = None)
	blog = models.ForeignKey(Blog_Site)
	#tags = models.ManyToManyField('Tag', blank=True, null=True)
	creation_date = models.DateTimeField(auto_now_add = True)
	modified = models.DateTimeField(auto_now = True, blank = True, null = True)
	gallery = models.ForeignKey(Gallery, blank = True, null = True)
	comments = models.ManyToManyField('Comment', blank = True, null = True)
	published = models.BooleanField(default = False)
	def save(self, *args, **kwargs):
		if not self.id:
			self.creation_date = datetime.datetime.today()
		self.modified = datetime.datetime.today()
		super(Blog, self).save(*args, **kwargs)
	
	def __unicode__(self):
		return self.title
	
class Comment(models.Model):
	author = models.CharField(max_length = 50)
	email = models.EmailField(blank = True, null = True)
	creation_date = models.DateTimeField(auto_now_add = True)
	body = models.TextField(max_length = None)