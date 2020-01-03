---
layout: post
title:  "从s3的GLACIER上批量下载对象的Python代码"
categories: aws python
tags: aws python
author: flame
description: 从s3的GLACIER上批量下载对象的Python代码
---

### 从s3的GLACIER上批量下载对象的Python代码

python代码

```py
#!/usr/bin/env python
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
LOCAL_PATH=""
PREFIX=""


# restore object 
def restore_object(bucket_name, object_name, days, retrieval_type='Standard'):
    """Restore an archived S3 Glacier object in an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :param days: number of days to retain restored object
    :param retrieval_type: 'Standard' | 'Expedited' | 'Bulk'
    :return: True if a request to restore archived object was submitted, otherwise
    False
    """

    # Create request to restore object
    request = {'Days': days,
               'GlacierJobParameters': {'Tier': retrieval_type}}

    # Submit the request
    s3 = boto3.client('s3')
    try:
        s3.restore_object(Bucket=bucket_name, Key=object_name, RestoreRequest=request)
    except ClientError as e:
        # NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's
        # storage class was not GLACIER
        logging.error(e)
        return False
    return True



# head object
def head_object(bucket_name, object_name):
    """Restore an archived S3 Glacier object in an Amazon S3 bucket

    :param bucket_name: string
    :param object_name: string
    :param days: number of days to retain restored object
    :param retrieval_type: 'Standard' | 'Expedited' | 'Bulk'
    :return: True if a request to restore archived object was submitted, otherwise
    False
    """

    # Submit the request
    s3 = boto3.client('s3')
    response = None
    try:
        response = s3.head_object(Bucket=bucket_name, Key=object_name)
    except ClientError as e:
        # NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's
        # storage class was not GLACIER
        logging.error(e)
        logging.error(f"NoSuchBucket, NoSuchKey, or InvalidObjectState error == the object's, storage class was not GLACIER. {bucket_name} {object_name} ")
        return None
    return response


# list object
def list_bucket_objects(bucket_name, prefix=None):
    """List the objects in an Amazon S3 bucket

    :param bucket_name: string
    :return: List of bucket objects. If error, return None.
    """

    # Retrieve the list of bucket objects
    s_3 = boto3.client('s3')
    try:
        if prefix:
            response = s_3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        else:
            response = s_3.list_objects_v2(Bucket=bucket_name)
    except ClientError as e:
        # AllAccessDisabled error == bucket not found
        logging.error(e)
        return None

    # Only return the contents if we found some keys
    if response['KeyCount'] > 0:
        return response['Contents']
    return None


# download file
def download_object(bucket_name, object_name, local):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).download_file(object_name, local+object_name)
    except ClientError as e:
        if e.response['Error']['Code'] == "404":
            logging.error(f"The object does not exist. {bucket_name} {object_name}")
        return False
    return True


# mkdir 
def mkdir(path):
    if os.path.exists(path):
        return True
    os.makedirs(path, 0o770, exist_ok=True)
    return True


# 下载
def download_objects(bucket_name, object_name, local, progress_call=None):
    objects = list_bucket_objects(bucket_name, object_name)
    # no object
    if not objects:
        return False
    count = 0
    # show object list
    logging.info(f"*********object list begin************")
    for obj in objects:
        count+=1
        logging.info(f"{obj['Key']}")
    logging.info(f"*********object list count {count}************")

    long_time_wait = False
    # restore all objects 
    for obj in objects:
        # {'Key': 'a/b/c/d.xml'
        # , 'LastModified': datetime.datetime(2019, 11, 26, 8, 26, 24, tzinfo=tzutc())
        # , 'ETag': '"1234948ca1db112382c26d07db83971a"'
        # , 'Size': 2518
        # , 'StorageClass': 'GLACIER'}
        response = head_object(bucket_name, obj['Key'])
        # not in statdrad and not restore
        if (obj['StorageClass'] != 'STANDRAD' or obj['StorageClass'] != 'STANDRAD_IA') and not response.get('Restore'):
            # start restore  一天20G
            days = obj['Size']//20000000000 + 1
            success = restore_object(bucket_name, obj['Key'], days, 'Standard')
            if not success:
                return False
            long_time_wait = True
    downloaded = []
    download_count = 0
    is_complete = True
    while True:       
        for obj in objects:
            if obj['Key'] in downloaded:
                continue
            response = head_object(bucket_name, obj['Key'])
            if not response:
                return False
            #    
            if (obj['StorageClass'] != 'STANDRAD' or obj['StorageClass'] != 'STANDRAD_IA') and not response.get('Restore'):
                # start restore 
                days = obj['Size']//20000000000 + 1
                success = restore_object(bucket_name, obj['Key'], days, 'Standard')
                if not success:
                    return False
                continue

            if obj['StorageClass'] != 'STANDRAD' or obj['StorageClass'] != 'STANDRAD_IA':
                restore = response['Restore']
                index = restore.find('ongoing-request=\"false\"')
                if -1 == index:
                    logging.info(f"{obj['Key']} 正在还原中...")
                    continue
                else:
                    expiry = restore[restore.find('expiry-date='):]
                    logging.debug(f"{obj['Key']} 还原成功. {restore[restore.find('expiry-date='):]}")
            # download
            path = local + obj['Key']
            path = os.path.dirname(path) + "/"
            mkdir(path)
            logging.info(f"{obj['Key']} 开始下载...")
            success = download_object(bucket_name, obj['Key'], local)
            if success:
                logging.info(f"{obj['Key']} 下载成功.")
                downloaded.append(obj['Key'])
                if progress_call:
                    download_count+=1
                    progress_call(count, download_count, obj['Key'])
        # is complate
        for obj in objects:
            if obj['Key'] in downloaded:
                continue
            is_complete = False
        if is_complete:
            logging.info(f"All objects downloads successful!")
            # The download is complete
            break
        # waiting
        logging.info("Sleep and wait restore...")
        if long_time_wait:  # 
            long_time_wait = False
            time.sleep(60*60)
        else:  # 
            time.sleep(5*60)
    return is_complete


# 进度
next_commint=0
def progress_call(count, downloads, obj_name):
    global next_commint 
    percent = (100*downloads)//count
    if percent >= next_commint:
        next_commint += 5
    logging.info(f"downloads percent {percent}%!")
    return True


# test 
def test_mkdir():
    mkdir('e:/data/111/222/333')
    return True


def test_download_object():
    """Exercise restore_object()"""
    # Assign these values before running the program
    test_bucket_name = BUCKET_NAME
    test_object_name = OBJECT_NAME

    # Restore archived object for two days. Expedite the restoration.
    success = download_object(test_bucket_name, test_object_name, 'E:/data/')
    if success:
        logging.info(f'Submitted request to restore {test_object_name} '
                     f'in {test_bucket_name}')
    logging.info(f'{success}')
    return success


def test_restore_object():
    """Exercise restore_object()"""
    # Assign these values before running the program
    test_bucket_name = BUCKET_NAME
    test_object_name = OBJECT_NAME

    # Restore archived object for two days. Expedite the restoration.
    success = restore_object(test_bucket_name, test_object_name, 2, 'Expedited')
    if success:
        logging.info(f'Submitted request to restore {test_object_name} '
                     f'in {test_bucket_name}')
    logging.info(f'restore object {success}')
    return success


def test_head_object():
    """Exercise restore_object()"""
    # Assign these values before running the program
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


def test_list_bucket_objects():
    """Exercise list_bucket_objects()"""
    bucket_name = BUCKET_NAME
    prefix = PREFIX
    # Retrieve the bucket's objects
    objects = list_bucket_objects(bucket_name, prefix)
    if objects is not None:
        # List the object names
        logging.info(f'Objects in {bucket_name}')
        for obj in objects:
            logging.info(f'  {obj["Key"]}')
    else:
        # Didn't get any keys
        logging.info(f'No objects in {bucket_name}')


def test_download_objects():
    success = download_objects(BUCKET_NAME, OBJECT_NAME, LOCAL_PATH, progress_call)
    return success


if __name__ == '__main__':
    # Set up logging
    # logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    # logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    # logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s', datefmt='%Y-%m-%d  %H:%M:%S')
    global BUCKET_NAME
    global OBJECT_NAME
    global LOCAL_PATH
    global PREFIX
    BUCKET_NAME="mybucket"  # 桶名
    OBJECT_NAME="obj/list1/"  # 批量下载的前缀
    LOCAL_PATH = "e:/download/"  # 放置目录
    PREFIX="show"  # 查询时使用的前缀
    # test_download_objects()
    # test_download_object()
    # test_mkdir()
    test_download_objects()
```