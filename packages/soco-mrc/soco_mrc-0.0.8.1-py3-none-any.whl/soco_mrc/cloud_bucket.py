import boto3
import oss2
import os
import time


class CloudBucket(object):
    roles = {'reader-s3': ('AKIAIXQ4BV6ORFZ3JKPA', 'D+9W2Zii2Hvpo6G0IJ77tofKUM59ZasC/HE3Kf/w'),
             'full-s3': ('AKIAIRZZT5BICC5NFNOA', 'HB2ixc2F12xaFEuqN1G7HwP4VvfgB+l/kgxNXLFd'),
             'reader-oss': ('LTAINYtHd5knNlAg', 'HIg89gNwNYpbEKoC38SdnYCn3Db8cI'),
             'full-oss': ('LTAIkryioiCP2Wn9', 'cutsfNk7rY05qhBVNikYkxny8I4UkK')}

    def __init__(self, region='us', permission='reader'):
        self.region = region.lower()
        self.permission = permission.lower()
        if permission == 'reader':
            s3_key = self.roles['reader-s3']
            oss_key = self.roles['reader-oss']
        elif permission == 'full':
            s3_key = self.roles['full-s3']
            oss_key = self.roles['full-oss']
        else:
            raise Exception("Unknown permission {}".format(permission))

        self._s3 = boto3.resource('s3', aws_access_key_id=s3_key[0], aws_secret_access_key=s3_key[1])
        self._s3_bucket = self._s3.Bucket('convmind-models')
        self._oss_bucket = oss2.Bucket(oss2.Auth(oss_key[0], oss_key[1]),
                                       str('http://oss-cn-hongkong.aliyuncs.com'),
                                       str('convmind-models'))

    def safe_mkdir(self, path):
        if not os.path.exists(path):
            os.mkdir(path)

    def download(self, folder_dir, files, local_dir):
        start = time.time()
        for f in files:
            try:
                if self.region.lower() == 'cn':
                    self._oss_bucket.get_object_to_file('{}/{}'.format(folder_dir, f), os.path.join(local_dir, f))
                else:
                    self._s3_bucket.download_file('{}/{}'.format(folder_dir, f), os.path.join(local_dir, f))
            except:
                print("Failed to download {}".format(f))

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))

    def download_dir(self, folder_dir, dirs, local_dir):
        start = time.time()
        for d in dirs:
            cur_remote_dir = os.path.join(folder_dir, d)
            cur_local_dir = os.path.join(local_dir, d)

            self.safe_mkdir(cur_local_dir)

            files = []
            if self.region.lower() == 'cn':
                for o in self._oss_bucket.list_objects(prefix=cur_remote_dir).object_list:
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])
            else:
                for o in self._s3_bucket.objects.filter(Prefix=cur_remote_dir):
                    f_name = o.key.split('/')[-1]
                    if f_name != '':
                        files.append(o.key.split('/')[-1])

            self.download(cur_remote_dir, files, cur_local_dir)

        end = time.time()
        print(("download models using {:.4f} sec".format(end - start)))


    def download_model(self, asset_dir, asset_id, local_dir='resources'):
        self.safe_mkdir(local_dir)

        if not os.path.exists(os.path.join(local_dir, asset_id, 'config.json')):
            self.download_dir(asset_dir, [asset_id], local_dir)
        else:
            print("Download is canceled since the asset already exists.")




if __name__ == '__main__':
    b = CloudBucket('cn')
    for d in b._oss_bucket.list_objects(prefix='mrc-models').object_list:
        print(d.key)