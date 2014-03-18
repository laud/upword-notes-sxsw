__author__ = 'dlau'

from storages.backends.s3boto import S3BotoStorage
from django.conf import settings

StaticS3BotoStorage = lambda: S3BotoStorage(location='static',
                                            acl='public-read',
                                            querystring_auth=False,
                                            secure_urls=False,
                                            custom_domain=settings.CLOUDFRONT_DOMAIN)
MediaS3BotoStorage = lambda: S3BotoStorage(location='media',
                                           acl='public-read',
                                           querystring_auth=False,
                                           secure_urls=False,
                                           custom_domain=settings.CLOUDFRONT_DOMAIN)