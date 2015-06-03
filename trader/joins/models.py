from django.db import models


class Join(models.Model):
    email = models.EmailField()
    friend = models.ForeignKey("self", related_name='referral', null=True, blank=True)
    ref_id = models.CharField(max_length=123, default='ABC', unique=True)
    ip_address = models.CharField(max_length=123, default='ABC')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return self.email

    class Meta:
        unique_together = ("email", "ref_id",)
