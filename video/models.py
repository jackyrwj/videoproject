import os

from django.conf import settings
from django.db import models
from django.dispatch import receiver


class VideoQuerySet(models.query.QuerySet):

    def get_count(self):
        return self.count()

    def get_published_count(self):
        return self.filter(status=0).count()

    def get_not_published_count(self):
        return self.filter(status=1).count()

    def get_published_list(self):
        return self.filter(status=0).order_by('-create_time')

    def get_search_list(self, q):
        if q:
            return self.filter(title__contains=q).order_by('-create_time')
        else:
            return self.order_by('-create_time')

    def get_recommend_list(self):
        return self.filter(status=0).order_by('-view_count')[:4]


class Classification(models.Model):
    list_display = ("title",)
    title = models.CharField(max_length=100,blank=True, null=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "v_classification"




class Video(models.Model):
    STATUS_CHOICES = (
        ('0', '发布中'),
        ('1', '未发布'),
    )
    title = models.CharField(max_length=100,blank=True, null=True)
    desc = models.CharField(max_length=255,blank=True, null=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, null=True)
    file = models.FileField(max_length=255)
    cover = models.ImageField(upload_to='cover/',blank=True, null=True)
    status = models.CharField(max_length=1 ,choices=STATUS_CHOICES, blank=True, null=True)
    view_count = models.IntegerField(default=0, blank=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   blank=True, related_name="liked_videos",through='VideoUser')
    collected = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   blank=True, related_name="collected_videos")
    create_time = models.DateTimeField(auto_now_add=True, blank=True, max_length=20)


    objects = VideoQuerySet.as_manager()
    class Meta:
        db_table = "v_video"

    def increase_view_count(self):
        self.view_count += 1
        self.save(update_fields=['view_count'])

    def add_like(self, user):
        # if user in self.liked.all():
        #     self.liked.remove(user)
        # else:
        # self.liked.add(user)

        # VideoUser.objects.create(video=self,user=user,number=3)
        vu = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first()
        if vu is None:
            VideoUser.objects.create(video=self, user=user, number=1)
        else:
            number = vu.number
            number += 1
            VideoUser.objects.filter(user_id=user.id, video_id=self.id).update(number = number)



    def count_likers(self,user):
        # return self.liked.count()
        vu = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first()
        if vu is None:
            return 0
        else:
            return VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().number

    def user_liked(self, user):
        if user in self.liked.all():
            return 0
        else:
            return 1

    def switch_collect(self, user):
        if user in self.collected.all():
            self.collected.remove(user)

        else:
            self.collected.add(user)

    def get_coupon(self, user):
        VideoUser.objects.filter(user_id=user.id, video_id=self.id).update(coupon_get=1)

    def is_get(self, user):
        return VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().coupon_get

    # def message(self, user):
    #     coupon_getd = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().coupon_get
    #     coupon_used = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().coupon_used
    #     if coupon_getd == 1:
    #         if coupon_used == 0:
    #             return "播放结束,是否购买本片(使用优惠券)"
    #         else:
    #             return "播放结束,是否购买本片"
    #     else:
    #         return "播放结束,是否购买本片"
    #
    def buy(self, user):
        coupon_getd = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().coupon_get
        coupon_used = VideoUser.objects.filter(user_id=user.id, video_id=self.id).first().coupon_used
        if coupon_getd == 1:
            if coupon_used == 0:
                VideoUser.objects.filter(user_id=user.id, video_id=self.id).update(coupon_used=1)


    def count_collecters(self):
        return self.collected.count()

    def user_collected(self, user):
        if user in self.collected.all():
            return 0
        else:
            return 1



class VideoUser(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    number = models.IntegerField(blank=True, null=True)
    coupon_get = models.BooleanField(default=False)
    coupon_used = models.BooleanField(default=False)

    class Meta:
        db_table = "video_user_relationship"

@receiver(models.signals.post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    删除FileField文件
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


