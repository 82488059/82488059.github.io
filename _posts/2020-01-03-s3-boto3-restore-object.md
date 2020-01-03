---
layout: post
title:  "使用Python还原s3的GLACIER对象"
categories: aws
tags: aws
author: flame
description: 使用Python还原s3的GLACIER对象
---

### 使用Python还原s3的GLACIER对象的代码

注意：发起还原之前要先检查是不是有正在进行的还原任务，或者有已经还原的临时对象。

以下是发起任务后调用head-object返回的json。 
```json
{
    "AcceptRanges": "bytes",
    "Restore": "ongoing-request=\"true\"",
    "LastModified": "Tue, 26 Nov 2019 08:26:24 GMT",
    "ContentLength": 735,
    "ETag": "\"1e0284fa4441896a4a267777caef067a\"",
    "ContentType": "text/plain",
    "Metadata": {},
    "StorageClass": "GLACIER"
}
```
`"Restore"`表示有正还原的任务或者存在已经还原的临时对象。值`"ongoing-request=\"true\""`表示正在还原对象，当值为`"ongoing-request=\"false\", expiry-date=\"Sun, 05 Jan 2020 00:00:00 GMT\""`时表示对象已经还原成功，持续时间到`05 Jan 2020 00:00:00 GMT`。


### 测试脚本 

```py
#!/usr/bin/ python3
# -*- coding: utf-8 -*-
import logging
import boto3
from botocore.exceptions import ClientError
import sys
import os
import time
import botocore


BUCKET_NAME=""
OBJECT_NAME=""


# 发起还原 bucket_name桶名 object_name对象名
# days还原出来的临时对象有效天数，到期后自动删除，不包括还原出来当天。
def restore_object(bucket_name, object_name, days, retrieval_type='Standard'):
    request = {'Days': days,
               'GlacierJobParameters': {'Tier': retrieval_type}}
    s3 = boto3.client('s3')
    try:
        s3.restore_object(Bucket=bucket_name, Key=object_name, RestoreRequest=request)
    except ClientError as e:
        logging.error(e)
        logging.error(f"NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's, storage class was not GLACIER. {bucket_name} {object_name} ")

        return False
    return True


# 查看对象 bucket_name桶名 object_name对象名
def head_object(bucket_name, object_name):
    s3 = boto3.client('s3')
    response = None
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        logging.error(e)
        logging.error(f"NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's, storage class was not GLACIER. {bucket_name} {object_name} ")
        return None
    return response


# 测试restore_object
def test_restore_object():
    test_bucket_name = BUCKET_NAME
    test_object_name = OBJECT_NAME
    # Expedited 快速还原 
    days = 1  # 还原出来的临时对象有效天数，到期后自动删除，不包括还原出来当天。
    success = restore_object(test_bucket_name, test_object_name, days, 'Expedited')
    if success:
        logging.info(f'Submitted request to restore {test_object_name} '
                     f'in {test_bucket_name}')
    logging.info(f'restore object {success}')
    return success


# 测试head_object
def test_head_object():
    test_bucket_name = BUCKET_NAME
    test_object_name = OBJECT_NAME
    # head object.
    success = head_object(test_bucket_name, test_object_name)
    if success:
        logging.info(f'Submitted request to restore {test_object_name} '
                     f'in {test_bucket_name}')
        if success.get('Restore'):
            logging.info('Restore {}'.format(success['Restore']))
            index = success['Restore'].find('ongoing-request=\"false\"')
            if -1 == index:
                logging.info("正在还原...")
            else:
                logging.info(success['Restore'][success['Restore'].find('expiry-date='):])
                logging.info("还原成功.")
        else:
            logging.info('need restore object {} {}'.format(test_bucket_name, test_object_name))
    # logging.info(f'{success}')
    return success


if __name__ == '__main__':
    # Set up logging
    # logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    # logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    BUCKET_NAME="mybucket"
    OBJECT_NAME="obj/test.png"
    test_restore_object()
    test_head_object()
```