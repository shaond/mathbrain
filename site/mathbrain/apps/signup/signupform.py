from pinax.apps.account.forms import SignupForm as BaseSignupForm 

class SignupForm(BaseSignupForm): 
    def __init__(self, *args, **kwargs): 
        super(SignupForm, self).__init__(*args, **kwargs) 
        # remove the username field from fields 
        del self.fields["username"]
        del self.fields["password1"]
        del self.fields["password2"]
        # re-order the fields where email comes first 
        self.fields.keyOrder = [ 
            "email", 
            #"password1",
            #"password2",
            "confirmation_key", 
        ] 
    def create_user(self, username=None, commit=True): 
        # pass in empty username which requires a migration of auth_user table 
        user = super(SignupForm, self).create_user(username="", commit=False) 
        if commit: 
            user.save() 
        return user 
