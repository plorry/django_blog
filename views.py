# Create your views here.
from models import Blog, Comment, Blog_Site
from gallery.models import Gallery
from calendar.models import Calendar
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import Comment_Form
import datetime
from django.template import RequestContext

BLOG_TITLE = "blog title"
blog_site = Blog_Site.objects.get(id=1)

def blog_view(request, year=0,month=0,day=0):
	response_dict = {}
	today = datetime.date.today()
	if not year: year = today.year
	if not month: month = today.month
	if not day: day = 0
	calendar_table = blog_site.month_as_table(int(year), int(month))

	if day == 0:
		blogs = Blog.objects.filter(
			creation_date__month = month,
			creation_date__year = year
			).order_by('-creation_date')
	else:
		blogs = Blog.objects.filter(
			creation_date__day = day,
			creation_date__month= month,
			creation_date__year = year
			).order_by('-creation_date')
	title = BLOG_TITLE
	response_dict.update({'blogs':blogs, 'title':title, 'calendar':calendar_table})
	return render_to_response('blog_view.html',
		response_dict,
		context_instance=RequestContext(request))

def blog_single(request, blog_id):
	response_dict = {}
	today = datetime.date.today()
	calendar_table = blog_site.month_as_table(today.year, today.month)
	response_dict.update({'calendar':calendar_table})
	comment = ''
	blog = Blog.objects.get(id=blog_id)
	title = blog.title

	if request.method == 'POST':
		post = request.POST
		comment_form = Comment_Form(post)
		if comment_form.is_valid():
			cd = comment_form.cleaned_data
			author = cd['author']
			body = cd['body']
			email = cd['email']
			comment = Comment.objects.create(
				author = author,
				body = body,
				email = email,
				creation_date = datetime.datetime.now())
			blog.comments.add(comment)
			blog.save()
		response_dict.update({ 'blog':blog, 'title':title, 'form':comment_form })
		return HttpResponseRedirect('/blog/blog_id/' + str(blog.id))
	else:
		comment_form = Comment_Form()
		response_dict.update({ 'blog':blog, 'title':title, 'form':comment_form })
	return render_to_response('blog_single.html',
		response_dict,
		context_instance=RequestContext(request))