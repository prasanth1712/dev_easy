from django.shortcuts import render,reverse,HttpResponseRedirect
from django.views.generic import  FormView,ListView,DetailView,UpdateView
from django.views import View
from app.forms.form_fileupload import fileupload,load_file,PullJiraProject
from app import forms_test as frm
from django.http import request,HttpResponse
from app.models.objectmodel import wmobject,upsert,wmobject_details,wmobject_attachments,wmobject_rel_notes,lookups
from django import forms
from django.db.models import Count
from django.db.models.functions import Substr
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from app.jira_api import get_objects


#pr code
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        #result = finders.find(uri)
        result = None
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:   
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path


def render_pdf_view(request,*args,**kwargs):
    
    if 'release' in kwargs.keys():
        template_path = 'rel_notes_print.html'
        obj = rel_notes_listview(kwargs={'release':kwargs['release']})
        rows = obj.get_queryset()
        context = obj.get_context_data(object_list=rows)
    if 'release_plan' in kwargs.keys():
        template_path = 'imp_plan_print.html'
        obj = imp_plan(kwargs={'release':kwargs['release_plan']})
        rows = obj.get_queryset()
        context = obj.get_context_data(object_list=rows)


    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)
    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

#pr code




# Create your views here.



def my_test_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse(request)
    else:
        pass
        #return HttpResponse('Invalid User')

@login_required(login_url='/accounts/login/')
def test_view(request):
    return HttpResponse('This is authentication')

class upload_view(FormView):
    template_name = 'upload.html'
    form_class = fileupload
    success_url = '/sucess/'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            cols = ['object_id','object_desc','object_rel','object_sprint','object_dev']      
            data=load_file(wmobject,cols,request.FILES['file'])
            print(data)
            upsert(wmobject,data,cols,'object_id')
            return render(request, self.template_name,{'message':'Upload successful'})
        else:
            return render(request, self.template_name,{})


class jira_load_view(LoginRequiredMixin,FormView):
    template_name = 'jira_load.html'
    form_class = PullJiraProject
    success_url = '/sucess/'

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            prjt = str(request.POST['project_name']).strip()
            fixver = str(request.POST['fix_version']).strip()
            data = get_objects(project=prjt,fixver=fixver)
            cols = ['object_id','object_desc','object_rel','object_sprint','object_dev']
            print(data)
            upsert(wmobject,data,cols,'object_id')
            return render(request, self.template_name,{'message':'Upload successful'})
        else:
            return render(request, self.template_name,{})

class ReleaseListView(LoginRequiredMixin,ListView):
    login_url ='login'
    context_object_name ='release_list'
    queryset = wmobject.objects.all().values('object_rel').order_by('object_rel').distinct()
    template_name = 'release_list.html'

class ReleaseObjectListView(LoginRequiredMixin,ListView): 
    login_url ='login'    
    context_object_name ='release_objects'
    template_name = 'release_objects.html'
    
    def get_queryset(self):
        return wmobject.objects.filter(object_rel=self.kwargs['release'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'Rel':self.kwargs['release']})
        return context

class ReleaseObjectDetailView(LoginRequiredMixin,DetailView):
    login_url ='login'
    context_object_name='object'
    template_name = 'object_detail.html'
    
    def get_queryset(self):
        return wmobject.objects.filter(object_rel=self.kwargs['release'],
                                        object_id=self.kwargs['pk'])
    
    def get_context_data(self,**kwargs):
        p = wmobject_details.objects.select_related('object_type','fk_wmobject').filter(fk_wmobject__object_rel=self.kwargs['release'])
        p = p.filter(fk_wmobject__object_id=self.kwargs['pk'])
        res = p.values('object_type__lookup_desc').annotate(cnt=Count('object_type__lookup_desc'))
        attach = wmobject_attachments.objects.filter(fk_wmobject__object_id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context.update({'dtls':wmobject_details.objects.filter(fk_wmobject=self.kwargs['pk']),'res':res,'attach':attach})
        return context

class rel_overview(LoginRequiredMixin,View):
    login_url ='login'
    def get(self,request,*args,**kwargs):
        p = wmobject_details.objects.select_related('object_type','fk_wmobject').filter(fk_wmobject__object_rel=kwargs['release'])
        res = p.values('object_type__lookup_desc').annotate(cnt=Count('object_type__lookup_desc',distinct=True),tot=Count('object_type__lookup_desc')).order_by('object_type__lookup_order')
        objs = p.values('object_type__lookup_desc','object_path').annotate(cnt=Count('object_path')).order_by('object_type__lookup_order')
        #objs = p.values('object_type__lookup_desc','object_path').order_by('object_type__lookup_order')
        p1 = p.annotate(typ=Substr('fk_wmobject__object_id',1,2))
        usde = p1.values('typ').annotate(cnt=Count('typ'))
        merg_objs = objs.filter(cnt__gt=1).aggregate(Count('cnt'))
        return render(request,'release_overview.html',{'rel':kwargs['release'],'res':res,'objs':objs,'usde':usde,'merg':merg_objs})


    def post(self,request,*args,**kwargs):
        return render(request,'release_overview.html',{'rel':kwargs['release']})

class wmobject_attach_update(LoginRequiredMixin,View):
    login_url='login'
    frm_set = forms.modelformset_factory(wmobject_attachments,can_order=True,can_delete=True,fields=['attach_type','attach_file'])
    def get(self,request,*args,**kwargs):
        obj = wmobject.objects.get(pk=kwargs['pk'])       
        frm_set = self.frm_set(queryset= wmobject_attachments.objects.filter(fk_wmobject__object_id=kwargs['pk']))
        return render(request,'wmobject_attach.html',{'formset':frm_set,'obj':obj})

    def post(self,request,*args,**kwargs):
        frm_set = self.frm_set(request.POST,request.FILES)        
        data = wmobject.objects.get(pk=kwargs['pk'])

        if frm_set.is_valid():
            instances = frm_set.save(commit=False)
            for obj in frm_set.deleted_objects:
                obj.delete()
            for inst in instances:
                inst.fk_wmobject=data
                inst.save()
            frm_set = self.frm_set(queryset= wmobject_attachments.objects.filter(fk_wmobject__object_id=kwargs['pk']))
            return render(request,'wmobject_attach.html',{'formset':frm_set,'obj':data})
        else:
            return render(request,'wmobject_attach.html',{'formset':frm_set,'obj':data})

class wmobject_detail_update(LoginRequiredMixin,View):
    login_url ='login'
    frm_set = forms.modelformset_factory(wmobject_details,form=frm.wmobject_details_form,can_order=True,can_delete=True)
    
    def get(self,request,*args,**kwargs):
        obj = wmobject.objects.get(pk=kwargs['pk'])
        frm_set = self.frm_set(queryset= wmobject_details.objects.filter(fk_wmobject=kwargs['pk']))
        return render(request,'wmobject_update.html',{'formset':frm_set,'obj':obj})

    def post(self,request,*args,**kwargs):
        frm_set = self.frm_set(request.POST)

        if frm_set.is_valid():
            instances = frm_set.save(commit=False)        
            data = wmobject.objects.get(pk=kwargs['pk'])

            for obj in frm_set.deleted_objects:
                obj.delete()

            for inst in instances:
                inst.fk_wmobject=data
                inst.save()
            frm_set = self.frm_set(queryset= wmobject_details.objects.filter(fk_wmobject=kwargs['pk']))
            return render(request,'wmobject_update.html',{'formset':frm_set,'obj':data})
        else:
            print(frm_set.errors)
            print(frm_set.non_form_errors())
            return render(request,'wmobject_update.html',{'formset':frm_set,'obj':data})

class rel_notes_view(LoginRequiredMixin,View):
    login_url='login'    
    frm_set = forms.modelform_factory(wmobject_rel_notes,form=frm.rel_notes_form)

    def get(self,request,*args,**kwargs):
        obj  = wmobject.objects.get(object_id=kwargs['pk'])
        inst = wmobject_rel_notes.objects.filter(fk_wmobject__object_id=kwargs['pk'])
        if len(inst)>0:
            frm_set = self.frm_set(instance=inst[0])
            return render(request,'wmobject_rel_notes.html',{'formset':frm_set,'obj':obj,'prev':inst[0]})
        else:    
            frm_set = self.frm_set()
            return render(request,'wmobject_rel_notes.html',{'formset':frm_set,'obj':obj})
    
    def post(self,request,*args,**kwargs):
        obj  = wmobject.objects.get(object_id=kwargs['pk'])
        inst = wmobject_rel_notes.objects.filter(fk_wmobject__object_id=kwargs['pk'])
        if len(inst)>0:
            frm_set = self.frm_set(request.POST,request.FILES,instance=inst[0])
        else:
            frm_set = self.frm_set(request.POST,request.FILES)

        if frm_set.is_valid():
            frm_inst = frm_set.save(commit=False)
            frm_inst.fk_wmobject = obj
            frm_inst.save() 
        
        inst = wmobject_rel_notes.objects.filter(fk_wmobject__object_id=kwargs['pk'])

        return HttpResponseRedirect(reverse('app:rel_notes',kwargs={'release':kwargs['release'],'pk':kwargs['pk']}))

class rel_notes_listview(LoginRequiredMixin,ListView):
    template_name = 'rel_notes.html'
    login_url='login'
    context_object_name='release_objects'
     
    def get_queryset(self,**kwargs):
        return wmobject_rel_notes.objects.select_related('fk_wmobject').filter(fk_wmobject__object_rel=self.kwargs['release'])

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)                   
        context.update({'Rel':self.kwargs['release']})
        return context


class imp_plan(LoginRequiredMixin,ListView):
    template_name='imp_plan.html'
    login_url = 'login' 

    def get_queryset(self):
        return lookups.objects.all()

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)        
        lkps = lookups.objects.all()
        rel_objs = wmobject_details.objects.select_related('object_type','fk_wmobject').filter(fk_wmobject__object_rel=self.kwargs['release'])
        con_dic ={}
        tmp_dic = {}
        for lkp in lkps:
            con_dic[lkp.lookup_desc]= rel_objs.filter(object_type__lookup_desc=lkp.lookup_desc)
            
        context.update({'cont':con_dic,'Rel':self.kwargs['release']})
        return context

@login_required(login_url='/accounts/login/')
def update_item(request,release,pk):
    cols = ['object_id','object_desc','object_rel','object_dev','object_type','object_track','object_qa']      
    data = get_objects('Q2C1',obj_id=pk)
    upsert(wmobject,data,cols,'object_id')
    return HttpResponseRedirect(reverse('app:object',kwargs={'release':release,'pk':pk}))


@login_required(login_url='/accounts/login/')
def update_release_items(request,release):
    cols = ['object_id','object_desc','object_rel','object_dev','object_type','object_track','object_qa']  
    prjs = ['QCAR','QCOM','QCCR','Q2CO','Q2C1']
    for prj in prjs:    
        data = get_objects(prj,fixver=release)
        print(len(data))
        upsert(wmobject,data,cols,'object_id')
    return HttpResponseRedirect(reverse('app:release_objects',kwargs={'release':release}))