import sys
import os
import dropbox
import io


dropbox_key = ''
test_file = "/Users/ekstrah/Desktop/waterBox/dropspace/example.jpeg"
class DropboxAPI():


    def __init__(self, key):
        self.key = [key]
        dbx = dropbox.Dropbox(key)
        allocated_space = dbx.users_get_space_usage().allocation.get_individual().allocated
        used_space = dbx.users_get_space_usage().used
        self.dbx_object = {key: {"dbx": dbx, "allocated": allocated_space, "used": used_space}}
    
    @staticmethod
    def storage_info(dbx):
        allocted_space = dbx.users_get_space_usage().allocation.get_individual().allocated
        used_space = dbx.users_get_space_usage().used
        return allocated_space, used_space

    def add_account(slef, key):
        self.key.append(key)
        dbx = dropbox.Dropbox(key)
        allocted_space, used_space = storage_info(dbx)
        self.dbx_object[key] = {"dbx": dbx, "allocated": allocated_space, "used": used_space}
    
    def upload(self, file, key):
        f_name = os.path.basename(file)
        f_name = "/" + f_name
        f = io.open(file, "rb")
        self.dbx_object[key].files_upload(f.read(), f_name, mute=True)
    
    def __get_storage_by_key(self, key):
        dbx = self.dbx_object[key]
        return dbx

    def get_storage(self, key=None):
        if key is not None:
            dbx = self.__get_storage_by_key(key)
            print("Dropbox Account with Key: {}\nAllocated: {}, Used: {}, Remained: {}".format(key, dbx['allocated'],dbx['used'],dbx['allocated']-dbx['used'] ))    
        else:
            print("Needs to be integrated")


if __name__ == "__main__":
    dd = DropboxAPI(dropbox_key)
    dd.get_storage(dropbox_key)
# f = io.open("/Users/ekstrah/Desktop/waterBox/dropspace/example.jpeg", "rb")
# dbx.files_upload(f.read(), "/example.jpeg", mute=True)