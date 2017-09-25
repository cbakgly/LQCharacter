# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.template import defaultfilters


import uuid
from oss import get_oss_by_name
# [Django API](https://docs.djangoproject.com/en/1.11/)
# [Django中null和blank的区别](http://www.tuicool.com/articles/2ABJbmj)


class UsableStatus(object):
    UNUSABLE = 0
    USABLE = 1
    DELETED = 99
    STATUS = (
        (UNUSABLE, u'不可用'),
        (USABLE, u'启用'),
        (DELETED, u'删除'),
    )


class ORGGroup(object):
    ALI = 0
    BAIDU = 1
    SKY = 2
    IDS = (
        (ALI, u'阿里'),
        (BAIDU, u'百度'),
        (SKY, u'社科院'),
    )


class FinalStatus(object):
    INIT = 0
    FIRSTCHECK = 1
    TWICECHECK = 2
    STATUS = (
        (INIT, u'新入库'),
        (FIRSTCHECK, u'已初校'),
        (TWICECHECK, u'已二校'),
    )


class BatchVersion(models.Model, UsableStatus, ORGGroup):
    class Meta:
        verbose_name = '版本批次'
        verbose_name_plural = u"版本批次管理"
        ordering = ('-submit_date', )

    class Config:
        list_display_fields = ('id', 'organiztion', 'submit_date', 'des', 'accepted', 'upload_field')
        list_form_fields = list_display_fields
        search_fields = list_display_fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    organiztion = models.PositiveSmallIntegerField(verbose_name=u'组织名称', choices=ORGGroup.IDS,
            default=ORGGroup.ALI)
    submit_date = models.DateTimeField(null=True, blank=True, verbose_name=u'提交日期', auto_now_add = True)
    des = models.TextField(verbose_name=u'描述', null=True, blank=True, max_length= 128)
    accepted = models.PositiveSmallIntegerField(u'状态', choices=UsableStatus.STATUS,
            default=UsableStatus.UNUSABLE, db_index=True)
    upload_field = models.FileField(null=True, blank=True, upload_to="", verbose_name="zip文件")


    def __str__(self):
        return '%s: %s' % (ORGGroup.IDS[int(self.organiztion)][1],
                           defaultfilters.date(self.submit_date, "SHORT_DATE_FORMAT"))


class OPage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=128, blank=True, null=True)
    final = models.BooleanField(default=False)
    md5 = models.CharField(max_length=128, db_index=True)

    def __str__(self):
        return self.name


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_version = models.ForeignKey(BatchVersion, blank=True, null=True, on_delete=models.CASCADE,
                                      related_name="page_batchversion")
    image = models.ForeignKey(OPage)
    final = models.SmallIntegerField(verbose_name='校对情况', choices=FinalStatus.STATUS, default=0)
    created_at = models.DateTimeField(u'创建于', null=True, blank=True, auto_now_add=True)
    updated_at = models.DateTimeField(u'更新于', null=True, blank=True, auto_now=True)

    class Meta:
        verbose_name = '页'
        verbose_name_plural = u"页面管理"
        ordering = ('-created_at', )

    class Config:
        list_display_fields = ('id', 'batch_version', 'created_at', 'image', 'final')
        list_form_fields = list_display_fields
        search_fields = list_display_fields

    @property
    def image_name(self):
        return self.image.name

    @property
    def image_md5(self):
        return self.image.md5

    @property
    def get_image_url(self):
        # return os.path.join(settings.IMAGE_ROOT, self.image.name)
        return "http://tripitaka.oss-cn-shanghai.aliyuncs.com/" + get_oss_by_name(self.image.name)

    @property
    def get_page_url(self):
        return "http://127.0.0.1:8000/" + str(self.id)

    def __str__(self):
        return self.image_name


class CutBatchOP(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    page = models.ForeignKey(Page, blank=True, null=True, on_delete=models.CASCADE, related_name="c_page")
    cut_data = models.TextField(blank=True, null=True)
    submit_date = models.DateTimeField(null=True, blank=True, verbose_name=u'提交日期', auto_now = True)

    def __str__(self):
        return '%s: %s' % (self.id, self.cut_data)
