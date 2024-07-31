from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from datetime import datetime

def login_with_service_account():
    """
    Google Drive service with a service account.
    note: for the service account to work, you need to share the folder or
    files with the service account email.

    :return: google auth
    """
    # Define the settings dict to use a service account
    # We also can use all options available for the settings dict like
    # oauth_scope,save_credentials,etc.
    settings = {
                "client_config_backend": "service",
                "service_config": {
                    "client_json_file_path": "storage\webscrapehoc-f7ee5859ad23.json"
                }
            }
    # Create instance of GoogleAuth
    gauth = GoogleAuth(settings=settings)
    # Authenticate
    gauth.ServiceAuth()
    return gauth

#fetch from drive, download and save as a dataframe return
def load_storage():
    drive = GoogleDrive(login_with_service_account()) #connect to the drive
    file_list = drive.ListFile({'q': "title = 'final.json'"}).GetList() #return query of the final.json file in the drive
    if len(file_list) == 1: #validation of 
        file_list[0].GetContentFile('storage/final_loaded.json')
        print(f"SUCCESS: pulling data from cloud")
    else:
        print(f"ERROR: Incorrect number of files in drive query. Should be 1 but it is: {len(file_list)} /n {datetime.now}")        

#push the updated dataframe to the drive for storage
def upload_storage():
    drive = GoogleDrive(login_with_service_account())
    file_list = drive.ListFile({'q': "title = 'final.json'"}).GetList() #return query of the final.json file in the drive
    if len(file_list) == 1: #validation of file query
        file_list[0].SetContentFile("storage/final_loaded.json")
        file_list[0].Upload()
        print(f"SUCCESS: data lake uploaded to cloud")
    else:
        print(f"ERROR: Incorrect number of files in drive query. Should be 1 but it is: {len(file_list)} /n {datetime.now}")

if __name__ == "__main__":
    load_storage()
