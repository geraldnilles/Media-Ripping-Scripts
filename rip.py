#! /usr/bin/env python

## Import Libs
import subprocess,os

# Generic function for running a shell command
def cmd(cmd):
	subprocess.call(cmd)

# Rip All
#
# Rips an entire DVD from the disk to the raw/ folder
def rip_all():
	rip(["all"])


# Rip Title
# 
# Rips the provided list of titls to the raw folder
def rip(titles):
	for t in titles:
		cmd("makemkvcon mkv disc:1 "+t+" raw")

#-------------
# Transfer Funtions
#-------------

## Upload a local file to a Samba Share
def upload_to_SMB(filename,path):
	pass

## Download a local file from the Samba Share
def download_from_SMB(path):
	pass

#---------------
# Video Transcode Functions
#---------------

# Transcode Video
def transcode_video(filename):
	transcode_video_x264(filename)

def transcode_video_x264(infile,outfile):
	# Strip MPEG2 video to video.mpeg2
	# TODO This assumes video is the first track. Adjust to find the video
	# track
	cmd(["mkvextract", "tracks", infile, "1:video.mpeg2"])
	# Strip the timecodes
	cmd(["mkvextract", "timecodes_v2", infile, "1:timecodes.txt"])

	# Convert Video to H264
	cmd(["avconv", "-i", "video.mpeg2", "-c:v", "libx264", "-preset", "veryslow", "-crf", "20" ,"video.h264"])

	# Replace MPEG2 with H264
	cmd(["mkvmerge", "-o", outfile, "--timecodes", "0:timecodes.txt", "video.h264", "-D", infile])

	cmd(["rm", "video.h264", "video.mpeg2", "timecodes.txt"])



#-------------------
# Audio Transcode Functions
#-------------------

# Transcode Audio
def transcode_audio(filename):
	pass

def transcode_audio_aac(filename):
	pass

def transcode_audio_opus(filename):
	
	cmd("ffmpeg -i audio.ac3 -c:a opus -b:a 384k -ac audio.opus")

# Strips all Audio except english
def only_english(filename):
	pass


# Generic Transcode Function
def transcode(filename):
	transcode_video(filename)
	transcode_audio(filename)



def run():
	for x in os.listdir("raw"):
		transcode_video_x264("raw/"+x,"h264/"+x)

run()

