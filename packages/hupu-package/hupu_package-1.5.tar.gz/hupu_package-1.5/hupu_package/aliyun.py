#!/usr/bin/env python
#coding=utf-8

import os
import oss2
import configparser
import socket

oss_shanghai = ["hupu-a1a4", "hupu-b1b4", "hupu-bbs-static", "hupu-cba-image",
               "hupu-imgsf-hupucdn", "hupu-w1goalhi", "hupu-w1goalhicom", "hupu-w1w4", "huputv-vod-in-hd2"]

class oss(object):
    def __init__(self, bucketname, localdir, remotedir, DryRun=False, endpoint="None", accesskey="<key>", secretkey="<secret>"):
        self.bucketname = bucketname
        self.localdir = localdir
        self.remotedir = remotedir
        self.DryRun = DryRun
        self.endpoint = endpoint
        self.accesskey = accesskey
        self.secretkey = secretkey

    def upload_oss(self, remotepath, localpath):
        if "<" in self.accesskey:
            CONFIGFILE = '/etc/ansible/.aliyuncli/credentials'
            config = configparser.ConfigParser()
            config.read(CONFIGFILE)
            access_key_id = config.get('default', 'aliyun_access_key_id')
            access_key_secret = config.get('default', 'aliyun_access_key_secret')
        else:
            access_key_id = self.accesskey
            access_key_secret = self.secretkey
        auth = oss2.Auth(access_key_id, access_key_secret)
        if self.bucketname in oss_shanghai:
            region = "shanghai"
        else:
            region = "hangzhou"
        hostName = socket.gethostname()
        if hostName.endswith(("ecs", "ess")):
            if region != "hangzhou":
                endpoint = 'http://oss-cn-{0}.aliyuncs.com'.format(region)
            else:
                endpoint = 'http://oss-cn-{0}-internal.aliyuncs.com'.format(region)
        else:
            endpoint = 'http://oss-cn-{0}.aliyuncs.com'.format(region)
        if self.endpoint != "None":
            endpoint = self.endpoint
        bucket = oss2.Bucket(auth, endpoint, self.bucketname)
        try:
            bucket.put_object_from_file(remotepath, localpath)
        except oss2.exceptions.OssError as e:
            return False, eval(str(e)).get("details").get("Message")
        except Exception as e:
            return False, e
        return True, remotepath

    def get_list_upload(self, filepath):
        files= os.listdir(filepath)
        if len(files) == 0:
            return False, "Directory is empty, no files to sync"
        for file in files:
            path = os.path.join(filepath, file)
            if os.path.isdir(path):
                self.get_list_upload(path)
            else:
                relative_path = path.split(self.localdir)[1]
                code, output = self.upload_oss(relative_path, path)
                if not code:
                    return False, output
        return True, ""

    def get_list_upload_relatively(self, filepath):
        files= os.listdir(filepath)
        if len(files) == 0:
            return False, "Directory is empty, no files to sync"
        for file in files:
            path = os.path.join(filepath, file)
            if os.path.isdir(path):
                self.get_list_upload_relatively(path)
            else:
                relative_path = path.split(self.localdir)[1]
                code, output = self.upload_oss(self.remotedir+relative_path, path)
                if not code:
                    return False, output
        return True, self.remotedir

    def upload(self):
        local_dir = self.localdir
        DryRun = self.DryRun
        remote_dir = self.remotedir

        if os.path.isdir(local_dir) and not local_dir.endswith("/"):
            local_dir = local_dir + '/'

        if DryRun:
            return True, "Action not running"

        if not os.path.exists(local_dir):
            return False, "Local file or directory does not exist"

        if os.path.isfile(local_dir):
            if remote_dir == "/":
                file_name = local_dir.split('/')[-1]
                code, output = self.upload_oss(file_name, local_dir)
            else:
                if not remote_dir.endswith("/"):
                    remote_dir = remote_dir + "/"
                if remote_dir[0] == "/":
                    remote_dir = remote_dir[1:]
                file_name = local_dir.split('/')[-1]
                code, output = self.upload_oss(remote_dir + file_name, local_dir)
            if not code:
                return False, output
            else:
                return True, "File upload successful"
        else:
            if remote_dir == "/":
                self.localdir = local_dir
                code, output = self.get_list_upload(local_dir)
            else:
                if not remote_dir.endswith("/"):
                    remote_dir = remote_dir + "/"
                if remote_dir[0] == "/":
                    remote_dir = remote_dir[1:]
                self.remotedir = remote_dir
                self.localdir = local_dir
                code, output = self.get_list_upload_relatively(local_dir)
            if not code:
                return False, output
            else:
                return True, "File upload successful"
