from django import forms
from .models import AccountSetting, RestaurantDetail,MenuCategory,MenuItem,BillingDetail
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column,Field,HTML,Div

class RestaurantForm(forms.ModelForm):
    class Meta:
        model = RestaurantDetail
        fields = ['name','gstin','desc','location','image','logo','allowCalltoWaiter','allowCustomerOrder','pickup']
    def __init__(self,*args,**kargs):
        super(RestaurantForm,self).__init__(*args,**kargs)
        self.fields['name'].label = 'Restaurant Name'
        self.fields['desc'].label = 'Restaurant Description'
        self.fields['location'].label = 'Restaurant Location'
        self.fields['image'].label = 'Restaurant Image'
        self.fields['logo'].label = 'Restaurant Logo'
        self.fields['allowCalltoWaiter'].label = 'Allow Call to Waiter'
        self.fields['allowCustomerOrder'].label = 'Allow on-table order'
        self.fields['pickup'].label = 'Store Pickup'
        self.fields['pickup'].widget.attrs['disabled'] = True

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('name'),
                    Field('desc'),
                    Field('location'),
                    css_class='col-md col-sm pr-5'
                ),
                Column(
                    HTML("""
                        {%load static%}
                        <h5 class="text-center">Change Logo</h5>
                        <div class="profile-pic mb-4">
                            <div class="img-container">
                            <label class="-label" for="id_logo">
                                <span><i class="bi bi-pencil"></i></span>
                                <span>Edit</span>
                            </label>
                            <input id="id_logo" type="file" name="logo" accept="image/*" onchange="loadLogo(event)"/>
                            {% if form.logo.value %}
                            <img src="/media/{{ MEDIA_URL }}{{ form.logo.value }}" id="output_logo" width="200" />
                            {%else%}
                            <img src="{%static 'imgs/default/default.png'%}" id="output_logo" width="200" />
                            {%endif%}
                            </div>
                        </div>
                        """, 
                        ),
                    HTML("""
                        {%load static%}
                        <h5 class="text-center">Change Cover Photo</h5>
                        <div class="background-pic mb-4">
                            <label class="-label" for="id_image">
                                <span><i class="bi bi-pencil"></i></span>
                                <span>Edit</span>
                            </label>
                            <input id="id_image" type="file" name="image" accept="image/*" onchange="loadImage(event)"/>
                            {% if form.image.value %}
                            <img src="/media/{{ MEDIA_URL }}{{ form.image.value }}" class="img-fluid" id="output_image" width="200" />
                            {%else%}
                            <img src="{%static 'imgs/default/default.png'%}" class="img-fluid" id="output_image" width="200" />
                            {%endif%}
                        </div>
                        """, 
                        ),
                    css_class='col-md col-sm pl-4'
                ),
            ),
            Div(
                Div('allowCalltoWaiter',css_class='w-100'),
                HTML("""
                   <!-- <small class="help"><i class="bi bi-question-circle-fill"></i></small>
                    <div class="help-content">
                        This is help
                    </div> -->
                    {%load static%}
                    <span class="qs"><i class="bi bi-question-circle-fill"></i>
                        <span class="popover-help shadow">
                            <p class="text-center pb-2 m-0">Allow call to waiter</p>
                            <img class="img-fluid" src="{%static 'imgs/calltowaiter.PNG'%}" />
                        </span>
                    </span>
                """),
                css_class = 'd-flex px-2'
            ),
            Div(
                Div('allowCustomerOrder',css_class='w-100'),
                HTML("""
                   <!-- <small class="help"><i class="bi bi-question-circle-fill"></i></small>
                    <div class="help-content">
                        This is help
                    </div> -->
                    {%load static%}
                    <span class="qs"><i class="bi bi-question-circle-fill"></i>
                        <span class="popover-help shadow">
                            <p class="text-center pb-2 m-0">Allow on table orders</p>
                            <img class="img-fluid" src="{%static 'imgs/placeorder.PNG'%}" />
                        </span>
                    </span>
                """),
                css_class = 'd-flex px-2'
            ),
            Field('pickup'),
            Submit('submit','Save Changes',disabled=True,css_class='btn btn-success disabled float-right mt-2')
        )

class MenuCategoryForm(forms.ModelForm):
    class Meta:
        model = MenuCategory
        fields = ['name']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name','price','desc','food_type','img','display','start_time','end_time']

class AccountSettingForm(forms.ModelForm):
    class Meta:
        model = AccountSetting
        fields = ['phone','currency_model','menu_layout','menu_language']
    def __init__(self,*args,**kargs):
        super(AccountSettingForm,self).__init__(*args,**kargs)
        self.fields['menu_layout'].widget.attrs['disabled'] = True
        self.fields['menu_language'].widget.attrs['disabled'] = True
        self.fields['currency_model'].label = 'Currency'
        self.fields['currency_model'].empty_label = None
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Column(
                Field('phone'),
                css_class = 'col-sm-6'
            ),
            Column(
                Field('currency_model'),
                css_class = 'col-sm-6'
            ),
            Column(
                Field('menu_layout'),
                css_class = 'col-sm-6'
            ),
            Column(
                Field('menu_language'),
                css_class = 'col-sm-6'
            ),
            Submit('submit','Save Changes', disabled=True,css_class='btn btn-primary disabled  mt-2')
        )

class BillingDetailForm(forms.ModelForm):
    class Meta:
        model = BillingDetail
        fields = ['name','address','gstin','city','state','zipcode','country']
    def __init__(self,*args,**kargs):
        super(BillingDetailForm,self).__init__(*args,**kargs)
        self.fields['gstin'].label = 'GSTIN or VAT'
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    Field('name'),
                    css_class='col-sm-12'
                ),
                Column(
                    Field('address'),
                    css_class='col-sm-12'
                ),
                Column(
                    Field('gstin',css_class='text-uppercase'),
                    css_class='col-sm-12'
                ),
                Column(
                    Field('city'),
                    css_class='col-sm-5'
                ),
                Column(
                    Field('state'),
                    css_class='col-sm-4'
                ),
                Column(
                    Field('zipcode'),
                    css_class='col-sm-3'
                ),
                Column(
                    Field('country'),
                    css_class='col-sm-12'
                ),
                Submit('submit','Save Changes',disabled=True,css_class='btn btn-primary disabled mt-2')
            )
        )