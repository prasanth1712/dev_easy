from django import forms
import pandas as pd
class fileupload(forms.Form):
    file = forms.FileField(required=False)


def load_file(model,cols,file):
    data = pd.read_excel(file)
    col_len = len(data.columns)
    data.columns = cols[:col_len]
    #print('2')
    data = data.to_dict('records')
    return data