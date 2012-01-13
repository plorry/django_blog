# Create your views here.
from models import Blog, Comment
from gallery.models import Gallery
from calendar.models import Calendar
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from forms import Comment_Form
import datetime
from django.template import RequestContext

def blog_default(request):
	response_dict = {}
	calendar = Calendar.objects.get(id=1)
	today = datetime.date.today()
	calendar_table = calendar.month_as_table(today.year, today.month)
	blogs = Blog.objects.all().order_by('-creation_date')[0:5]
	title = "Blog Title"
	response_dict.update({'blogs':blogs, 'title':title, 'calendar':calendar_table})
	return render_to_response('blog_view.html',
		response_dict,
		context_instance=RequestContext(request))

def blog_single(request, blog_id):
	response_dict = {}
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

def month_view(request, year, month):
	response_dict = {}
	blogs = Blog.objects.filter(
		creation_date__year = year,
		creation_date__month = month)
	title = "Blog"
	response_dict.update({ 'blogs':blogs, 'title':title })
	return render_to_response('blog_view.html',
		response_dict)