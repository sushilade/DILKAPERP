from django.db import models


class CollegeProfile(models.Model):
    college_name = models.CharField(max_length=200)
    college_address = models.TextField()
    college_contact_number = models.CharField(max_length=20)
    expiry_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "College Profile"
        verbose_name_plural = "College Profile"

    def __str__(self):
        return self.college_name


class College(models.Model):
    college_name = models.CharField(max_length=200)
    college_address = models.TextField()
    college_contact_number = models.CharField(max_length=20)
    college_id = models.CharField(max_length=100, blank=True, null=True)
    college_password = models.CharField(max_length=100, blank=True, null=True)
    college_image = models.ImageField(upload_to='college_images/', blank=True, null=True)
    expiry_date = models.DateField()

    class Meta:
        verbose_name = "College"
        verbose_name_plural = "Colleges"

    def __str__(self):
        return self.college_name
