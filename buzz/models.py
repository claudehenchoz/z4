from django.db import models

class BuzzItem(models.Model):
    title = models.CharField(max_length=512)
    blurb = models.CharField(max_length=4096)
    content = models.CharField(max_length=65536)
    source = models.CharField(max_length=32)
    url = models.CharField(max_length=512)
    date = models.DateTimeField('date published')

    def __unicode__(self):
        return "%s: %s - %s" % (self.source, self.date.strftime("%Y-%m-%d %H:%M"), self.title)

    class Meta:
        ordering = ['-date']
