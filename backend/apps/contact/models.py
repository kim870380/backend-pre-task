from django.db import models

class Label(models.Model):
    """
    연락처 라벨 모델
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "label"

class Contact(models.Model):
    """
    프로필 사진 URL, 이름, 이메일, 전화번호, 회사, 직책, 메모, 라벨(다대다), 주소, 생일, 웹사이트 등을 포함하는 연락처 모델
    """
    profile_url = models.URLField(blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    labels = models.ManyToManyField(Label, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "contact"