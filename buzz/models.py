from django.db import models
from datetime import datetime, timedelta

class BuzzItem(models.Model):
    title = models.CharField(max_length=512)
    blurb = models.CharField(max_length=4096)
    content = models.CharField(max_length=65536)
    source = models.CharField(max_length=32)
    url = models.CharField(max_length=512,unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "%s: %s - %s" % (self.source, self.date.strftime("%Y-%m-%d %H:%M"), self.title)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs):
        time_threshold = datetime.now() - timedelta(days=3)
        BuzzItem.objects.filter(date__lt=time_threshold).delete() # remove old stuff
        super(BuzzItem, self).save(*args, **kwargs)
