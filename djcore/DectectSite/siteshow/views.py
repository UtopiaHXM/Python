from django.shortcuts import render_to_response
from django.http import HttpResponse
from siteshow import models
from django.core.paginator import Paginator,InvalidPage,EmptyPage
import re
import simplejson
from django.utils.safestring import SafeString
from django import template
from django.core import serializers
from django.core.mail import send_mail, BadHeaderError
from django.template import RequestContext
from siteshow.whoisTool import crawl
from siteshow.virusAPI import apikey,analysis,reportURL
# Create your views here.
def index(request):
	return render_to_response('index.html',context_instance=RequestContext(request))
def contact(request):
	return render_to_response('contact.html',context_instance=RequestContext(request))
def staff(request):	
	return render_to_response('staff.html',context_instance=RequestContext(request))
def phish(request):
	phish_record = models.TPhish.objects.all()[0:10]
	return render_to_response('phish.html',{'phish_record':phish_record},context_instance=RequestContext(request))
def malware(request):
	mal_record = models.TMalware.objects.all()[0:10]
	return render_to_response('malware.html',{'mal_record':mal_record,},context_instance=RequestContext(request))
def zeus(request):
	zeus_record = models.TZeustracker.objects.all()[0:10]
	return render_to_response('zeus.html',{'zeus_record':zeus_record},context_instance=RequestContext(request))
def search_phish(request):
	error = False
	errors = []
	each_page = 10
	if 'search' in request.GET:
		search = request.GET['search']
		colsearch = request.GET['colsearch']
		if search:
			if colsearch == 'phish_id':
				if not re.match(r'^\d{1,}\d$',search):
					error = True
					errors.append('Please enter the correct number formation:e.g 2890114')
				else:
					phish_record = models.TPhish.objects.filter(phish_id=search)
			if colsearch == 'url':
				# search = formatURL(search)
				# print search
				phish_record = models.TPhish.objects.filter(url=search)
			if colsearch == 'online':
				if not re.match(r'yes|no',search):
					error = True
					errors.append('Please enter yes or no')
				else:
					phish_record = models.TPhish.objects.filter(online=search)
			if colsearch == 'target':
				if not re.match(r'^\D*$',search):
					error = True
					errors.append('Please enter the correct country')
				else:
					phish_record = models.TPhish.objects.filter(target=search)
		else:
			error = True
			errors.append('Enter a search item')
		if error:
			return render_to_response('search_phish.html',{'error':error,'errors':errors[0],},context_instance=RequestContext(request))
		else:
			paginator = Paginator(phish_record,each_page)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				contacts = paginator.page(page)
			except(EmptyPage,InvalidPage):
				contacts = paginator.page(paginator.num_pages) 
			condition = 'search=%s&colsearch=%s'%(search,colsearch)
			return render_to_response('search_phish.html',{'phish_record':contacts,'condition':condition,},context_instance=RequestContext(request))
	
	else:
		phish_record = models.TPhish.objects.all()
		paginator = Paginator(phish_record,each_page)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			contacts = paginator.page(page)
		except(EmptyPage,InvalidPage):
			contacts = paginator.page(paginator.num_pages)
		return render_to_response('search_phish.html',{'phish_record':contacts,},context_instance=RequestContext(request))
def search_zeus(request):
	each_page = 10
	if 'search' in request.GET:
		search = request.GET['search']
		colsearch = request.GET['colsearch']
		if search:
			if colsearch == 'URL':
				print 'URL'
				zeus_record = models.TZeustracker.objects.filter(info_type=r'ZeuS compromised URL blocklist')
			if colsearch == 'Domain':
				print 'Domain'
				zeus_record = models.TZeustracker.objects.filter(info_type=r'ZeuS domain blocklist (BadDomains)')
			if colsearch == 'Standard':
				print 'Standard'
				zeus_record = models.TZeustracker.objects.filter(info_type=r'ZeuS domain blocklist (Standard)')
			paginator = Paginator(zeus_record,each_page)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				contacts = paginator.page(page)
			except(EmptyPage,InvalidPage):
				contacts = paginator.page(paginator.num_pages) 
			condition = 'colsearch=%s&search=%s'%(colsearch,search)
			return render_to_response('search_zeus.html',{'zeus_record':contacts,'condition':condition,},context_instance=RequestContext(request))
	else:
		zeus_record = models.TZeustracker.objects.all()
		paginator = Paginator(zeus_record,each_page)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			contacts = paginator.page(page)
		except(EmptyPage,InvalidPage):
			contacts = paginator.page(paginator.num_pages)
	return render_to_response("search_zeus.html",{'zeus_record':contacts},context_instance=RequestContext(request))	
def search_malware(request):
	error = False
	errors = []
	each_page = 10
	if 'search' in request.GET:
		search = request.GET['search']
		colsearch = request.GET['colsearch']
		if search:
			if colsearch == 'domain':
				mal_record = models.TMalware.objects.filter(domain=search)
			if colsearch == 'ip':
				if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',search):
					error = True
					errors.append('Please enter correct IP')
				else:
					mal_record = models.TMalware.objects.filter(ip=search)
			if colsearch == 'country':
				if not re.match(r'^\D*$',search):
					error = True
					errors.append('Please enter the correct country')
				else:
					mal_record = models.TMalware.objects.filter(country=search)
		else:
			error = True
			errors.append('Enter a search item')
		if error:
			return render_to_response('search_malware.html',{'error':error,'errors':errors[0],},context_instance=RequestContext(request))
		else:
			paginator = Paginator(mal_record,each_page)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				contacts = paginator.page(page)
			except(EmptyPage,InvalidPage):
				contacts = paginator.page(paginator.num_pages) 
			condition = 'search=%s&colsearch=%s'%(search,colsearch)
			return render_to_response('search_malware.html',{'mal_record':contacts,'condition':condition,},context_instance=RequestContext(request))
	else:
		mal_record = models.TMalware.objects.all()
		paginator = Paginator(mal_record,each_page)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			contacts = paginator.page(page)
		except(EmptyPage,InvalidPage):
			contacts = paginator.page(paginator.num_pages)
		return render_to_response('search_malware.html',{'mal_record':contacts,},context_instance=RequestContext(request))
def download_cvs_phish(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="phish.csv"'
	phish_data = [('phish_id','url','phish_detail_url','submission_time','verified','verification_time','online','target'),]
	phish_record = models.TPhish.objects.all()
	for record in phish_record:
		temp = (record.phish_id,record.url,record.phish_detail_url,record.submission_time,record.verified,record.verification_time,record.online,record.target)
		phish_data.append(temp)
	t = template.loader.get_template('phish.txt')
	c = template.Context({'data': phish_data,})
	response.write(t.render(c))
	return response
def download_cvs_zeus(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="zeus.csv"'
	zeus_data = [('id','info_type','bad_content','description'),]
	zeus_record = models.TZeustracker.objects.all()
	for record in zeus_record:
		temp = (record.id,record.info_type,record.bad_content,record.description)
		zeus_data.append(temp)
	t = template.loader.get_template('zeus.txt')
	c = template.Context({'data': zeus_data,})
	response.write(t.render(c))
	return response
def download_cvs_malware(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename="malware.csv"'
	mal_data = [('id','date_update','domain','ip','reverse_lookup','description','registrant','asn','country'),]
	mal_record = models.TMalware.objects.all()
	for record in mal_record:
		temp = (record.id,record.date_update,record.domain,record.ip,record.reverse_lookup,record.description,record.registrant,record.asn,record.country)
		mal_data.append(temp)
	t = template.loader.get_template('malware.txt')
	c = template.Context({'data': mal_data,})
	response.write(t.render(c))
	return response
def download_cvs(request):
	return render_to_response("download_cvs.html",context_instance=RequestContext(request))
def download_txt(request):
	return render_to_response("download_txt.html",context_instance=RequestContext(request))
def download_txt_phish(request):
	response = HttpResponse(content_type='text/plain')                                   
	response['Content-Disposition'] = 'attachment; filename=phish.txt'
	response.write("(phish_id,url,phish_detail_url,submission_time,verified,verification_time,online,target)\n")
	phish_record = models.TPhish.objects.all()
	for record in phish_record:
		temp = (record.phish_id,record.url,record.phish_detail_url,record.submission_time,record.verified,record.verification_time,record.online,record.target)
		response.write(temp)
		response.write('\n')
	return response
def download_txt_zeus(request):
	response = HttpResponse(content_type='text/plain')                                   
	response['Content-Disposition'] = 'attachment; filename=zeus.txt'
	response.write("(id,info_type,bad_content,description)\n")
	zeus_record = models.TZeustracker.objects.all()
	for record in zeus_record:
		temp = (record.id,record.info_type,record.bad_content,record.description)
		response.write(temp)
		response.write('\n')
	return response
def download_txt_malware(request):
	response = HttpResponse(content_type='text/plain')                                   
	response['Content-Disposition'] = 'attachment; filename=malware.txt'
	response.write("(id,date_update,domain,ip,reverse_lookup,description,registrant,asn,country)\n")
	mal_record = models.TMalware.objects.all()
	for record in mal_record:
		temp = (record.id,record.date_update,record.domain,record.ip,record.reverse_lookup,record.description,record.registrant,record.asn,record.country)
		response.write(temp)
		response.write('\n')
	return response
def download_json(request):
	return render_to_response("download_json.html")
def download_json_phish(request):
	phish_json = serializers.serialize("json", models.TPhish.objects.all())
	response = HttpResponse(content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="phish.json"'
	response.write(phish_json)
	return response
def download_json_zeus(request):
	zeus_json = serializers.serialize("json", models.TZeustracker.objects.all())
	response = HttpResponse(content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="zeus.json"'
	response.write(zeus_json)
	return response
def download_json_malware(request):
	mal_json = serializers.serialize("json", models.TMalware.objects.all())
	response = HttpResponse(content_type="application/json")
	response['Content-Disposition'] = 'attachment; filename="malware.json"'
	response.write(mal_json)
	return response
def faq(request):
	return render_to_response("faq.html",context_instance=RequestContext(request))
def emailToServer(request):
	success = False
	error = None
	title = request.POST.get('title', '')
	email = request.POST.get('email', '')
	password = request.POST.get('password','')
	comment = request.POST.get('comment', '')
	if title and email and password and comment:
		try:
			send_mail(title, comment, email, ['3216171295@qq.com'], auth_user=email, auth_password=password,)
		except BadHeaderError:
			error = 'Invalid header found.'
			return render_to_response('contact.html',{'success':success,'error':error})
			#return HttpResponse('Invalid header found.')
		except Exception as e:
			error = str(e)
			return render_to_response('contact.html',{'success':success,'error':error})
		success = True
		return render_to_response('contact.html',{'success':success,'error':error})
	else:
		error = 'Make sure all fields are entered and valid.'
		return render_to_response('contact.html',{'success':success,'error':error})
		#return HttpResponse('Make sure all fields are entered and valid.')
def whois(request):
	if 'domainField' in request.GET:
		domainField = request.GET['domainField']
		if domainField:
			registryInfo = crawl(domainField)
			if registryInfo:
				registryInfo_json = simplejson.dumps(registryInfo)
				return render_to_response('index.html',{'registryInfo':SafeString(registryInfo_json)},context_instance=RequestContext(request))
			else:
				return render_to_response('index.html',{'noInfo':True},context_instance=RequestContext(request))
		else:
			print 'none'
			return render_to_response('index.html',{'noInfo':True},context_instance=RequestContext(request))
def virustotal(request):
	error = False
	errors = []
	each_page = 10
	if 'search' in request.GET:
		search = request.GET['search']
		colsearch = request.GET['colsearch']
		if search:
			if colsearch == 'url':
				virus_record = models.TVirusapi.objects.filter(url=search)
		else:
			error = True
			errors.append('Enter a correct url')
		if error:
			return render_to_response('virustotal.html',{'error':error,'errors':errors[0],},context_instance=RequestContext(request))
		else:
			paginator = Paginator(virus_record,each_page)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				contacts = paginator.page(page)
			except(EmptyPage,InvalidPage):
				contacts = paginator.page(paginator.num_pages) 
			condition = 'search=%s&colsearch=%s'%(search,colsearch)
			return render_to_response('virustotal.html',{'virus_record':contacts,'condition':condition,},context_instance=RequestContext(request))
	else:
		virus_record = models.TVirusapi.objects.all()
		paginator = Paginator(virus_record,each_page)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			contacts = paginator.page(page)
		except(EmptyPage,InvalidPage):
			contacts = paginator.page(paginator.num_pages)
		return render_to_response('virustotal.html',{'virus_record':contacts,},context_instance=RequestContext(request))
def safebrowsing(request):
	error = False
	errors = []
	each_page = 10
	if 'search' in request.GET:
		search = request.GET['search']
		colsearch = request.GET['colsearch']
		if search:
			if colsearch == 'url':
				google_record = models.TSafebrowsing.objects.filter(url=search)
			elif colsearch == 'type':
				if search in ['no_content','phishing','malware']:
					google_record = models.TSafebrowsing.objects.filter(type=search)
				else:
					error = True
					errors.append('enter the correct select type')
		else:
			error = True
			errors.append('select a search item')
		if error:
			return render_to_response('safebrowsing.html',{'error':error,'errors':errors[0],},context_instance=RequestContext(request))
		else:
			paginator = Paginator(google_record,each_page)
			try:
				page = int(request.GET.get('page','1'))
			except ValueError:
				page = 1
			try:
				contacts = paginator.page(page)
			except(EmptyPage,InvalidPage):
				contacts = paginator.page(paginator.num_pages) 
			condition = 'search=%s&colsearch=%s'%(search,colsearch)
			return render_to_response('safebrowsing.html',{'google_record':contacts,'condition':condition,},context_instance=RequestContext(request))
	else:
		google_record = models.TSafebrowsing.objects.all()
		paginator = Paginator(google_record,each_page)
		try:
			page = int(request.GET.get('page','1'))
		except ValueError:
			page = 1
		try:
			contacts = paginator.page(page)
		except(EmptyPage,InvalidPage):
			contacts = paginator.page(paginator.num_pages)
		return render_to_response('safebrowsing.html',{'google_record':contacts,},context_instance=RequestContext(request))
def detectOnline(request):
	if 'domainField' in request.GET:
		domainField = request.GET['domainField']
		if domainField:
			detect_info = reportURL(domainField,apikey)
			if detect_info:
				json = analysis(detect_info)
				detect_info_dict = simplejson.dumps(json)
				return render_to_response('detectOnline.html',{'detect_info_dict':SafeString(detect_info_dict)},context_instance=RequestContext(request))
			else:
				return render_to_response('detectOnline.html',{'noDetect':True},context_instance=RequestContext(request))
		else:
			print 'none'
			return render_to_response('detectOnline.html',{'noDomain':True},context_instance=RequestContext(request))
	else:
		return render_to_response('detectOnline.html',RequestContext(request))