from django.db import models
from django.urls import reverse
from PIL import Image


class field_map(models.Model):
    app_class = models.CharField(max_length=200,null=False,blank=False)
    app_field = models.CharField(max_length=200,null=False,blank=False)
    map_field = models.CharField(max_length=200,null=False,blank=False)
    status = models.CharField(choices=[('A','ACTIVE'),('I','INACTIVE')],blank=False,null=False,default='INACTIVE',max_length=50) 

    
class lookups(models.Model):
    lookup_type_code = models.CharField(max_length=200)
    lookup_value_code = models.CharField(max_length=200)
    lookup_value = models.CharField(max_length=200,)
    lookup_desc = models.CharField(max_length=200,blank=True,null=True)
    lookup_order = models.IntegerField(null=True,blank=True,default=0)

    class Meta:
        ordering = ['lookup_order']

    def __str__(self):
        return self.lookup_desc


class wmobject(models.Model):
    object_id = models.CharField(primary_key=True,max_length=200)
    object_type = models.CharField(max_length=200,blank=False,null=False,default='Other')
    object_desc = models.CharField(blank=True,max_length=2000,null=True)
    object_rel = models.CharField(blank=True,max_length=200,null=True)
    object_track = models.CharField(blank=True,max_length=200,null=True)
    object_dev = models.CharField(blank=True,max_length=200,null=True)
    object_qa = models.CharField(blank=True,max_length=200,null=True)
    
    class Meta:
        ordering = ['object_rel','object_id']

    def __str__(self):
        return self.object_id + ' - ' + (self.object_desc)[0:200]

    def get_absolute_url(self):
        return reverse('object',kwargs={'release':self.object_rel,'pk':self.pk})

class wmobject_rel_notes(models.Model):
    fk_wmobject  = models.OneToOneField(wmobject,on_delete=models.CASCADE)
    app_imp = models.CharField(blank=True,max_length=2000,null=True,verbose_name="Application Impact")
    proc_imp = models.CharField(blank=True,max_length=2000,null=True,verbose_name="Process Impact")
    objective = models.CharField(blank=True,max_length=2000,null=True,verbose_name="Objective")
    resolution =  models.CharField(blank=True,max_length=2000,null=True,verbose_name="Resolution")
    img1 = models.ImageField(upload_to='Rel_Notes',null=True,blank=True)
    img2 = models.ImageField(upload_to='Rel_Notes',null=True,blank=True)
    img3 = models.ImageField(upload_to='Rel_Notes',null=True,blank=True)

    def save(self, *args, **kwargs):        
        super().save(*args, **kwargs)
        def set_size(img):        
            imag = Image.open(img)
            if imag.width > 600 or imag.height> 550:
                output_size = (600, 550)
                imag.resize(output_size)
                imag.save(img)
        if self.img1:
            set_size(self.img1.path)
        if self.img2:
            set_size(self.img2.path)
        if self.img3:
            set_size(self.img3.path)        

    def __str__(self):
        return 'Release Notes - '+str(self.fk_wmobject)

class wmobject_details(models.Model):
    fk_wmobject = models.ForeignKey(wmobject,on_delete=models.CASCADE)    
    object_type = models.ForeignKey(lookups,on_delete=models.SET_NULL,null=True)     
    object_path = models.CharField(max_length=300,blank=True)
    object_backout = models.CharField(max_length=300,blank=True)
    object_special = models.CharField(max_length=300,blank=True,null=True)
    object_comment = models.CharField(max_length=300,blank=True,null=True)

    def __str__(self):
        return str(self.object_type).strip() +' - '+ str(self.object_path).strip()

    def get_absolute_url(self):
        return reverse('object',kwargs={'release':self.fk_wmobject.object_rel,'pk':self.fk_wmobject.object_id})

class attach_lookup(models.Model):
    lookup_value = models.CharField(max_length=200,)
    lookup_desc = models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        return self.lookup_desc

class wmobject_attachments(models.Model):
    fk_wmobject  = models.ForeignKey(wmobject,on_delete=models.CASCADE)
    attach_type  = models.ForeignKey(attach_lookup,on_delete=models.SET_NULL,null=True)
    attach_file  = models.FileField(upload_to='USDE_Attach')
    

def upsert(model,data_dic,cols,pk):    
    for data in data_dic:
        if isinstance(data,dict) and len(data)>0:
            records = model.objects.filter(object_id=data[pk])
            if len(records)>0:
                for rec in records:
                    for col in cols:
                        if col in data.keys():                    
                            setattr(rec,col,data[col])                        
                    rec.save()
            else:
                new_rec = model()
                for col in cols:
                    if col in data.keys():                                
                        setattr(new_rec,col,data[col])                        
                new_rec.save()



# lst=[{'object_id': 'US54814', 'object_desc': 'BACKLOG - As an OSC', 'object_rel': 'Modernization Rel 1'}]
# upsert(wmobject,lst,'object_id')
