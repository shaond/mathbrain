from django.db import models

# Model for Registration
class Registration(models.Model):
    email = models.CharField(max_length=200)
    received_date = models.DateField(auto_now_add=True)
    
    def __unicode__(self):
        return 'Registration: %s %s' % (self.email, self.received_date)

    class Meta:
        ordering = ['email', 'received_date']
