from django.db import models

# Model for ExamQuestion
class Question(models.Model):

    MATHS_SUBJECT_CHOICES = (
        ('1', 'General Mathematics'),
        ('2', 'Mathematics'),
        ('3', 'Extension Maths 1'),
        ('4', 'Extension Maths 2'),
    )

    question_img = models.ImageField(upload_to='questions')
    num = models.IntegerField() #This depends, for 2U it is 10 Question, for Extension1 7 Questions.
    topic = models.CharField(max_length=200) # THIS SHOULD BE CHOICE OUT OF POSSIBLE TOPICS IF 2U/3U etc.
    mark = models.IntegerField()
    subject = models.CharField(max_length=1, choices=MATHS_SUBJECT_CHOICES)
    source = models.CharField(max_length=200, blank=True) #From where it is sourced from e.g. HSC, CSSA, Trial Paper
    pub_date = models.DateField(blank=True) #The date this paper was published e.g. 01/01/2001
    
    def __unicode__(self):
        return 'Question: %s %s %s %s' % (self.num, self.pub_date, self.source,
                self.topic)

    class Meta:
        ordering = ['pub_date', 'num']

# Model for ExamAnswer
class Answer(models.Model):

    question = models.OneToOneField('Question')
    answer_img = models.ImageField(upload_to='answers')
    
    def __unicode__(self):
        return 'Question: %s' % (self.answer_img)

    class Meta:
        ordering = ['answer_img']
