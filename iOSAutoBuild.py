#Filename iOSAutoBuild.py
import os,sys,getopt,subprocess
import requests
import json
import shutil


# pgyer
UserKey        = "fabaa06a32d77bbb295edda6f9dc5a4a"
APIKey         = "70c9fef4bc73236ae64907c8e6ec82f5"
pgyerRequestBaseURL = "http://www.pgyer.com/apiv1/app/upload"
downBaseURL = "http://www.pgyer.com"

# fir
FIR_TOKEN     = "Ppbn9wrmJryz6Eb9ZTlQistr2fya2Jf6xSu0whp6"




def changeDir(directory):
    print("project dir %s" % directory)
    os.chdir(directory)


def xcbuild(targetName, directory="./build/"):
    print("target %s, configuration %s" % (targetName, ""))

    exportIpaPath =  directory + "/" + targetName + ".ipa"

    archiveCmd = "xcodebuild -workspace " + targetName +".xcworkspace -scheme " + targetName + " -sdk iphoneos archive -archivePath " + directory +"/" + targetName + ".xcarchive" + " -configuration Inhouse archive"
    ipaCmd = "xcodebuild -exportArchive -exportFormat ipa" + " -archivePath " + directory + "/" + targetName + ".xcarchive" + " -exportPath " + exportIpaPath + " -exportWithOriginalSigningIdentity"

    print("archive cmd %s, ipa cmd %s" % (archiveCmd, ipaCmd))

    process = subprocess.Popen(archiveCmd, shell=True)
    process.wait()

    process = subprocess.Popen(ipaCmd, shell=True)
    output = process.communicate()
    print output

    # uploadIPAToPgyer(exportIpaPath)
    upload_ipaToFir(exportIpaPath)





def resultJson(jsonResult):
    resultCode = jsonResult['code']
    if resultCode == 0:
      downUrl = downBaseURL +"/"+jsonResult['data']['appShortcutUrl']
      print "Upload Success"
      print "DownUrl is:"+downUrl
    else:
        print "Upload Fail!"
        print "Reason:"+jsonResult['message']



def uploadIPAToPgyer(ipaDirectory):
    uploadUrl = pgyerRequestBaseURL+"?"+"uKey="+UserKey+"&"+"_api_key="+APIKey+"&"+"publishRange="+"2"+"&"+"isPublishToPublic="+"2"
    print "ipaDirectory: "+ipaDirectory
    print "uploadUrl: "+uploadUrl
    files = {'file': open(ipaDirectory, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'uKey':UserKey,'_api_key':APIKey,'publishRange':'2','isPublishToPublic':'2'}
    print "uploading...."
    r = requests.post(uploadUrl,data = payload ,files=files,headers=headers)
    if r.status_code == requests.codes.ok:
         result = r.json()
         resultJson(result)
         os.unlink(ipaDirectory)
    else:
        print 'HTTPError,Code:'+r.status_code





def upload_ipaToFir(ipaDirectory):

    uploadCmd = "fir p " + ipaDirectory + " -T " + FIR_TOKEN
    process = subprocess.Popen(uploadCmd, shell=True)
    process.wait()
    projectName = ipaDirectory[:-3]
    shutil.rmtree("build")
    shutil.rmtree("tmp")
    return



def main():
    try:
        print("start")
        opts, args = getopt.getopt(sys.argv[1:], "x", ["target="])

        print(opts)
        #swtich to project directory
        changeDir(".")
        print("xcodebuild opts %s" % opts)

        #execute xcodebuile
        xcbuild(opts[0][1])
    except getopt.GetoptError as e:
        # usage()
        print("error %s" % e)
        sys.exit(2)


if __name__ == '__main__':
    main()
